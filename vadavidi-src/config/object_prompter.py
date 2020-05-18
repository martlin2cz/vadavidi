"""
TODO doc
"""
from config.base_objecter import BaseObjectSchemater, BaseObjectBuilder
from config.value_obtainers_impls import \
    ObjectConstructionPrompter, ClassChoosePrompter
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
class ImplementingClassPrompter(BaseCompositePrompter):
    
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
        
    
    def to_next(self):
        cp = self.current_composite_prompter()
        prompter = cp.current()
        
        if prompter is None:
            prompter = self.pop_up_to_next()
        elif isinstance(prompter, ClassChoosePrompter):
            clazz = prompter.clazz
            self.start_prompting_new_class(clazz)
        # TODO if is list prompter/dict promter
        else:
            cp.next()
            
        return prompter
        
    def set_value(self, value): 
        cp = self.current_composite_prompter()
        
        if isinstance(cp, ImplementingClassPrompter):
            self.start_prompting_new_object(value)
        
        prompter = cp.current()
       
        
        
        print("setted " + str(cp) + " to " + str(value))    
        
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
    def start_prompting_new_class(self, clazz):
        print("# prompting new class: " + clazz)
        
        prompter = self.create_new_class_prompter(clazz)
        cp = ImplementingClassPrompter(prompter)
        self.push_composite_prompter(cp)
        
    def start_prompting_new_object(self, clazz):
        print("# prompting new object: " + clazz)
         
        prompter = self.create_new_object_prompter(clazz)
        fields_prompters = self.schemater.list_fields(clazz)
        
        cp = ObjectInstanceCompositePrompter(prompter, fields_prompters)
        
        self.pop_composite_prompter()
        self.push_composite_prompter(cp)
  
    def pop_up_to_next(self):
        print("# going back")
        while True:
            cp = self.current_composite_prompter()
            if cp is None:
                return None
            
            prompter = cp.next()
            if prompter is not None:
                return prompter
            
            self.pop_composite_prompter()

################################################################################
    def create_new_class_prompter(self, clazz):
        impls_names = self.schemater.list_impls(clazz)
        impls = dict(map(lambda n: (n, self.create_new_object_prompter(n)),
                         impls_names))
        
        return ClassChoosePrompter(clazz, clazz)

    def create_new_object_prompter(self, clazz):
        return ObjectConstructionPrompter(clazz, clazz)

 