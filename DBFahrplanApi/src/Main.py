from PyQt5 import QtWidgets
from GUI import GUI
import sys

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    application = GUI()
    application.show()
    sys.exit(app.exec_())
