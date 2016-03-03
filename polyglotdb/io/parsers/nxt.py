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
    _extensions = ['.phonwords.xml']
    debug = True

    def __getitem__(self, key):
        for at in self.annotation_types:
            if at.name == key:
                return at
        raise(KeyError('No annotation type named {} found.'.format(key)))

    def parse_discourse(self, word_path):
        # directory path that is associated with only words
        # use path to make the names of all the associated files
        # load them all into minidom objects. 
        #
        # words = read_words(word_path)
        # phones = read_phones(phone_path)
        parent_dir,file_name = os.path.split(word_path)
        parent_dir = os.path.split(parent_dir)[0]
        file_name,ext = os.path.splitext(file_name)
        speaker_name, file_type = os.path.splitext(file_name)
        
        for a in self.annotation_types:
            a.reset()
            a.speaker = speaker_name


        tree = minidom.parse(word_path)
        assert(tree.firstChild.tagName == "nite:phonword_stream")
        words = tree.getElementsByTagName('phonword')
        


        syllables_tree = minidom.parse(os.path.join(parent_dir,'syllables',".".join([speaker_name,'syllables','xml'])))
        assert(syllables_tree.firstChild.tagName == "nite:syllable_stream")
        syllables = syllables_tree.getElementsByTagName('syllable') 
        for s in syllables:
            s.setIdAttribute('nite:id')

        phones_tree = minidom.parse(os.path.join(parent_dir,'phones',".".join([speaker_name,'phones','xml'])))
        assert(phones_tree.firstChild.tagName == "nite:phoneme_stream")
        phones = phones_tree.getElementsByTagName('ph')
        
        for p in phones:
            phones_list = []
            p.setIdAttribute('nite:id')
            phone = p.firstChild.data
            beg = float(p.getAttribute('nite:start'))
            end = float(p.getAttribute('nite:end'))
            alignment_issue = True if beg > end else False
            # experiment with adding all the phones at once!
            self['phone'].add([(phone,beg,end)]) # phones_list.append((phone,beg,end)) 
            # need to make a dummy word for silence phones
            if phone == 'SIL':
                self['word'].add([('SIL',beg,end)])
                self['stress'].add([('SIL',beg,end)])

            if alignment_issue:
                self['alignment_issue'].add([('negative duration',beg,end)])
                continue
            self['alignment_issue'].add([('none',beg,end)])



        
        for w in words:
            w.setIdAttribute('nite:id')
            word = w.getAttribute('orth')
            beg = float(w.getAttribute('nite:start'))
            end = float(w.getAttribute('nite:end'))
            stress = w.getAttribute('stressProfile')
            self['word'].add([(word,beg,end)]) # self.annotation_types[0].add([(word,beg,end)])
            self['stress'].add([(stress,beg,end)])

            # Get syllables belonging to word
            # child_syllable_ids = getChildren(w)
            # child_syllables = []
            # for i in child_syllable_ids:
            #     child_syllables.append(syllables_tree.getElementById(i))
            # child_syllable_data = [(s.getAttribute('nite:id'),beg,end) for s in child_syllables]
            # child_phones = []
            # alignment_errors = []
            # for i in child_syllables:
            #     child_phone_ids = getChildren(i)
            #     for k in child_phone_ids:
            #         phone = phones_tree.getElementById(k)
            #         if float(phone.getAttribute('nite:start')) > float(phone.getAttribute('nite:end')):
            #             if self.debug:
            #                 print('Warning: {} in {} has negative duration (id = {}; begin = {}; end = {})'.format(
            #                             phone.firstChild.data, file_name, phone.getAttribute('nite:id'), phone.getAttribute('nite:start'),
            #                             phone.getAttribute('nite:end')))
            #             alignment_errors.append(('negative duration', float(phone.getAttribute('nite:start')), float(phone.getAttribute('nite:end'))))
            #         else:
            #             alignment_errors.append(('none', float(phone.getAttribute('nite:start')), float(phone.getAttribute('nite:end'))))
            #         if phone is not None:
            #             child_phones.append(phones_tree.getElementById(k))
            #         else:
            #            raise(Exception("no phone : {}".format(k)))

            # if child_phones == []:
            #     self['phone'].add([('??',beg,end)])
            #     # self['phone'].add([('??',beg,end)])
            # else:
            #     self['phone'].add([(ph.firstChild.data,float(ph.getAttribute('nite:start')),float(ph.getAttribute('nite:end')) )for ph in child_phones])
            #     self['alignment_issue'].add(alignment_errors) # EXPERIMENTAL!!



            
            # self.annotation_types[1].add([('ph1',beg,end),('ph2',beg,end)])
        

        
            # syll = s.getAttribute('nite:id')
            # beg = s.getAttribute('nite:start')
            # end = s.getAttribute('nite:end')
            # self.annotation_types[1].add([(syll,beg,end)])
            # phone = p.firstChild.data
            # beg = p.getAttribute('nite:start')
            # end = p.getAttribute('nite:end')
            # self.annotation_types[2].add([(phone,beg,end)])


        # print("Working on file {}".format(speaker_name))
        
        pg_annotations = self._parse_annotations()


        data = DiscourseData(re.sub('[.]','',speaker_name), pg_annotations, self.hierarchy)

        for a in self.annotation_types:
            a.reset()

        return data

    # Having trouble getting the test_io_next.py to import these functions
    # def read_words(path):
    #     tree = minidom.parse(path)
    #     assert tree.firstChild.tagName == "nite:phonword_stream"
    #     output = tree.getElementsByTagName('phonword')
    #     return output
    #     return tree
def getChildren(node):
    nitechild = node.getElementsByTagName('nite:child')[0]
    hrefs = re.search('.*#(.*)',nitechild.getAttribute('href')).groups()[0]
    idStartEnd = hrefs.split('..')
    # print idStartEnd
    childIDs = []
    if idStartEnd[0]==idStartEnd[-1]:
        childIDs.append(re.search('id\((\w*)\)',idStartEnd[0]).groups()[0])
        # print "Only 1 child : " + " ".join(childIDs)
    else:
        assert len(idStartEnd)==2, "Can't find first/last child IDs for %s" % str(node)
        start = re.search('id\((\w*)\)',idStartEnd[0]).groups()[0]
        end = re.search('id\((\w*)\)',idStartEnd[1]).groups()[0]
        startNo = re.search('.*\_..(\d+)',start).groups()[0]
        endNo = re.search('.*\_..(\d+)',end).groups()[0]
        prefix = re.search('(.*\_..)\d+',start).groups()[0]
        for n in range(int(startNo),int(endNo)+1):
            childIDs.append(prefix+str(n))
        # print childIDs
    return childIDs



