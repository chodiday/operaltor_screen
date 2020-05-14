from enum import Enum

class Line():

    def __init__(self):
        self.__tokenList = []
        self.__insertion_style = "<span style=\" background-color: #FFFF00; color:#000000;\" >"
        self.__deletion_style = "<span style=\" background-color: #FFFF00; color:#000000;\" >"
        self.__replace_style = "<span style=\" background-color: #FFFF00; color:#000000;\" >"
        self.reset()

    def reset(self):
        self.__tokenList = []

    def add(self, token):
        self.__tokenList.append(token)

    def getTokenList(self):
        return self.__tokenList

    def getFormattedLine(self):
        line = ''
        for token in self.__tokenList:
            if token.error == Error.Insertion or  token.error == Error.Deletion or token.error ==  Error.Substitution :
                if token.error == Error.Insertion:
                 line += self.__insertion_style
                elif token.error == Error.Deletion:
                    line += self.__deletion_style
                else:
                    line += self.__replace_style
                line += token.word
                line += "</span>"
            else:
                line += token.word
        #line += "<br></br>"
        return line

class Error(Enum):
    NoError = 0
    Insertion = 1
    Deletion = 2
    Substitution = 3
    Temp = 99
    Default = -1

class Token():

    def __init__(self):
        self.error = Error.Default
        self.word = ''
        self.reading = ''
        self.index = 0
        self.partsOfSpeech = ''
        self.sentenceIndex = 0
        self.errorListChar = None  # List object
        self.substitutionMatch = None  # Token object
        self.charLen = 0  # Length of the reading.
        self.levWord = ''  # Word/Reading used in actual Levenshtein editops.

class Text():

    def __init__(self):
        self.__lineList = []
        self.reset()

    def reset(self):
        self.__lineList = []

    def add(self, line ):
        self.__lineList.append(line)

    def update(self, filteredTokens):
        for token_index in range(len(filteredTokens)):
           for line_index in range(len(self.__lineList)):
               for inner_token in range(len(self.__lineList[line_index].getTokenList())):
                   if self.__lineList[line_index].getTokenList()[inner_token].index != filteredTokens[token_index].index:
                       continue
                   else:
                      self.__lineList[line_index].getTokenList()[inner_token].error = filteredTokens[token_index].error

    def getTokenizeText(self):
        return self.__lineList

    def getFormattedText(self):

        texts = ''
        index = 1
        size = len(self.__lineList)
        for line in self.__lineList:
            texts = texts + Text.formatLineText(line.getFormattedLine(), index, size, 4)
            index = index + 1
        return texts

    @staticmethod
    def formatLineText(data, number, size , offset):
        newData = "<span style=\" background-color: #E0E0E0; color:#6A6A6A;\">"

        nbsp = '&nbsp;'
        for i in range( len(str(size)) -len(str(number))):
            newData = newData +'0'

        newData = newData + str(number)

        for x in range(offset):
            newData = newData + nbsp

        newData = newData + '</span>'
        newData = newData + data
        newData = newData + '<br></br>'

        return newData

