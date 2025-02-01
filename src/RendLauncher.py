import sys
from PyQt5.QtWidgets import (QWidget, QApplication, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QCheckBox, QMessageBox)
from PyQt5.QtCore import QTimer, QProcess
import subprocess
import os
import configparser
import time  # Added the import for the 'time' module

def get_executable_path():
    if getattr(sys, 'frozen', False):
        # If the application is run as a bundle, the PyInstaller bootloader
        # extends the sys module by a flag frozen=True and sets the _MEIPASS attribute
        # to the path where the executable is located.
        return os.path.dirname(sys.executable)
    else:
        # If running the script directly, return the script's directory
        return os.path.dirname(os.path.abspath(__file__))

class RendClientLauncher(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.loadSettings()

    def initUI(self):
        vbox = QVBoxLayout()

        self.nameEdit = QLineEdit(self)
        self.factionEdit = QLineEdit(self)
        self.ipPortEdit = QLineEdit(self)
        self.uue4uFix = QCheckBox("Check this box if you need the UUE4U fix", self)
        self.delayEdit = QLineEdit("15", self)
        self.delayEdit.setToolTip("If the fix doesn't work, set this value higher. Default is 15 seconds.")

        playButton = QPushButton('Play', self)
        playButton.clicked.connect(self.onPlayButtonClicked)

        vbox.addWidget(QLabel('Name:'))
        vbox.addWidget(self.nameEdit)
        vbox.addWidget(QLabel('Faction#:'))
        vbox.addWidget(self.factionEdit)
        vbox.addWidget(QLabel('IP:Port:'))
        vbox.addWidget(self.ipPortEdit)
        vbox.addWidget(self.uue4uFix)
        vbox.addWidget(QLabel("If the fix doesn't work set this value higher (default 15):"))
        vbox.addWidget(self.delayEdit)
        vbox.addWidget(playButton)

        self.setLayout(vbox)
        self.setWindowTitle('Rend Client Launcher')
        self.show()

    def loadSettings(self):
        config = configparser.ConfigParser()
        ini_path = os.path.join(get_executable_path(), 'RendLauncher.ini')
        
        if not os.path.exists(ini_path):
            config['Settings'] = {
                'name': '',
                'faction': '',
                'ipPort': '',
                'delay': '15'
            }
            with open(ini_path, 'w') as configfile:
                config.write(configfile)
        else:
            config.read(ini_path)
        
        try:
            self.nameEdit.setText(config['Settings']['name'])
            self.factionEdit.setText(config['Settings']['faction'])
            self.ipPortEdit.setText(config['Settings']['ipPort'])
            self.delayEdit.setText(config['Settings']['delay'])
        except KeyError:
            # Handle case where keys are missing in the ini file
            pass

    def saveSettings(self):
        config = configparser.ConfigParser()
        ini_path = os.path.join(get_executable_path(), 'RendLauncher.ini')
        
        config['Settings'] = {
            'name': self.nameEdit.text(),
            'faction': self.factionEdit.text(),
            'ipPort': self.ipPortEdit.text(),
            'delay': self.delayEdit.text()
        }
        
        with open(ini_path, 'w') as configfile:
            config.write(configfile)

    def onPlayButtonClicked(self):
        name = self.nameEdit.text()
        faction = self.factionEdit.text()
        ip_port = self.ipPortEdit.text()
        args = ['-playername=' + name, '-faction=' + faction, '-connect=' + ip_port]

        try:
            delay = int(self.delayEdit.text())
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid number for delay.")
            return

        if self.uue4uFix.isChecked():
            self.blockAndLaunchUUE4U(args, delay)
        else:
            self.launchRendClient(args)
        
        # Schedule the application to close after execution
        QTimer.singleShot(5000, lambda: QApplication.instance().quit())  # 5 seconds delay before closing

    def blockAndLaunchUUE4U(self, args, delay):
        exe_path = os.path.join(get_executable_path(), 'Otherlands', 'Binaries', 'Win64', 'OtherlandsClient-Win64-Shipping.exe')
        rule_name = "BlockOtherlandsClient"

        # Add firewall rule to block the executable
        subprocess.run(['netsh', 'advfirewall', 'firewall', 'add', 'rule', 'name=' + rule_name, 'dir=out', 'action=block', 'program=' + exe_path], shell=True)

        # Launch the game with user-defined arguments
        self.launchRendClient(args)

        # Wait for user-defined delay after launching the game
        time.sleep(delay)

        # Launch dll-injection.exe
        injection_path = os.path.join(get_executable_path(), 'dll-injection.exe')
        subprocess.Popen([injection_path, 'UniversalUE4Unlocker.dll', 'OtherlandsClient-Win64-Shipping.exe'])

        # Remove the firewall rule
        subprocess.run(['netsh', 'advfirewall', 'firewall', 'delete', 'rule', 'name=' + rule_name], shell=True)

    def launchRendClient(self, args):
        rend_client_path = os.path.join(get_executable_path(), 'RendClient.exe')
        if os.path.exists(rend_client_path):
            subprocess.Popen([rend_client_path] + args)
        else:
            print(f"Error: {rend_client_path} not found!")

    def closeEvent(self, event):
        self.saveSettings()
        super().closeEvent(event)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = RendClientLauncher()
    sys.exit(app.exec_())