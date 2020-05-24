"""
The test for the pitree module.
"""
import unittest
from config.pitree import PiTreePath, PiTree, PiTreeIterator, SimpleOrderedBag
from functools import reduce

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

        print("Chi? Yu: " + str(parent.is_child(first)))
        print("Chi? Nu: " + str(first.is_child(parent)))

        print("Chi? Nu: " + str(parent.is_child(child)))
        print("Chi? Nu: " + str(first.is_child(second)))


################################################################################
    def place_path_in(self, items, item):
        if item.is_root():
            return None
        else:
            return item.parent()
        
    def place_int_after(self, items, item):
        if len(items) == 0:
            return None
        
        if item < items[0]:
            return None

        before = reduce(lambda ai, ci : (ci if ci < item else ai), items)
        return before
        
    def test_simple_ordered_bag(self):
        print("=== TESTING SIMPLE ORDERED BAG")
        
        lst = SimpleOrderedBag(lambda its, ni: self.place_int_after(its, ni))
        lst.add(10)
        lst.add(11)
        lst.add(45)
        lst.add(8)
        lst.add(26)
        print(lst)
        
        lst.remove(11)
        lst.add(30)
        print(lst)
        
        lst = SimpleOrderedBag(lambda its, ni: self.place_path_in(its, ni))
            
        lst.add(PiTreePath())
        lst.add(PiTreePath("foo"))
        lst.add(PiTreePath("bar"))
        lst.add(PiTreePath("foo", "BAZ"))
        lst.add(PiTreePath("foo", "AUX"))
        lst.add(PiTreePath("bar", "QUX"))
        print("\n".join(map(str, list(lst))))
        
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
        tree.add(fobb, 420)
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
        tree.add(PiTreePath(1, 2, 99), "karel")
        tree.add(PiTreePath(1, 4), "franta")
        tree.add(PiTreePath(1, 2, 88), "pepa")
        tree.add(PiTreePath(1, 3, -1), "lojza")
        tree.add(PiTreePath(1, 2, 77), "jirka")
        
        print("The tree:")
        tree.printit()
        
        print("The iterator:")
        triter = PiTreeIterator(tree)
        while True:
            path = triter.next()
            print(path)
            if path is None:
                break
        
        
################################################################################
if __name__ == "__main__":
    unittest.main()
