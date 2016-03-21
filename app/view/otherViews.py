from PySide.QtGui import *
from PySide.QtCore import *
from model.model import *
from view.gen.loginView import Ui_LoginDialog
from view.gen.menuView import Ui_MenuDialog
from view.gen.newPasswordView import Ui_NewPasswordDialog
from view.gen.externView import Ui_ExternDialog
from view.gen.addExternView import Ui_AddExternDialog
from view.gen.closeExternView import Ui_CloseExternDialog
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
    
    msgBox.exec_()

def confirmBox(title = None, text = None, info = None):
    "Generic confirmation box"
    msgBox = QMessageBox()
    msgBox.setWindowTitle(title)
    msgBox.setText(text)
    msgBox.setInformativeText(info)
    msgBox.setIcon(QMessageBox.Warning)
    msgBox.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
    msgBox.setDefaultButton(QMessageBox.No)
    
    for button in msgBox.buttons():
        button.setMinimumWidth(100)
        button.setMinimumHeight(50)

    return msgBox


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
        self.btExternMenu.clicked.connect(self.showExternDialog)


    def confirmNewList(self):
        msgBox = confirmBox(
                'Nieuwe lijst?',
                'Je gaat nu de huidige lijst sluiten en een nieuwe aanmaken!',
                'Er wordt een Excel-bestand gegenereerd, de turfjes worden weer op 0 gezet.'
            )

        ret = msgBox.exec_()

        if ret == QMessageBox.Yes:

            l = self.session.query(List).order_by(desc(List.id)).first()
            members = (self.session.query(
                Member.name, func.count(Member.id))
                .join(Tally)
                .join(List)
                .filter(List.id == l.id)
                .group_by(Member)
            )

            filename = writeToExcel(members, l)

            self.session.add(List())
            self.session.commit()
            MessageBox('Een nieuw lijst is aangemaakt!', 
                "Er is een Excel-bestand aangemaakt, te vinden in 'data/sheets/{}'.".format(filename),
                QMessageBox.Information
            )
    

    def showNewPasswordDialog(self):
        NewPasswordView(self.session).exec_()

    def showExternDialog(self):
        ExternView(self.session).exec_()


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


class ExternView(QDialog, Ui_ExternDialog):
    "Extern menu dialog, enabling one to add or remove extern members"
    def __init__(self, session):
        super(ExternView, self).__init__()
        self.setupUi(self)
        self.session = session
        self.initialize()
        self.setupConnections()

    def setupConnections(self):
        self.btCancel.clicked.connect(self.reject)
        self.btAddExtern.clicked.connect(self.showAddExternDialog)
        self.btCloseExtern.clicked.connect(self.showCloseExternDialog)

    def initialize(self):
        externs = self.session.query(Member).filter(Room.member).filter(Room.id > 18)

        if externs.count() > 0:
            self.btCloseExtern.setEnabled(True)
        if externs.count() < 3:
            self.btAddExtern.setEnabled(True)

    def showAddExternDialog(self):
        addExternDialog = AddExternView(self.session)
        ret = addExternDialog.exec_()

        if ret:
            self.accept()

    def showCloseExternDialog(self):
        closeExternDialog = CloseExternView(self.session)
        ret = closeExternDialog.exec_()

        if ret:
            self.accept()

class AddExternView(QDialog, Ui_AddExternDialog):
    "Add new extern member"
    def __init__(self, session):
        super(AddExternView, self).__init__()
        self.setupUi(self)
        self.session = session
        self.setupConnections()

    def setupConnections(self):
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.accepted.connect(self.verify)

    def verify(self):
        name = self.lName.text().lstrip().rstrip()

        if len(name) > 0:
            room = (self.session.query(Room)
                    .filter(Room.member == None)
                    .filter(Room.id > 18)
                    .first()
                    )

            extern = Member(name)
            self.session.add(extern)
            room.member = extern

            self.session.commit()

            MessageBox(
                'Extern toegevoegd!',
                "Extern is toegevoegd als '{}'.".format(name),
                QMessageBox.Information
            )

            self.accept()
        else:
            MessageBox(
                'Error!',
                'Ongeldige naam! Naam moet minimaal 1 karakter bevatten!',
                QMessageBox.Critical
            ) 


class CloseExternView(QDialog, Ui_CloseExternDialog):
    "Close extern member slot"
    def __init__(self, session):
        super(CloseExternView, self).__init__()
        self.setupUi(self)
        self.session = session
        self.initialize()
        self.setupConnections()

    def setupConnections(self):
        self.btCancel.clicked.connect(self.reject)
        self.btExtern1.clicked.connect(lambda: self.verify(1))
        self.btExtern2.clicked.connect(lambda: self.verify(2))
        self.btExtern3.clicked.connect(lambda: self.verify(3))

    def initialize(self):
        externs = self.session.query(Member).filter(Room.member).filter(Room.id > 18)

        for extern in externs:
            if extern.room.id == 19:
                self.btExtern1.setEnabled(True)
                self.btExtern1.setText(extern.name)
            elif extern.room.id == 20:
                self.btExtern2.setEnabled(True)
                self.btExtern2.setText(extern.name)
            elif extern.room.id == 21:
                self.btExtern3.setEnabled(True)
                self.btExtern3.setText(extern.name)

    def verify(self, id):
        member = self.session.query(Room).get(18 + id).member

        msgBox = confirmBox(
                'Extern sluiten?',
                "Je staat op het punt om '{}' te sluiten!".format(member.name),
                'Turfjes worden niet verwijderd, maar er kan niet meer geturfd worden op deze naam!'
            )

        ret = msgBox.exec_()

        if ret == QMessageBox.Yes:
            member.room.member = None
            self.session.commit()

            MessageBox(
                'Extern gesloten',
                "'{}' is gesloten!".format(member.name),
                QMessageBox.Information
            )

            self.accept()