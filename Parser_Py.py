# global variables
indent = 0
stringO = ""


class Node:
    def __init__(self, t, c, s):
        self.token_value = t
        self.code_value = c
        self.shape = s
        self.children = []
        self.sibling = None
        self.index = None

    def set_children(self, y):
        try:
            assert isinstance(y, list)
            for i in y:
                self.children.append(i)
        except:
            self.children.append(y)

    def set_sibling(self, y):
        self.sibling = y


class Parser(object):
    nodes_table = {}
    iterator = 0
    edges_table = []

    def __init__(self, tiny_tokens, tokens_list, values_list):
        self.tiny_tokens = tiny_tokens
        self.token = str
        self.tokens_list = tokens_list
        self.values_list = values_list
        self.iterator = 0
        self.token = self.tokens_list[self.iterator]
        self.parse_tree = None
        self.nodes_table = None
        self.edges_table = None
        self.same_rank_nodes = []

    def stmt_sequence(self):
        t = self.statement()
        p = t
        while self.token == 'semicolon':
            self.match('semicolon')
            q = self.statement()
            if q is None:
                break
            else:
                if t is None:
                    t = p = q
                else:
                    p.set_sibling(q)
                    p = q
        return t

    def statement(self):
        if self.token == 'if':
            t = self.if_stmt()
            return t
        elif self.token == 'repeat':
            t = self.repeat_stmt()
            return t
        elif self.token == 'identifier':
            t = self.assign_stmt()
            return t
        elif self.token == 'read':
            t = self.read_stmt()
            return t
        elif self.token == 'write':
            t = self.write_stmt()
            return t
        else:
            raise ValueError('SyntaxError', self.values_list[self.iterator - 1])

    def if_stmt(self):
        t = Node('if', '', 's')
        if self.token == 'if':
            self.match('if')
            t.set_children(self.exp())
            self.match('then')
            t.set_children(self.stmt_sequence())
            if self.token == 'else':
                self.match('else')
                t.set_children(self.stmt_sequence())
            self.match('end')
        return t

    def repeat_stmt(self):
        t = Node('repeat', '', 's')
        if self.token == 'repeat':
            self.match('repeat')
            t.set_children(self.stmt_sequence())
            self.match('until')
            t.set_children(self.exp())
        return t

    def assign_stmt(self):
        t = Node('assign', '(' + self.values_list[self.iterator] + ')', 's')
        self.match('identifier')
        self.match('assign')
        t.set_children(self.exp())
        return t

    def read_stmt(self):
        t = Node('read', '(' + self.values_list[self.iterator + 1] + ')', 's')
        self.match('read')
        self.match('identifier')
        return t

    def write_stmt(self):
        t = Node('write', '', 's')
        self.match('write')
        t.set_children(self.exp())
        return t

    def exp(self):
        t = self.simpleexp()
        if self.token == '>' or self.token == 'lessthan' or self.token == 'equal':
            p = Node('op', '(' + self.values_list[self.iterator] + ')', 'o')
            p.set_children(t)
            t = p
            self.compareop()
            t.set_children(self.exp())
        return t

    def simpleexp(self):
        t = self.term()
        while self.token == 'plus' or self.token == 'minus':
            p = Node('op', '(' + self.values_list[self.iterator] + ')', 'o')
            p.set_children(t)
            t = p
            self.addop()
            t.set_children(self.term())
        return t

    def term(self):
        t = self.factor()
        while self.token == 'mult' or self.token == 'div':
            p = Node('op', '(' + self.values_list[self.iterator] + ')', 'o')
            p.set_children(t)
            t = p
            self.mulop()
            p.set_children(self.factor())
        return t

    def factor(self):
        if self.token == 'openbracket':
            self.match('openbracket')
            t = self.exp()
            self.match('closedbracket')
        elif self.token == 'number':
            t = Node('const', '(' + self.values_list[self.iterator] + ')', 'o')
            self.match('number')
        elif self.token == 'identifier':
            t = Node('id', '(' + self.values_list[self.iterator] + ')', 'o')
            self.match('identifier')
        else:
            raise ValueError('SyntaxError', self.values_list[self.iterator - 1])
        return t

    def addop(self):
        if self.token == 'plus':
            self.match('plus')
        elif self.token == 'minus':
            self.match('minus')

    def mulop(self):
        if self.token == 'mult':
            self.match('mult')
        elif self.token == 'div':
            self.match('div')

    def compareop(self):
        if self.token == '>':
            self.match('>')
        elif self.token == 'lessthan':
            self.match('lessthan')
        elif self.token == 'equal':
            self.match('equal')

    def match(self, token):
        if self.token == token:
            if self.iterator == len(self.tokens_list) - 1:
                return False
            self.iterator += 1
            self.token = self.tokens_list[self.iterator]
            return True
        else:
            raise ValueError('Token Mismatch', self.values_list[self.iterator - 1])

    def create_nodes_table(self, args=None):
        if args is None:
            self.parse_tree.iterator = Parser.iterator
            Parser.nodes_table.update(
                {Parser.iterator: [self.parse_tree.token_value, self.parse_tree.code_value, self.parse_tree.shape]})
            Parser.iterator = Parser.iterator + 1
            if len(self.parse_tree.children) != 0:
                for i in self.parse_tree.children:
                    self.create_nodes_table(i)
            if self.parse_tree.sibling is not None:
                self.create_nodes_table(self.parse_tree.sibling)
        else:
            args.iterator = Parser.iterator
            Parser.nodes_table.update(
                {Parser.iterator: [args.token_value, args.code_value, args.shape]})
            Parser.iterator = Parser.iterator + 1
            if len(args.children) != 0:
                for i in args.children:
                    self.create_nodes_table(i)
            if args.sibling is not None:
                self.create_nodes_table(args.sibling)

    def create_edges_table(self, args=None):
        if args is None:
            if len(self.parse_tree.children) != 0:
                for i in self.parse_tree.children:
                    Parser.edges_table.append((self.parse_tree.iterator, i.iterator))
                for j in self.parse_tree.children:
                    self.create_edges_table(j)
            if self.parse_tree.sibling is not None:
                Parser.edges_table.append(
                    (self.parse_tree.iterator, self.parse_tree.sibling.iterator))
                self.same_rank_nodes.append(
                    [self.parse_tree.iterator, self.parse_tree.sibling.iterator])
                self.create_edges_table(self.parse_tree.sibling)
        else:
            if len(args.children) != 0:
                for i in args.children:
                    Parser.edges_table.append((args.iterator, i.iterator))
                for j in args.children:
                    self.create_edges_table(j)
            if args.sibling is not None:
                Parser.edges_table.append((args.iterator, args.sibling.iterator))
                self.same_rank_nodes.append([args.iterator, args.sibling.iterator])
                self.create_edges_table(args.sibling)

    def run(self):
        self.parse_tree = self.stmt_sequence()
        self.create_nodes_table()
        self.create_edges_table()
        self.edges_table = Parser.edges_table
        self.nodes_table = Parser.nodes_table
        if self.iterator == len(self.tokens_list) - 1:
            print('success')
        elif self.iterator < len(self.tokens_list):
            raise ValueError('SyntaxError', self.values_list[self.iterator - 1])

    def print_tree(self, node=False):
        global indent
        global stringO
        if not node:
            node = self.parse_tree
        if node:
            stringO += "    " * indent + "Node [ " + node.token_value + " " + node.code_value + " " + node.shape + " ]\n"
            if node.children:
                indent += 1
                stringO += "    " * indent + "Children of [ " + node.token_value + " " + node.code_value + " " + node.shape + " ] {\n"
                for child in node.children:
                    self.print_tree(child)
                indent -= 1
                stringO += "    " * indent + "}end children of [ " + node.token_value + " " + node.code_value + " " + node.shape + " ]\n"
            if node.sibling:
                stringO += "    " * indent + "sibling of [ " + node.token_value + " " + node.code_value + " " + node.shape + " ] {\n"
                self.print_tree(node.sibling)
                stringO += "    " * indent + "}end sibling of [ " + node.token_value + " " + node.code_value + " " + node.shape + " ]\n"
        return stringO

    def clear_tables(self):
        global indent
        global stringO
        self.nodes_table.clear()
        self.edges_table.clear()
        indent = 0
        stringO = ""
