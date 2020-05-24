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
    
    # function (items, new_item) => item_to_add_after
    add_after: Callable
    # the actual list of items
    items: List[Any]
    
    def __init__(self, add_after, *items):
        self.add_after = add_after
        self.items = list()
        
        for item in items:
            self.add(item) 
            
    ####################################################################
        
    def add(self, item):
        add_after_item = self.add_after(self.items, item)
        
        if add_after_item is None:
            self.items.insert(0, item)
        else:
            index = self.items.index(add_after_item)
            if (index + 1) < len(self.items):
                self.items.insert(index + 1, item)
            else:
                self.items.append(item)

    
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
        """ Creates the tree """
        
        self.paths = SimpleOrderedBag(lambda its, ni : self.add_after(its, ni))
        self.nodes = dict()
        
        for p,v in nodes.items():
            self.add(p, v)
    
    def add_after(self, items, item):
        if len(items) == 0:
            return None
        
        parent = item.parent()
        siblings = self.subpaths(parent)
        #print("S {0} of {1}".format(siblings, item))
        if len(siblings) > 0:
            return siblings[-1]
        else:
            return parent
        
        #if parent.is_root():
        #    return None
        # 
        #grandpa = parent.parent()
        #cousins = self.subpaths(grandpa)
        #print("C {0} of {1}".format(cousins, item))
        #if len(cousins) > 0:
        #    return cousins[-1]
        #    
        #if grandpa.is_root():
        #    return None
        #    
        #return None
       
        
        #if not (before.is_root() or after.is_root() or new.is_root()):
        #    if (before.parent() is new.parent()) and(new.parent() is not after.parent()):
        #        return True
        #     
        #if before.is_child(after):
         #   return False
        
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
