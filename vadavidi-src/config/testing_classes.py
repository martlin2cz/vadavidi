"""
Just the testing classes declaration.
"""
from abc import ABC, abstractmethod
from math import sqrt
from typing import List, Dict
from functools import reduce
from dataclasses import dataclass

################################################################################
class BaseOperation(ABC):
    
    @abstractmethod
    def evaluate(self, context):
        pass

################################################################################
class BaseAtom(ABC):
    
    @abstractmethod
    def get_value(self, context):
        pass

################################################################################
class AtomicValueOperation(BaseOperation):
    
    def __init__(self, value: BaseAtom):
        self.value = value

    def evaluate(self, context):
        return self.value.get_value(context)

################################################################################
class UnaryOperation(BaseOperation):
    
    def __init__(self, operator: str, operand: BaseOperation):
        self.operator = operator
        self.operand = operand        
        
        
    def evaluate(self, context):
        if self.operator == "+":
            return self.operand.evaluate(context)
        elif self.operator == "-":
            return - self.operand.evaluate(context)
        elif self.operator == "sqrt":
            return sqrt(self.operand.evaluate(context))


################################################################################
class BinaryOperation(BaseOperation):
    
    def __init__(self, operator: str, first_operand: BaseOperation, second_operand: BaseOperation):
        self.operator = operator
        self.first_operand = first_operand
        self.second_operand = second_operand
        
        
    def evaluate(self, context):
        if self.operator == "+":
            return self.first_operand.evaluate(context) + self.second_operand.evaluate(context)
        elif self.operator == "-":
            return self.first_operand.evaluate(context) - self.second_operand.evaluate(context)
        elif self.operator == "*":
            return self.first_operand.evaluate(context) * self.second_operand.evaluate(context)
        elif self.operator == "/":
            return self.first_operand.evaluate(context) / self.second_operand.evaluate(context)

################################################################################
class NaryOperation(BaseOperation):
    
    def __init__(self, operator: str, operands: List[BaseOperation]):
        self.operator = operator
        self.operands = operands
        
        
    def evaluate(self, context):
        op = None
        if self.operator == "+":
            op = lambda  x, y : x + y
        elif self.operator == "-":
            op = lambda  x, y : x - y
        elif self.operator == "*":
            op = lambda  x, y : x * y
        elif self.operator == "/":
            op = lambda  x, y : x / y
                
        return reduce(op, map(lambda o: o.evaluate(context), self.operands))

################################################################################
class PolynomOperation(BaseOperation):
    
    def __init__(self, cooeficients: Dict[BaseOperation, int]):
        self.cooeficients = cooeficients
        
        
    def evaluate(self, context):
        return reduce(lambda x, y: x + y, \
                      map(lambda ce: ce[0].get_value(context) ** ce[1], \
                          self.cooeficients.items()))
    
################################################################################
@dataclass(unsafe_hash = True)
class VariableAtom(BaseAtom):
    
    variable_name: str

    def get_value(self, context):
        return context[self.variable_name]

################################################################################
@dataclass(unsafe_hash = True)
class IntNumberAtom(BaseAtom):
    
    int_value: int
    
    def get_value(self, context):
        return self.int_value

################################################################################
@dataclass(unsafe_hash = True)
class FloatNumberAtom(BaseAtom):
    
    float_value: float
    
    def get_value(self, context):
        return self.float_value


################################################################################
@dataclass(unsafe_hash = True)
class ComplexNumberAtom(BaseAtom):
    
    real_value: float
    imaginary_value: float
    
    def get_value(self, context):
        return complex(self.real_value, self.imaginary_value)

################################################################################
if __name__ == '__main__':
    print("Testing the testing math expressions")
    var_op = AtomicValueOperation(VariableAtom("x_0"))
    
    bin_op = BinaryOperation("*", \
                 AtomicValueOperation(ComplexNumberAtom(0.9, 0.01)), \
                 AtomicValueOperation(IntNumberAtom(42)))
    
    unary_op = UnaryOperation("-", \
                 AtomicValueOperation(IntNumberAtom(1010)))
    
    poly_op = PolynomOperation({ \
         VariableAtom("x_0"): 3, \
         IntNumberAtom(4): 2, \
         FloatNumberAtom(0.9): 1 })
    
    nary = NaryOperation("+", [var_op, bin_op, unary_op, poly_op])
    
    context = {"x_0": -1}
    print(nary.evaluate(context))
