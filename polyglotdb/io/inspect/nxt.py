
from polyglotdb.structure import Hierarchy

from ..types.parsing import *

from ..parsers import NxtParser

def inspect_nxt(word_path):
    """
    Generate a :class:`~polyglotdb.io.parsers.nxt.NxtParser`
    for the Buckeye corpus.

    Parameters
    ----------
    word_path : str
        Full path to text file

    Returns
    -------
    :class:`~polyglotdb.io.parsers.nxt.NxtParser`
        Auto-detected parser for NXT format files.
    """
    annotation_types = [OrthographyTier('word', 'word'), 
    						# OrthographyTier('syllable','syllable'), 
    						OrthographyTier('surface_transcription','surface_transcription')
    						]
    hierarchy = Hierarchy({'surface_transcription':'word','word': None})

    return NxtParser(annotation_types, hierarchy, make_transcription = False)
