import requests
# from requests.packages.urllib3.exceptions import InsecureRequestWarning
# requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import urllib3
urllib3.disable_warnings()

coreURL= "https://fireflies-ut4ac7mf.cywar.xyz:50310/index.php?FIREFLIES="

is_on=True
nextMethod = "GET"

def checkMethod(text):
    global nextMethod     
    isGET = text.find("GET")
    isPOST = text.find("POST")
    if isGET > 0:
        print ("GET is in the house")
        nextMethod = "GET"
        return "GET"
    elif isPOST > 0:
        print ("POST is in the house")
        nextMethod = "POST"
        return "POST"
    else:
        print ("FLAGGGG is in the house")
        return "FLAG"

def extractNewNumber(Text, methodType):

    if (methodType == "GET") :
        string=Text[768:773]

    elif (methodType == "POST"):
        string=Text[769:774]
    else:
        print ("FLAG\n\n\n\n\n\n")
        print(Text)
        exit()
    return string

def getPostNewNumber(currNum):

    postURL="https://fireflies-ut4ac7mf.cywar.xyz:50310/index.php"
    data = {'FIREFLIES' : currNum }
    newPost = requests.post(postURL, data, verify=False)
    string=newPost.text[769:774]
    print (string)
    return str(int(string))


def sendGET(currNum):
    print("\n\n Sending GET request ")
    newGET = requests.get(coreURL+currNum,  verify=False)
    responseString = newGET.text
    
    methodType = checkMethod(responseString)
    print("next method type is : "+ methodType)
    
    newNumber = extractNewNumber(responseString, methodType)
    print ("next new number is : " + newNumber)

    return str(int(newNumber))

def sendPOST(currNum):
    print("\n\n Sending POST request ")
    postURL="https://fireflies-ut4ac7mf.cywar.xyz:50310/index.php"
    data = {'FIREFLIES' : currNum }
    newPost = requests.post(postURL, data, verify=False)
    responseString = newPost.text
    methodType = checkMethod(responseString)
    print("next method type is : "+ methodType)
    
    newNumber = extractNewNumber(responseString, methodType)
    print ("next new number is : " + newNumber)

    return str(int(newNumber))

def main():
    
    currNum="64969"
    while is_on:
        # currNum=getNewNumber(currNum)
        if nextMethod == "GET":
           currNum= sendGET(currNum)

        else:
            currNum= sendPOST(currNum)



if __name__ == "__main__":
    main()
