#
import unittest

from common.datas import Schema, Entry
from common.datas_util import MutableTable
from outport_data.base_outporters import Query
from outport_data.queriers_impls import DefaultQuerier


class QueriersTest(unittest.TestCase):


    def test_DefaultQuerier(self):
        querier = DefaultQuerier()
        
        schema = Schema({"foo": "str", "bar": "int", "baz": "enum"})
        mt = MutableTable(schema)
        mt.add(Entry(0, {"foo": "hello", "bar": 11, "baz": "YES"}))
        mt.add(Entry(1, {"foo": "world", "bar": 12, "baz": "NO"}))
        mt.add(Entry(2, {"foo": "test", "bar": 15, "baz": "MAYBE"}))
        mt.add(Entry(3, {"foo": "hello", "bar": 45, "baz": "NO"}))
        mt.add(Entry(4, {"foo": "hello", "bar": 48, "baz": "YES"}))
        mt.add(Entry(5, {"foo": "test", "bar": 99, "baz": "YES"}))
        mt.add(Entry(6, {"foo": "test", "bar": 65, "baz": "MAYBE"}))
        
        table = mt.toTable()
        print("-- original --")
        table.printit()
        print("-- done --")
        
        query = Query(xAxisSpecifier = "foo", yAxisSpecifiers = {"maxs of bar": "$bar.count", "count of baz": "$baz.count"})
        
        result = querier.query(table, query)
        print("-- executed --")
        result.printit()
        print("-- done --")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()