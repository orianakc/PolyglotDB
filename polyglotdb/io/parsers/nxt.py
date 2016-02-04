#parser

import os
import re
import sys
from xml.dom import minidom

from .base import BaseParser, PGAnnotation, PGAnnotationType, DiscourseData

class NxtParser(BaseParser):
    '''
    Parser for the NXT file formats.

    

    Parameters
    ----------
    annotation_types: list
        Annotation types of the files to parse
    hierarchy : :class:`~polyglotdb.structure.Hierarchy`
        Details of how linguistic types relate to one another
    stop_check : callable, optional
        Function to check whether to halt parsing
    call_back : callable, optional
        Function to output progress messages
    '''
    def parse_discourse(self, word_path):
    	# directory path that is associated with only words
    	# use path to make the names of all the associated files
    	# load them all into minidom objects. 
    	#
    	# words = read_words(word_path)
    	# phones = read_phones(phone_path)
    	name = "testA"
    	
    	tree = minidom.parse(word_path)
    	assert(tree.firstChild.tagName == "nite:phonword_stream")
    	words = tree.getElementsByTagName('phonword')
    	
    	for w in words:
    		word = w.getAttribute('orth')
    		beg = float(w.getAttribute('nite:start'))
    		end = float(w.getAttribute('nite:end'))

    		self.annotation_types[0].add([(word,beg,end)])


    	pg_annotations = self._parse_annotations()
    	data = DiscourseData(name, pg_annotations, self.hierarchy)

    	return data

    # def read_words(path):
    # 	tree = minidom.parse(path)
    # 	assert tree.firstChild.tagName == "nite:phonword_stream"
    # 	output = tree.getElementsByTagName('phonword')
    # 	return output




