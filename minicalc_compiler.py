import sys
import re

# Clases para tokens
class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {self.value})"

# Analizador Léxico
class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if self.text else None

    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def identifier(self):
        result = ''
        while self.current_char is not None and self.current_char.isalnum():
            result += self.current_char
            self.advance()
        # Palabra reservada: 'var'
        if result == 'var':
            return Token('VAR', 'var')
        return Token('IDENTIFIER', result)

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            if self.current_char.isdigit():
                return Token('INTEGER', self.integer())
            if self.current_char.isalpha():
                return self.identifier()  # Ahora maneja 'var' aquí
            if self.current_char == '+':
                self.advance()
                return Token('PLUS', '+')
            if self.current_char == '-':
                self.advance()
                return Token('MINUS', '-')
            if self.current_char == '*':
                self.advance()
                return Token('MUL', '*')
            if self.current_char == '/':
                self.advance()
                return Token('DIV', '/')
            if self.current_char == '(':
                self.advance()
                return Token('LPAREN', '(')
            if self.current_char == ')':
                self.advance()
                return Token('RPAREN', ')')
            if self.current_char == '=':
                self.advance()
                return Token('ASSIGN', '=')
            if self.current_char == ';':
                self.advance()
                return Token('SEMICOLON', ';')
            raise ValueError(f"Invalid character: {self.current_char}")
        return Token('EOF', None)

# Nodos del AST
class AST:
    pass

class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class Var(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class Assign(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class VarDecl(AST):
    def __init__(self, var_node, assign_node):
        self.var_node = var_node
        self.assign_node = assign_node

# Analizador Sintáctico (Parser Recursivo Descendente)
class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            raise ValueError(f"Expected {token_type}, got {self.current_token.type}")

    def factor(self):
        token = self.current_token
        if token.type == 'INTEGER':
            self.eat('INTEGER')
            return Num(token)
        elif token.type == 'IDENTIFIER':
            self.eat('IDENTIFIER')
            return Var(token)
        elif token.type == 'LPAREN':
            self.eat('LPAREN')
            node = self.expr()
            self.eat('RPAREN')
            return node
        raise ValueError("Invalid factor")

    def term(self):
        node = self.factor()
        while self.current_token.type in ('MUL', 'DIV'):
            token = self.current_token
            self.eat(token.type)
            node = BinOp(left=node, op=token, right=self.factor())
        return node

    def expr(self):
        node = self.term()
        while self.current_token.type in ('PLUS', 'MINUS'):
            token = self.current_token
            self.eat(token.type)
            node = BinOp(left=node, op=token, right=self.term())
        return node

    def statement(self):
        if self.current_token.type == 'VAR':
            self.eat('VAR')
            var_token = self.current_token
            self.eat('IDENTIFIER')
            self.eat('ASSIGN')
            expr_node = self.expr()
            self.eat('SEMICOLON')
            return VarDecl(Var(var_token), Assign(Var(var_token), Token('ASSIGN', '='), expr_node))
        else:
            var_token = self.current_token
            self.eat('IDENTIFIER')
            self.eat('ASSIGN')
            expr_node = self.expr()
            self.eat('SEMICOLON')
            return Assign(Var(var_token), Token('ASSIGN', '='), expr_node)

    def program(self):
        statements = []
        while self.current_token.type != 'EOF':
            statements.append(self.statement())
        return statements

    def parse(self):
        return self.program()

# Tabla de Símbolos
class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def declare(self, name, type='int'):
        if name in self.symbols:
            raise ValueError(f"Variable {name} already declared")
        self.symbols[name] = {'type': type, 'value': None}

    def assign(self, name, value):
        if name not in self.symbols:
            raise ValueError(f"Variable {name} not declared")
        self.symbols[name]['value'] = value

    def get(self, name):
        if name not in self.symbols:
            raise ValueError(f"Variable {name} not declared")
        return self.symbols[name]

# Analizador Semántico
class SemanticAnalyzer:
    def __init__(self, symbol_table):
        self.symbol_table = symbol_table

    def visit(self, node):
        if isinstance(node, VarDecl):
            self.symbol_table.declare(node.var_node.value)
            self.visit(node.assign_node.right)
        elif isinstance(node, Assign):
            self.symbol_table.get(node.left.value)  # Check if declared
            self.visit(node.right)
        elif isinstance(node, BinOp):
            self.visit(node.left)
            self.visit(node.right)
        elif isinstance(node, Var):
            self.symbol_table.get(node.value)
        # Num no necesita verificación

    def analyze(self, ast):
        for stmt in ast:
            self.visit(stmt)

# Generador de Código Intermedio (Tres Direcciones)
class IntermediateCodeGenerator:
    def __init__(self):
        self.code = []
        self.temp_count = 0

    def new_temp(self):
        self.temp_count += 1
        return f"t{self.temp_count}"

    def generate(self, node):
        if isinstance(node, VarDecl):
            temp = self.generate(node.assign_node.right)
            self.code.append(f"{node.var_node.value} = {temp}")
        elif isinstance(node, Assign):
            temp = self.generate(node.right)
            self.code.append(f"{node.left.value} = {temp}")
        elif isinstance(node, BinOp):
            left_temp = self.generate(node.left)
            right_temp = self.generate(node.right)
            temp = self.new_temp()
            self.code.append(f"{temp} = {left_temp} {node.op.value} {right_temp}")
            return temp
        elif isinstance(node, Num):
            return str(node.value)
        elif isinstance(node, Var):
            return node.value
        return ""

    def get_code(self, ast):
        for stmt in ast:
            self.generate(stmt)
        return self.code

# Función principal
def compile_minicalc(source_code):
    # Debugging: Imprimir tokens leídos (descomenta las líneas siguientes para activar)
    # print("Tokens leídos:")
    # temp_lexer = Lexer(source_code)
    # token = temp_lexer.get_next_token()
    # while token.type != 'EOF':
    #     print(token)
    #     token = temp_lexer.get_next_token()
    # print("--- Fin de tokens ---\n")
    
    lexer = Lexer(source_code)
    parser = Parser(lexer)
    ast = parser.parse()
    
    symbol_table = SymbolTable()
    semantic_analyzer = SemanticAnalyzer(symbol_table)
    semantic_analyzer.analyze(ast)
    
    code_gen = IntermediateCodeGenerator()
    intermediate_code = code_gen.get_code(ast)
    
    return intermediate_code, symbol_table.symbols

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python minicalc_compiler.py <input_file>")
        sys.exit(1)
    
    with open(sys.argv[1], 'r') as f:
        source = f.read()
    
    try:
        intermediate_code, symbols = compile_minicalc(source)
        print("Intermediate Code:")
        for line in intermediate_code:
            print(line)
        print("\nSymbol Table:")
        for var, info in symbols.items():
            print(f"{var}: {info}")
    except ValueError as e:
        print(f"Error: {e}")
        
    input("Presiona Enter para salir...")  # Esto pausa la ejecución
