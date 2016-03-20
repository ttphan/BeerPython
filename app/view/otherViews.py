from PySide.QtGui import *
from PySide.QtCore import *
from model.model import *
from view.gen.loginView import Ui_LoginDialog
from view.gen.menuView import Ui_MenuDialog
from view.gen.newPasswordView import Ui_NewPasswordDialog
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
        self.buttonBox.accepted.connect(self.verify)
        self.buttonBox.rejected.connect(self.reject)

    def verify(self):
        hashed = self.session.query(Password).one().password
        plaintext = self.tPass.text().encode('utf-8')

        if bcrypt.hashpw(plaintext, hashed) == hashed:
            self.accept()
        else:
            MessageBox('Error!', 
                'Wachtwoord is onjuist!', 
                QMessageBox.Critical
            )

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
        self.btPassword.clicked.connect(self.showNewPasswordDialog) 


    def confirmNewList(self):
        msgBox = QMessageBox()
        msgBox.setWindowTitle('Nieuwe lijst?')
        msgBox.setText('Je gaat nu de huidige lijst sluiten en een nieuwe aanmaken!')
        msgBox.setInformativeText('Er wordt een Excel-bestand gegenereerd, \
            de turfjes worden weer op 0 gezet.')
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
        msgBox.setDefaultButton(QMessageBox.No)
        
        for button in msgBox.buttons():
            button.setMinimumWidth(100)
            button.setMinimumHeight(50)

        ret = msgBox.exec_()

        if ret == QMessageBox.Yes:

            listId = self.session.query(List).order_by(desc(List.id)).first().id
            members = (self.session.query(
                Member.name, func.count(Member.id))
                .join(Tally)
                .join(List)
                .filter(List.id == listId)
                .group_by(Member)
            )

            filename = writeToExcel(members, listId)

            self.session.add(List())
            self.session.commit()
            MessageBox('Een nieuw lijst is aangemaakt!', 
                'Er is een Excel-bestand aangemaakt: data/sheets/' + filename
            )
    

    def showNewPasswordDialog(self):
        NewPasswordView(self.session).exec_()


class NewPasswordView(QDialog, Ui_NewPasswordDialog):
    "New password dialog"
    def __init__(self, session):
        super(NewPasswordView, self).__init__()
        self.setupUi(self)
        self.session = session
        self.setupConnections()

    def setupConnections(self):
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.accepted.connect(self.verify)

    def verify(self):
        plaintext = self.tPass.text().encode('utf-8')

        if plaintext == self.tPass2.text().encode('utf-8'):
            hashed = bcrypt.hashpw(plaintext, bcrypt.gensalt())
            self.session.query(Password).one().password = hashed

            MessageBox('Wachtwoord gewijzigd!', 
                'Nieuw wachtwoord is ingevoerd.', 
                QMessageBox.Information
            )

            self.accept()
        else:
            MessageBox('Error!', 
                'Wacthwoorden komen niet overeen!', 
                QMessageBox.Critical
            )
