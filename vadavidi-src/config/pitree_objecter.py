"""
The implementation of the objecter classes, but based on the pitree module.
"""
from config.pitree import PiTree, PiTreePath, PiTreeIterator
from config.base_objecter import BaseObjectPrompter, BaseValueObtainer,\
    BaseObjectSchemater, NO_VALUE
from typing import Any
from config.value_obtainers_impls import ClassChoosePrompter, ListPrompter,\
    DictPrompter
import getpass

################################################################################
class OpiTreeValueNode:
    prompter: BaseValueObtainer
    value: Any
    
    def __init__(self, prompter):
        self.prompter = prompter
        self.value = None

    def __str__(self):
        return "OpiTreeValueNode[" \
                + "p=" + str(self.prompter) + ", " \
                + "v=" + str(self.value) + "]"

################################################################################
#===============================================================================
# class OpiTree:
#     """
#     The tree structure based on the PiTree, which works with object structure.
#     """
#     
#     tree: PiTree
# 
#     def __init__(self):
#         self.tree = PiTree()
#         
#     def prompter(self, path):
#         node = self.tree.get(path)
#         return node.prompter
#     
#     def set_value(self, path, value):
#         node = self.tree.get(path)
#         node.value = value
#===============================================================================

################################################################################
class PiTreeObjectPrompter(BaseObjectPrompter):
    
    schemater: BaseObjectSchemater
    tree: PiTree
    pti: PiTreeIterator
    
    def __init__(self, schemater, root_clazz_prompter):
        self.schemater = schemater
        
        self.tree = self.init_tree(root_clazz_prompter)
        #TODO add inital root class choose prompt
        self.pti = PiTreeIterator(self.tree)
    
    
    def init_tree(self, root_clazz_prompter):
        tree = PiTree()
        
        node = None
        path = PiTreePath()
        tree.add(path, node)
        
        node = OpiTreeValueNode(root_clazz_prompter)
        path = path.child("root")
        tree.add(path, node)
        return tree
    
    ################################################
    
    def to_next(self):
        if not self.pti.has_next():
            return NO_VALUE
        
        next_path = self.pti.next()
        next_node = self.tree.get(next_path)
        return next_node.prompter
        
    def specify_value(self, value):
        self.handle_current(value)
        self.handle_specific_parent(value)


    ################################################
    def handle_current(self, value):
        current_path = self.pti.current()
        current_node = self.tree.get(current_path)
        current_prompter = current_node.prompter
        
        if value is NO_VALUE:
            return
        elif isinstance(current_prompter, ClassChoosePrompter):
            self.set_current_value(value)
            self.push_choosen_class_fields(current_path, value)
            
        elif isinstance(current_prompter, ListPrompter):
            self.push_list_item_prompter(current_path)
            
        elif isinstance(current_prompter, DictPrompter):
            self.push_dict_item_prompter(current_path)
                
        else:
            self.set_current_value(value)
            
    def handle_specific_parent(self, value):
        current_path = self.pti.current()
        parent_path = current_path.parent()
        if parent_path.is_root():
            return
        
        parent_node = self.tree.get(parent_path)
        parent_prompter = parent_node.prompter
        
        if isinstance(parent_prompter, ListPrompter):
            if value is not NO_VALUE:
                self.push_list_item_prompter(parent_path)
            
        if isinstance(parent_prompter, DictPrompter):
            if value is not NO_VALUE:
                self.push_dict_item_prompter(parent_path)
           
    ################################################
    def push_list_item_prompter(self, list_prompter_path):
        list_node = self.tree.get(list_prompter_path)
        list_prompter = list_node.prompter
        
        item_prompter = list_prompter.item_prompter
        key = self.size_of_subtree(list_prompter_path)
        
        self.push_prompter(list_prompter_path, key, item_prompter)
        
    def push_dict_item_prompter(self, dict_prompter_path):
        dict_node = self.tree.get(dict_prompter_path)
        dict_prompter = dict_node.prompter
        
        size = self.size_of_subtree(dict_prompter_path)
        is_odd =  size % 2 == 0
        new_key_num = int(size / 2)
                
        item_prompter = dict_prompter.key_prompter \
                if  is_odd\
                else dict_prompter.value_prompter
        
        key = ("key-" + str(new_key_num)) \
                if  is_odd \
                else ("value-" + str(new_key_num))
        
        self.push_prompter(dict_prompter_path, key, item_prompter)

    
    def push_choosen_class_fields(self, object_prompter_path, clazz):
        fields = self.schemater.list_fields(clazz)
        
        for field_name in fields.keys():
            prompter = fields[field_name]
            # TODO only if not already present
            self.push_prompter(object_prompter_path, field_name, prompter)
        
    
    ################################################
    def set_current_value(self, value):
        current_path = self.pti.current()
        current_node = self.tree.get(current_path)
        
        current_node.value = value
    
    def size_of_subtree(self, path):
        childs = self.tree.child_paths(path)
        return len(childs)
        
    def push_prompter(self, parent_path, key, value_prompter):
        
        new_path = parent_path.child(key)
        node = OpiTreeValueNode(value_prompter)
        self.tree.add(new_path, node)
        
        