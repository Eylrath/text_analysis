import re
import numpy as np

class ContextAnalyser():
    def __init__(self, execute_all=True, file1='files/zdania.txt', file2='files/konteksty.txt'):
        self.stopwords = self.polish_stopwords()
        self.context_dict = self.context_dictionary()
        self.words = []
        self.sentences = []
        self.contexts = []
        if execute_all:
            self.read_sentences(file1)
            self.read_contexts(file2)
    
    def clean(self, text):
        res = ""
        text = text.replace('\n', ' ')
        text = text.lower()
        for el in text:
            if el not in [".",",","?","!",";",":","%", "&", ")",">","]","$","@","(", "[", "<", "0","1","2","3","4","5","6","7","8","9"]:
                res += el 
        return res
    
    def lemmatisation(self, text):
        text = self.clean(text)
        return " ".join([self.context_dict[word] for word in text.split(" ") if word in self.context_dict and word not in self.stopwords])    

    def read_sentences(self, filename='files/zdania.txt'):
        with open(filename, 'r', encoding='utf8') as f:
            sentences = []
            words = []
            sentence = ""
            count_breaks = 0
            while line := f.readline():
                if line == '\n':
                    count_breaks += 1
                else:
                    sentence += line
                if count_breaks == 2:
                    sentence = self.lemmatisation(sentence)
                    sentences.append(sentence)
                    words += sentence.split(" ")
                    sentence = ""
                    count_breaks = 0
            self.words = sorted(list(set(words).union(set(self.words))))
            self.sentences += sentences


    def read_contexts(self, filename='files/konteksty.txt'):
        contexts = []
        with open(filename, 'r', encoding='utf8') as f:
            while word := f.readline():
                word = word.replace("\n", "")
                contexts.append(word)
        self.contexts += contexts
        self.contexts_set = list(set(contexts) .union(set(self.contexts)))

        
    def vectorize(self, sentence):
        sentence_L = sentence.split(" ")
        vector = np.zeros(len(self.words))
        for word in sentence_L:
            if word in self.words:
                idx = self.words.index(word)
                vector[idx] += 1
        return vector

    def vectorize_output(self, word):
        out = np.zeros(len(self.contexts_set))
        index = self.contexts_set.index(word)
        out[index] = 1
        return out
    
    def polish_stopwords(self, filename='files/polish.stopwords.txt', max_val=3):
        with open (filename, "r", encoding="utf8") as file:
            lista = file.read()
        lista_sp = []
        for el in lista.split():
            if len(el) >= max_val:
                lista_sp.append(el)
        return lista_sp

    def context_dictionary(self, filename="files/odm.txt", min_length=4, max_length=10):
        D = {}
        # cores = []
        with open("files/odm.txt", "r", encoding="utf8") as f:
            while words_list := f.readline():
                words = words_list.replace(", ", ",").replace("\n", "")
                found = False
                for sign in ".:- !?":
                    if sign in words:
                        found = True
                words_list = words.split(",")
                core = words_list[0].lower()
                if found or len(core) > max_length or len(core) < min_length or core in self.stopwords:
                    continue 
                # cores.append(core)
                for word in words_list:
                    word = word.lower()
                    if word not in D:
                        D[word] = core  
        return D
    
    def getXY(self):
        X = []
        Y = []
        for sentence, context in zip(self.sentences, self.contexts):
            x = self.vectorize(self.lemmatisation(sentence))
            y = self.vectorize_output(context)
            X.append(x)
            Y.append(y)
        return np.array(X), np.array(Y)
    
    def get_context(self, index):
        return self.contexts_set[index]
    
    def get_sentence(self, index):
        return self.sentences[index]

    def get_len(self):
        return len(self.contexts)