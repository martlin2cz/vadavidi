"""
The test for the queriers
"""
import unittest

from common.datas import Schema, Entry, ID, SOURCE
from common.datas_util import RowsMutableTable
from common.elang import ELangNativeRenderer, ELangExpression, \
    ELangFieldReference, ELangParser
from outport_data.base_queriers import AggregatingExpression
from outport_data.base_queriers import Query
from outport_data.queriers_impls import DefaultQuerier, SQLLiteQuerier
from common.sqlite_db import SQL_LITE_POOL


################################################################################
class QueriersTest(unittest.TestCase):
    schema = Schema({"foo": "str", "bar": "int", "baz": "enum"})
    elang = ELangParser()
    dataset_name = "/tmp/testing_queriers"
    
    def _test_DefaultQuerier_compute(self):
        values_map = { "foo/baz": self.e("€foo + '/' + €baz"),
                       "2 x bar": self.e("2 * €bar")}
        
        querier = DefaultQuerier()
        querier.renderer = ELangNativeRenderer()
        table = self.create_table()
        table.printit()
        
        computed = querier.compute(table, values_map)
        computed.printit()
        
    def _test_DefaultQuerier_group(self):
        grouppers_names = [ "foo", "baz" ]
        
        querier = DefaultQuerier()
        table = self.create_table()
        table.printit()
        
        computed = querier.group(table, grouppers_names)
        computed.printit()

    def _test_DefaultQuerier_agregate(self):
        grouppers = {ID: "avg", SOURCE: "count", "foo": None, "baz": None }
        grouppers_names = [ "foo", "baz" ]
        
        querier = DefaultQuerier()
        table = self.create_table()
        table.printit()
        
        groupped = querier.group(table, grouppers_names)
        computed = querier.agregate(groupped, grouppers)
        computed.printit()

################################################################################

    def test_DefaultQuerier(self):
        values_map = {"fof": self.e("€foo [0]"), \
#                      "foo": self.e("€foo"), \
                      "lbaz": self.e("€baz . lower()"), \
                      "bardiv": self.e("€bar / 10")}
        groups_map = {ID: "avg", SOURCE: "count", "fof": None, "lbaz": None,  "bardiv": "max" }
        query = Query(values_map, groups_map)
        
        querier = DefaultQuerier()
        querier.renderer = ELangNativeRenderer()
        table = self.create_table()
        table.printit()
        
        result = querier.query(self.dataset_name, table, query)
        result.printit()
        
        
    def test_SQLLiteQuerier(self):
        try:
            table = self.create_table()
            sqll = SQL_LITE_POOL.get(self.dataset_name)
            sqll.create_table(table.schema)
            sqll.insert_entries(table.schema, table)
        except Exception as ex:
            print("Notice: Cannot prepare table because: " + str(ex))
        
        
        values_map = {"fof": self.e("SUBSTR( €foo , 1, 1)"), \
#                      "foo": self.e("€foo"), \
                      "lbaz": self.e("LOWER( €baz )"), \
                      "bardiv": self.e("€bar / 10")}
        groups_map = {ID: "AVG", SOURCE: "COUNT", "fof": None, "lbaz": None,  "bardiv": "MAX" }
        query = Query(values_map, groups_map)
        
        querier = SQLLiteQuerier()
        querier.renderer = ELangNativeRenderer()
        
        result = querier.query(self.dataset_name, None, query)
        result.printit()

################################################################################
        
    def _test_DefaultQuerier(self):
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


################################################################################

    def e(self, elang_str):
        return self.elang.parse(self.schema, elang_str)
    
    
    def create_table(self):
        mt = RowsMutableTable(self.schema)

        mt.add(Entry.create_new(self.schema, 0, "a", {"foo": "hello", "bar": 31, "baz": "YES"}))
        mt.add(Entry.create_new(self.schema, 1, "b", {"foo": "world", "bar": 41, "baz": "NO"}))
        mt.add(Entry.create_new(self.schema, 2, "a", {"foo": "test", "bar": 51, "baz": "MAYBE"}))
        mt.add(Entry.create_new(self.schema, 3, "b", {"foo": "hello", "bar": 41, "baz": "NO"}))
        mt.add(Entry.create_new(self.schema, 4, "a", {"foo": "hello", "bar": 51, "baz": "YES"}))
        mt.add(Entry.create_new(self.schema, 5, "b", {"foo": "test", "bar": 91, "baz": "YES"}))
        mt.add(Entry.create_new(self.schema, 6, "a", {"foo": "test", "bar": 61, "baz": "MAYBE"}))
        mt.add(Entry.create_new(self.schema, 7, "a", {"foo": "test", "bar": 41, "baz": "YES"}))
        
        return mt.to_table()
      

################################################################################
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()