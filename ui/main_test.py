# * author : Philippe Vo
# * date : Aug-22-2020 00:52:03

# * Imports
# 3rd Party Imports
import sys
from PySide2 import QtWidgets
from PySide2 import QtGui
# User Imports
from client_window import ClientWindow

# * Code
if __name__ == '__main__':

    # Init App
    app = QtWidgets.QApplication(sys.argv)

    # load font
    # fontDb = QtGui.QFontDatabase()
    # fontPixel = fontDb.addApplicationFont("resources/fonts/dogicapixel.ttf")

    # load stylesheet
    # with open("resources/style.qss", "r") as f:
    #     app.setStyleSheet(f.read())

    # Open MainWindow
    clientWindow = ClientWindow()
    clientWindow.show()

    # Exit
    sys.exit(app.exec_())
