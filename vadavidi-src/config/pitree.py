"""
The pitree module contains the implementation of "path involved tree" tree
structure implementation.
"""
from typing import Tuple, Mapping, Any, List, Callable
from dataclasses import dataclass

################################################################################
@dataclass(unsafe_hash = True, eq = True, order=True)
class PiTreePath:
    """ The path of the PiTree node in the PiTree tree. """
    
    segments: Tuple[Any]
    
    def __init__(self, *segments):
        self.segments = tuple(segments)
        
    def last(self):
        if self.is_root():
            raise ValueError("Already root")
        
        return self.segments[-1]
    
    def parent(self):
        if self.is_root():
            raise ValueError("Already root")
        
        segments = self.segments[:-1]
        return PiTreePath(*segments)
    
    def child(self, child):
        segments = self.segments + (child,)
        return PiTreePath(*segments)
    
    def common_predcestor(self, apath):
        segments = list()
        
        for i in range(min(len(self), len(apath))):
            first_seg = self.segments[i]
            second_seg = apath.segments[i]
            
            if first_seg is not second_seg:
                break
            
            segments.append(first_seg)
        
        return PiTreePath(*segments)
    
    def is_root(self):
        return len(self.segments) == 0
    
    def is_subpath(self, subpath):
        if len(self) >= len(subpath):
            return False
        
        for i in range(0, len(self)):
            this_seg = self.segments[i]
            subpath_seg = subpath.segments[i]
            
            if this_seg is not subpath_seg:
                return False
        
        return True
    
    def is_child(self, child_path):
        if not self.is_subpath(child_path):
            return False
        
        if (len(self) + 1) is not len(child_path):
            return False
        
        return True
        
    
    def __len__(self):
        return len(self.segments)
    
    def __str__(self):
        return "P:/" + "/".join(map(str, self.segments))

################################################################################
class SimpleOrderedBag:
    """ The simple set/bag which respects the ordering of the items. """
    
    # function (item_before, new_item, item_after) => bool
    place_in: Callable
    # the actual list of items
    items: List[Any]
    
    def __init__(self, place_in, *items):
        self.place_in = place_in
        self.items = list()
        
        for item in items:
            self.add(item) 
            
            
    ####################################################################
        
    def add(self, item):
        #print("YUUUMY {0}".format(item))
        
        for i in range(-1, len(self.items)):
            before = self.items[i] if i >= 0 else None
            after = self.items[i+1] if i + 1 < len(self.items) else None
            #print("Y {0} | {1} ? {2}".format(before, after, self.place_in(before, item, after)))
            if self.place_in(before, item, after):
                if i+1 < len(self.items):
                    #print("HAAA inserting {0} at {1}".format(item, i+1))
                    self.items.insert(i+1, item)
                else:
                    #print("HAAA appending {0} at E".format(item))
                    self.items.append(item)
                return
         
             
        raise ValueError("Nowhere to put")

    
    def remove(self, item):
        self.items.remove(item)
    
    def get(self, index):
        return self.items[index]
    
    def has(self, item):
        return item in self.items
    
    def count(self):
        return len(self.items)
    
    def list(self):
        return list(self.items)
    
    
    ####################################################################
    
    def __len__(self):
        return self.count()
    
    def __list__(self):
        return self.list()
    
    def __iter__(self):
        return self.items.__iter__()
    
    def __str__(self):
        return "SOL: " + str(self.items)
    
################################################################################
class PiTree:
    """
    PiTree means "path involved tree". In other words just mapping of paths to
    node values.
    """
    
    # the ordered list of the paths
    paths = SimpleOrderedBag
    
    # the mapping of paths to nodes
    nodes: Mapping[PiTreePath, Any]

    def __init__(self, nodes = dict()):
        """ Creates the empty tree """
        
        self.paths = SimpleOrderedBag(lambda b, n, a : self.place_in(b, n, a))
        self.nodes = dict()
        
        for p,v in nodes.items():
            self.add(p, v)
    
    def place_in(self, before, new, after):
        if before is None:
            if after is None:
                return True
            else:
                return False
            
        if after is None:
            return True
       
        
       
       
        
        #if not (before.is_root() or after.is_root() or new.is_root()):
        #    if (before.parent() is new.parent()) and(new.parent() is not after.parent()):
        #        return True
        #     
        if before.is_child(after):
            return False
        
        #if not (before.is_root() or after.is_root() or new.is_root()):
        #    bfr_prdc = before.common_predcestor(new)
        #    aft_prdc = after.common_predcestor(new)
        #    
        #    if bfr_prdc is not aft_prdc:
        #        return True
        
        return True
        
        
        #return self.is_before(before, new) and self.is_before(new, after)
        
        #before_check = len(before) <= len(new)
        #after_check = len(after) <= len(new)
        #
        #if before_check and after_check:
        #    return False
         
        #before_check = before.is_child(new)
        #after_check = not after.is_child(new)
        #
        #print("Y | {0} | {1} | ? {2},{3}".format(before, after, before_check, after_check))
        #if before_check and after_check:
        #    return True
        #    
        #return False
    
    def is_before(self, before, after):
        if before.is_child(after):
            return True
        
        if len(before) == len(after):
            return True
        
        print()
        

        
    ####################################################################
        
    def add(self, path, value):
        if self.has(path):
            raise ValueError("Already present")
        
        #if not path.is_root():
        #    if not self.has(path.parent()):
        #        raise ValueError("No such parent")
        
        self.paths.add(path)
        self.nodes[path] = value
        
    def remove(self, path):
        if not self.has(path):
            raise ValueError("No such node")
        
        for subpath in self.subpaths(path):
            self.paths.remove(subpath)
            self.nodes.pop(subpath)
            
        
        self.paths.remove(path)    
        self.nodes.pop(path)
    
    ####################################################################
    
    def has(self, path):
        return path in self.nodes.keys()
    
    def get(self, path):
        return self.nodes[path]
    
    def subtree(self, path):
        paths = self.subpaths(path)
        nodes = self.values_of(paths)
        
        return PiTree(nodes)   
    
    def children(self, path):
        paths = self.child_paths(path)
        nodes = self.values_of(paths)
        
        return PiTree(nodes)   
    
    ####################################################################
    
    def subpaths(self, path):
        return list(filter(lambda p: path.is_subpath(p), self.paths))
    
    def child_paths(self, path):
        return list(filter(lambda p: path.is_child(p), self.paths))
    
    def values_of(self, paths):
        return dict(map(lambda p: (p, self.nodes[p]), paths))
    
    ####################################################################
    
    def printit(self):
        for path in self.paths:
            value = self.nodes[path]
            print("{0} => {1}".format(path, value))
            
################################################################################
class PiTreeIterator:
    """ The class responsible for iterating over the PiTree nodes. """
    
    def __init__(self, tree: PiTree):
        self.tree = tree
        self.current_path = self.get_path(0)
        
    ####################################################################

    def next(self):
        index = self.path_index(self.current_path)
        self.current_path = self.get_path(index + 1)
        return self.current_path
        
    def previous(self):
        index = self.path_index(self.current_path)
        self.current_path = self.get_path(index - 1)    
        return self.current_path
        
    ####################################################################
        
    def get_path(self, index):
        lst = list(self.tree.paths)

        if index < 0 or index >= len(lst):
            return None
        else:
            return lst[index]
    
    def path_index(self, path):
        lst = list(self.tree.paths)
        return lst.index(path)    
    
    


            
################################################################################