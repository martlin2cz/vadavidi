""" The test for the sqlite_db module. """

import unittest

from common.datas import Schema, Entry, ID
from common.sqlite_db import SQL_LITE_POOL
from IPython.utils import timing


################################################################################
class Test(unittest.TestCase):

    schema: Schema = Schema({"foo": "str", "bar": "int", "baz": "float"})
    dataset_name: str = "/tmp/sqlite-test"
    

        
    def test_insert_entry(self):
        sql = SQL_LITE_POOL.get(self.dataset_name)
        
        entry = Entry.create_new(self.schema, 1, "sqll", \
                { "foo": "hello", "bar": 42, "baz": 99.9 })   
        sql.insert_entry(self.schema, entry)
    
    def test_insert_entries(self):
        sql = SQL_LITE_POOL.get(self.dataset_name)
        
        entries = [ \
            Entry.create_new(self.schema, 2, "sqll", \
                             {"foo": "lorem", "bar": 99, "baz": 11.11}),    
            Entry.create_new(self.schema, 3, "sqll", \
                             {"foo": "ipsum", "bar": 11, "baz": -1.01}),
            Entry.create_new(self.schema, 4, "sqll", \
                             {"foo": "dolor", "bar": 11, "baz": 3.14})
        ]
        
        sql.insert_entries(self.schema, entries)

    def test_load_all(self):
        sql = SQL_LITE_POOL.get(self.dataset_name)
        
        table = sql.load(self.schema)
        table.printit()

    def test_load_better(self):
        sql = SQL_LITE_POOL.get(self.dataset_name)

        table = sql.load_better(self.schema, \
            {"identity" : ID, "fooo" : "foo", "baar": "bar + 1"}, \
            "bar < 50", None, "fooo")
        
        table.printit()
    
    
    

        
        
################################################################################
    def create_table(self):
        sql = SQL_LITE_POOL.get(self.dataset_name)
        
        sql.create_table(self.schema)
        
    def delete_table(self):
        sql = SQL_LITE_POOL.get(self.dataset_name)
        
        sql.delete_table()

    def setUp(self):
        self.create_table()
                
    def tearDown(self):
        self.delete_table()

################################################################################
if __name__ == "__main__":
    unittest.main()