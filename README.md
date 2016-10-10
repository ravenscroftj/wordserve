# WordServe - a basic word2vec REST server

Word embeddings are super useful but large models are often memory hungry. This can be annoying if:

  * You are debugging/frequently restarting an machine learning application that uses a huge w2v model
  * You are working with w2v on a system with limited memory.
 
Wordserve can help you with both of these scenarios. The idea is that you run a lightweight REST server that provides read-only 
access to a word2vec model. Once this service is up (on your dev machine or on another machine if you have limited RAM) you don't
have to constantly read in huge files off disk if you want to restart your main app.

This repository provides a lightweight REST server and a [gensim](https://radimrehurek.com/gensim/models/word2vec.html) compatible Word2Vec proxy object.


## Installation

First grab the dependencies (setup.py will try this for you but modern pip will use wheels which is much faster):

`pip install numpy gensim flask`

Then, simply run `python setup.py install` to grab the relevant dependencies and install the module.

You will also need a word2vec model. I highly recommend the [Google News](https://drive.google.com/file/d/0B7XkCwpI5KDYNlNUTTlSS21pQmM/edit?usp=sharing) model.


## Usage


### Setting up the server
On the server machine (which could be your development machine or could be a remote server) run the server script:

```
python -m wordserve -p 5000 --host 0.0.0.0 /path/to/GoogleNews-vectors-negative300.bin.gz -w
```

The script will use gensim's `Word2Vec` model to load the vectors. If it encounters the `-w` argument it will try and use `load_word2vec_format()` to load a Google word2vec compatible model. It will assume that the file is binary if it finds a .bin or a .gz suffix. If you do not pass `-w` then it will just use the normal `load()` method for a gensim model.


### Setting up the client/application

Then in your application swap the Gensim word2vec class for the Word2Vec proxy object.



```python

#from gensim.models import Word2Vec
from wordserve.client import Word2VecProxy


def cool_ml_application():

	
	#w2v = Word2Vec.load_word2vec_format()
	w2v = Word2VecProxy("http://localhost:5000")

	#get a single vector from the server
	cat = w2v['cat']
	dog = w2v['dog']
	
	#show closest words to given vector
	print(w2v.similar_by_vector( w2v['man'] - w2v['boy'] + w2v['girl']  ))
	
	#show closest words to given word
	print(w2v.similar_by_word('dog')
	
	#calculate similarity between 2 words
	w2v.similarity('cat','dog')
	
	#retrieve multiple words
	words = w2v.fetch_many('cat','dog','hamster','snake')
	
	print(w2v.similar_by_vector(words['cat'] - words['hamster']))
	
	#which of these things is not like the others?
	print(w2v.doesnt_match(['cat','dog','hamster','dragon']))
	
	


```

# Performance

Using Wordserve is definitely slower than directly accessing the vector space in RAM. However, it does work reasonably fast for development and prototyping on the same box or across a LAN. 

As you can probably imagine, using this script over WAN does slow things down somewhat. If you really must do this then try to chain your vector requests together as much as possible using `Word2VecProxy.fetch_many` which accepts a list of words and returns a dict of { word:vector }

This script is not necessarily designed for production use so if you are thinking of building the next facebook off the back of this script and making millions of queries per second then you might want to stick to running word2vec in the same application memory space.


# Todo

Not yet implemented:
  * most_similar(positive=[], negative=[], topn=10, restrict_vocab=None, indexer=None)
  * most_similar_cosmul(positive=[], negative=[], topn=10)
  * wmdistance(document1, document2)