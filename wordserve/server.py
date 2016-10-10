"""
Wordserv - simple server application that provides mapping service to/from word vectors over HTTP

"""

from flask import Blueprint, jsonify, Flask, request

import numpy as np

from .word2vec import w2v

help_text =  """

<html><head><title>WordServ</title></head>

<body>

<h1>WordServ</h1>
<h2>A simple word2vec server By <a href="http://brainsteam.co.uk">James Ravenscroft</a></h2>

<div>
<h3>GET /vector</h3>
<p>Make a get request to /vector endpoint with a query variable 'word' to receive a wordvector for that word 
or get an array of words and get an array of words back.
</p>

<h4>Example</h4>
<pre>
curl http://localhost:5000/vector?word=hello&word=goodbye
</pre>
</div>

<div>
<h3>GET /similar_by_word</h3>
<p>Make a get request to /similar_by_word endpoint with a path variable representing the word you want to query. 
Optionally specify a maximum number of results to return (default 10)

</p>

<h4>Example</h4>

<p>
<pre>
curl http://localhost:5000/similar_by_word/cat/10
</pre>
</p>
</div>


<div>
<h3>POST /similar_by_vector</h3>
<p>Find a number of similar words via an input vector posted to the server. Optionally specify a maximum number of results to return (default 10)</p>

<h4>Example</h4>

<p>
<pre>
curl -X POST -H "Content-Type: application/json" -d "[0.12, -0.23, 0.53 ... ]" http://localhost:5000/similar_by_vector/10
</pre>
</p>
</div>


</body>
</html>

"""

word_server_bp = Blueprint('wordserver', __name__)


@word_server_bp.route("/")
def index():
    return help_text

@word_server_bp.route("/vector", methods=['GET'] )
def vector():
    _wv = w2v.word2vec
    
    wordvecs = {}
    
    for word in request.args.getlist('word'):
        if word in _wv:
            wordvecs[word] = _wv[word].tolist()
        else:
            wordvecs[word] = [0] * 300
        
    return jsonify(wordvectors=wordvecs)

@word_server_bp.route("/similar_by_word/<string:word>/<int:topn>", methods=['GET'])
def similar_by_word(word,topn=10):
    _wv = w2v.word2vec
    
    
    if word in _wv:
        similar = _wv.similar_by_word(word,topn)
    else:
        similar = []
        
    return jsonify(similar=similar)


@word_server_bp.route("/similar_by_vector/<int:topn>", methods=['POST'])
def similar_by_vector(topn=10):
    
    _wv = w2v.word2vec
    
    vector = np.asarray(request.get_json())

    similar = _wv.similar_by_vector(vector, topn=topn)
        
    return jsonify(similar=similar)


@word_server_bp.route("/similarity/<string:word1>/<string:word2>", methods=['GET'])
def similarity(word1,word2):
    _wv = w2v.word2vec
    return jsonify(similarity=_wv.similarity(word1,word2))


@word_server_bp.route("/n_similarity", methods=['GET'])
def n_similarity():
    _wv = w2v.word2vec
    return jsonify(similarity=_wv.n_similarity((request.args.getlist('ws1'),request.args.getlist('ws2'))))

@word_server_bp.route("/doesnt_match", methods=['GET'])
def doesnt_match():
    _wv = w2v.word2vec
        
    return jsonify(doesnt_match=_wv.doesnt_match(request.args.getlist('word')))


@word_server_bp.route("/benchmark", methods=['GET'])
def benchmark():
    import time
    _wv = w2v.word2vec
    
    w2vdesc = "An estimated 90% of all data is unstructured and the amount of it is increasing at a daunting rate across our ever more connected world. Unlocking the value of big data is one of the biggest challenges for businesses today. Fortunately a new age of AI and cognitive computing is upon us which can help us make sense of unstructured data like never before."
        
    start = time.time()
    
    for x in w2vdesc.split(" "):
        if x in _wv:
            vec = _wv[x]
        
    end = time.time()
    wordtest = end - start
    
    
    start = time.time()
    
    for word in w2vdesc.split(" "):
        if x in _wv:
            _wv.similar_by_word(word)
    
    end = time.time()#
    simtest = end-start
    
    
    return jsonify(wordtest=wordtest, similar = simtest)

    