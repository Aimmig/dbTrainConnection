import sys
from PyQt5 import QtWidgets as qw
from MainWidget import FormWidget

if __name__=="__main__":
        app=qw.QApplication(sys.argv)
        formwidget=FormWidget()
        formwidget.show()
        sys.exit(app.exec_())

