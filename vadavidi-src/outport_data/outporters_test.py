""" The test for the outporters. """
import unittest

from common.datas import ID, Schema, Entry, SOURCE
from common.datas_util import RowsMutableTable
from common.elang_query import ELangExpression, ELangFieldReference, \
    ELangNativeRenderer
from common.fieldname_query import FieldRefExpression, FieldRefNativeRenderer
from import_data.dumpers_impls import SimpleCSVDumper, SimplyBackupingHandler, \
    SQLiteDumper
from outport_data.base_displayers import BaseSeriesStyle
from outport_data.base_query import Query, ExpressionRenderers
from outport_data.default_querier import DefaultQuerier
from outport_data.outporters_impls import DefaultOutporter
from outport_data.raisers_impls import SimpleCSVRaiser, NoopRaiser
from outport_data.simple_displayer import SimpleDisplayer, LineChartSeriesStyle, \
    BarChartSeriesStyle
from outport_data.sqllite_querier import SQLLiteQuerier


################################################################################
class RaisersTest(unittest.TestCase):
    schema = Schema({"day": "int", "amount": "float", "bar": "enum"})

################################################################################
    def test_Default(self):
        try:
            self.create_table_and_dump_to_csv()
        except Exception as ex:
            print("Note: Could not prepare the csv dump:" + str(ex))
            
        # outporter
        outporter = DefaultOutporter()
        
        # outporter
        outporter.raiser = SimpleCSVRaiser()
        
        # querier
        outporter.querier = DefaultQuerier()
        outporter.querier.renderer = ExpressionRenderers([
            ELangNativeRenderer(), FieldRefNativeRenderer()
            ])
        
        # displayer
        outporter.displayer = SimpleDisplayer()
        
        # query
        query = Query(None, {
            "day": FieldRefExpression("day"),
            "amount": FieldRefExpression("amount"),
            "bar": ELangExpression(["2", "*", ELangFieldReference("bar")])},
        ELangExpression([ELangFieldReference("amount"), ">", "'1'"]),
        None, None, None)
        
        # config
        config = {
            ID: BaseSeriesStyle.create(BarChartSeriesStyle, width = 0.1),
            "amount": BaseSeriesStyle.create(LineChartSeriesStyle, color = "green"),
            "bar": BaseSeriesStyle.create(BarChartSeriesStyle, color = "blue")
        }
        
        # queries and styles
        outporter.queries = {"amnt of br": query}
        outporter.configs = {"amnt of br": config}
        
        # and go!
        outporter.run("amnt and br", self.schema, "amnt of br", "day")
        

    def create_table_and_dump_to_csv(self):
        table = self.create_table()
        
        dumper = SimpleCSVDumper()
        dumper.existing_file_handler = SimplyBackupingHandler()
        dumper.dump("amnt and br", table)

################################################################################

    def test_SQLLite(self):
        try:
            self.create_table_and_dump_to_sqllite()
        except Exception as ex:
            print("Note: Could not prepare the sqllite dump:" + str(ex))
            
        # outporter
        outporter = DefaultOutporter()
        
        # outporter
        outporter.raiser = NoopRaiser()
        
        # querier
        outporter.querier = SQLLiteQuerier()
        outporter.querier.renderer = ExpressionRenderers([
            ELangNativeRenderer(), FieldRefNativeRenderer()
            ])
        
        # displayer
        outporter.displayer = SimpleDisplayer()
        
        # query
        query = Query(None, {
            "day": FieldRefExpression("day"),
            "amount": FieldRefExpression("amount"),
            "bar": ELangExpression(["2", "*", ELangFieldReference("bar")])},
        ELangExpression([ELangFieldReference("amount"), ">", "'1'"]),
        None, None, None)
        
        # config
        config = {
            ID: BaseSeriesStyle.create(BarChartSeriesStyle, width = 0.1),
            "amount": BaseSeriesStyle.create(LineChartSeriesStyle, color = "green"),
            "bar": BaseSeriesStyle.create(BarChartSeriesStyle, color = "blue")
        }
        
        # queries and styles
        outporter.queries = {"amnt of br": query}
        outporter.configs = {"amnt of br": config}
        
        # and go!
        outporter.run("amnt and br", self.schema, "amnt of br", "day")
        

    def create_table_and_dump_to_sqllite(self):
        table = self.create_table()
        
        dumper = SQLiteDumper()
        dumper.existing_file_handler = SimplyBackupingHandler()
        dumper.dump("amnt and br", table)


################################################################################
    def create_table(self):
        result = RowsMutableTable(self.schema)
        
        result += Entry({ID: 1, SOURCE: "any", "day": 1, "amount": 14.5, "bar": 1})
        result += Entry({ID: 2, SOURCE: "any", "day": 2, "amount": 17.2, "bar": 2})
        result += Entry({ID: 3, SOURCE: "any", "day": 4, "amount": 18.2, "bar": 3})
        result += Entry({ID: 4, SOURCE: "any", "day": 2, "amount": 11.1, "bar": 2})
        result += Entry({ID: 5, SOURCE: "any", "day": 3, "amount": 16.3, "bar": 1})
        result += Entry({ID: 6, SOURCE: "any", "day": 5, "amount": 14.4, "bar": 2})
        result += Entry({ID: 7, SOURCE: "any", "day": 4, "amount": 17.1, "bar": 1})
        result += Entry({ID: 8, SOURCE: "any", "day": 2, "amount": 19.4, "bar": 1})        
        result += Entry({ID: 9, SOURCE: "any", "day": 3, "amount": 16.4, "bar": 1})
        
        return result.to_table()

################################################################################
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()