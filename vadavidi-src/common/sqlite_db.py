"""
The module implementing the SQLLite database (in fact just only one table) "DAO"
"""
from builtins import str
import os
from sqlite3 import Connection
import sqlite3

from common.datas import ID, Entry, Schema, SOURCE
from common.datas_util import RowsMutableTable


################################################################################
class SQLLite:
    """ The SQL Lite database acessor implementation. """
    
    # the database file
    db_file: str
    
    # the database table
    table_name: str
    
    # the connection
    _conn: Connection
    
    def  __init__(self, db_file, table_name):
        self.db_file = db_file
        self.table_name = table_name
        
    
    def connect(self):
        """ Connects to database """
    
        self._conn = sqlite3.connect(self.db_file)
    
    def disconnect(self):
        """ Disconnects from the database """
        
        self._conn.close()
    
################################################################################   
    
    def create_table(self, schema):
        sql = self.create_create_table_sql(schema)
        self.execute(sql)

    def insert_entry(self, schema, entry):
        sql = self.create_insert_sql(schema)
        values = self.create_entry_values(schema, entry)
        self.execute(sql, values)
        
    def insert_entries(self, schema, entries):
        sql = self.create_insert_sql(schema)
        values = self.create_entries_values(schema, entries)
        self.execute(sql, values)
        
    def load(self, schema):
        sql = self.create_simple_select_sql()
        result = self.execute(sql)
        return self.to_table(schema, result)
    
    def load_better(self, schema, \
                    fields = None, where = None, group = None, order = None):
        sql = self.create_select_sql(schema, fields, where, group, order)
        result = self.execute(sql)
        new_schema = self.create_schema(fields)
        return self.to_table(new_schema, result)
        
################################################################################   

    def create_create_table_sql(self, schema):
        fields_decl = ", ".join(list(map(
            lambda fn: \
                "{0} {1} {2}".format( \
                    self.column_name(fn), self.sql_type_of_field(schema, fn), \
                    "PRIMARY KEY" if fn == ID else ""),
            schema)))
    
        return "CREATE TABLE {0} ({1})" \
                .format(self.table_name, fields_decl)

    def create_insert_sql(self, schema):
        fields_decl = ", ".join(list(map(
            lambda fn: self.column_name(fn),
            schema)))
        
        values_decl = ", ".join(list(map(
            lambda fn: "?",
            schema)))
        
        return "INSERT INTO {0} ({1}) VALUES ({2})" \
                .format(self.table_name, fields_decl, values_decl)

    def create_simple_select_sql(self):
        return "SELECT * FROM {0}" \
            .format(self.table_name)
            
            
    def create_select_sql(self, schema, fields, where, group, order):
        
        sql = "SELECT "
        if fields:
            sql += self.fields_to_sql(schema, fields)
        else:
            sql += "*"
        
        sql += " FROM "
        sql += self.table_name
        
        if where:
            sql += " WHERE "
            sql += self.condition_to_sql(schema, where)
            
        if group:
            sql += " GROUP BY "
            sql += self.group_to_sql(schema, group)        
        
        if order:
            sql += " ORDER BY "
            sql += self.order_to_sql(schema, order)        
         
        return sql
################################################################################
    def to_table(self, schema, result):          
        table = RowsMutableTable(schema)
        for row in result:
            entry = self.to_entry(schema, row)
            table += entry
            
        return table.to_table()
            
    def to_entry(self, schema, row):
        values = dict(map( \
            lambda fn, val: (fn, val), \
            schema, row))
        
        return Entry.create(schema, values)
    
    def create_entry_values(self, schema, entry):
        return tuple(map(
            lambda fn: entry[fn],
            schema))
        
    def create_entries_values(self, schema, entries):
        return list(map(
            lambda e: self.create_entry_values(schema, e),
            entries))

    def create_schema(self, fields):
        new_fields = dict(map(
            lambda fn: (fn, self.field_type(fn, fields[fn])),
            fields.keys()))
        
        return Schema(new_fields)

################################################################################
    
    def column_name(self, field_name):
        #return "\'" + field_name + "\'" 
        return field_name
        
    def field_type(self, field_name, field_expression):
        return "Computed" #TODO

        
    def sql_type_of_field(self, schema, field_name):
        field_type = schema[field_name]
        
        if field_type in ("int", "integer"):
            return "INT"
            
        if field_type in ("decimal", "float"):
            return "REAL"
        
        if field_type in ("bool", "boolean"):
            return "BOOL"
            
        return "TEXT"
    

    def fields_to_sql(self, schema, fields):
        if ID not in fields.keys():
            fields = { **{ID: "'no id'"}, **fields }
        
        if SOURCE not in fields.keys():
            fields = { **{SOURCE: "'sql lite'"}, **fields }
        
            
        return ", ".join(map( \
            lambda fn: "{0} AS {1}".format(fields[fn], fn),
            fields.keys()))
        
    def condition_to_sql(self, schema, condition):
        if isinstance(condition, str):
            return condition
        else:
            return " AND ".join(condition)
    
    def group_to_sql(self, schema, group):
        if isinstance(group, str):
            return group
        else:
            return ", ".join(group)
        
    def order_to_sql(self, schema, order):
        if isinstance(order, str):
            return order
        else:
            return ", ".join(order)
    
    
    
################################################################################

    def execute(self, sql, values = ()):
        print("SQL: " + str(sql) + ", WITH " + str(values)) #TODO debug
        
        c = self._conn.cursor()
        if isinstance(values, tuple):
            result = c.execute(sql, values)
        else:
            result = c.executemany(sql, values) 
            
        self._conn.commit()
        return result
    
################################################################################    
    def __enter__(self):
        self.connect()
        return self
        
#    def __exit__(self, exc_type, exc_value, traceback):
#        self.disconnect()
#        return self
        
################################################################################
if __name__ == '__main__':
    print("Testing the SQL Lite")
    schema = Schema({"foo": "str", "bar": "int"})

    os.remove("/tmp/dbf.db")
#    with SQLLite("/tmp/dbf.db", "samples") as sqll:
    sqll = SQLLite("/tmp/dbf.db", "samples")
    sqll.connect()
    
    print("creating table")
    sqll.create_table(schema)
    
    print("inserting entry")
    entry = Entry.create_new(schema, 1, "sqll", {"foo": "hello", "bar": 42})   
    sqll.insert_entry(schema, entry)
    
    print("inserting entries")
    entries = [ \
        Entry.create_new(schema, 2, "sqll", {"foo": "lorem", "bar": 99}),    
        Entry.create_new(schema, 3, "sqll", {"foo": "ipsum", "bar": 11}),
        Entry.create_new(schema, 4, "sqll", {"foo": "dolor", "bar": 11})
    ]
    sqll.insert_entries(schema, entries)
    
    print("loading")
    table = sqll.load(schema)
    table.printit()
    
    print("query without group")
    table = sqll.load_better(schema, \
        {"identity" : ID, "fooo" : "foo", "baar": "bar + 1"}, \
        "bar < 50", None, "fooo")
    table.printit()
    
    # TODO the groupping
    