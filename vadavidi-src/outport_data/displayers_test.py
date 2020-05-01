"""
The test for the displayers.
"""
import math
import unittest

from common.datas import Schema, Entry, ID, Table
from outport_data.base_displayers import StyleBuilder
from outport_data.simple_displayer import SimpleDisplayer, LineChartSeriesStyle, \
    BarChartSeriesStyle, ScatterChartSeriesStyle, PieChartSeriesStyle
import time


###############################################################################
class TestDisplayers(unittest.TestCase):
    schema = Schema({"time":"int", "speed":"decimal"})

    def _test_Line(self):
        displayer = SimpleDisplayer()
        styles = {
            ID: StyleBuilder(LineChartSeriesStyle).sets(color="y", line_width=4).build(),
            "speed": StyleBuilder(LineChartSeriesStyle).sets(marker_size = 10, marker_style = "*").build(),
            "age": StyleBuilder(LineChartSeriesStyle).build()
            }
        
        self.run_displayer(displayer, styles)

    def _test_Bar(self):
        displayer = SimpleDisplayer()
        styles = {
            ID: StyleBuilder(BarChartSeriesStyle).sets(color="b", bar_width=1).build(),
            "speed": StyleBuilder(BarChartSeriesStyle).sets(hatch_style="/", space_after = 4).build(),
            "age": StyleBuilder(BarChartSeriesStyle).sets().build(),
            }
        
        self.run_displayer(displayer, styles)

    def _test_Scatter(self):
        displayer = SimpleDisplayer()
        styles = {
            ID: StyleBuilder(ScatterChartSeriesStyle).sets(color="r").build(),
            "speed": StyleBuilder(ScatterChartSeriesStyle).sets(marker_base_size = 10 ).build(),
            "age": StyleBuilder(ScatterChartSeriesStyle).sets(marker_sizes_field = "speed").build(),
            }
        
        self.run_displayer(displayer, styles)
        
    def _test_Pie(self):
        displayer = SimpleDisplayer()
        styles = {
            "age": StyleBuilder(PieChartSeriesStyle).sets().build(),
            ID: StyleBuilder(PieChartSeriesStyle).sets(first_color="r", last_color="b", radius = 0.9).build(),
            "speed": StyleBuilder(PieChartSeriesStyle).sets(first_color="yellow", radius = 0.5, explode = 0.1).build()
            }
        
        self.run_displayer(displayer, styles)
        
        
    def test_rerun_one_test(self):
        displayer = SimpleDisplayer()
        
        styles = {
            "speed": StyleBuilder(LineChartSeriesStyle).sets(marker_size = 10, marker_style = "*").build(),
            }
        
        self.run_displayer(displayer, styles)

        styles = {
            "age": StyleBuilder(LineChartSeriesStyle).build()
            }
        
        self.run_displayer(displayer, styles)
        

###############################################################################
    def create_table(self):
        entries = list((Entry.create_new(self.schema, i, "cmptd", { \
                "time": (i ** 1), \
                "speed": math.e**i / 10, \
                "age": 2 * math.cos(i) } \
            )) for i in range(1, 7))
            
                
        return Table(self.schema, entries)

        
    def run_displayer(self, displayer, styles):
        print("RUNNING DISPLAYER: " + str(displayer))
        table = self.create_table()
        table.printit()
        
        dataset_name = "The test"
        x_axis_name = "time"
        series_names = styles.keys()
        
        displayer.show(dataset_name, table, x_axis_name, series_names, styles)

###############################################################################

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()