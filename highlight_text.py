import os
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, json
)

import Levenshtein
from Tokenizer import JanomeTokenizer
import threading
import traceback

import TextFormatter as TextFormatter


tokenizer_lock = threading.Lock()
debug = True
__custom_words_filter = []
__part_of_speech_filter = []

bp = Blueprint('highlight_text', __name__)

@bp.route('/home')
def home():
    highlight_keywords = ["三菱", "トラフィック", "マツダ", "衝突", "道路"]
    convoStringList = [
		{'speaker': "クライアント", 'sentence_line': "こんにちは道路、これは緊急ホットラインですか？第11地区カムニン道路沿いの 三菱とマツダ3両が 衝突して渋 滞しているとのことです。"},
        {'speaker': "オペレーター", 'sentence_line': "こんにちは、この緊急ヘルプデスク、あなたの場所を教えてください。"},
        {'speaker': "クライアント", 'sentence_line': "私は三菱自動車の道路を走っていますこれは緊急事態です助けてください。"},
        {'speaker': "オペレーター", 'sentence_line': "奥さん、トヨタの車に乗っていますか？。"}]
    modified_convo = []
    
    try:
        speech_text_unfiltered = TextFormatter.Text()
        index = 0
        lineIndex = 0
        for ln in convoStringList:
            if (' ' in ln['sentence_line']) == True:
                ln['sentence_line'] = "".join(ln['sentence_line'].split())
            list_tokenize = newTokenizer(ln['sentence_line'])
            line = TextFormatter.Line()
            for word in list_tokenize:
                if debug == True:
                    print(f'word: {word}')
                    print(f'Surface Form: {word.surface}')
                    print(f'Reading: {word.reading}')
                    print(f'lineIndex: {lineIndex}')
                index += 1
                token = TextFormatter.Token()
                token.word = word.surface
                token.reading = word.reading
                token.partsOfSpeech = word.part_of_speech.split(',')
                token.index = index
                token.line = lineIndex
                line.add(token)
            lineIndex += 1

            speech_text_unfiltered.add(line)
            shaped_text = data_shaper(speech_text_unfiltered, highlight_keywords)
            #print(shaped_text)
            for sentence in shaped_text:
                modified_sentence = ''
                for token in sentence:
                    modified_sentence = modified_sentence + token.word
            ln['sentence_line'] = modified_sentence
            convo_line = {'speaker':ln['speaker'], 'sentence_line':ln['sentence_line']}
            modified_convo.append(convo_line.copy())
                        
    except Exception as e:
        traceback.print_exc()
	#raise
    
    print('look for this:==========================================================')
    print(modified_convo)
    data = {'name': 'sample data', 'info': 'sample data'}
    updated_convo = modified_convo
    #return render_template('cbs/test.html')
    return render_template('cbs/index.html', data=data, updated_convo=updated_convo)
    
def data_shaper(speech_text_unfiltered, highlight_keywords):
    speech_text_filtered = TextFormatter.Text()
    tokenizer = JanomeTokenizer()
    tokenizer.setStopWords(__custom_words_filter)
    tokenizer.setPartsOfSpeech(__part_of_speech_filter)

    # Filter Speech Text by removing stop words
    for line_unfiltered in speech_text_unfiltered.getTokenizeText():
        speech_line_filtered = TextFormatter.Line()
        for token_unfiltered in line_unfiltered.getTokenList():
            if tokenizer.tokenize(token_unfiltered) == False:  # Not stop word
                speech_line_filtered.add(token_unfiltered)
        speech_text_filtered.add(speech_line_filtered)


    # Now separate the Text file into sentences.
    # Separate Line to sentences
    speech_sentence_builder = []
    speech_token_sentence = []
    totalSpeechWords = 0
    for speech_line in speech_text_filtered.getTokenizeText():
        for token in speech_line.getTokenList():
            if token.word == '。' or token.word == '、':
                if len(speech_sentence_builder) > 0:
                    speech_token_sentence.append(speech_sentence_builder)
                speech_sentence_builder = []
            else:
                totalSpeechWords += 1
                speech_sentence_builder.append(token)


    if debug:
        print(f'Pre-checking Tokenized Sentence: ')
        i = 0
        for sentence in speech_token_sentence:
            print(f'\nTokenized Sentence: {i}', end=" ")
            for token in sentence:
                print(token.word, end=" ")
            i += 1

    print('\n\nPerform Highlighting Text ------------------------ Start')
    #shaped_token_sentence = []
    for speech_sentence in speech_token_sentence:
        for speech_token in speech_sentence:
            for highlight_keyword in highlight_keywords:
                #speech_reading = getReading(speech_token)
                lev_distance = Levenshtein.distance(speech_token.word, highlight_keyword)
                print(f'Lev Distance:  {lev_distance} for speech word: [{speech_token.word}] and highlight word: [{highlight_keyword}]')
                if lev_distance == 0:
                    speech_token.word = "<span id=\"key\" class=\"keyword\">" + speech_token.word + "</span>"
                    break

    print('Perform Highlighting Text ------------------------ End')

    if debug:
        print(f'\nPost with Highlighted Sentence: ')
        i = 0
        for sentence in speech_token_sentence:
            print(f'\nTokenized Sentence: {i}', end=" ")
            for token in sentence:
                print(token.word, end=" ")
            i += 1

    return speech_token_sentence


def newTokenizer(line):
    result = []
    tokenizer_lock.acquire()
    try:
        rawTokenizer = JanomeTokenizer()
        result = rawTokenizer.rawTokenize(line.strip('\n'))
    finally:
            tokenizer_lock.release()
    return result

def getReading(token):
    reading = token.reading
    if reading == '*':
        reading = token.word

    return reading

