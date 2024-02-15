import time
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtCore import pyqtSignal, QObject
import socket
import pathlib
import json
from typing import Dict
import sys
import mainpage  # Importing mainpage module
import threading


# Constants for socket communication
BUFFER_SIZE = 1024
SERVER_PORT = 5555
SERVER_PORT2 = 5556

client_details = {}
online_users: Dict[str,str] = {}

# Define a signal for updating online friends
class OnlineFriendsSignal(QObject):
    online_friends_updated = pyqtSignal(dict)

# Create an instance of the signal
online_friends_signal = OnlineFriendsSignal()

parent_directory_src = str(pathlib.Path(__file__).parent.resolve().parents[1])
sys.path.append(parent_directory_src)
sys.path.append(parent_directory_src+"/server")

def save_username_and_server_ip(username: str, server_ip: str):
    # Save the username and server IP for later use
    client_details["name"] = username
    client_details["server_ip"] = server_ip

def establish_connection():
    try:
        your_name = client_details["name"]
        server_ip = client_details["server_ip"]

        # Client Socket for general communication with the server
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Connecting to server...")
        client.connect((server_ip, SERVER_PORT))
        message = "I am " + your_name + " for online"
        client.send(message.ljust(BUFFER_SIZE, '\x00').encode('utf-8'))

        # Client socket for receiving who is online from the server
        client2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Connecting to server (2nd socket)...")
        client2.connect((server_ip, SERVER_PORT2))
        message = "I am " + your_name + " for online"
        client2.send(message.ljust(BUFFER_SIZE, '\x00').encode('utf-8'))

        return client, client2

    except Exception as e:
        print("Error in establish_connection function in basicDetails.py:", e)
        return None, None
    
# Heartbeat function to maintain connection and get online friends
def heartbeat(client2: socket.socket):
    global online_users

    try:
        print("Heartbeat function started.")
        while True:
            message = "I am " + client_details["name"] + " for online"
            client2.send(message.ljust(BUFFER_SIZE, '\x00').encode('utf-8'))

            print("Sent message:", message)

            serialized_data = client2.recv(BUFFER_SIZE).decode().rstrip('\x00')
            print("Received data:", serialized_data)

            online_friends = json.loads(serialized_data)

            print("Online Friends:", online_friends)

            # Emit signal to update online friends
            online_friends_signal.online_friends_updated.emit(online_friends)

            # Perform heartbeat at a rate of 10 seconds
            time.sleep(10.0)

    except Exception as e:
        print("Error in heartbeat function:", e)

class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(484, 403)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(100, 230, 291, 28))
        self.pushButton_2.setObjectName("pushButton_2")

        # Connect the button click to the appropriate function
        self.pushButton_2.clicked.connect(self.basicDetails_On_Continue)

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(100, 160, 55, 16))
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(100, 180, 291, 28))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_3.setGeometry(QtCore.QRect(100, 110, 291, 28))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(100, 90, 91, 16))
        self.label_3.setObjectName("label_3")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Basic Details"))
        self.pushButton_2.setText(_translate("MainWindow", "Continue"))
        self.label.setText(_translate("MainWindow", "Server IP"))
        self.label_3.setText(_translate("MainWindow", "Username"))


    def basicDetails_On_Continue(self, MainWindow):
        print(self.lineEdit.text()) #ToDo: To store username and move to next 
        server_ip = self.lineEdit.text()

        print(self.lineEdit_3.text()) #ToDo: To store username and move to next 
        username = self.lineEdit_3.text()

        # Store the username and server IP for later use
        save_username_and_server_ip(username, server_ip)

        # Establish the connection with the server
        client, client2 = establish_connection()
        if client and client2:
            print("Connection established successfully")
            heart_beat = threading.Thread(target=heartbeat, args=(client2,), daemon=True)
            heart_beat.start()
        else:
            print("Failed to establish connection")

        self.window = QtWidgets.QMainWindow()
        self.ui = mainpage.Ui_MainPageWindow()
        self.ui.setupUi(self.window)
        self.window.show()
        self.MainWindow.close()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    ui.MainWindow = MainWindow
    sys.exit(app.exec_())
