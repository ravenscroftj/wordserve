'''
WordServe - a word2vec REST service

@author: James Ravenscroft
@copyright: Filament Consultancy Group Ltd 2016

'''

from .server import word_server_bp
from .word2vec import w2v

from gensim.models.word2vec import Word2Vec

from flask import Flask


def main():
    global _wv
    
    import argparse
    
    ap = argparse.ArgumentParser()
    
    ap.add_argument("vector_file", action="store", help="Path to the word2vec file to serve")
    ap.add_argument("-t", "--testclient", dest="test", action="store_true", help="If set, runs the test client against an existing server instance")
    ap.add_argument("--host", dest="host", action="store", default="localhost", help="The host to bind to, defaults to localhost")
    ap.add_argument("-p", "--port", dest="port", action="store", help="The port to serve on, defaults to 5000", default=5000)
    ap.add_argument("-d", "--debug", dest="debug", action="store_true", help="If true, provides debug output")
    ap.add_argument("-w", "--word2vec", dest="word2vec", action="store_true", help="If set then treat file as Google word2vec format")
    
    args = ap.parse_args()
    
    if args.test:
        print("Running test client against http://{}:{}".format(args.host,args.port))
        
        #tc = WordservClient(args.host,args.port)
        
        #for i in range(0,500):
        #    vecs = tc.vector(["hello","world"])
        
        #sys.exit(1)
        
        
    app = Flask(__name__)
    
    app.config['WORD2VEC_FILE'] = args.vector_file
    
    app.config['IS_WORD2VEC_NATIVE'] = args.word2vec
    
    if args.vector_file.endswith(".bin") or args.vector_file.endswith(".gz"):
        app.config['WORD2VEC_FILE_BINARY'] = True
    
    app.register_blueprint(word_server_bp)
    w2v.init_app(app)
    
    app.run(port=args.port, debug=args.debug)
    
    
    
if __name__ == "__main__":
    main()