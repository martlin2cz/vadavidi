"""
The test for the queriers
"""
import unittest

from common.datas import Schema, Entry, ID, SOURCE
from common.datas_util import RowsMutableTable, DatasUtil
from common.elang import ELangNativeRenderer, ELangExpression, \
    ELangFieldReference, ELangParser
from outport_data.base_queriers import AggregatingExpression
from outport_data.base_queriers import Query
from outport_data.queriers_impls import DefaultQuerier, SQLLiteQuerier, COMPUTED
from common.sqlite_db import SQL_LITE_POOL


################################################################################
class QueriersTest(unittest.TestCase):
    schema = Schema({"foo": "str", "bar": "int", "baz": "enum"})
    elang = ELangParser()
    dataset_name = "/tmp/testing_queriers"
    
    def _test_DefaultQuerier_filter(self):
        print("=== DefaultQuerier filter")
        expr = self.e("( €baz in ('YES', 'NO') ) and ( €bar < 50 )")
        
        querier = DefaultQuerier()
        querier.renderer = ELangNativeRenderer()
        table = self.create_table()
        table.printit()
        
        filtered = querier.filter(table, expr)
        filtered.printit()
    
    def _test_DefaultQuerier_compute(self):
        print("=== DefaultQuerier compute")
        values_map = { "foo/baz": self.e("€foo + '/' + €baz"),
                       "2 x bar": self.e("2 * €bar")}
        
        querier = DefaultQuerier()
        querier.renderer = ELangNativeRenderer()
        table = self.create_table()
        table.printit()
        
        computed = querier.compute(table, values_map)
        computed.printit()
        
    def _test_DefaultQuerier_group(self):
        print("=== DefaultQuerier group")
        grouppers_map = { "foo": None, "baz": None, ID: "...", SOURCE: "...", "baz": "..." }
        
        querier = DefaultQuerier()
        table = self.create_table()
        table.printit()
        
        computed = querier.group(table, grouppers_map)
        computed.printit()

    def _test_DefaultQuerier_agregate(self):
        print("=== DefaultQuerier agregate")
        grouppers_map = {ID: "avg", SOURCE: "count", "foo": None, "bar": "count", "baz": None }
        
        querier = DefaultQuerier()
        table = self.create_table()
        table.printit()
        
        groupped = querier.group(table, grouppers_map)
        computed = querier.agregate(groupped, grouppers_map)
        computed.printit()

    def _test_DefaultQuerier_order(self):
        print("=== DefaultQuerier order")
        order_by = [SOURCE, "baz"]
        
        querier = DefaultQuerier()
        table = self.create_table()
        table.printit()
        
        filtered = querier.order(table, order_by)
        filtered.printit()
################################################################################

    def test_DefaultQuerier(self):
        print("=== DefaultQuerier")
        before_values_filter = self.e("€" + ID + " < 7")
        values_map = {"fof": self.e("€foo [0]"), \
                      "lbaz": self.e("€baz . lower()"), \
                      "bardiv": self.e("€bar / 10")}
        after_values_filter = self.e("€bardiv < 8")
        groups_map = {ID: "avg", SOURCE: "count", "fof": None, "lbaz": None,  "bardiv": "max" }
        after_groupped_filter = self.e("€bardiv < 6")
        order_by = ["fof", "lbaz"]
         
        query = Query(before_values_filter, values_map, after_values_filter, \
                      groups_map, after_groupped_filter, order_by)
        
        querier = DefaultQuerier()
        querier.renderer = ELangNativeRenderer()
        table = self.create_table()
        table.printit()
        
        result = querier.query(self.dataset_name, table, query)
        result.printit()
        
        
    def test_SQLLiteQuerier(self):
        print("=== SQLLiteQuerier")
        self.try_create_db_table()
        
        
        before_values_filter = self.e("€" + ID + " < 7")
        values_map = {"fof": self.e("SUBSTR( €foo , 1, 1)"), \
                      "lbaz": self.e("LOWER( €baz )"), \
                      "bardiv": self.e("€bar / 10")}
        after_values_filter = self.e("€bardiv < 8")
        groups_map = {ID: "AVG", SOURCE: "COUNT", "fof": None, "lbaz": None,  "bardiv": "MAX" } #FIXME ID and SOURCE aggregator has no sense
        after_groupped_filter = self.e("€bardiv < 6")
        order_by = ["fof", "lbaz"]
         
        query = Query(before_values_filter, values_map, after_values_filter, \
                      groups_map, after_groupped_filter, order_by)
        
        
        querier = SQLLiteQuerier()
        querier.renderer = ELangNativeRenderer()
        table = DatasUtil.empty_table(self.schema) #FIXME avoid such
        result = querier.query(self.dataset_name, table, query)
        result.printit()



################################################################################

        
    def try_create_db_table(self):    
        try:
            table = self.create_table()
            table.printit()
            sqll = SQL_LITE_POOL.get(self.dataset_name)
            sqll.create_table(table.schema)
            sqll.insert_entries(table.schema, table)
        except Exception as ex:
            print("Notice: Cannot prepare table because: " + str(ex))
        
    def __test_DefaultQuerier(self):
        print("Deprecated")
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
        xschema = self.schema
        xschema = DatasUtil.add_to_schema(xschema, "fof", COMPUTED)
        xschema = DatasUtil.add_to_schema(xschema, "lbaz", COMPUTED)
        xschema = DatasUtil.add_to_schema(xschema, "bardiv", COMPUTED)
            
        return self.elang.parse(xschema, elang_str)
    
    
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