import re

class Calculator():
    def __init__(self):
        self.operators = {
            "+": 1,
            "-": 1,
            "*": 2,
            "/": 2
        }
        
    def get_tokens(self, expression):
        expression = re.sub(r"\s+", "", expression)
        result = []
        last_element = ""
        for element in expression:
            if not element.isnumeric():
                if last_element:
                    result.append(last_element)
                    last_element = ""

                result.append(element)
                continue

            last_element += element

        if last_element:
            result.append(last_element)
        return result    
    
    def apply(self, op, first, second):
        first = float(first)
        second = float(second)
        if op == "+":
            return first + second
        if op == "-":
            return first - second
        if op == "*":
            return first * second
        if op == "/":
            return first / second
        
    def evaluate_postfix(self, postfix):
        stack = []
        for token in postfix:
            if token.isdigit():
                stack.append(token)

            if token in self.operators:
                second = stack.pop()
                first = stack.pop()
                stack.append(self.apply(token, first, second))

        return stack.pop()
    
    # Shunting-yard algorithm to transform expression to the postfix notation
    def calculate(self, expression):
        tokens = self.get_tokens(expression)

        output_queue = []
        operator_stack = []

        for token in tokens:
            if token.isnumeric():
                output_queue.append(token)

            if token in self.operators: 
                while (len(operator_stack) > 0
                        and operator_stack[-1] in self.operators 
                        and not self.operators[operator_stack[-1]] < self.operators[token]):
                    output_queue.append(operator_stack.pop())

                operator_stack.append(token)

            if token == "(":
                operator_stack.append("(")

            if token == ")":
                while operator_stack[-1] != "(":
                    output_queue.append(operator_stack.pop())

                if operator_stack[-1] == "(":
                    operator_stack.pop()


        while len(operator_stack) > 0:
            output_queue.append(operator_stack.pop())

        return self.evaluate_postfix(output_queue)