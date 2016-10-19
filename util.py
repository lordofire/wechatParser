#!/usr/bin/python

"""
parsedbContactRemark: input blob buffer for dbContactRemark in WCDB_Contact.sqlite
format: byte size key + size + value
output: a map of key/value pairs
"""
def parsedbContactRemark( binBuffer ):
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
    return friendBinDict

"""
parsedbContactRemark: input blob buffer for dbContactProfile in WCDB_Contact.sqlite
format: size + value
output: a array values
"""
def parsedbContactProfile( binBuffer ):
    binArray = bytearray(binBuffer)
    contactProfileArray = []
    index = 3
    while index < binArray.__len__():
        size = binArray[index]
        index += 1
        contactProfileArray.append(str(binArray[index:index+size]))
        index += size+1
    return contactProfileArray
