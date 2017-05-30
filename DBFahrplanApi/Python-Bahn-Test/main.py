import sys
from PyQt5 import QtWidgets as qw
from MainWidget import FormWidget

if __name__=="__main__":
        app=qw.QApplication(sys.argv)
        formwidget=FormWidget()
        mainWindow=qw.QMainWindow()
        mainWindow.setCentralWidget(formwidget)
        mainWindow.setWindowTitle("Fahrplanzeige")
        mainWindow.show()
        sys.exit(app.exec_())

