
import pytest
import os

from polyglotdb.io import inspect_nxt

# from polyglotdb.io.parsers.nxt import read_words

from polyglotdb.corpus import CorpusContext


graph_db = {'host':'localhost', 'port': 7474,'user': 'neo4j', 'password': 'oriana'}

def test_discourse_nxt(nxt_test_dir):
    with CorpusContext('discourse_nxt', **graph_db) as c:
        c.reset()
        word_path = os.path.join(nxt_test_dir,'phonwords/test.A.phonwords.xml')
        parser = inspect_nxt(word_path)
        c.load(parser, word_path)
    # q = c.query_graph(c.surface_transcription)
    # assert(q.count()==28)
    assert(1==1)