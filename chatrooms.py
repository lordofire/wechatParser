from util import *
import md5
import sqlite3

"""
Wechat ChatRoom class, containing most of the useful information of a wechat chatRoom
"""
class ChatRoom:
    def __init__(self, roomName, memberList, roomCreator, roomDataXML):
        self.roomName = roomName
        try:
            self.uNmd5 = md5.new(roomName).hexdigest()
        except UnicodeEncodeError:
            self.uNmd5 = md5.new(roomName.encode('utf-8')).hexdigest()
        self.memberList = memberList
        self.roomCreator = roomCreator
        self.roomDataXML = roomDataXML

    def __str__(self):
        membersList = ''
        for member in self.memberList:
            membersList += member + ", "

        return "ChatRoom " + self.roomName.encode('utf-8') + " with md5(" + self.uNmd5 +  "), memberList size is " + str(self.memberList.__len__()) + ", content:" + membersList + "roomCreator:" + self.roomCreator + ", roomDataXML:" + str(self.roomDataXML)

"""
collectChatRoomsMeta(): parse/collect the chatroom meta from WCDB_Contact.sqlite
"""
def collectChatRoomsMeta(weChatAccountFolder, Friends):
    ChatRooms = {}

    WCDB_ContactFile = weChatAccountFolder + "/DB/WCDB_Contact.sqlite"
    conn = sqlite3.connect(WCDB_ContactFile)
    c = conn.cursor()
    c.execute("SELECT userName, dbContactRemark, dbContactHeadImage, dbContactProfile, dbContactChatRoom FROM Friend where userName like '%@chatroom'")

    for chatroom in c.fetchall():
        (memberList, roomCreator, RoomDataXML) = parsedbContactChatRoom(chatroom[4], Friends)
        ChatRooms[chatroom[0]] = ChatRoom(chatroom[0], memberList, roomCreator, RoomDataXML)

    return ChatRooms
