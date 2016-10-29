import sys
import os
import re
import time
from friends import *
from chatrooms import *

def main():
    if len(sys.argv) != 2 or not os.path.isdir(sys.argv[1]) or not os.path.exists(sys.argv[1]):
        print "only one input arg should be wechat folder location"
        return

    weChatFolder = sys.argv[1]
    weChatAccounts = []
    """ acquire the accounts inside the passed in wechat folder """
    for filename in os.listdir(weChatFolder):
        if len(filename) == 32 and filename != "00000000000000000000000000000000":
            weChatAccounts.append(filename)

    """ Iterate through all the accounts and use their db to recover metas """
    for account in weChatAccounts:
        weChatAccountFolder = weChatFolder + "/" + account
        print weChatAccountFolder
        """ Initial Meta """
        Friends = collectFriendsMeta(weChatAccountFolder)
        ChatRooms = collectChatRoomsMeta(weChatAccountFolder, Friends)

        print "==========================================="
        print "Friends List"
        print "==========================================="

        """ Iterate through the Friends list and print the content """
        for userName, friend in Friends.iteritems():
            chatRecord = "Chat_" + friend.uNmd5
            MMFile = weChatAccountFolder + "/DB/MM.sqlite"
            conn = sqlite3.connect(MMFile)
            c = conn.cursor()
            try:
                c.execute("select CreateTime, Message, Status from " + str(chatRecord))
            except sqlite3.OperationalError:
                print "This db " + str(chatRecord) + " is not found"
                continue

            print "This db " + str(chatRecord) + " for " + userName + " is found"
            for chatEntry in c.fetchall():
                timestamp = chatEntry[0]
                content = chatEntry[1]
                if chatEntry[2] == 2:
                    print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp)) + ", me: " + content
                elif chatEntry[2] == 4:
                    print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp)) + ", " + userName + ": " + content
            print ''

        print "==========================================="
        print "ChatRoom List"
        print "==========================================="

        """ Iterate through the ChatRooms list and print the content """
#        for roomName, chatroom in ChatRooms.iteritems():
#            print chatroom
#            print ''


if __name__ == "__main__":
    main()
