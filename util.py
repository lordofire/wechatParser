import re

"""
parsedbContactRemark: input blob buffer for dbContactRemark in WCDB_Contact.sqlite
format: byte size key + size + value
output: a map of key/value pairs
"""
def parsedbContactRemark(binBuffer):
    binArray = bytearray(binBuffer)
    contactRemarkDict = {}
    index = 0
    while index < binArray.__len__():
        key = binArray[index]
        size = binArray[index+1]
        index += 2
        val = ''
        if size != 0:
            val = str(binArray[index : index+size])
        contactRemarkDict[key] = val
        index += size
    return contactRemarkDict

"""
parsedbContactRemark: input blob buffer for dbContactProfile in WCDB_Contact.sqlite
format: size + value
output: a array values
"""
def parsedbContactProfile(binBuffer):
    binArray = bytearray(binBuffer)
    contactProfileArray = []
    index = 3
    while index < binArray.__len__():
        size = binArray[index]
        index += 1
        contactProfileArray.append(str(binArray[index:index+size]))
        index += size+1
    return contactProfileArray

"""
parsedbContactHeadImage: input blob buffer for dbContactHeadImage in WCDB_Contact.sqlite
format: friend head profile photo miniature & HD one
output: a tuple of miniPhoto and a HDPhoto
"""
def parsedbContactHeadImage(binBuffer):
    profilePhotoMini = ''
    profilePhotoHD = ''
    miniMatchRule = re.compile("http://wx.qlogo.cn/mmhead/([\w]+)/132")
    miniMatch = miniMatchRule.search(str(binBuffer))
    if miniMatch:
        profilePhotoMini = miniMatch.group(0)
    HDMatchRule = re.compile("http://wx.qlogo.cn/mmhead/([\w]+)/0")
    HDMatch = HDMatchRule.search(str(binBuffer))
    if HDMatch:
        profilePhotoHD = HDMatch.group(0)
    return (profilePhotoMini, profilePhotoHD)

"""
parsedbContactChatRoom: input blob buffer for dbContactChatRoom in WCDB_Contact.sqlite
### There is some issue with the size calculation when the member list got pretty big,
### the size value is stored with two bytes instead of one in that case, and the values
### are not corresponding well.
format: chatroom member userName lists, and a XML payload for RoomData
output: a tuple of userName Lists, RoomCreator and XML payload data
"""
def parsedbContactChatRoom(binBuffer):
    binArray = bytearray(binBuffer)
    memberList = []
    RoomCreator = ''
    RoomDataXML = ''

    """ Get the member list """
    memberListSize = binArray[1]
    memberListBin = binArray[2:2+memberListSize]
    index = 0
    memberSize = 0

    while index < memberListSize:
        if memberListBin[index] == ord(';'):
            memberList.append(str(memberListBin[index-memberSize:index]))
            memberSize = 0
        else:
            memberSize += 1
        index += 1

    """ Get the chatroom creator string size/content """
    RoomCreatorSize = binArray[3+memberListSize]
    RoomCreator = str(binArray[4+memberListSize:4+memberListSize+RoomCreatorSize])

    """ Get the room xml data """
    roomDataXMLRule = re.compile("<RoomData>(.*?)<\/RoomData>")
    roomDataXMLMatch = roomDataXMLRule.search(str(binBuffer))
    if roomDataXMLMatch:
        RoomDataXML = roomDataXMLMatch.group(0)

    return (memberList, RoomCreator, RoomDataXML)
