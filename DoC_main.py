import io
import sys
import Parser_Py
from Scannar import Scanner
from DoC_project import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
import networkx as nx
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use("TkAgg")


class MainApp(QMainWindow, Ui_MainWindow):
    def __init__(self) -> None:
        QMainWindow.__init__(self)
        self.G = None
        self.graph = None
        self.setupUi(self)
        self.parser_obj = None
        self.apply_scanner.clicked.connect(self.scan)
        self.apply_parser.clicked.connect(self.parse)
        self.copy.clicked.connect(self.copied)
        self.paste.clicked.connect(self.pasted)
        self.toolButton.clicked.connect(self.browse)
        self.parse_btn.clicked.connect(self.parse_btn_fn)
        self.textBrowser.clear()
        self.textBrowser_2.clear()
        self.statusBar.showMessage("Ready...")

    def copied(self):
        if self.textBrowser.toPlainText() == '':
            self.statusBar.showMessage("Nothing to copy!")
        else:
            self.textBrowser.selectAll()
            self.textBrowser.copy()
            self.statusBar.showMessage("copied!")

    def pasted(self):
        self.textEdit_2.clear()
        self.textEdit_2.paste()
        self.statusBar.showMessage("pasted!")

    def browse(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open file", "", "Text files (*.txt);;All files (*)")
        if file_name:
            try:
                with open(file_name, 'r') as inp:
                    input_text = inp.read()
                    self.textEdit.setText(input_text)
                    self.scan()
            except Exception as e:
                self.statusBar.showMessage("Error" + " " + str(e))

    def parse_btn_fn(self):
        if self.textBrowser.toPlainText() == '':
            self.statusBar.showMessage("Nothing to parse!")
        else:
            self.textBrowser.selectAll()
            self.textBrowser.copy()
            self.textEdit_2.clear()
            self.textEdit_2.paste()
            self.tabWidget.setCurrentIndex(1)
            self.parse()

    def scan(self):
        self.textBrowser.clear()
        found_text = False
        input_text = self.textEdit.toPlainText()
        path_input = self.lineEdit.text()
        if path_input == '':
            if input_text == '':
                self.statusBar.showMessage("No input!!")
            else:
                found_text = True
        else:
            try:
                with open(path_input, 'r') as inp:
                    input_text = inp.read()
                    found_text = True
                    self.textEdit.setText(input_text)
            except Exception as e:
                self.statusBar.showMessage("Error" + " " + str(e))
        if found_text:
            scr = Scanner(input_text)
            scr.scan()
            output_list = scr.token_list
            for output_tup in output_list:
                self.textBrowser.append(output_tup[0] + " , " + output_tup[1])
            self.statusBar.showMessage("Done...")
        else:
            self.textBrowser.clear()

    def parse(self):
        self.textBrowser_2.clear()
        token_text = self.textEdit_2.toPlainText()
        types = []
        values = []
        i = 0
        if token_text == '':
            self.statusBar.showMessage("Empty input!")
            return
        for line in io.StringIO(token_text):
            try:
                i += 1
                line_list = line.split(',')
                values.append(line_list[0].strip().lower())
                types.append(line_list[1].strip().lower())
            except Exception as e:
                self.statusBar.showMessage(f"Error at line {str(i)}: ({line}) ({str(e)})")
                return
        self.parser_obj = Parser_Py.Parser(token_text, types, values)
        try:
            self.parser_obj.run()
            st = self.parser_obj.print_tree()
            self.textBrowser_2.append(st)
            nodes_list = self.parser_obj.nodes_table
            edges_list = self.parser_obj.edges_table
            self.G = nx.DiGraph(ordering='out')
            for node_number, node in nodes_list.items():
                self.G.add_node(
                    node_number, value=node[0] + '\n' + node[1], shape=node[2])
            self.G.add_edges_from(edges_list)
            self.parser_obj.clear_tables()
            self.draw(self.parser_obj.same_rank_nodes)
            self.statusBar.showMessage("Done...")
        except Exception as e:
            self.statusBar.showMessage("Error" + " " + str(e))
            return

    def draw(self, same_rank_nodes):
        graph = self.G
        pos = pygraphviz_layout_with_rank(
            graph, prog='dot', sameRank=same_rank_nodes)
        labels = dict((n, d['value']) for n, d in graph.nodes(data=True))
        # #e0e1e3 #19232d #455364
        plt.rcParams['axes.facecolor'] = '#19232d'
        f = plt.figure("Syntax tree", figsize=(10, 7), layout='constrained')
        for shape in ['s', 'o']:
            nx.draw_networkx_nodes(graph, pos, node_color='#455364', node_size=2200, node_shape=shape,
                                   nodelist=[sNode[0] for sNode in
                                             filter(lambda x: x[1]["shape"] == shape, graph.nodes(data=True))])
        nx.draw_networkx_edges(graph, pos, arrows=True, arrowsize=38, edge_color='#e0e1e3')
        nx.draw_networkx_labels(graph, pos, labels=labels, font_size=14, font_color='#e0e1e3',
                                font_family='Arial Rounded MT Bold')
        f.canvas.manager.window.wm_geometry("+%d+%d" % (600, 10))
        plt.show()


def pygraphviz_layout_with_rank(G, prog="dot", root=None, sameRank=[], args=""):
    try:
        import pygraphviz
    except ImportError:
        raise ImportError('requires pygraphviz ',
                          'http://networkx.lanl.gov/pygraphviz ',
                          '(not available for Python3)')
    if root is not None:
        args += "-Groot=%s" % root
    A = nx.nx_agraph.to_agraph(G)
    for sameNodeHeight in sameRank:
        if type(sameNodeHeight) == str:
            print("node \"%s\" has no peers in its rank group" %
                  sameNodeHeight)
        A.add_subgraph(sameNodeHeight, rank="same")
    A.layout(prog=prog, args=args)
    node_pos = {}
    for n in G:
        node = pygraphviz.Node(A, n)
        try:
            xx, yy = node.attr["pos"].split(',')
            node_pos[n] = (float(xx), float(yy))
        except:
            print("no position for node", n)
            node_pos[n] = (0.0, 0.0)
    return node_pos


app = QApplication(sys.argv)
window = MainApp()
window.show()
app.exec_()
