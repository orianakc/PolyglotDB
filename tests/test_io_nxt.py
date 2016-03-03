
import pytest
import os

from polyglotdb.io import inspect_nxt

# from polyglotdb.io.parsers.nxt import read_words # Functions from the parser to be added to test suite later on.

from polyglotdb.corpus import CorpusContext

def test_discourse_nxt(graph_db,nxt_test_dir):
    with CorpusContext('discourse_nxt', **graph_db) as c:
        c.remove_discourse('testA')
        word_path = os.path.join(nxt_test_dir,'phonwords/test.A.phonwords.xml')
        parser = inspect_nxt(word_path)
        print([k.name for k in parser.annotation_types])
        c.load(parser, word_path)
        q = c.query_graph(c.word)
        q = q.filter(c.word.discourse.name=='testA')
        assert(q.count()==28)
        # assert(False)
        
        # q = c.query_graph(c.phone)
        # assert(q.count()==85) # Should be equal to 85, but problem with parsing in the <SIL> phones right now.


        # syllabics = ['ah','ax','ih','ay','ih']
        # q = c.query_graph(c.surface_transcription).filter(c.surface_transcription.label == 't')
        # q = q.filter(c.surface_transcription.previous.in_(syllabics))








