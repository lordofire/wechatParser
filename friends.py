from util import *
import sqlite3
import hashlib

"""
Some global variables
"""
Friends = {}
ChatRooms = {}
m = hashlib.md5()

"""
Wechat Friend class, containing most of the useful information of a wechat friend
"""
class Friend:
    def __init__(self, userName, nickName, alias, contactRemark, MiniPhoto, HDPhoto, country, state, city, whatsup):
        self.userName = userName
        m.update(userName.encode('utf-8'))
        self.uNmd5 = m.hexdigest()
        self.nickName = nickName
        self.alias = alias
        self.contactRemark = contactRemark
        self.MiniPhoto = MiniPhoto
        self.HDPhoto = HDPhoto
        self.country = country
        self.state = state
        self.city = city
        self.whatsup = whatsup

    def __str__(self):
        return "Friend " + self.userName.encode('utf-8') + " with md5(" + self.uNmd5 +  "), nickName:" + self.nickName + ", alias:" + self.alias + ", contactRemark:" + self.contactRemark + ", MiniPhoto:" + self.MiniPhoto + ", HDPhoto:" + self.HDPhoto +", country:" + self.country + ", state:" + self.state + ", city:" + self.city + ", whatsup:" + self.whatsup

"""
Wechat ChatRoom class, containing most of the useful information of a wechat chatRoom
"""
class ChatRoom:
    def __init__(self, roomName, memberList, roomCreator, roomDataXML):
        self.roomName = roomName
        m.update(roomName.encode('utf-8'))
        self.uNmd5 = m.hexdigest()
        self.memberList = memberList
        self.roomCreator = roomCreator
        self.roomDataXML = roomDataXML

    def __str__(self):
        membersList = ''
        for member in self.memberList:
            membersList += member + ", "

        return "ChatRoom " + self.roomName.encode('utf-8') + " with md5(" + self.uNmd5 +  "), memberList size is " + str(self.memberList.__len__()) + ", content:" + membersList + "roomCreator:" + self.roomCreator + ", roomDataXML:" + str(self.roomDataXML)

"""
collectFriendsMeta(): parse/collect the friend meta from WCDB_Contact.sqlite
"""
def collectFriendsMeta():
    conn = sqlite3.connect("/Users/jiananwa/Documents/wechat_backup_jianan/8cd7299222b76fd76e53cc56e424a363/DB/WCDB_Contact.sqlite")
    c = conn.cursor()

    """ collect the Friends Meta First"""
    c.execute("SELECT userName, dbContactRemark, dbContactHeadImage, dbContactProfile, dbContactChatRoom FROM Friend where userName not like '%@chatroom'")
    
    for friend in c.fetchall():
        """ First parse the contact remark """
        remarkDat = parsedbContactRemark(friend[1])
        nickName = ''
        if 0x0a in remarkDat.keys():
            nickName = remarkDat[0x0a]
        alias = ''
        if 0x12 in remarkDat.keys():
            alias = remarkDat[0x12]
        contactRemark = ''
        if 0x1a in remarkDat.keys():
            contactRemark = remarkDat[0x1a]

        """ Next parse the contact head Image """
        (MiniPhoto, HDPhoto) = parsedbContactHeadImage(friend[2])

        """ Then parse the contact profile """
        profileDat = parsedbContactProfile(friend[3])
        country = ''
        if(profileDat.__len__() > 0):
            country = profileDat[0]
        state = ''
        if(profileDat.__len__() > 1):
            state = profileDat[1]
        city = ''
        if(profileDat.__len__() > 2):
            city = profileDat[2]
        whatsup = ''
        if(profileDat.__len__() > 3):
            whatsup = profileDat[3]

        Friends[friend[0]] = Friend(friend[0], nickName, alias, contactRemark, MiniPhoto, HDPhoto, country, state, city, whatsup)

    """ collect the Chatrooms Meta Then"""
    c.execute("SELECT userName, dbContactRemark, dbContactHeadImage, dbContactProfile, dbContactChatRoom FROM Friend where userName like '%@chatroom'")

    for chatroom in c.fetchall():
            (memberList, roomCreator, RoomDataXML) = parsedbContactChatRoom(chatroom[4], Friends)
            ChatRooms[chatroom[0]] = ChatRoom(chatroom[0], memberList, roomCreator, RoomDataXML)

def main():
    """ Initial the Friends Meta """
    collectFriendsMeta()

    print "==========================================="
    print "Friends List"
    print "==========================================="

    """ Iterate through the Friends list and print the content """
    for userName, friend in Friends.iteritems():
        print friend
        print ''

    print "==========================================="
    print "ChatRoom List"
    print "==========================================="

    """ Iterate through the ChatRooms list and print the content """
    for roomName, chatroom in ChatRooms.iteritems():
        print chatroom
        print ''

if __name__ == "__main__":
    main()
