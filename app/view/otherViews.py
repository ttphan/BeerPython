from PySide.QtGui import *
from PySide.QtCore import *
from model.model import *
from view.gen.loginView import Ui_LoginDialog
from view.gen.menuView import Ui_MenuDialog
import bcrypt
from excel import writeToExcel
import pdb

def MessageBox(title = None, text = None, icon = None):
    "Generic message box"
    msgBox = QMessageBox()

    if title:
        msgBox.setWindowTitle(title)
    
    if text:
        msgBox.setText(text)
    
    if icon:
        msgBox.setIcon(icon)

    msgBox.setStandardButtons(QMessageBox.Ok) 
    button = msgBox.buttons()[0]
    button.setMinimumWidth(100)
    button.setMinimumHeight(50) 
    ret = msgBox.exec_()

class LoginView(QDialog, Ui_LoginDialog):
    "Login dialog popup"
    def __init__(self, session):
        super(LoginView, self).__init__()
        self.setupUi(self)
        self.setupConnections()
        self.session = session

    def setupConnections(self):
        self.buttonBox.accepted.connect(self.checkPassword)
        self.buttonBox.rejected.connect(self.reject)

    def checkPassword(self):
        hashed = self.session.query(Password).one().password
        plaintext = self.tPass.text().encode('utf-8')

        if bcrypt.hashpw(plaintext, hashed) == hashed:
            self.accept()
        else:
            MessageBox('Error!', 'Incorrect password!', QMessageBox.Critical)

class MenuView(QDialog, Ui_MenuDialog):
    "Main menu dialog"
    def __init__(self, session):
        super(MenuView, self).__init__()
        self.setupUi(self)
        self.session = session
        self.setupConnections()

    def setupConnections(self):
        self.btBack.clicked.connect(self.reject)
        self.btNewList.clicked.connect(self.confirmNewList)


    def confirmNewList(self):
        msgBox = QMessageBox()
        msgBox.setWindowTitle('Nieuwe lijst?')
        msgBox.setText('Je gaat nu de huidige lijst sluiten en een nieuwe aanmaken!')
        msgBox.setInformativeText('Er wordt een Excel-bestand gegenereerd, de turfjes worden weer op 0 gezet.')
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
        msgBox.setDefaultButton(QMessageBox.No)
        
        for button in msgBox.buttons():
            button.setMinimumWidth(100)
            button.setMinimumHeight(50)

        ret = msgBox.exec_()

        if ret == QMessageBox.Yes:

            members = self.session.query(Member).filter(Member.room != None)
            tallies = {}
            for member in members:
                tallies[member.name] = member.getTotalTallies(self.session)

            filename = writeToExcel(tallies, 
                self.session.query(List).order_by(desc(List.id)).first().id)

            MessageBox('Een nieuw lijst is aangemaakt!', 
                'Er is een Excel-bestand aangemaakt: data/sheets/' + filename)
