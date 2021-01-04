'''
FTP Client

v1.0.0 - 04/01/2020

Developed by:
Matheus Fay Soares
@matheusfay
'''

from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QTextEdit, QGroupBox, QLineEdit, QComboBox, \
    QMessageBox, QLabel
from PyQt5 import uic, QtCore, QtGui
from PyQt5.QtCore import QTimer, QTime
from PyQt5.QtGui import QPixmap
import sys
import os

from datetime import datetime
from pythonping import ping
import socket

import pysftp
import paramiko

class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        uic.loadUi(os.getcwd() + "\gui.ui", self)

        # Diretorios
        global imagens
        imagens = os.getcwd() + "\images\\"
        global output_files
        output_files = os.getcwd() + "\output_files\\"

        self.setWindowTitle('FTP Client by MFS')
        self.init()

        self.ping.clicked.connect(self.ping_test)  # Ping
        self.start.clicked.connect(self.bt_connection)  # Start
        self.stop.clicked.connect(self.bt_disconnection)  # Stop

        self.show()

    def init(self):
        self.host = self.findChild(QLineEdit, "host")
        self.port = self.findChild(QLineEdit, "port")
        self.user = self.findChild(QLineEdit, "user")
        self.password = self.findChild(QLineEdit, "password")

        self.start = self.findChild(QPushButton, "start")
        self.stop = self.findChild(QPushButton, "stop")
        self.ping = self.findChild(QPushButton, "ping")

        self.status = self.findChild(QTextEdit, "status")
        self.status.setReadOnly(True)
        self.files = self.findChild(QTextEdit, "files")
        self.files.setReadOnly(True)

        self.logo = self.findChild(QLabel, "logo")

    def ping_test(self):
        IP_TESTE = str(self.host.text())
        self.status.clear()
        self.status.append(f"Pinging [{IP_TESTE}]:")

        ping_file = open(output_files + "ping_output.txt", "w")
        ping(IP_TESTE, verbose=True, out=ping_file)
        ping_file.close()

        ping_file = open(output_files + "ping_output.txt", "r")
        test_data_list = ping_file.readlines()
        for linha in test_data_list:
            self.status.append(linha.rstrip())
        ping_file.close()

    def bt_connection(self):
        sftpURL = str(self.host.text())
        sftpUser = str(self.user.text())
        sftpPass = str(self.password.text())

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            ssh.connect(sftpURL, username=sftpUser, password=sftpPass, timeout=5)
            self.status.append("Connected")
            self.status.append(f"Connection with host {sftpURL} succesful.")

            ftp = ssh.open_sftp()
            files_etc = ftp.listdir()
            self.files.append(files_etc)

        except Exception as e:
            ssh.close()
            self.status.clear()
            self.status.append("Not connected")
            self.status.append(f'Error on host {sftpURL}: {e}.')

    def bt_disconnection(self):
        self.status.clear()
        self.status.append("Not connected")
        ssh.close()


app = QApplication(sys.argv)
window = UI()
app.exec_()