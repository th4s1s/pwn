from pwn import *
def convertASCII_to_Hex(value):
      res = ""
      for i in value:
            res += hex(ord(i))[2:]
      return res      

def changeEndian(value):
      length = len(value)
      res = "0x"
      for i in range(length-1, 0, -2):
            res += value[i-1]+ value[i]
      return res      

def generateString(value):
      return int(changeEndian(convertASCII_to_Hex(value)), 16)

print(p64(generateString("/bin/sh")))
print(p64(0x68732F6E69622F))