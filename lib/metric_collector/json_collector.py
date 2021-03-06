import logging
import time
import requests
import warnings
warnings.filterwarnings('ignore')

logger = logging.getLogger('json_collector')


class JsonCollector(object):

    def __init__(self, host, address, credential, port=443, timeout=15, retry=3, parsers=None,
                 context=None, device_type='f5'):
        self.hostname = host
        self.host = address
        self.credential = credential
        self.__port = port
        self.__timeout = timeout
        self.__retry = retry
        self.__is_connected = False
        self.parsers = parsers
        if context:
            self.context = {k: v for i in context for k, v in i.items()}
        else:
            self.context = None
        self.facts = {}
        self.device_type = device_type
        self.base_url = 'http://{}/'.format(self.host)
        if port == 443:
            self.base_url = 'https://{}/'.format(self.host)
        elif port != 80:
            self.base_url = 'https://{}:{}/'.format(self.host, port)

    def connect(self):
        logger.info('Connecting to host: %s at %s', self.hostname, self.host)

        use_token = False
        user = self.credential.get('username')
        passwd = self.credential.get('password')
        if self.credential['method'] == 'vault':
            user, passwd = self._get_credentials_from_vault()
        if self.credential.get('use_token', 'false').lower() == 'true':
            use_token = True
        if not user or not passwd:
            logger.error('Invalid or no credentials specified')
            return
        self.session = requests.Session()
        self.session.auth = (user, passwd)
        self.session.verify = False
        self.__is_connected = True

    def collect_facts(self):
        logger.info('[%s]: Collecting Facts on device', self.hostname)

        if self.hostname:
            self.facts['device'] = self.hostname

        # TODO(Mayuresh) Collect any other relevant facts here

    def execute_query(self, query):
        for retry in range(self.__retry):
            logger.debug('[%s]: execute : %s', self.hostname, query)
            try:
                if self.device_type == 'f5':
                    q = self.base_url + query
                    result = self.session.get(q, timeout=self.__timeout)
                    result.raise_for_status()
                    return result.json()
                elif self.device_type == 'arista':
                    q = self.base_url + 'command-api'
                    body = {
                        'jsonrpc': '2.0',
                        'method': 'runCmds',
                        'params': {
                          'format': 'json',
                          'timestamps': False,
                          'autoComplete': False,
                          'expandAliases': False,
                          'cmds': [ query ],
                          'version': 1
                        },
                        'id': 'MetricCollector-1'
                    }
                    result = self.session.post(q, timeout=self.__timeout, json=body)
                    result.raise_for_status()
                    resp = result.json()
                    return resp['result'][0]
            except Exception as ex:
              logger.error('Failed to execute query: %s on %s: %s, retrying #%d', query, self.hostname, str(ex), retry)
              time.sleep(2)
              continue
        logger.error('Failed to connect to execute on  %s at %s after %d tries', self.hostname, self.host, self.__retry)

    def collect(self, command):

        # find the command/query to execute
        logger.debug('[%s]: parsing : %s', self.hostname, command)
        parser = self.parsers.get_parser_for(command)
        try:
            if self.device_type == 'f5':
                raw_data = self.execute_query(parser['data']['parser']['query'])
            elif self.device_type == 'arista':
                raw_data = self.execute_query(parser['data']['parser']['command'])
        except TypeError as e:
            logger.error('Parser returned no data. Message: {}'.format(e))
            raw_data = None
        if not raw_data:
            return None
        datapoints = self.parsers.parse(command, raw_data)

        if datapoints is not None:
            measurement = self.parsers.get_measurement_name(input=command)
            timestamp = time.time_ns()
            for datapoint in datapoints:
                if not datapoint['fields']:
                    continue
                if datapoint['measurement'] is None:
                    datapoint['measurement'] = measurement
                datapoint['tags'].update(self.facts)
                if self.context:
                    datapoint['tags'].update(self.context)
                datapoint['timestamp'] = timestamp
                yield datapoint

        else:
            logger.warn('No parser found for command > %s', command)
            return None

    def is_connected(self):
        return self.__is_connected

    def close(self):
        # rest connection is not stateful so nothing to close
        return
