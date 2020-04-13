# the simple csv module for loading/saving

from common.datas import *


########################################################################
class SimpleCSV():
    separator = '\t'
    
    def listLines(self, fileName):
        with open(fileName, "r") as f:
            lines = f.readlines()
            clean = list(map(lambda line: line.replace('\n', ''), lines)) 
            return clean

    def lineToEntry(self, ordnum, schema, line):
        parts = line.split(self.separator)
        values = dict(map(lambda part, field: (field, part), parts, schema.listFieldNames()))
        
        return Entry.create(schema, ordnum, values)
    
    def saveLines(self, lines, fileName):
        with open(fileName, "w") as f:
            for line in lines:
                f.write(line)
                f.write('\n')
    
    def schemaToLine(self, schema):
        values = schema.listFieldNames()
        return self.separator.join(values)
    
    def entryToLine(self, schema, entry):
        values = [entry.ordernum()] + list(map(
            lambda fn: str(entry.value(fn)),
            schema.listFieldNames()))
        return self.separator.join(values)

    
########################################################################
if __name__ == '__main__':
    print("Testing the SimpleCSV")
    schema = Schema({"foo": "int", "bar": "str"})
    table = Table(schema, [ \
        Entry(0, {"foo": 42, "bar": "lorem"}), \
        Entry(1, {"foo": 99, "bar": "ipsum"}) \
    ])
    
    table.printit()
    
    csv = SimpleCSV()
    print("Saving!")
    lines = list(csv.entryToLine(schema, e) for e in table.list())
    csv.saveLines(lines, "/tmp/test.csv")
    
    print("Loading!")
    lines = csv.listLines("/tmp/test.csv")
    entries = list(csv.lineToEntry(i, schema, l) for (i, l) in enumerate(lines))
    
    table = Table(schema, entries)
    table.printit()
    
    
