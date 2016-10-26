import sys
import os
import re
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
