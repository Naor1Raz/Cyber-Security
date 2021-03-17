import time


def GGGGotate(lol):
    bit = lol << 1
    movebit = bit & 255
    if (lol > 127 ):
        movebit = movebit | 1
    return (movebit)
def encryptor(tempValue):
    # value = input("Enter your value: ")
    value = tempValue
    ListMoveBit = []
    Index_Move_bit = 1
    Index_Value = 0
    ORD_value = []
    ORD_key = []
    Under_10 = []
    Index_star = 0
    Final_encrypted = ""
    Passs = []
    List_values_back = []
    Uncrypt = []
    for i in value:
        ORD_value.append(ord(i))
    a = ord("a")
    ORD_key.append(a)
    lol = int(ORD_key[0]) ^ int(ORD_value[0])
    ListMoveBit.append(GGGGotate(lol))
    for chars in ORD_value:
        if Index_Value == 0:
            Index_Value += 1
            pass
        else:
            lol = int(ListMoveBit[Index_Value-1]) ^ int(chars)
            ListMoveBit.append(GGGGotate(lol))
            Index_Value += 1
    for i in ListMoveBit:
        Under_10.append("0")
    for i in ListMoveBit:
        if (i < 9):
            Under_10[Index_star] = "1"
        Index_star += 1
    for i in ListMoveBit:
        x = hex(i)
        val = x[2:]
        if(i > 9) and (i < 16):
            Final_encrypted = Final_encrypted + "0" + val
        else:
            if (i<10):
                Final_encrypted = Final_encrypted +"0"+val
            else:
                Final_encrypted = Final_encrypted + val
    # print("\nThe encrypted message is:")
    return Final_encrypted


def main():
    """ The encryptor is up above simulating another encrypt script"""

    # messageToDycrype = "2e84cb5f6c34b0a38fcdf99749"

    messageToDycrype=input("Enter message to decrypt --> ")
    inputList= ""
    indexStart = 0

    print("======================================================================")
    print("|   Welcome To The Decryptor")
    print("|   Message To Decrypt: {0} ".format(messageToDycrype))
    print("====================================================================")
    time.sleep(2)

    for indexEnd in range (1, len(messageToDycrype)+1):
        print("Testing for index [0:{0}]".format(indexEnd))

        for asciiIndex in range(33, 127):
            inputValueChar = chr(asciiIndex)
            encryptedResult = encryptor(inputList+inputValueChar)
            # print(inputList+inputValueChar)

            if encryptedResult == messageToDycrype[indexStart:indexEnd]:
                print("Found char for {0} , The key is: '{1}'".format(encryptedResult, inputValueChar))
                inputList += inputValueChar
                print("Moving forward")
                break
        print("---------------------------------------------------------")
    print("Final Decrypted Result: ", inputList)


if __name__ == '__main__':
    main()

