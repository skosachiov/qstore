# imports

import json
import sys

from PyQt6 import uic, QtGui, QtCore, QtWidgets
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QDialog, QGroupBox, QButtonGroup
from PyQt6.QtWidgets import QPushButton, QLabel, QHBoxLayout, QWidget, QListWidgetItem
import pickle
import copy
import datetime
import random
import logging
import requests
import subprocess
import socket
import getpass

# create class of sofsaasdtware(Card)


class Card(QWidget):

    selected_cards = {}  # software to install

    def __init__(self, name, dcard=None):
        super(QWidget, self).__init__()
        self.layoutWidget = QtWidgets.QWidget()
        self.setObjectName("Card")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.labelLogo = QtWidgets.QLabel(parent=self.layoutWidget)
        self.labelLogo.setObjectName("labelLogo")
        self.horizontalLayout.addWidget(self.labelLogo)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")

        self.labelDescription = QtWidgets.QLabel(parent=self.layoutWidget)
        self.labelDescription.setWordWrap(True)
        self.labelDescription.setObjectName("labelDescription")
        self.verticalLayout.addWidget(self.labelDescription)

        self.horizontalLayout_soft = QtWidgets.QHBoxLayout()
        self.horizontalLayout_soft.setObjectName("horizontalLayout_soft")
        self.labelName = QtWidgets.QLabel(parent=self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.labelName.setFont(font)
        self.labelName.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading |
                                    QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignTop)
        self.labelName.setObjectName("labelName")
        self.horizontalLayout_soft.addWidget(self.labelName)
        self.labelDescription = QtWidgets.QLabel(parent=self.layoutWidget)
        self.labelDescription.setWordWrap(True)
        self.labelDescription.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading | QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignTop)
        self.labelDescription.setObjectName("labelDescription")
        self.horizontalLayout_soft.addWidget(self.labelDescription)
        self.horizontalLayout_soft.setStretch(0, 1)
        self.horizontalLayout_soft.setStretch(1, 4)
        self.verticalLayout.addLayout(self.horizontalLayout_soft)

        self.horizontalLayout_buttons = QtWidgets.QHBoxLayout()
        self.horizontalLayout_buttons.setObjectName("horizontalLayout_buttons")
        self.labelProp = QtWidgets.QLabel(parent=self.layoutWidget)
        self.labelProp.setObjectName("labelProp")
        self.horizontalLayout_buttons.addWidget(self.labelProp)

        self.checkBox = QtWidgets.QCheckBox(parent=self.layoutWidget)
        self.checkBox.setObjectName("checkBox")
        self.checkBox.setAutoFillBackground(True)
        self.horizontalLayout_buttons.addWidget(self.checkBox)

        self.horizontalLayout_buttons.setStretch(0, 6)
        self.horizontalLayout_buttons.setStretch(1, 1)
        self.horizontalLayout_buttons.setStretch(2, 1)
        self.verticalLayout.addLayout(self.horizontalLayout_buttons)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 4)

        self.data = dcard  # keep original dict
        self.labelName.setText(dcard['name'].upper())
        self.labelDescription.setText(dcard['description'])

        if 'image' in dcard:
            self.pixmap = QPixmap("html/" + dcard['image'])
            self.labelLogo.setPixmap(self.pixmap)

        prop = 'type: ' + dcard['type'] + \
            ', size: ' + str(dcard['size']/1000000) + 'M' + \
            ', cat: ' + dcard['category'] + \
            ', appr: ' + str(dcard['approve'])
        self.labelProp.setText(prop)

        self.retranslateUi(Card)
        self.setLayout(self.horizontalLayout)

        self.checkBox.stateChanged.connect(self.install_checkbox)

    def retranslateUi(self, Card):
        _translate = QtCore.QCoreApplication.translate
        # self.labelLogo.setText(_translate("Card", "Logo"))
        # self.labelDescription.setText(_translate("Card", "Description"))
        # self.labelProp.setText(_translate("Card", "Prop"))
        # self.pushButtonUninstall.setText(_translate("Card", "Uninstall"))
        # self.pushButtonInstall.setText(_translate("Card", "Install"))
        self.checkBox.setText(_translate("Card", "Install"))

    # select the software to install

    def install_checkbox(self):
        if self.checkBox.isChecked():
            Card.selected_cards[self.data['name']] = self.data
        else:
            del Card.selected_cards[self.data['name']]
        ex.lcdNumber_apps.display(len(Card.selected_cards))
        all_size = 0
        for k in Card.selected_cards:
            all_size += Card.selected_cards[k]['size']
        ex.lcdNumber_size.display(all_size//1000000)
        logging.debug(Card.selected_cards)


class ConfigDialog(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('./qstoreconfig.ui', self)

        self.level = {"debug": logging.DEBUG, 'info': logging.INFO,
                      'warning': logging.WARNING, 'error': logging.ERROR, 'critical': logging.CRITICAL}

        with open("qstore.conf", mode="r") as f:
            self.config = json.load(f)

        if self.config["managed_by_org"]:
            self.radioButton_local.setChecked(True)
        else:
            self.radioButton_server.setChecked(True)

        if self.config["local_db"]:
            self.radioButton_2.setChecked(True)
        else:
            self.radioButton.setChecked(True)

        self.comboBox.setCurrentText(self.config["logging"])

        self.lineEdit_server.setText(self.config['server_url'])

        self.comboBox.activated.connect(self.set_logging)
        self.changingGroup = QButtonGroup()
        self.changingGroup.addButton(self.radioButton_local)
        self.changingGroup.addButton(self.radioButton_server)
        self.changingGroup.buttonClicked.connect(self.set_logging)
        self.localGroup = QButtonGroup()
        self.localGroup.addButton(self.radioButton)
        self.localGroup.addButton(self.radioButton_2)
        self.localGroup.buttonClicked.connect(self.set_logging)
        self.lineEdit_server.textChanged.connect(self.set_logging)

    def set_logging(self, item):
        # with open("qstore.conf", mode="r") as f:
        #     config = json.load(f)
        config = {}

        config['logging'] = self.comboBox.currentText()
        logging.getLogger().setLevel(level=self.level[config['logging']])

        if self.radioButton_2.isChecked():
            managed = True
        else:
            managed = False

        config['managed_by_org'] = managed

        if self.radioButton.isChecked():
            local = True
        else:
            local = False

        config['local_db'] = local

        config['server_url'] = self.lineEdit_server.text()

        with open("qstore.conf", mode="w") as f:
            json.dump(config, f)

# class main window


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('./qstore.ui', self)

        self.level = {"debug": logging.DEBUG, 'info': logging.INFO,
                      'warning': logging.WARNING, 'error': logging.ERROR, 'critical': logging.CRITICAL}

        configs = [
            './qstore.conf',
            '~/.local/qstore/qstore.conf',
            '/usr/local/etc/qstore/qstore.conf']

        self.config = {}
        for c in configs:
            try:
                with open(c, 'rb') as f:
                    self.config.update(json.load(f))
            except:
                pass

        logging.getLogger().setLevel(level=self.level[self.config['logging']])

        self.pushButton_execute.clicked.connect(self.execute_button)
        self.pushButton_config.clicked.connect(self.config_button)

        self.lineEdit.textEdited.connect(self.search)

        self.listWidget_categories.itemClicked.connect(self.click_category)

        # check server
        try:
            response = requests.get(self.config['server_url'])
            logging.debug(response.status_code)
            if response.status_code == 200:
                self.statusbar.showMessage("Server OK")
            else:
                self.statusbar.showMessage(
                    "Server is accessible but sth is not right. Response codde")
                self.statusbar.setStyleSheet("background-color : red")
        except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError) as e:
            self.statusbar.showMessage("Unable to establish server connection")
            self.statusbar.setStyleSheet("background-color : red")

        sources = [
            'html/qstore/qstore.flatpak.json',
            'html/qstore/qstore.package.json',
            'html/qstore/qstore.ansible.json',
            'html/qstore/qstore.repo.json']
        self.repo = {}
        if self.config['local_db']:
            for s in sources:
                with open(s, 'rb') as f:
                    self.repo.update(json.load(f))
        else:
            for s in sources:
                resp = requests.get(url=self.config['server_url']+s)
                self.repo.update(resp.json())

        categories = set()

        self.listWidget_software.setSpacing(8)
        for k, v in sorted(self.repo.items()):
            widget = Card(k.upper(), v)
            item = QListWidgetItem()
            self.listWidget_software.addItem(item)
            self.listWidget_software.setItemWidget(item, widget)
            item.setSizeHint(widget.sizeHint())
            categories.add(v['category'])

        self.listWidget_categories.addItems(sorted(categories))

# search software by category

    def click_category(self, item):
        self.listWidget_software.clear()

        for k, v in list(filter(lambda x: x[1]['category'] == item.text(), sorted(self.repo.items()))):
            widget = Card(k.upper(), v)
            item = QListWidgetItem()
            self.listWidget_software.addItem(item)
            self.listWidget_software.setItemWidget(item, widget)
            item.setSizeHint(widget.sizeHint())

# search software by name and description

    def search(self, searchstr):
        self.listWidget_software.clear()

        for k, v in list(filter(lambda x: (x[1]['description']+x[0]).lower().find(searchstr.lower()) >= 0, sorted(self.repo.items()))):
            widget = Card(k.upper(), v)
            item = QListWidgetItem()
            self.listWidget_software.addItem(item)
            self.listWidget_software.setItemWidget(item, widget)
            item.setSizeHint(widget.sizeHint())

# button to send selected software to server

    def execute_button(self):
        self.statusbar.showMessage("install")
        url = self.config['server_url']+'/html/post/'+getpass.getuser()+'@'+socket.gethostname().split('.')[0]+'.json'
        resp = requests.post(url, data=json.dumps(Card.selected_cards))
        logging.debug(resp.text)
        subprocess.run(["dbus-send", "--system", "--type=signal", "--dest=org.freedesktop.qstore",
                "/org/freedesktop/qstore", "org.freedesktop.qstore"])

# button to open settings

    def config_button(self):
        dialog = ConfigDialog()
        dialog.exec()

# open main window


if __name__ == '__main__':
    logging.basicConfig(level=logging.ERROR)
    # logging.basicConfig(filename='/tmp/qstore.log', level=logging.DEBUG)
    logging.debug("qstore start")
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
