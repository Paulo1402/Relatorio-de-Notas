import sys

from PyQt6 import QtWidgets, QtGui, QtCore, QtPrintSupport, QtWebEngineWidgets, QtWebEngineCore, QtWebEngineQuick


class App(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # Create some widgets
        self.setGeometry(500, 150, 800, 500)
        self.button = QtWidgets.QPushButton(
            'Print QTextEdit widget (the one below)', self)
        self.button.setGeometry(20, 20, 260, 30)
        #self.editor = QtWidgets.QTextEdit('Wow such text why not change me?', self)
        #self.editor.setGeometry(20, 60, 260, 200)
        self.button.clicked.connect(self.print_html)
        self.view = QtWebEngineWidgets.QWebEngineView(self)
        self.view.setGeometry(20, 60, 450, 400)

    def handle_preview(self):
        dialog = QtPrintSupport.QPrintPreviewDialog()
        dialog.paintRequested.connect(self.print_html)
        dialog.exec()

    def print_html(self, printer=None):
        # self.view = QtWebEngineWidgets.QWebEngineView()

        with open('templates/report.html', 'r', encoding='utf-8') as f:
            self.view.setHtml(f.read())

        self.view.setZoomFactor(0.8)

        # self.view.setHtml('<h1>Hello World!</h1>')
        # self.view.show()

        # self.view.printToPdf('test.pdf')
        # view.print(printer)

    def print_widget(self, printer):
        print('print_widget start')
        # Create painter
        painter = QtGui.QPainter()
        # Start painter
        painter.begin(printer)
        # Grab a widget you want to print
        screen = self.editor.grab()
        # Draw grabbed pixmap
        painter.drawPixmap(10, 10, screen)
        # End painting
        painter.end()
        print('print_widget end')


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    gui = App()
    gui.show()
    app.exec()
