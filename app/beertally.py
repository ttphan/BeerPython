import signal
import sys
from PySide import QtGui, QtCore
import db
import os

from view.mainWindow import MainWindow
import inspect, os

class BeerTally(QtGui.QApplication):
    def __init__(self, sys_argv):
        super(BeerTally, self).__init__(sys_argv)

        if getattr(sys, 'frozen', False):
            # frozen
            basepath = os.path.dirname(sys.executable)
        else:
            # unfrozen
            basepath = os.path.dirname(os.path.realpath(__file__))

        self.mainWindow = MainWindow()
        
        if os.name == 'nt':
            # This is needed to display the app icon on the taskbar on Windows 7
            import ctypes
            myappid = 'JvB.7' # arbitrary string
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

if __name__ == '__main__':
    # Enable ctrl-c closeable
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    db.initialize()

    app = BeerTally(sys.argv)   
    app.mainWindow.show();

    app.mainWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)
    app.mainWindow.showFullScreen()

    sys.exit(app.exec_())