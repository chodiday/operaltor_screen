from janome.tokenizer import Tokenizer

class JanomeTokenizer:

    def __init__(self):
        self.debug = False
        self.custom_words_filter = []
        self.part_of_speech_filter = []

    def setStopWords(self, list):
        self.custom_words_filter = list

    def setPartsOfSpeech(self, list):
        self.part_of_speech_filter = list

    def rawTokenize(self, string_list):
        all_token_list = []
        t = Tokenizer()
        #for string in file_string_list:
        for token in t.tokenize(string_list):
            #print(f'Token: {token}')
            all_token_list.append(token)

       #print("All Token List: ", all_token_list)
        return all_token_list

    def tokenize(self, token):
        all_token_list = []

        stop_word = False
        if self.debug == True:
            print(f'token.partsOfSpeech: {token.partsOfSpeech}')
            print(f'token.word: {token.word}')
            print(f'part_of_speech_filter: {self.part_of_speech_filter}')
            print("custom_words_filter:", self.custom_words_filter)
        for pos in token.partsOfSpeech:
            if pos in self.part_of_speech_filter:
                stop_word = True
                break
        else:
            remove_char = ['。', '、']  # , '、'
            newCustomwordsFilter = [elem for elem in self.custom_words_filter if elem not in remove_char]
            for word in newCustomwordsFilter:
                if word == token.word:
                    stop_word = True
                    break

        if self.debug == True:
            print(f'stop_word: {stop_word}')
            print('')
        return stop_word