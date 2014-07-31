
import os
import sys
import string

class cleaner:
    def __init__(self,fileName="test"):
        self.fileName = fileName

    def parseFile(self):
        end = 0
        index = 0
        lineBuffer = ""

        fd = open(self.fileName,'r')
        buf = fd.readlines()
        fd.close()
        
        size = len(buf)

        while index < size:
            if (buf[index] >= ' ' and buf[index] <= '~') \
            or (buf[index] == '\n') or (buf[index] == '\t') \
            or (buf[index] == '\r'):
                lineBuffer += buf[index]
            
            index += 1


        newFileName = ""
        newFileName = self.fileName + ".ty"
        print newFileName

        fd = open(newFileName, 'w')
        fd.write(lineBuffer)
        fd.close()
        

if __name__ == "__main__":
    
    if len(sys.argv) == 2:
        c = cleaner(sys.argv[1])
    else:
        c = cleaner()

    c.parseFile()
