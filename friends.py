from util import *
import sqlite3
import hashlib

"""
Some global variables
"""
Friends = {}
m = hashlib.md5()

"""
Wechat Friend class, containing most of the useful information of a wechat friend
"""
class Friend:
    def __init__(self, userName, nickName, alias, contactRemark, country, state, city, whatsup):
        self.userName = userName
        m.update(userName.encode('utf-8'))
        self.uNmd5 = m.hexdigest()
        self.nickName = nickName
        self.alias = alias
        self.contactRemark = contactRemark
        self.country = country
        self.state = state
        self.city = city
        self.whatsup = whatsup

    def __str__(self):
        return "Friend " + self.userName.encode('utf-8') + " with md5(" + self.uNmd5 +  "), nickName:" + self.nickName + ", alias:" + self.alias + ", contactRemark:" + self.contactRemark + ", country:" + self.country + ", state:" + self.state + ", city:" + self.city + ", whatsup:" + self.whatsup

"""
collectFriendsMeta(): parse/collect the friend meta from WCDB_Contact.sqlite
"""
def collectFriendsMeta():
    conn = sqlite3.connect("/Users/jiananwa/Documents/wechat_backup_jianan/8cd7299222b76fd76e53cc56e424a363/DB/WCDB_Contact.sqlite")
    c = conn.cursor()
    c.execute("SELECT userName, dbContactRemark, dbContactProfile FROM Friend")
    
    for friend in c.fetchall():
        print friend[0]
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

        """ Then parse the contact profile """
        profileDat = parsedbContactProfile(friend[2])
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
        
        Friends[friend[0]] = Friend(friend[0], nickName, alias, contactRemark, country, state, city, whatsup)

def main():
    """ Initial the Friends Meta """
    collectFriendsMeta()

    """ Iterate through the Friends list and print the content """
    for userName, friend in Friends.iteritems():
        print friend

if __name__ == "__main__":
    main()
