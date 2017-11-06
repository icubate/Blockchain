# BlockChainClient1.py

from threading import Thread
import socket, time
import serial
import os


VERBOSE = True
# micro-room incubator
IP_ADDRESS = "172.27.70.148"
IP_PORT = 22000

serialport = serial.Serial("/dev/tty0")
serialport.write("serial port initialized")

#Patient Record
LName = " "
FName = " "
MName = " " 
DOB = " " 
Physician = " "
PCode = " "
Illness = " "
Diagnosis = " "
TPlan = " "
Patient_ID = "5678 "
Physician_ID = "1234 "
Hospital_ID = "99 "



def debug(text):
    if VERBOSE:
        print "Debug:---", text

# ------------------------- class Receiver ---------------------------
class Receiver(Thread):
    def run(self):
        debug("Receiver thread started")
        while True:
            try:
                rxData = self.readServerData()
            except:
                debug("Exception in Receiver.run()")
                isReceiverRunning = False
                closeConnection()
                break
        debug("Receiver thread terminated")

    def readServerData(self):
        debug("Calling readResponse")
        bufSize = 4096
        data = ""
        while data[-1:] != "\0": # reply with end-of-message indicator
            try:
                blk = sock.recv(bufSize)
                if blk != None:
                    debug("Received data block from server, len: " + \
                        str(len(blk)))
                else:
                    debug("sock.recv() returned with None")
            except:
                raise Exception("Exception from blocking sock.recv()")
            data += blk
        print "Data received:", data
# ------------------------ End of Receiver ---------------------

def startReceiver():
    debug("Starting Receiver thread")
    receiver = Receiver()
    receiver.start()

def sendCommand(cmd):
    debug("sendCommand() with cmd = " + cmd)
    try:
        # append \0 as end-of-message indicator
        sock.sendall(cmd + "\0")
    except:
        debug("Exception in sendCommand()")
        closeConnection()

def closeConnection():
    global isConnected
    debug("Closing socket")
    sock.close()
    isConnected = False

def connect():
    global sock
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    debug("Connecting...")
    try:
        sock.connect((IP_ADDRESS, IP_PORT))
    except:
        debug("Connection failed.")
        return False
    startReceiver()
    return True

def menu():
    os.system('clear')
    Date = time.strftime("%x")
    Time = time.strftime("%X")
 
    print(" ")
    print(" ")
    print("============================================================================================")
    print("--------------------------------  PATIENT RECORDS ------------------------------------------")
    print("------------------------------- Huntsville Hospital ----------------------------------------")
    print(" ")
    print(" ")   
    print(Date)
    print(Time)
    print(" ")
    print(" ")
    print('Patient Last Name: ' + LName)
    print('Patient First Name: ' + FName)
    print("Patient Middle Initial: " + MName)
    print("Patient Date-Of-Birth: " + DOB)
    print(" ")
    print("Attending Physician: " + Physician)
    print("Physician Code: " + PCode)
    print(" ")
    print(" ")
    print("Illness: " + Illness)
    print("Diagnosis: " + Diagnosis)
    print("Treatment Plan: " + TPlan)
    print(" ")
#    key = str(raw_input("Press key to continue... "))
    print(" ")
    print("=============================================================================================")
    print("==================================  End Of Record  ==========================================")
    print(" ")
    print(" ")

def accession():
    os.system('clear')
    global LName,FName,MName,DOB,Physician,PCode,Illness,Diagnosis,TPlan 

    print(" ")
    print(" ")
    print("=============================  Patient Accessioning Screen  =================================")
    print("=============================================================================================")
    print(" ")
    print(" ")  
    LName = str(raw_input("Enter Patient Last Name: "))
    FName = str(raw_input("Enter Patient First Name: "))
    MName = str(raw_input("Enter Patient Middle Name: "))
    DOB = str(raw_input("Enter Patient Date of birth: "))
    Physician = str(raw_input("Enter Physician name: "))
    PCode = str(raw_input("Enter Physicians Code: "))
    Illness = str(raw_input("Enter description of patient illness: "))
    Diagnosis = str(raw_input("Enter Patient diagnosis: "))
    TPlan = str(raw_input("Enter prescribed treatment plan: "))

    print(" ")
    print(" ")
    print("===================================  Record Complete  ======================================")
    print("============================================================================================")
    print(" ")
    print(" ")

def validate():
    os.system('clear')
    global Physician_ID, Patient_ID, Hospital_ID

    print("Physician_ID:  " + Physician_ID)
    print("Patient_ID: " + Patient_ID)
    if(Physician_ID == '000916461') and (Patient_ID == '99'):
        return True
    else:
        return False       
       
def submit_record():
    os.system('clear')
    DataPkg = Physician_ID + Patient_ID + Hospital_ID + FName + MName + LName + DOB
    print("Submitting Record...")
    print("DataPkg:" + DataPkg)
    sendCommand("Record: " + DataPkg)
    

def retrieve_record():
    os.system('clear')
    print("Retrieving records...")
    time.sleep(4)
    menu()


def login_screen():
    os.system('clear')
    global Physician_ID, Patient_ID, Hospital_ID
    
    print(" ")
    print(" ")
    print("============================================================================================")
    print("--------------------------------  PATIENT RECORDS ------------------------------------------")
    print("------------------------------- Huntsville Hospital ----------------------------------------")
    print(" ")
    print(" ")   
    Patient_ID = str(raw_input("Enter Patient Biometric ID: "))
    Hospital_ID = str(raw_input("Enter Hospital/Clinic ID: "))
    Physician_ID = str(raw_input("Enter Physician ID: "))
    
    if validate():
        os.system('clear')
        print("============================================================================================")
        print("--------------------------------  PATIENT RECORDS ------------------------------------------")
        print("------------------------------- Huntsville Hospital ----------------------------------------")
        print(" ")
        print(" ")   
        print("Option 1: Enter Patient information")
        print("Option 2: Submit Record to Archive")
        print("Option 3: Retrieve Records from Archive")
        print(" ")
        print(" ")
        Option = str(raw_input("Select Option from list: "))
        if(Option == "1"):
            accession()
        elif(Option == "2"):
            submit_record()
        elif(Option == "3"):
            retrieve_record()
        else:
            print("Invalid Option!")
            time.sleep(3)
            login_screen()
    else:
        print("Invalid ID Code. Permission Denied!")
        time.sleep(1)
        login_screen()


sock = None
isConnected = False

if connect():
    isConnected = True
    print "Connection established"
    time.sleep(1)
    while isConnected:
        print "Begin Menu.."
	os.system('clear')
	login_screen()    	
        sendCommand("Go to the BlockChain!")
        time.sleep(5)
else:
    print "Connection to %s:%d failed" % (IP_ADDRESS, IP_PORT)
print "done"    

