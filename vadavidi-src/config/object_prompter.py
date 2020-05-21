"""
TODO doc
"""
from config.base_objecter import BaseObjectSchemater, BaseObjectBuilder
from config.value_obtainers_impls import \
    ObjectConstructionPrompter, ClassChoosePrompter, ListPrompter, DictPrompter
from abc import abstractmethod

################################################################################
class BaseCompositePrompter:
    
    @abstractmethod
    def current(self):
        pass
    
    @abstractmethod    
    def next(self):
        pass
        
    @abstractmethod
    def prev(self):
        pass

################################################################################
class ObjectInstanceCompositePrompter(BaseCompositePrompter):
    
    def __init__(self, prompter, fields_prompters):
        self.prompter = prompter
        self.fields_prompters = fields_prompters
        self.current_field = 0
    
    def get_current(self):
        fields_list = list(self.fields_prompters.values())
        if self.current_field in range(0, len(fields_list)): 
            return fields_list[self.current_field]
        else:
            return None
    
    def current(self):
        return self.get_current()
    
    def next(self):
        self.current_field += 1
        return self.get_current()
        
    def prev(self):
        self.current_field -= 1
        return self.get_current()

################################################################################
class ImplementingClassCompositePrompter(BaseCompositePrompter):
    
    def __init__(self, prompter):
        self.prompter = prompter
        self.current_index = 0
    
    def prompter_if_current(self):
        if self.current_index == 0:
            return self.prompter
        else:
            return None
    
    def current(self):
        return self.prompter_if_current()
    
    def next(self):
        self.current_index += 1
        return self.prompter_if_current()
        
    def prev(self):
        self.current_index -= 1
        return self.prompter_if_current()

################################################################################
class ListCompositePrompter(BaseCompositePrompter):
    
    def __init__(self, prompter):
        self.prompter = prompter
        self.current_index = 0
    
    def current(self):
        return self.prompter.item_prompter
    
    def next(self):
        self.current_index += 1
        return self.prompter.item_prompter
        
    def prev(self):
        if self.current_index > 0:
            self.current_index -= 1
            return self.prompter.item_prompter 
        else:
            return None   

################################################################################
class DictCompositePrompter(BaseCompositePrompter):
    
    def __init__(self, prompter):
        self.prompter = prompter
        self.current_index = 0
    
    def is_key(self):
        return (self.current_index % 2) == 0
    
    def pick_prompter(self, index):
        if (index % 2) == 0:
            return self.prompter.key_prompter
        else:
            return self.prompter.value_prompter
    
    def current(self):
        return self.pick_prompter(self.current_index)
    
    def next(self):
        return self.pick_prompter(self.current_index + 1)
        
    def prev(self):
        if self.current_index > 0:
            return self.pick_prompter(self.current_index - 1)
        else:
            return None
################################################################################
################################################################################
class ObjectPrompter():
    """
    TODO doc
    """
    #clazz: str
    
    schemater: BaseObjectSchemater
    builder: BaseObjectBuilder
    
    
    def __init__(self, schemater, builder, clazz):
        self.schemater = schemater
        self.builder = builder
        
        self._prompters = []
        self.start_prompting_new_class(clazz)
        
################################################################################

    def to_next(self):
        cp = self.current_composite_prompter()
        if cp is None:
            return None
        
        prompter = cp.current()

        self.prepare_builder_for(cp, prompter)        
        self.prepare_stack_for(cp, prompter)
            
        return prompter
        
    def prepare_stack_for(self, cp, prompter):
        if isinstance(cp, ObjectInstanceCompositePrompter) \
           and prompter is None:
            prompter = self.finish_prompting_object()
            
        elif isinstance(prompter, ClassChoosePrompter):
            clazz = prompter.clazz
            self.start_prompting_new_class(clazz)
            
        elif isinstance(prompter, ListPrompter):
            self.start_prompting_new_list(prompter)
            
        elif isinstance(prompter, DictPrompter):
            self.start_prompting_new_dict(prompter)
            
        else:
            cp.next()
            
    def prepare_builder_for(self, cp, prompter):
        if isinstance(cp, ObjectInstanceCompositePrompter):
            if prompter is not None:
                field_name = self.find_field_name(cp.prompter.clazz, prompter)
                self.builder.add_field(field_name)
            
        elif isinstance(prompter, ListPrompter):
            self.builder.add_list_item()
            
        elif isinstance(prompter, DictPrompter):
            if cp.is_key():
                self.builder.add_dict_key()
            else:
                self.builder.add_dict_value()

    def find_field_name(self, clazz, prompter):
        fields_prompters = self.schemater.list_fields(clazz)
        
        for field_name, field_prompter in fields_prompters.items():
            if field_prompter == prompter:
                return field_name
################################################################################

    def set_value(self, value): 
        cp = self.current_composite_prompter()
        
        if isinstance(cp, ImplementingClassCompositePrompter):
            self.start_prompting_new_object(value)
            return
        
        elif isinstance(cp, ListCompositePrompter):
            if value is None:
                self.finish_prompting_list()
            
            return
            
        elif isinstance(cp, DictCompositePrompter):
            if value is None:
                self.finish_prompting_dict()
        
            return
        
        #print("setting " + str(cp) + " to " + str(value))
        self.builder.set_value(value)    
        
################################################################################
    def current_composite_prompter(self):
        if len(self._prompters) > 0:
            return self._prompters[-1]
        else:
            return None
    
    def push_composite_prompter(self, prompter):
        return self._prompters.append(prompter)
    
    def pop_composite_prompter(self):
        return self._prompters.pop()
    
################################################################################
    def pop_up_to_next(self):
        while True:
            self.pop_up_builder()
            self.pop_composite_prompter()
            
            cp = self.current_composite_prompter()
            if cp is None:
                return None
            
            prompter = cp.next()
            if prompter is not None:
                # FIXME if uncommented, works second sample, but not first
                #self.prepare_builder_for(cp, prompter)
                return prompter

    def pop_up_builder(self):
        cp = self.current_composite_prompter()
        if isinstance(cp, ObjectInstanceCompositePrompter):
            self.builder.end_object()
            
        elif isinstance(cp, ListCompositePrompter):
            self.builder.end_list()
            
        elif isinstance(cp, DictCompositePrompter):
            self.builder.end_dict()


    def start_prompting_new_class(self, clazz):
        print("# prompting new class: " + clazz)
        
        prompter = self.create_new_class_prompter(clazz)
        cp = ImplementingClassCompositePrompter(prompter)
        self.push_composite_prompter(cp)
        
        
    def start_prompting_new_object(self, clazz):
        print("# prompting new object: " + clazz)
         
        prompter = self.create_new_object_prompter(clazz)
        fields_prompters = self.schemater.list_fields(clazz)
        
        cp = ObjectInstanceCompositePrompter(prompter, fields_prompters)
        
        self.pop_composite_prompter()
        self.push_composite_prompter(cp)
        self.builder.new_object(clazz)
    
    def finish_prompting_object(self):
        print("# finishing the object")
        self.pop_up_to_next()
        #self.builder.end_object()
  
    def start_prompting_new_list(self, prompter):
        print("# prompting new list")
        
        cp = ListCompositePrompter(prompter)
        self.push_composite_prompter(cp)
        self.builder.new_list()
    
    def finish_prompting_list(self):
        print("# finishing the list")
        self.pop_up_to_next()
        #self.builder.end_list()
  
    def start_prompting_new_dict(self, prompter):
        print("# prompting new dict")
        
        cp = DictCompositePrompter(prompter)
        self.push_composite_prompter(cp)
        self.builder.new_dict()
  
    def finish_prompting_dict(self):
        print("# finishing the dict")
        self.pop_up_to_next()
        #self.builder.end_dict()

################################################################################
    def create_new_class_prompter(self, clazz):
        impls_names = self.schemater.list_impls(clazz)
        impls = dict(map(lambda n: (n, self.create_new_object_prompter(n)),
                         impls_names))
        
        return ClassChoosePrompter(clazz, clazz)

    def create_new_object_prompter(self, clazz):
        return ObjectConstructionPrompter(clazz, clazz)

 