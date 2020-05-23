"""
The pitree module contains the implementation of "path involved tree" tree
structure implementation.
"""
from typing import Tuple, Mapping, Any
from dataclasses import dataclass

################################################################################
@dataclass(unsafe_hash = True, eq = True, order=True)
class PiTreePath:
    """ The path of the PiTree node in the PiTree tree. """
    
    segments: Tuple[Any]
    
    def __init__(self, *segments):
        self.segments = tuple(segments)
    
    def parent(self):
        if self.is_root():
            raise ValueError("No parent")
        
        segments = self.segments[:-1]
        return PiTreePath(*segments)
    
    def child(self, child):
        segments = self.segments + (child,)
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
        
        if len(self) != len(child_path) + 1:
            return False
        
        return True
        
    
    def __len__(self):
        return len(self.segments)
    
    def __str__(self):
        return "P:/" + "/".join(map(str, self.segments))

################################################################################
class PiTree:
    """
    PiTree means "path involved tree". In other words just mapping of paths to
    node values.
    """
    
    nodes: Mapping[PiTreePath, Any]

    def __init__(self, nodes = dict()):
        """ Creates the empty tree """
        
        self.nodes = nodes
    
    ####################################################################
        
    def add(self, path, value):
        if not path.is_root():
            if not self.has(path.parent()):
                raise ValueError("No such parent")
        
        self.nodes[path] = value
        
    def remove(self, path):
        for subpath in self.subpaths(path):
            self.nodes.pop(subpath)
            
        self.nodes.pop(path)
    
    
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
    
    def subpaths(self, path):
        return list(filter(lambda p: path.is_subpath(p), self.nodes.keys()))
    
    def child_paths(self, path):
        return list(filter(lambda p: path.is_child(p), self.nodes.keys()))
    
    
    def values_of(self, paths):
        return dict(map(lambda p: (p, self.nodes[p]), paths))
    ####################################################################
    
    def printit(self):
        for path in self.nodes.keys(): #sorted(self.nodes.keys()):
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
        lst = list(self.tree.nodes.keys())

        if index < 0 or index >= len(lst):
            return None
        else:
            return lst[index]
    
    def path_index(self, path):
        lst = list(self.tree.nodes.keys())
        return lst.index(path)    
    
    


            
################################################################################