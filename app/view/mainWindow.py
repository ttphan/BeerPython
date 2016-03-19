from PySide import QtCore, QtGui
from PySide.QtCore import *
from PySide.QtGui import *
from view.gen.mainView import Ui_MainWindow 

class MainWindow(QMainWindow, Ui_MainWindow):

    MAX_ROOMS = 21
    rooms = {}

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        
        self.initializeValues()
        self.setupConnections()

    def setupConnections(self):
        self.btMember1.clicked.connect(lambda: self.addTally(1))
        self.btMember2.clicked.connect(lambda: self.addTally(2))
        self.btMember3.clicked.connect(lambda: self.addTally(3))
        self.btMember4.clicked.connect(lambda: self.addTally(4))
        self.btMember5.clicked.connect(lambda: self.addTally(5))
        self.btMember6.clicked.connect(lambda: self.addTally(6))
        self.btMember7.clicked.connect(lambda: self.addTally(7))
        self.btMember8.clicked.connect(lambda: self.addTally(8))
        self.btMember9.clicked.connect(lambda: self.addTally(9))
        self.btMember10.clicked.connect(lambda: self.addTally(10))
        self.btMember11.clicked.connect(lambda: self.addTally(11))
        self.btMember12.clicked.connect(lambda: self.addTally(12))
        self.btMember13.clicked.connect(lambda: self.addTally(13))
        self.btMember14.clicked.connect(lambda: self.addTally(14))
        self.btMember15.clicked.connect(lambda: self.addTally(15))
        self.btMember16.clicked.connect(lambda: self.addTally(16))
        self.btMember17.clicked.connect(lambda: self.addTally(17))
        self.btMember18.clicked.connect(lambda: self.addTally(18))
        self.btMember19.clicked.connect(lambda: self.addTally(19))
        self.btMember20.clicked.connect(lambda: self.addTally(20))
        self.btMember21.clicked.connect(lambda: self.addTally(21))


    def addTally(self, id):
        oldValue = int(self.rooms[id][2].text())
        self.rooms[id][2].setText(str(oldValue + 1))


    def initializeValues(self):
        self.rooms[1] = [self.btMember1, self.lTotalTallies1, self.lCurrentTallies1]
        self.rooms[2] = [self.btMember2, self.lTotalTallies2, self.lCurrentTallies2]
        self.rooms[3] = [self.btMember3, self.lTotalTallies3, self.lCurrentTallies3]
        self.rooms[4] = [self.btMember4, self.lTotalTallies4, self.lCurrentTallies4]
        self.rooms[5] = [self.btMember5, self.lTotalTallies5, self.lCurrentTallies5]
        self.rooms[6] = [self.btMember6, self.lTotalTallies6, self.lCurrentTallies6]
        self.rooms[7] = [self.btMember7, self.lTotalTallies7, self.lCurrentTallies7]
        self.rooms[8] = [self.btMember8, self.lTotalTallies8, self.lCurrentTallies8]
        self.rooms[9] = [self.btMember9, self.lTotalTallies9, self.lCurrentTallies9]
        self.rooms[10] = [self.btMember10, self.lTotalTallies10, self.lCurrentTallies10]
        self.rooms[11] = [self.btMember11, self.lTotalTallies11, self.lCurrentTallies11]
        self.rooms[12] = [self.btMember12, self.lTotalTallies12, self.lCurrentTallies12]
        self.rooms[13] = [self.btMember13, self.lTotalTallies13, self.lCurrentTallies13]
        self.rooms[14] = [self.btMember14, self.lTotalTallies14, self.lCurrentTallies14]
        self.rooms[15] = [self.btMember15, self.lTotalTallies15, self.lCurrentTallies15]
        self.rooms[16] = [self.btMember16, self.lTotalTallies16, self.lCurrentTallies16]
        self.rooms[17] = [self.btMember17, self.lTotalTallies17, self.lCurrentTallies17]
        self.rooms[18] = [self.btMember18, self.lTotalTallies18, self.lCurrentTallies18]
        self.rooms[19] = [self.btMember19, self.lTotalTallies19, self.lCurrentTallies19]
        self.rooms[20] = [self.btMember20, self.lTotalTallies20, self.lCurrentTallies20]
        self.rooms[21] = [self.btMember21, self.lTotalTallies21, self.lCurrentTallies21]