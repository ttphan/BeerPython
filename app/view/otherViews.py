from PySide.QtGui import *
from PySide.QtCore import *
from model.model import *
from view.gen.loginView import Ui_LoginDialog
from view.gen.menuView import Ui_MenuDialog
from view.gen.newPasswordView import Ui_NewPasswordDialog
from view.gen.externView import Ui_ExternDialog
from view.gen.addExternView import Ui_AddExternDialog
from view.gen.closeExternView import Ui_CloseExternDialog
from view.gen.memberMenuView import Ui_MemberMenuDialog
from view.gen.newMemberView import Ui_NewMemberDialog
from view.gen.closeMemberView import Ui_CloseMemberDialog
from view.gen.moveMemberView import Ui_MoveMemberDialog
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

        if button.text() == '&Yes':
            button.setText('Ja')
        else:
            button.setText('Nee')

    return msgBox


class LoginView(QDialog, Ui_LoginDialog):
    "Login dialog popup"
    def __init__(self, session):
        super(LoginView, self).__init__()
        self.setupUi(self)
        self.setupConnections()
        self.session = session
        self.initialize()

    def setupConnections(self):
        self.buttonBox.accepted.connect(self.verify)
        self.buttonBox.rejected.connect(self.reject)

    def initialize(self):
        for button in self.buttonBox.buttons():
            button.setMinimumHeight(50)
            button.setMinimumWidth(100)

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
        self.btNewList.clicked.connect(self.verify)
        self.btPassword.clicked.connect(self.showNewPasswordDialog)
        self.btExternMenu.clicked.connect(self.showExternDialog)
        self.btMemberMenu.clicked.connect(self.showMemberMenuDialog)


    def verify(self):
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

    def showMemberMenuDialog(self):
        MemberMenuView(self.session).exec_()


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


class MemberMenuView(QDialog, Ui_MemberMenuDialog):
    "Members menu for editing and closing"
    def __init__(self, session):
        super(MemberMenuView, self).__init__()
        self.setupUi(self)
        self.session = session
        self.setupConnections()
        self.initialize()

    def setupConnections(self):
        self.btCancel.clicked.connect(self.reject)
        self.btCloseMember.clicked.connect(self.showCloseMemberDialog)
        self.btNewMember.clicked.connect(self.showNewMemberDialog)
        self.btMoveMember.clicked.connect(self.showMoveMemberDialog)

    def initialize(self):
        emptyRooms = self.session.query(Room).filter(Room.member == None).filter(Room.id <= 18).all()

        if emptyRooms:
            self.btNewMember.setEnabled(True)
            self.btMoveMember.setEnabled(True)

    def showNewMemberDialog(self):
        newMemberDialog = NewMemberView(self.session)
        ret = newMemberDialog.exec_()

        if ret:
            self.accept()

    def showCloseMemberDialog(self):
        closeMemberDialog = CloseMemberView(self.session)
        ret = closeMemberDialog.exec_()

        if ret:
            self.accept()

    def showMoveMemberDialog(self):
        moveMemberDialog = MoveMemberView(self.session)
        ret = moveMemberDialog.exec_()
        
        if ret:
            self.accept()


class NewMemberView(QDialog, Ui_NewMemberDialog):
    def __init__(self, session):
        super(NewMemberView, self).__init__()
        self.setupUi(self)
        self.session = session
        self.setupConnections()
        self.initialize()

    def setupConnections(self):
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.accepted.connect(self.verify)

    def verify(self):
        name = self.tName.text().lstrip().rstrip()
        item = self.lRooms.currentItem()

        if len(name) > 0:
            if item:
                room = item.data(Qt.UserRole)
                msgBox = confirmBox(
                    'Nieuw huisgenoot',
                    '{} wordt toegevoegd als een nieuw huisgenoot voor kamer {}.'.format(name, room.id),
                    'Is dit juist?'
                )

                ret = msgBox.exec_()

                if ret == QMessageBox.Yes:
                    member = Member(name)
                    member.room = room
                    self.session.add(member)
                    self.session.commit()

                    MessageBox(
                        'Huisgenoot toegevoegd',
                        '{} is toegevoegd als een nieuw huisgenoot voor kamer {}!'.format(name, room.id),
                        QMessageBox.Information
                    )

                self.accept()
            else:
                MessageBox(
                    'Error!',
                    'Geen kamer geselecteerd!',
                    QMessageBox.Critical
                )
        else:
            MessageBox(
                'Error!',
                'Ongeldige naam! Naam moet minimaal 1 karakter bevatten!',
                QMessageBox.Critical
            )

    def initialize(self):
        emptyRooms = self.session.query(Room).filter(Room.member == None).filter(Room.id <= 18)

        for room in emptyRooms:
            item = QListWidgetItem('Kamer {}'.format(room.id), self.lRooms)
            item.setData(Qt.UserRole, room)            

        for button in self.buttonBox.buttons():
            button.setMinimumHeight(50)
            button.setMinimumWidth(100)

class CloseMemberView(QDialog, Ui_CloseMemberDialog):
    def __init__(self, session):
        super(CloseMemberView, self).__init__()
        self.setupUi(self)
        self.session = session
        self.setupConnections()
        self.initialize()

    def setupConnections(self):
        self.btCancel.clicked.connect(self.reject)
        self.btConfirm.clicked.connect(self.verify)

    def initialize(self):
        members = self.session.query(Member).filter(Room.member).filter(Room.id <= 18)

        for member in members:
            item = QListWidgetItem(member.name, self.lMembers)
            item.setData(Qt.UserRole, member)


    def verify(self):
        item = self.lMembers.currentItem()

        if item:
            member = item.data(Qt.UserRole)
            msgBox = confirmBox(
                'Huisgenoot vertrekt', 
                'Klopt het dat {} (Kamer {}) uit huis gaat? Hij of zij wordt dan van de lijst afgehaald!'.format(member.name, member.room.id),
                'DIT IS DUS NIET VOOR INTERN DOORVERHUIZEN!'
            )

            ret = msgBox.exec_()

            if ret == QMessageBox.Yes:
                member.room = None

                MessageBox(
                    'Huisgenoot vertrokken',
                    '{} is vertrokken en uit het huis!'.format(member.name),
                    QMessageBox.Information
                )

                self.accept()

class MoveMemberView(QDialog, Ui_MoveMemberDialog):
    def __init__(self, session):
        super(MoveMemberView, self).__init__()
        self.setupUi(self)
        self.session = session
        self.setupConnections()
        self.initialize()

    def setupConnections(self):
        self.btCancel.clicked.connect(self.reject)
        self.btConfirm.clicked.connect(self.verify)

    def initialize(self):
        members = self.session.query(Member).filter(Room.member).filter(Room.id <= 18)
        emptyRooms = self.session.query(Room).filter(Room.member == None).filter(Room.id <= 18)

        for member in members:
            item = QListWidgetItem(member.name, self.lMembers)
            item.setData(Qt.UserRole, member)

        for room in emptyRooms:
            item = QListWidgetItem('Kamer {}'.format(room.id), self.lRooms)
            item.setData(Qt.UserRole, room)

    def verify(self):
        memberItem = self.lMembers.currentItem()
        roomItem = self.lRooms.currentItem()

        if memberItem:
            if roomItem:
                member = memberItem.data(Qt.UserRole)
                room = roomItem.data(Qt.UserRole)

                msgBox = confirmBox(
                    'Interne doorverhuizing', 
                    'Klopt het dat {} intern gaat doorverhuizen?'.format(member.name),
                    'Hij of zij zal dan doorverhuizen naar kamer {}.'.format(room.id)
                )

                ret = msgBox.exec_()

                if ret == QMessageBox.Yes:
                    member.room = room
                    self.session.commit()

                    MessageBox(
                        'Interne doorverhuizing',
                        '{} is doorverhuisd naar kamer {}!'.format(member.name, room.id),
                        QMessageBox.Information
                    )

                    self.accept()

            else:
                MessageBox(
                    'Error!',
                    'Geen kamer geselecteerd!',
                    QMessageBox.Critical
                )
        else:
            MessageBox(
                'Error!',
                'Geen huisgenoot geselecteerd!',
                QMessageBox.Critical
            )
