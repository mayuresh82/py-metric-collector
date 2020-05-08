import unittest
import yaml
import sys
import logging
import pprint
import json
from os import path
from metric_collector import parser_manager

here = path.abspath(path.dirname(__file__))
parsers_dir = here + '/../../parsers'
pp = pprint.PrettyPrinter(indent=4)

class Test_Parsers(unittest.TestCase):
  logger = logging.getLogger()
  logger.setLevel(logging.DEBUG)


  def test_parser_show_interfaces_extensive(self):
    test_dir = here+'/input/41_validate_parsers'

    pm = parser_manager.ParserManager( parser_dir=parsers_dir )

    ## Read XML content
    xml_data = open( test_dir + "/rpc-reply/show_interfaces_extensive_01.xml").read()

    ## Return a list dict
    ## NOTE: input arg needs to include full path to the parser as line 109 of
    ## lib/metric_collector/parser_manager.py doesnt do a substring match
    data = pm.parse( input="/source/parsers/juniper/show-interfaces-extensive.parser.yaml", data=xml_data.encode() )

    # pprint.pprint(data)

    ## Read XML content
    xml_data = open( test_dir + "/rpc-reply/show_interfaces_extensive_02.xml").read()

    ## Return a list dict
    data = pm.parse( input="/source/parsers/juniper/show-interfaces-extensive.parser.yaml", data=xml_data.encode() )

    # pprint.pprint(data)

    self.assertTrue( True )


  def test_parser_f5_pools_json(self):
    test_dir = here+'/input/41_validate_parsers'

    pm = parser_manager.ParserManager( parser_dir=parsers_dir )

    # Read JSON Content
    with open(test_dir + "/json-reply/f5-pools.json") as f:
        data = f.read()

    json_data = json.loads(data)

    data = pm.parse(input="/source/parsers/f5/f5-pools.yaml", data=json_data)

    self.assertTrue(True)
