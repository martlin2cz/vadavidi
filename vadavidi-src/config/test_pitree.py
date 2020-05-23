"""
The test for the pitree module.
"""
import unittest
from config.pitree import PiTreePath, PiTree, PiTreeIterator

################################################################################
class PitreeTest(unittest.TestCase):

################################################################################
    def test_path(self):
        print("=== TESTING PATH")
        
        first = PiTreePath("foo", 42, "Bar", True)
        second = PiTreePath("foo", 42, "BAAZ")
        
        parent = first.parent()
        print("Parent: " + str(parent))
        
        child = first.child("Karel")
        print("Child: " + str(child))
        
        print("Sub? No: " + str(first.is_subpath(second)))
        print("Sub? No: " + str(second.is_subpath(first)))
        
        print("Sub? Nu? " + str(first.is_subpath(first)))
        print("Sub? No: " + str(first.is_subpath(parent)))
        
        print("Sub? Yu: " + str(parent.is_subpath(first)))
        print("Sub? Yu: " + str(parent.is_subpath(child)))
        
################################################################################
    def test_tree(self):
        print("=== TESTING TREE")
        
        root = PiTreePath()
        foo = PiTreePath("foo")
        bar = PiTreePath("foo", "bar")
        baz = PiTreePath("foo", "baz")
        aux = PiTreePath("foo", "aux")
        qux = PiTreePath("foo", "aux", "qux")
        quux = PiTreePath("foo", "aux", "qux", "quux")
        
        
        tree = PiTree()
        print("New tree:")
        tree.printit()
        
        tree.add(root, -1)
        tree.add(foo, 42)
        tree.add(bar, 99)
        tree.add(baz, False)
        tree.add(aux, "Lorem")
        tree.add(qux, "Ipsum")
        tree.add(quux, "Dolor")
        print("Constructed (added):")
        tree.printit()
        
        subtree = tree.subtree(PiTreePath("foo", "aux"))
        print("Subtree:")
        subtree.printit()
        
        print("Removed:")
        tree.remove(aux)
        tree.printit()
        
        fobb = PiTreePath("foo", "bar", "BAZ")
        print("Readded:")
        tree.add(fobb, "FAIL")
        tree.printit()

################################################################################
    def test_iterator(self):
        print("=== TESTING ITERATOR")
        tree = PiTree()
        
        tree.add(PiTreePath(), "lorem")
        tree.add(PiTreePath(1), "ispum")
        tree.add(PiTreePath(1, 2), "dolor")
        tree.add(PiTreePath(2), "sit")
        tree.add(PiTreePath(1, 3), "amet")
        
        iter = PiTreeIterator(tree)
        while True:
            path = iter.next()
            print(path)
            if path is None:
                break
        
        
################################################################################
if __name__ == "__main__":
    unittest.main()