from PySide import QtCore, QtGui
from PySide.QtCore import *
from PySide.QtGui import *
from view.gen.mainView import Ui_MainWindow 
from view.otherViews import LoginView, MenuView
from model.model import *
from db import sessionScope
import view.gen.resources_rc
from datetime import datetime

MAX_ROOMS = 21

class MainWindow(QMainWindow, Ui_MainWindow):

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

        self.btConfirmTallies.clicked.connect(self.confirmTallies)
        self.btCancelTallies.clicked.connect(self.refresh)
        self.btMenu.clicked.connect(self.showLoginDialog)


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

        self.fLeft.setStyleSheet('border: 0px')

        self.refresh()
        
    def refresh(self):
        with sessionScope() as session:
            tallies = []

            for i in range(1, MAX_ROOMS + 1):
                roomProps = self.rooms[i]
                room = session.query(Room).get(i)
                member = room.member

                roomProps[0].setStyleSheet('border: 0px')
                roomProps[1].setStyleSheet('border: 0px;')

                roomProps[2].display('-')
                roomProps[2].setStyleSheet('border: 0px;')
                
                if member:
                    totalTallies = member.getTotalTallies(session)
                    tallies.append([i, totalTallies])

                    roomProps[0].setText(member.name)
                    font = roomProps[0].font()
                    font.setPointSize(12)
                    roomProps[0].setFont(font)
                    roomProps[0].setStyleSheet('border: 1px solid #4A4949;')
                    roomProps[0].setEnabled(True)

                    roomProps[1].display(totalTallies)
                    roomProps[1].setEnabled(True)


                    roomProps[2].setEnabled(True)
                else:
                    roomProps[0].setText('')
                    roomProps[0].setEnabled(False)

                    roomProps[1].display('-')
                    roomProps[1].setEnabled(False)

                    roomProps[2].setEnabled(False)



            # Rank the top 3 members
            rankColour = ['gold', 'silver', '#693316']
            for rank in range(3):
                # Get all maximums
                top = maxes(tallies)

                # Don't rank if there are no tallies
                if top[0] > 0:
                    for room in top[1]:
                        # Give every ranked member an appropriate border color
                        self.rooms[room[0]][0].setStyleSheet('border: 3px outset ' 
                            + rankColour[rank] + ';')

                    # Filter out the top ranked to calculate the next maximums
                    tallies = [t for t in tallies if not any(t == x for x in top[1])]
                else:
                    break;
        

    def addTally(self, id):
        oldValue = self.rooms[id][2].value()
        self.rooms[id][2].display(oldValue + 1)
        self.rooms[id][2].setStyleSheet("color: green; border: 0px")


    def confirmTallies(self):
        with sessionScope() as session:
            for key, value in self.rooms.items():
                member = session.query(Room).get(key).member
                totalTallies = value[1]
                currentTallies = int(value[2].value())

                if currentTallies > 0:
                    time = datetime.now().strftime('%H:%M:%S')
                    member.addTally(session, currentTallies)
                    self.tLog.append('{} - {} heeft {} biertje(s) geturfd.'
                        .format(time, member.name, currentTallies))
                    if currentTallies == 7:
                        self.tLog.append("Waarvoor hulde!")
                    
                    
        self.refresh()


    def showLoginDialog(self):
        with sessionScope() as session:
            loginDialog = LoginView(session)
            ret = loginDialog.exec_()

            if ret:
                self.showMenuDialog(session)

    def showMenuDialog(self, session):
        menuDialog = MenuView(session)
        menuDialog.showFullScreen()
        menuDialog.exec_()

        self.refresh()



"""
Helper functions
"""
def maxes(array):
    "Get all maximums instead of just one"
    key = lambda x: x[1]

    m, max_list = key(array[0]), []
    for s in array:
        k = key(s)
        if k > m:
            m, max_list = k, [s]
        elif k == m:
            max_list.append(s)
    return m, max_list