# -*- coding: utf-8 -*-
"""
*****************************************************************************
 * Copyright (c) 2023 Tolsimir
 *
 * The program "Object Creator" and all subsequent modules are licensed
 * under the GNU General Public License version 3.
 *****************************************************************************
"""


from PyQt5.QtWidgets import QTextEdit, QSpinBox, QMainWindow, QDialog, QApplication, QMessageBox, QWidget, QGridLayout, QVBoxLayout, QHBoxLayout, QTabWidget, QDial, QSlider, QScrollBar, QGroupBox, QToolButton, QComboBox, QPushButton, QLineEdit, QLabel, QCheckBox, QDoubleSpinBox, QListWidget, QFileDialog
from PyQt5 import uic, QtGui, QtCore
from PIL import Image
from PIL.ImageQt import ImageQt
import traceback
import sys

if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


import io, os
from os import getcwd
from os.path import splitext, split, abspath,join, exists
from json import load as jload
from json import dump as jdump
from enum import Enum
import requests

from customwidgets import ColorSelectWidget, ToolBoxWidget
import customwidgets as cwdg
import widgets as wdg
import auxiliaries as aux



import ctypes
#import pyi_splash

# Update the text on the splash screen
#pyi_splash.update_text("Loading Object Creator")
"""path = self.app_data_path
        with open(f'{path}/config.json', mode='w') as file:
            jdump(obj=self.settings, fp=file, indent=2)"""

VERSION = 'v0.0.1'


myappid = f'objectcreator.{VERSION}' # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

class MainWindowUi(QMainWindow):
    def __init__(self, app_data_path, opening_objects = None):
        super().__init__()
        uic.loadUi(aux.resource_path('gui/MainWindow.ui'), self)
        self.setWindowIcon(QtGui.QIcon(aux.resource_path("gui/icon.png")))
        self.setWindowTitle(f'Item Ranker - {VERSION}')

        self.app_data_path = app_data_path
        self.loadSettings()
        self.bounding_boxes = aux.BoundingBoxes()
        self.symm_axes = aux.SymmetryAxes()
        self.last_open_folder = self.settings.get('opendefault', None)

        self.setAcceptDrops(True)

        ##### Tabs
       

        self.saveButton = self.findChild(QPushButton, "saveListButton")
        self.loadButton = self.findChild(QPushButton, "loadListButton")
        self.compareButton = self.findChild(QPushButton, "compareButton")
        self.cyclesSpinBox = self.findChild(QSpinBox, "cycleCountSpinBox")
        self.rulesLabel = self.findChild(QLabel, "listRulesLabel")
        self.cyclesLabel = self.findChild(QLabel, "howManyCyclesLabel")
        self.inputList = self.findChild(QTextEdit, "inputList") 
        
        self.saveButton.clicked.connect(self.saveList)
        self.loadButton.clicked.connect(self.loadList)
        self.cyclesSpinBox.valuedChanged.connect(self.spinboxChange)
        self.inputList.valueChanged.conenct(self.listChanged)


       
    
        self.show()
      #  self.checkForUpdates(silent = True)
    def saveList(self):
        return
    def loadList(self):
        folder = self.last_open_folder
        if not folder:
            folder = getcwd()
        filepaths, _ = QFileDialog.getOpenFileNames(
            self, "Open Object", folder, "All Object Type Files (*.parkobj *.DAT *.json);; Parkobj Files (*.parkobj);; DAT files (*.DAT);; JSON Files (*.json);; All Files (*.*)")

        if filepaths:
            for filepath in filepaths:
                self.loadObjectFromPath(filepath)
        try:
            o = obj.load(filepath, openpath = self.openpath)
            name = o.data.get('id', '').split('.',2)[-1]
            if not name:
                if o.old_id:
                    name = o.old_id
                else:
                    name = f'Object {self.new_object_count}'
                    self.new_object_count += 1
        except Exception as e:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Error Trapper")
            msg.setText("Failed to load object")
            msg.setInformativeText(str(traceback.format_exc()))
            msg.show()
            return
    def spinboxChange(self):
        return
    def comparePressed(self):
        return
    def listChanged(self):
        return
    
    def checkForUpdates(self, silent = False):
        try:
            response = requests.get("https://api.github.com/repos/danielmeinert/objectcreator/releases/latest")
        except requests.exceptions.ConnectionError:
            return

        # check if there is a higher version on git
        git_version = response.json()['tag_name']

        if not versionCheck(git_version):
            if not silent:
                msg = QMessageBox(self)
                msg.setIcon(QMessageBox.Information)
                msg.setWindowTitle("No update available")
                msg.setText(f"Object Creator {VERSION} is up to date!")
                msg.setStandardButtons(QMessageBox.Ok)

                msg.exec_()

            return

        url = response.json()['html_url']
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("New version available!")
        msg.setTextFormat(QtCore.Qt.RichText)

        msg.setText(f"Object Creator {git_version} is now available! <br> \
                Your version: {VERSION} <br> \
                <a href='{url}'>Click here to go to download page. </a> <br> <br> \
                Alternatively, would you like to update automatically? <br> \
                This only works if the program has been installed via the installer.")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)


        reply = msg.exec_()

        # Only in the .exe program the updater can be used
        if reply == QMessageBox.Yes:
            #quit and run updater
            try:
                os.execl('updater.exe', 'updater.exe')
            except FileNotFoundError:
                return


    ### Internal methods

        path = self.app_data_path
        with open(f'{path}/config.json', mode='w') as file:
            jdump(obj=self.settings, fp=file, indent=2)


        dialog = wdg.ChangeSettingsUi(self.settings)

        if dialog.exec():
            self.settings = dialog.ret

            self.openpath = self.settings['openpath']
            self.setCurrentImportColor(self.settings['transparency_color'])
            self.setCurrentPalette(self.settings['palette'], update_widgets = update_widgets)

            self.saveSettings()

        try:
            o = obj.load(filepath, openpath = self.openpath)
            name = o.data.get('id', '').split('.',2)[-1]
            if not name:
                if o.old_id:
                    name = o.old_id
                else:
                    name = f'Object {self.new_object_count}'
                    self.new_object_count += 1
        except Exception as e:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Error Trapper")
            msg.setText("Failed to load object")
            msg.setInformativeText(str(traceback.format_exc()))
            msg.show()
            return


        extension = splitext(filepath)[1].lower()
        author_id = None
        filepath, filename = split(filepath)
        if extension == '.parkobj':
            # We assume that when the filename has more than 2 dots that the first part corresponds to the author id
            if len(filename.split('.')) > 2:
                author_id = filename.split('.')[0]


        if not self.current_palette == pal.orct:
            o.switchPalette(self.current_palette)


        object_tab = wdg.ObjectTabSS(o, self, filepath, author_id = author_id)

        sprite_tab = wdg.SpriteTab(self, object_tab)

        self.object_tabs.addTab(object_tab, name)
        self.object_tabs.setCurrentWidget(object_tab)
        self.sprite_tabs.addTab(sprite_tab,  f"{name} (locked)")
        self.sprite_tabs.setCurrentWidget(sprite_tab)

        self.last_open_folder = filepath

    ### Tab actions



        current_object_tab = self.object_tabs.currentWidget()
        current_sprite_tab = self.sprite_tabs.currentWidget()

        if current_object_tab is None or current_sprite_tab is None:
            return

        if self.button_lock.isChecked():
            name = self.object_tabs.tabText(self.object_tabs.currentIndex())

            if current_object_tab.locked:
                old_sprite_Tab = current_object_tab.locked_sprite_tab
                old_sprite_Tab.unlockObjectTab()
                self.sprite_tabs.setTabText(self.sprite_tabs.indexOf(old_sprite_Tab), f"Sprite {self.new_sprite_count}")
                self.new_sprite_count += 1

            self.pushSprite()

            current_object_tab.lockWithSpriteTab(current_sprite_tab)
            current_sprite_tab.lockWithObjectTab(current_object_tab)

            self.sprite_tabs.setTabText(self.sprite_tabs.currentIndex(), f"{name} (locked)")

            self.button_pull_sprite.setEnabled(False)
            self.button_push_sprite.setEnabled(False)
            self.checkbox_all_views.setEnabled(True)

        else:

            name = f'Sprite {self.new_sprite_count}'
            self.new_sprite_count += 1

            current_object_tab.unlockSpriteTab()
            current_sprite_tab.unlockObjectTab()

            self.sprite_tabs.setTabText(self.sprite_tabs.currentIndex(), f"{name}")

            self.button_pull_sprite.setEnabled(True)
            self.button_push_sprite.setEnabled(True)
            self.checkbox_all_views.setEnabled(False)
            self.checkbox_all_views.setChecked(False)


        object_tab = self.object_tabs.currentWidget()
        sprite_tab = self.sprite_tabs.currentWidget()

        sprite_tab.setSprite(object_tab.giveCurrentMainViewSprite()[0])

    ### Menubar actions

        folder = self.last_open_folder
        if not folder:
            folder = getcwd()
        filepaths, _ = QFileDialog.getOpenFileNames(
            self, "Open Object", folder, "All Object Type Files (*.parkobj *.DAT *.json);; Parkobj Files (*.parkobj);; DAT files (*.DAT);; JSON Files (*.json);; All Files (*.*)")

        if filepaths:
            for filepath in filepaths:
                self.loadObjectFromPath(filepath)
#save button 

        widget = self.object_tabs.currentWidget()

        if widget is not None:
            widget.saveObject(get_path = True)

    

        url = "https://github.com/danielmeinert/objectcreator"

        icon = QtGui.QPixmap(aux.resource_path("gui/icon.png"))

        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("About Object Creator")
        msg.setTextFormat(QtCore.Qt.RichText)
        msg.setIconPixmap(icon)

        msg.setText(f"Object Creator version {VERSION} <br> \
                If you want to give feedback or issue bugs, \
                visit the <a href='{url}'>github page. </a> <br> <br> \
                Copyright (c) 2023 Tolsimir <br> \
                The program 'Object Creator' is licensed under the GNU General Public License version 3.")
        msg.setStandardButtons(QMessageBox.Close)

        msg.exec_()


    #### Color manipulations

    
        selected_colors = self.color_select_panel.selectedColors()

        if self.checkbox_all_views.isChecked():
            widget = self.object_tabs.currentWidget()

            widget.colorRemoveAll(selected_colors)

        else:
            widget = self.sprite_tabs.currentWidget()

            widget.colorRemove(selected_colors)

   

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Alt:
            self.toolbox.selectTool(cwdg.Tools.EYEDROPPER)



    def keyReleaseEvent(self, e):
        if e.key() == QtCore.Qt.Key_Alt:
            self.toolbox.restoreTool()

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls:
            for url in e.mimeData().urls():
                filepath = url.toLocalFile()
                extension = splitext(filepath)[1].lower()

                if extension in ['.parkobj', '.dat', '.json']:
                    e.accept()
        else:
            e.ingore()

    def dropEvent(self, e):
        for url in e.mimeData().urls():
            filepath = url.toLocalFile()
            extension = splitext(filepath)[1].lower()

            if extension in ['.parkobj', '.dat', '.json']:
                self.loadObjectFromPath(filepath)




def excepthook(exc_type, exc_value, exc_tb):

    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    print("error message:\n", tb)


    sys._excepthook(exc_type, exc_value, exc_tb)
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setWindowTitle("Error Trapper")
    msg.setText("Runtime error:")
    msg.setInformativeText(tb)
    msg.exec_()
    #sys.exit()

sys._excepthook = sys.excepthook
sys.excepthook = excepthook

def versionCheck(version):

    version = version[1:].split('.')
    version_this = VERSION[1:].split('.')

    for i in range(len(version_this),len(version)):
        version_this.append(0)

    for i, val in enumerate(version):

        if int(val) > int(version_this[i]):
            return True

    return False


def main():
    # if not QApplication.instance():
    #     app = QApplication(sys.argv)
    # else:
    #     app = QApplication.instance()

    #pyi_splash.close()
    app = QApplication(sys.argv)

    app_data_path = join(os.environ['APPDATA'],'Item Ranker')
    if not exists(app_data_path):
        os.makedirs(app_data_path)

    main = MainWindowUi(app_data_path= app_data_path, opening_objects= sys.argv[1:],)
    main.show()
    main.activateWindow()

    app.exec_()


    return main

if __name__ == '__main__':
    m = main()
