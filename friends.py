from util import *
import md5
import sqlite3

"""
Wechat Friend class, containing most of the useful information of a wechat friend
"""
class Friend:
    def __init__(self, userName, nickName, alias, contactRemark, MiniPhoto, HDPhoto, country, state, city, whatsup):
        self.userName = userName
        try:
            self.uNmd5 = md5.new(userName).hexdigest()
        except UnicodeEncodeError:
            self.uNmd5 = md5.new(userName.encode('utf-8')).hexdigest()
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
collectFriendsMeta(): parse/collect the friend meta from WCDB_Contact.sqlite
"""
def collectFriendsMeta(weChatAccountFolder):
    Friends = {}

    WCDB_ContactFile = weChatAccountFolder + "/DB/WCDB_Contact.sqlite"
    conn = sqlite3.connect(WCDB_ContactFile)
    c = conn.cursor()
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

    return Friends
