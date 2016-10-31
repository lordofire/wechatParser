import sqlite3
import time
from friends import *

"""
Wechat chat entry class, the basic message entry for each chatHistory
"""
class chatEntry:
    def __init__(self, userName, createtime, message, status):
        self.userName = userName
        self.createtime = createtime
        self.message = message
        self.status = status

    def __str__(self):
        if self.status == 2:
            return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.createtime)) + ", me: " + self.message.encode('utf-8')
        else:
            return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.createtime)) + ", " + self.userName.encode('utf-8') + ": " + self.message.encode('utf-8')

"""
collectChatHistory(): parse/collect the chat history from MM.sqlite
"""
def collectChatHistory(weChatAccountFolder, friend):
    chatRecord = "Chat_" + friend.uNmd5
    MMFile = weChatAccountFolder + "/DB/MM.sqlite"
    conn = sqlite3.connect(MMFile)
    c = conn.cursor()
    chatEntries = []

    try:
        c.execute("select CreateTime, Message, Status from " + str(chatRecord))
    except sqlite3.OperationalError:
        print "Chat history for " + str(friend.userName) + " is not found"
        return chatEntries

    for entry in c.fetchall():
        chatEntries.append(chatEntry(friend.userName, entry[0], entry[1], entry[2]))

    return chatEntries
