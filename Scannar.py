import io


def special_char_type(sp_ch):
    if sp_ch == ';':
        return "SEMICOLON"
    if sp_ch == '(':
        return "OPENBRACKET"
    if sp_ch == ')':
        return "CLOSEDBRACKET"
    if sp_ch == '+':
        return "PLUS"
    if sp_ch == '-':
        return "MINUS"
    if sp_ch == '*':
        return "MULT"
    if sp_ch == '/':
        return "DIV"
    if sp_ch == '=':
        return "EQUAL"
    if sp_ch == '<':
        return "LESSTHAN"
    # if sp_ch == '>':
    # 	return "GREATERTHAN"


def reserved_word_type(r_word):
    if r_word == 'if':
        return "IF"
    if r_word == 'then':
        return "THEN"
    if r_word == 'else':
        return "ELSE"
    if r_word == 'end':
        return "END"
    if r_word == 'repeat':
        return "REPEAT"
    if r_word == 'until':
        return "UNTIL"
    if r_word == 'read':
        return "READ"
    if r_word == 'write':
        return "WRITE"


class Scanner(object):
    def __init__(self, tiny_code="") -> None:
        self.token_list = None
        self.tiny_code = tiny_code
        self.code_list = None

    def setTinyCode(self, tiny_code):
        self.tiny_code = tiny_code

    def scan(self):
        tokens_list = []
        tiny_str = None
        special_chars = ['(', ')', '+', '-', '*', '/', '=', ';', '<', '>']
        reserved_words = ["if", "then", "else", "end", "repeat", "until", "read", "write"]
        for tiny_line in io.StringIO(self.tiny_code):
            tiny_str = ""
            state = "start"
            i = 0
            while i < len(tiny_line):
                # check for special chars and append them
                if tiny_line[i] in special_chars and state != "assign" and state != "comment":
                    if tiny_str != '':
                        tokens_list.append(tiny_str)
                        tiny_str = ''
                    tokens_list.append(tiny_line[i])
                    state = 'start'
                # at the start of each line we check to go for a state
                elif state == "start":
                    if tiny_line[i] == ' ':
                        state = "start"
                    elif tiny_line[i].isalpha():
                        tiny_str += tiny_line[i]
                        state = "id"
                    elif tiny_line[i].isdigit():
                        tiny_str += tiny_line[i]
                        state = "number"
                    elif tiny_line[i] == ':':
                        tiny_str += tiny_line[i]
                        state = "assign"
                    elif tiny_line[i] == '{':
                        # tiny_str += tiny_line[i]
                        state = "comment"
                    else:
                        state = 'done'
                # identifier state
                elif state == 'id':
                    # identifier can only start with alpha but after that it can contain numbers
                    if tiny_line[i].isalnum():  # {
                        tiny_str += tiny_line[i]
                        state = "id"
                    else:
                        state = "done"
                        i -= 1
                # number state
                elif state == "number":
                    if tiny_line[i].isdigit():
                        tiny_str += tiny_line[i]
                        state = "number"
                    else:
                        state = "done"
                        i -= 1
                # assign state
                elif state == "assign":
                    if tiny_line[i] == "=":
                        tiny_str += tiny_line[i]
                        state = "done"
                    else:
                        state = "done"
                # comment state
                elif state == "comment":
                    if tiny_line[i] == "}":
                        # tiny_str += tiny_line[i]
                        state = "start"
                    else:
                        pass
                # tiny_str += tiny_line[i]
                # done state
                elif state == "done":
                    tokens_list.append(tiny_str)
                    tiny_str = ""
                    state = "start"
                    i -= 1
                i += 1
            if tiny_str != "":
                tokens_list.append(tiny_str)
                tiny_str = ""
        output_tokens = []
        for token in tokens_list:
            if token in reserved_words:
                TokenType = reserved_word_type(token)
                output_tokens.append((token, TokenType))
            elif token in special_chars:
                TokenType = special_char_type(token)
                output_tokens.append((token, TokenType))
            elif token == ":=":
                output_tokens.append((token, "ASSIGN"))
            elif token.isdigit():
                output_tokens.append((token, "NUMBER"))
            elif token.isalnum():
                output_tokens.append((token, "IDENTIFIER"))
            else:
                # error state or comment
                pass
            self.code_list = tokens_list
            self.token_list = output_tokens

    # def createOutputFile(self, filename="output.txt"):
    #     self.scan()
    #     with open(filename, 'w+') as out:
    #         for t in self.token_list:
    #             out.write(str(t[0] + " , " + t[1]))
    #             out.write("\n")
