'''
Created on 4 Oct 2016

@author: James Ravenscroft
'''
import numpy as np
import requests

from urllib.parse import quote


class Word2VecProxy:
    
    def __init__(self, url):
        self.url = url
        
        
    def __getitem__(self, index):
        return np.asarray(requests.get("{}/vector?word={}".format(self.url,quote(index))).json()['wordvectors'][index])
    
    
    def fetch_many(self, words):
        qs = "&".join(["word={}".format(quote(x)) for x in words])
        results = requests.get("{}/vector?{}".format(self.url,qs)).json()['wordvectors']
        return { key: np.asarray(value) for key,value in results.items() }
    

    def similar_by_word(self, word, topn=10, restrict_vocab=None):
        results = requests.get("{}/similar_by_word/{}/{}".format(self.url, quote(word), topn)).json()
        return [ (x,y) for x,y in results['similar']]
    
    def similar_by_vector(self, vector, topn=10, restrict_vocab=None):
        
        results = requests.post("{}/similar_by_vector/{}".format(self.url, topn), json=vector.tolist()).json()
        
        return [ (x,y) for x,y in results['similar']]
    
    def similarity(self, word1, word2):
        
        r = requests.get("{}/similarity/{}/{}".format(self.url, quote(word1), quote(word2)))
        
        return r.json()['similarity']
    
    def n_similarity(self, ws1, ws2):

        ws1_qs = "&".join(["ws1={}".format(quote(x)) for x in ws1])
        ws2_qs = "&".join(["ws2={}".format(quote(x)) for x in ws2])

        r = requests.get("{}/similarity?{}&{}".format(self.url, quote(ws1_qs), quote(ws2_qs)))
        
        return r.json()['similarity']
    
    
    
    
    
    def doesnt_match(self, words):
        qs = "&".join(["word={}".format(quote(x)) for x in words])
        return requests.get("{}/doesnt_match?{}".format(self.url,qs)).json()['doesnt_match']