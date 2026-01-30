import re

class Lexer():
    def __init__(self):
        self.tokens = []

    def tokenize(self, data):
        data = data.lstrip()  # Remove espaços e \n no início
        if not data:
            return self.tokens

        if data.startswith("PUSH"):
            self.tokens.append("PUSH")
            return self.tokenize(data[4:])
        elif data.startswith("POP"):
            self.tokens.append("POP")
            return self.tokenize(data[3:])
        elif data.startswith("OP"):
            self.tokens.append("OP")
            return self.tokenize(data[2:])
        elif data.startswith("SWAP"):
            self.tokens.append("SWAP")
            return self.tokenize(data[4:])
        elif m := re.match(r'\d+', data):
            value = m.group(0)
            self.tokens.append(("NUM", int(value)))
            return self.tokenize(data[len(value):])
        elif data[0] in "+-*/":
            self.tokens.append(("OPERATOR", data[0]))
            return self.tokenize(data[1:])
        else:
            # Ignora qualquer outro caracter não esperado
            return self.tokenize(data[1:])

class Parser():
    def __init__(self, tokens):
        self.input = tokens
        self.stack = []

    def parse(self):
        self.Parse_S()
        
    def Parse_S(self):
        "S -> Instruções"
        self.parse_instruções()
        
    def parse_instruções(self):
        "instruções -> instrução instruções "
        self.parse_instrução()
        self.parse_instruções_()
        
    def parse_instruções_(self):
        "instruções -> instrução instruções | ε"
        if self.input:
            self.parse_instrução()
            self.parse_instruções_()
        else:
            return
    
    def parse_instrução(self):
        "instrução -> PUSH NUM | POP | OP | SWAP"
        match self.input[0]:
            case "PUSH":
                self.input.pop(0)
                match self.input[0]:
                    case ("NUM", num):
                        self.input.pop(0)
                        self.stack.append(num)
                    case _:
                        raise ValueError("Esperado um número após PUSH")  
            case "POP":
                self.input.pop(0)
                value= self.stack.pop() 
                print(f"Valor removido da pilha: {value}")
            case "SWAP":
                value1=self.input.pop(0)
                value2=self.input.pop(0)
                self.stack.append(value1)
                self.stack.append(value2)
            case "OP":
                self.input.pop(0)
                match self.input[0]:
                    case "+":
                        self.input.pop(0)
                        value1 = self.stack.pop()
                        value2 = self.stack.pop()
                        self.stack.append(value1 + value2)
                    case "-":
                        self.input.pop(0)
                        value1 = self.stack.pop()
                        value2 = self.stack.pop()
                        self.stack.append(value1 - value2)
                    case "*":
                        self.input.pop(0)  
                        value1 = self.stack.pop()
                        value2 = self.stack.pop()
                        self.stack.append(value1 * value2)
                    case "/":
                        self.input.pop(0)
                        value1 = self.stack.pop()
                        value2 = self.stack.pop()
                        if value2 == 0:
                            raise ValueError("Divisão por zero")
                        self.stack.append(value2 // value1)
            case _:
                raise ValueError("Instrução inválida")
        



# Teste
lexer = Lexer()
lexer.tokenize("""
    PUSH 3
    PUSH 5
    OP +
    POP
""")

print(lexer.tokens)
