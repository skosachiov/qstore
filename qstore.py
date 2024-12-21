# imports
import io
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

templatec = """<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>Dialog</class>
 <widget class="QDialog" name="Dialog">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>1007</width>
    <height>454</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>Config</string>
  </property>
  <layout class="QGridLayout" name="gridLayout">
   <item row="0" column="0">
    <layout class="QVBoxLayout" name="verticalLayout">
     <property name="spacing">
      <number>32</number>
     </property>
     <item>
      <layout class="QHBoxLayout" name="horizontalLayout_2">
       <item>
        <widget class="QGroupBox" name="groupBox_3">
         <property name="title">
          <string>Config</string>
         </property>
         <layout class="QFormLayout" name="formLayout">
          <item row="0" column="1">
           <layout class="QVBoxLayout" name="verticalLayout_2">
            <item>
             <widget class="QRadioButton" name="radioButton_local">
              <property name="text">
               <string>Local config</string>
              </property>
             </widget>
            </item>
            <item>
             <widget class="QRadioButton" name="radioButton_server">
              <property name="text">
               <string>Server side config</string>
              </property>
             </widget>
            </item>
           </layout>
          </item>
          <item row="1" column="1">
           <layout class="QHBoxLayout" name="horizontalLayout">
            <item>
             <widget class="QLabel" name="label">
              <property name="text">
               <string>Server folder URL</string>
              </property>
             </widget>
            </item>
            <item>
             <widget class="QLineEdit" name="lineEdit_server"/>
            </item>
           </layout>
          </item>
         </layout>
        </widget>
       </item>
      </layout>
     </item>
     <item>
      <layout class="QHBoxLayout" name="horizontalLayout_3">
       <item>
        <widget class="QGroupBox" name="groupBox">
         <property name="title">
          <string>Flatpak</string>
         </property>
         <layout class="QGridLayout" name="gridLayout_3">
          <item row="0" column="0">
           <layout class="QVBoxLayout" name="verticalLayout_4">
            <item>
             <widget class="QRadioButton" name="radioButton_2">
              <property name="text">
               <string>System wide install</string>
              </property>
             </widget>
            </item>
            <item>
             <widget class="QRadioButton" name="radioButton">
              <property name="text">
               <string>Userspace install</string>
              </property>
             </widget>
            </item>
           </layout>
          </item>
         </layout>
        </widget>
       </item>
      </layout>
     </item>
     <item>
      <layout class="QHBoxLayout" name="horizontalLayout_4">
       <item>
        <widget class="QGroupBox" name="groupBox_2">
         <property name="title">
          <string>Log</string>
         </property>
         <layout class="QGridLayout" name="gridLayout_2">
          <item row="0" column="0">
           <layout class="QHBoxLayout" name="horizontalLayout_5">
            <item>
             <widget class="QLabel" name="label_2">
              <property name="text">
               <string>Level</string>
              </property>
             </widget>
            </item>
            <item>
             <widget class="QComboBox" name="comboBox">
              <item>
               <property name="text">
                <string>debug</string>
               </property>
              </item>
              <item>
               <property name="text">
                <string>info</string>
               </property>
              </item>
              <item>
               <property name="text">
                <string>warning</string>
               </property>
              </item>
              <item>
               <property name="text">
                <string>error</string>
               </property>
              </item>
              <item>
               <property name="text">
                <string>critical</string>
               </property>
              </item>
             </widget>
            </item>
           </layout>
          </item>
          <item row="0" column="1">
           <spacer name="horizontalSpacer">
            <property name="orientation">
             <enum>Qt::Horizontal</enum>
            </property>
            <property name="sizeHint" stdset="0">
             <size>
              <width>40</width>
              <height>20</height>
             </size>
            </property>
           </spacer>
          </item>
         </layout>
        </widget>
       </item>
      </layout>
     </item>
    </layout>
   </item>
   <item row="1" column="0">
    <widget class="QDialogButtonBox" name="buttonBox">
     <property name="orientation">
      <enum>Qt::Horizontal</enum>
     </property>
     <property name="standardButtons">
      <set>QDialogButtonBox::Cancel|QDialogButtonBox::Ok</set>
     </property>
    </widget>
   </item>
  </layout>
 </widget>
 <resources/>
 <connections>
  <connection>
   <sender>buttonBox</sender>
   <signal>accepted()</signal>
   <receiver>Dialog</receiver>
   <slot>accept()</slot>
   <hints>
    <hint type="sourcelabel">
     <x>248</x>
     <y>254</y>
    </hint>
    <hint type="destinationlabel">
     <x>157</x>
     <y>274</y>
    </hint>
   </hints>
  </connection>
  <connection>
   <sender>buttonBox</sender>
   <signal>rejected()</signal>
   <receiver>Dialog</receiver>
   <slot>reject()</slot>
   <hints>
    <hint type="sourcelabel">
     <x>316</x>
     <y>260</y>
    </hint>
    <hint type="destinationlabel">
     <x>286</x>
     <y>274</y>
    </hint>
   </hints>
  </connection>
 </connections>
</ui>
"""

class ConfigDialog(QDialog):
    def __init__(self):
        super().__init__()
        fc = io.StringIO(templatec)
        uic.loadUi(fc, self)

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

template = """<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>1172</width>
    <height>661</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>QStore</string>
  </property>
  <widget class="QWidget" name="centralwidget">
   <property name="enabled">
    <bool>true</bool>
   </property>
   <property name="sizePolicy">
    <sizepolicy hsizetype="Preferred" vsizetype="Preferred">
     <horstretch>0</horstretch>
     <verstretch>0</verstretch>
    </sizepolicy>
   </property>
   <layout class="QGridLayout" name="gridLayout">
    <item row="0" column="0">
     <layout class="QVBoxLayout" name="verticalLayout">
      <property name="sizeConstraint">
       <enum>QLayout::SetMaximumSize</enum>
      </property>
      <property name="leftMargin">
       <number>0</number>
      </property>
      <item>
       <layout class="QHBoxLayout" name="horizontalLayout">
        <item>
         <widget class="QLineEdit" name="lineEdit"/>
        </item>
        <item>
         <widget class="QPushButton" name="pushButton_search">
          <property name="text">
           <string>Search</string>
          </property>
         </widget>
        </item>
        <item>
         <spacer name="horizontalSpacer_top">
          <property name="orientation">
           <enum>Qt::Horizontal</enum>
          </property>
          <property name="sizeHint" stdset="0">
           <size>
            <width>40</width>
            <height>20</height>
           </size>
          </property>
         </spacer>
        </item>
        <item>
         <widget class="QPushButton" name="pushButton_config">
          <property name="text">
           <string>Config</string>
          </property>
          <property name="icon">
           <iconset theme="emblem-system">
            <normaloff>.</normaloff>.</iconset>
          </property>
          <property name="iconSize">
           <size>
            <width>32</width>
            <height>32</height>
           </size>
          </property>
         </widget>
        </item>
       </layout>
      </item>
      <item>
       <layout class="QHBoxLayout" name="horizontalLayout_top" stretch="1,0,4">
        <item>
         <widget class="QListWidget" name="listWidget_categories">
          <property name="sortingEnabled">
           <bool>false</bool>
          </property>
         </widget>
        </item>
        <item>
         <widget class="Line" name="line">
          <property name="orientation">
           <enum>Qt::Vertical</enum>
          </property>
         </widget>
        </item>
        <item>
         <widget class="QListWidget" name="listWidget_software">
          <property name="verticalScrollMode">
           <enum>QAbstractItemView::ScrollPerPixel</enum>
          </property>
         </widget>
        </item>
       </layout>
      </item>
      <item>
       <layout class="QHBoxLayout" name="horizontalLayout_bottom">
        <item>
         <spacer name="horizontalSpacer">
          <property name="orientation">
           <enum>Qt::Horizontal</enum>
          </property>
          <property name="sizeHint" stdset="0">
           <size>
            <width>40</width>
            <height>20</height>
           </size>
          </property>
         </spacer>
        </item>
        <item>
         <spacer name="horizontalSpacer_3">
          <property name="orientation">
           <enum>Qt::Horizontal</enum>
          </property>
          <property name="sizeHint" stdset="0">
           <size>
            <width>40</width>
            <height>20</height>
           </size>
          </property>
         </spacer>
        </item>
        <item>
         <widget class="QLabel" name="label">
          <property name="text">
           <string>Apps to install</string>
          </property>
         </widget>
        </item>
        <item>
         <widget class="QLCDNumber" name="lcdNumber_apps">
          <property name="font">
           <font>
            <pointsize>14</pointsize>
            <bold>true</bold>
           </font>
          </property>
         </widget>
        </item>
        <item>
         <spacer name="horizontalSpacer_4">
          <property name="orientation">
           <enum>Qt::Horizontal</enum>
          </property>
          <property name="sizeHint" stdset="0">
           <size>
            <width>40</width>
            <height>20</height>
           </size>
          </property>
         </spacer>
        </item>
        <item>
         <widget class="QLabel" name="label_2">
          <property name="text">
           <string>Size</string>
          </property>
         </widget>
        </item>
        <item>
         <widget class="QLCDNumber" name="lcdNumber_size">
          <property name="font">
           <font>
            <pointsize>14</pointsize>
            <bold>true</bold>
           </font>
          </property>
         </widget>
        </item>
        <item>
         <widget class="QLabel" name="label_3">
          <property name="text">
           <string>M</string>
          </property>
         </widget>
        </item>
        <item>
         <spacer name="horizontalSpacer_2">
          <property name="orientation">
           <enum>Qt::Horizontal</enum>
          </property>
          <property name="sizeHint" stdset="0">
           <size>
            <width>20</width>
            <height>20</height>
           </size>
          </property>
         </spacer>
        </item>
        <item>
         <widget class="QPushButton" name="pushButton_cancel">
          <property name="text">
           <string>Cancel</string>
          </property>
          <property name="icon">
           <iconset theme="application-exit">
            <normaloff>.</normaloff>.</iconset>
          </property>
         </widget>
        </item>
        <item>
         <widget class="QPushButton" name="pushButton_execute">
          <property name="text">
           <string>Execute</string>
          </property>
          <property name="icon">
           <iconset theme="emblem-default">
            <normaloff>.</normaloff>.</iconset>
          </property>
         </widget>
        </item>
       </layout>
      </item>
     </layout>
    </item>
   </layout>
  </widget>
  <widget class="QMenuBar" name="menubar">
   <property name="geometry">
    <rect>
     <x>0</x>
     <y>0</y>
     <width>1172</width>
     <height>23</height>
    </rect>
   </property>
  </widget>
  <widget class="QStatusBar" name="statusbar"/>
 </widget>
 <resources/>
 <connections/>
</ui>
"""

class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        f = io.StringIO(template)
        uic.loadUi(f, self)

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
