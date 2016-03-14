
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
    						#GroupingTier('syllable','syllable'), 
    						SegmentTier('phone','phone'),
                            TobiTier('break','phone'),
    						OrthographyTier('alignment_issue','phone'),
    						OrthographyTier('stress','word')
    						]
    annotation_types[-2].type_property = False
    hierarchy = Hierarchy({'phone':'word','word': None})
    # hierarchy = Hierarchy({'phone':'syllable','syllable':'word','word': None})

    return NxtParser(annotation_types, hierarchy, make_transcription = False)
