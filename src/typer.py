
import os
import sys
import string
import curses
import time


lineNumbers = 60 
centerLine = lineNumbers/2

#Number of lines to skip when pressing tab
tab_line_numbers = 5

class readBuffer:
    def __init__(self,filename):
        self.filename = filename
        self.currentLine = 0
        self.lineCount = 0
        self.EOF = 0
        self.lines = list()

    def parseFile(self):
        end = 0
        index = 0
        lineBuffer = ""

        fd = open(self.filename,'r')
        buf = fd.readlines()
        fd.close()
        
        size = len(buf)

        while index < size:
            lineBuffer += buf[index]
            lineBuffer = lineBuffer.strip('\n\r')
            lineBuffer += ' '
            lineSize = len(lineBuffer)
            
            lineIndex = 0
            while lineIndex < 79 and lineIndex < lineSize:
                if lineBuffer[lineIndex] == ' ':
                    lineIndex += 1
                    end = lineIndex
                lineIndex += 1

            self.lines.append(lineBuffer[:end])
            self.lineCount += 1

            index += 1
            lineBuffer = lineBuffer[end:]

        lineSize = len(lineBuffer)
        
        while lineSize:
            lineIndex = 0
            while lineIndex < 79 and lineIndex < lineSize:
                if lineBuffer[lineIndex] == ' ':
                    lineIndex += 1
                    end = lineIndex
                lineIndex += 1

            self.lines.append(lineBuffer[:end])
            self.lineCount += 1

            lineBuffer = lineBuffer[end:]
            lineSize = len(lineBuffer)

    def getLine(self,index=None):
        if index==None:
            index = self.currentLine

        if index < self.lineCount:
            self.currentLine += 1
            return self.lines[index]
        else:
            self.EOF = 1
            return ""

class typer:
    def __init__(self,fileName="test"):
        self.display = []

        for i in range(0, lineNumbers):
            self.display.append("")

        self.center = self.display[centerLine]

        self.numberOfLines = 0
        self.lineCount = 0
        self.wordCount = 0
        self.wordPerMin = 0
        self.errorCount = 0
        self.lastWordCount = 0
        self.lastTime = time.time()

        self.fileName = fileName

        self.screen = curses.initscr()
        curses.start_color()
        curses.noecho()

    def __del__(self):
        curses.endwin()

    def newLine(self,buf):

        for i in range(0, lineNumbers-1):
            self.display[i] = self.display[i+1]
            
        self.display[lineNumbers-1] = buf.getLine()

    def printBlock(self):

        self.screen.erase()
        for i in range(0, lineNumbers):
            self.screen.addstr(i,0,self.display[i])
        
        currentTime = time.time()
        if ((currentTime - self.lastTime) > 60):
            self.wordPerMin = (self.wordCount - self.lastWordCount)
            self.lastWordCount = self.wordCount
            self.lastTime = currentTime

        percentageDone = (float(self.lineCount) / self.numberOfLines) * 100

        self.screen.addstr(i+2,0,'Word Count: {0}'.format(self.wordCount))
        self.screen.addstr(i+3,0,'Error Count: {0}'.format(self.errorCount))
        self.screen.addstr(i+4,0,'Words Per Min: {0}'.format(self.wordPerMin))
        self.screen.addstr(i+5,0,'Percentage done: {0}%'.format(percentageDone))

    def getChar(self):
        wordStart = 0
        currentPos = 0
        self.screen.move(centerLine,currentPos)
        self.center = self.display[centerLine]

        while 1:
            if currentPos >= len(self.center):
                currentPos = 0
                return 1

            c = self.screen.getch()

            if c == ord(self.center[currentPos]):
                currentPos += 1
                self.screen.move(centerLine,currentPos)
                
                if c == ord(' '):
                    wordStart = currentPos
                    self.wordCount += 1
            elif c == ord('\n'):
                return 1
            elif c == ord('\t'):
                return tab_line_numbers
            else:
                self.errorCount += 1
                currentPos = wordStart
                self.screen.move(centerLine,currentPos)

    def play(self):
        
        buf = readBuffer(self.fileName)
        buf.parseFile()

        self.numberOfLines = buf.lineCount

        for i in range(centerLine, lineNumbers-1):
            self.display[i] = buf.getLine()

        while 1:
            self.printBlock()
            newLines = self.getChar()
            self.lineCount += newLines
            for i in range(0, newLines):
                self.newLine(buf)
            if buf.EOF and self.center == "":
                self.screen.addstr(3,0,"Finished")
                temp = "Word Count: "
                temp += str(self.wordCount)
                self.screen.addstr(4,0,temp)
                temp = "Error Count: "
                temp += str(self.errorCount)
                self.screen.addstr(5,0,temp)
                break

        c = self.screen.getch()

if __name__ == "__main__":
    
    if len(sys.argv) == 2:
        c = typer(sys.argv[1])
    else:
        c = typer()

    c.play()
    
    
