"""
The test for the queriers
"""
import unittest

from common.datas import Schema, Entry
from common.datas_util import RowsMutableTable
from common.elang import ELangNativeRenderer, ELangExpression, \
    ELangFieldReference
from outport_data.base_queriers import AggregatingExpression
from outport_data.base_queriers import Query
from outport_data.queriers_impls import DefaultQuerier


################################################################################
class QueriersTest(unittest.TestCase):
    schema = Schema({"foo": "str", "bar": "int", "baz": "enum"})
        

    def test_DefaultQuerier(self):
        querier = DefaultQuerier()
        querier.renderer = ELangNativeRenderer()
        
        table = self.create_table()
        
        print("-- original --")
        table.printit()
        print("-- done --")
        
        query = Query(x_axis = "foo", \
            y_axis_specifiers = { \
                "maxs of bar": AggregatingExpression("max", "int", \
                    ELangExpression([ ELangFieldReference("bar") ])), \
                "count of baz": AggregatingExpression("count", "int", \
                    ELangExpression([ ELangFieldReference("baz") ])) })
        
        print(query)
        
        result = querier.query(table, query)
        print("-- executed --")
        result.printit()
        print("-- done --")

    def create_table(self):
        mt = RowsMutableTable(self.schema)

        mt.add(Entry.create_new(self.schema, 0, "a", {"foo": "hello", "bar": 31, "baz": "YES"}))
        mt.add(Entry.create_new(self.schema, 1, "b", {"foo": "world", "bar": 41, "baz": "NO"}))
        mt.add(Entry.create_new(self.schema, 2, "a", {"foo": "test", "bar": 51, "baz": "MAYBE"}))
        mt.add(Entry.create_new(self.schema, 3, "b", {"foo": "hello", "bar": 41, "baz": "NO"}))
        mt.add(Entry.create_new(self.schema, 4, "a", {"foo": "hello", "bar": 51, "baz": "YES"}))
        mt.add(Entry.create_new(self.schema, 5, "b", {"foo": "test", "bar": 91, "baz": "YES"}))
        mt.add(Entry.create_new(self.schema, 6, "a", {"foo": "test", "bar": 61, "baz": "MAYBE"}))
        
        return mt.to_table()
      

################################################################################
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()