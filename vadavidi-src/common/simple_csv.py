"""
The module with simple CSV file manipulation implemented.
"""

from common.datas import *
from common.datas_util import RowsMutableTable


###############################################################################
class SimpleCSV():
    """
    The simple implementation of the CSV file manipulator. Simply loads or saves
    the simple CSV file, with custom separator, optionally with the header
    or the ID and SOURCE.
    """
    # the separator of the items
    separator = '\t'
    
    # may save/load with header?
    with_header = False
    
    # may save metas to file / load from file or user the ordernum and file_name
    # as ID an SOURCE?
    with_metas = False
    
    def __init__(self, with_header, with_metas, separator = '\t'):
        self.with_header = with_header
        self.with_metas = with_metas
        self.separator = separator
    
    def load_table(self, schema, file_name):
        """ Loads the table from the file """
        
        lines = self.list_lines(file_name)
        return self.lines_to_table(file_name, schema, lines)
    
    def list_lines(self, file_name):
        """ Loads the lines from the file, including first if with_header """
        with open(file_name, "r") as f:
            lines = f.readlines()
            if self.with_header:
                lines = lines[1:]
                
            clean = list(map(lambda line: line.replace('\n', ''), lines)) 
            return clean

    def lines_to_table(self, file_name, schema, lines):
        """ Converts the lines to the table """
        table = RowsMutableTable(schema)
        
        for ordnum, line in enumerate(lines):
            entry = self.line_to_entry(file_name, schema, ordnum, line)
            table += entry
            
        return table.to_table()

    def line_to_entry(self, file_name, schema, ordnum, line):
        """ Converts the line to the entry """
        
        parts = line.split(self.separator)
        
        fields = self.fields(schema)
        values = dict(map(lambda part, field: (field, part), parts, fields))
        
        if self.with_metas:
            return Entry.create(schema, values)
        else:
            return Entry.create_new(schema, ordnum, file_name, values)
    
    def save_table(self, table, file_name):
        """ Saves the table into the given file """
        
        lines = self.table_to_lines(table)
        self.save_lines(lines, file_name)
    
    def save_lines(self, lines, file_name):
        """ Saves the given lines into the file """
        
        with open(file_name, "w") as f:
            for line in lines:
                f.write(line)
                f.write('\n')
    
    def table_to_lines(self, table):
        """ Converts the table to lines. If with_header, then adds schema as 
        well """
        
        result = []
        if self.with_header:
            result += [self.schema_to_line(table.schema)]
        
        result += map(lambda e: self.entry_to_line(table.schema, e),
                      table.entries)
        
        return result
    
    def schema_to_line(self, schema):
        """ Converts schema to line """
        fields = self.fields(schema)
        return self.separator.join(fields)
    
    def entry_to_line(self, schema, entry):
        """ Converts entry to line """
        
        fields = self.fields(schema)
            
        values = list(map(
            lambda fn: str(entry.value(fn)),
            fields))
        return self.separator.join(values)

    def fields(self, schema):
        """ Obtains the fields we are working with. If not with_metas, ID and 
        SOURCE gets excluded """
        
        if self.with_metas:
            return schema.list_field_names()
        else:
            return schema.list_raw()
    
###############################################################################
if __name__ == '__main__':
    print("See the test_simple_csv module to test it")

    
