import re
import hashlib

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
    miniMatchRule = re.compile("http://wx.qlogo.cn/mmhead/(.*)/132")
    miniMatch = miniMatchRule.search(str(binBuffer))
    if miniMatch:
        profilePhotoMini = miniMatch.group(0)
    HDMatchRule = re.compile("http://wx.qlogo.cn/mmhead/(.*)/0")
    HDMatch = HDMatchRule.search(str(binBuffer))
    if HDMatch:
        profilePhotoHD = HDMatch.group(0)
    return (profilePhotoMini, profilePhotoHD)

"""
parsedbContactChatRoom: input blob buffer for dbContactChatRoom in WCDB_Contact.sqlite
### There is some issue with the size calculation when the member list got pretty big,
### the size value is stored with two bytes instead of one in that case, and the values
### are not corresponding well. Use another method to work around this issue
format: chatroom member userName lists, and a XML payload for RoomData
output: a tuple of userName Lists, RoomCreator and XML payload data
"""
def parsedbContactChatRoom(binBuffer, Friends):
    binArray = bytearray(binBuffer)
    memberList = []
    memberCount = 0
    RoomCreator = ''
    RoomDataXML = ''

    """ The Chatromm is empty """
    if binArray[1] == 0:
        return (memberList, RoomCreator, RoomDataXML)

    """ Get the member contents """
    memberRule = re.compile('\n(.*)\x12')
    if memberRule.search(binArray):
        member = memberRule.search(str(binArray)).group()
        memberCount = str(member[2:-1]).count(';') + 1

    if memberCount == 1:
        memberList.append(str(member[2:-2]))
        RoomCreator = str(member[2:-2])
    else:
        """ Get the first member content """
        firstMemberRule = re.compile('\n[^;]+;')
        if firstMemberRule.search(binArray):
            firstMember = firstMemberRule.search(str(binArray)).group()
            if str(firstMember[2:-1]) in Friends:
                memberList.append(str(firstMember[2:-1]))
            else:
                memberList.append(str(firstMember[3:-1]))

        """ Get the second to final member content """
        secondToFinalMemberListRule = re.compile(';(.*)\x12')
        if secondToFinalMemberListRule.search(str(binArray)):
            secondToFinalMember = secondToFinalMemberListRule.search(str(binArray)).group()
            index = 1
            memberSize = 0
            while index < secondToFinalMember.__len__()-1:
                if secondToFinalMember[index] == ';':
                    memberList.append(str(secondToFinalMember[index-memberSize:index]))
                    memberSize = 0
                else:
                    memberSize += 1
                index += 1
            memberList.append(str(secondToFinalMember[index-memberSize:index]))

        """ Get the chatroom creator content """
        roomCreatorRule = re.compile('\x12(.*)\x18')
        if roomCreatorRule.search(binArray):
            roomCreator = roomCreatorRule.search(str(binArray)).group()
            if(roomCreator[1] == '\x12'):
                roomCreator = roomCreator[2:]
            else:
                roomCreator = roomCreator[1:]
            RoomCreatorSize = ord(roomCreator[0])
            RoomCreator = roomCreator[1:1+RoomCreatorSize]

    """ Do the validation on the memberList count """
    if len(memberList) != memberCount:
        print "there is something wrong here for " + RoomCreator + ": memberList count is " + str(len(memberList)) + " and memberCount is " + str(memberCount)

    """ Get the room xml data """
    roomDataXMLRule = re.compile("<RoomData>(.*)<\/RoomData>")
    if roomDataXMLRule.search(str(binArray)):
        RoomDataXML = roomDataXMLRule.search(str(binArray)).group()

    return (memberList, RoomCreator, RoomDataXML)
