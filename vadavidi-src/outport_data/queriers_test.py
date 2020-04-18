"""
The test for the queriers
"""
import unittest

from common.datas import Schema, Entry
from common.datas_util import RowsMutableTable
from outport_data.base_outporters import Query
from outport_data.queriers_impls import DefaultQuerier

################################################################################
class QueriersTest(unittest.TestCase):


    def test_DefaultQuerier(self):
        querier = DefaultQuerier()
        
        schema = Schema({"foo": "str", "bar": "int", "baz": "enum"})
        mt = RowsMutableTable(schema)
        mt.add(Entry.create_new(schema, 0, "a", {"foo": "hello", "bar": 11, "baz": "YES"}))
        mt.add(Entry.create_new(schema, 1, "b", {"foo": "world", "bar": 12, "baz": "NO"}))
        mt.add(Entry.create_new(schema, 2, "a", {"foo": "test", "bar": 15, "baz": "MAYBE"}))
        mt.add(Entry.create_new(schema, 3, "b", {"foo": "hello", "bar": 45, "baz": "NO"}))
        mt.add(Entry.create_new(schema, 4, "a", {"foo": "hello", "bar": 48, "baz": "YES"}))
        mt.add(Entry.create_new(schema, 5, "b", {"foo": "test", "bar": 99, "baz": "YES"}))
        mt.add(Entry.create_new(schema, 6, "a", {"foo": "test", "bar": 65, "baz": "MAYBE"}))
        
        table = mt.to_table()
        print("-- original --")
        table.printit()
        print("-- done --")
        
        query = Query(x_axis_specifier = "foo", y_axis_specifiers = {"maxs of bar": "$bar.count", "count of baz": "$baz.count"})
        
        result = querier.query(table, query)
        print("-- executed --")
        result.printit()
        print("-- done --")

################################################################################
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()