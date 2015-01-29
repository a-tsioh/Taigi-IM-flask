# -*- coding:utf8 -*-
import unicodedata as ud
import re

from collections import namedtuple


RimePatterns = namedtuple('RimePatterns', ['nuclei', 'medials'])

mcr = RimePatterns(nuclei=['ŏ','ŭ(?!i)','ae','e(?!o)','i','a','(?<!e)o','u'], medials=['(w|y|o|ŭ)$'])
rr = RimePatterns(nuclei=['eo','eu','ae','e(?!o)','i','a','o','(?<!e)u'], medials=['(w|y|o|u)$']) # oe et ui
api = RimePatterns(nuclei=['ʌ','ɯ','ɛ','e','i','a','o','u'], medials=['(w|j|ɥ|ɰ)$'])
on = RimePatterns(nuclei=['a|i|u|e|o'], medials=['(y)$'])


initial_tl_to_ipa = {None: u'\xd8',
                     u'': u'\xd8',
                     u'b': u'b',
                     u'g': u'\u0261',
                     u'h': u'h',
                     u'j': u'dz',
                     u'ji': u'\u0291',
                     u'k': u'k',
                     u'kh': u'k\u02b0',
                     u'l': u'l',
                     u'm': u'm',
                     u'n': u'n',
                     u'ng': u'\u014b',
                     u'p': u'p',
                     u'ph': u'p\u02b0',
                     u's': u's',
                     u'si': u'\u0255',
                     u't': u't',
                     u'th': u't\u02b0',
                     u'ts': u'ts',
                     u'tsh': u'ts\u02b0',
                     u'tshi': u't\u0255\u02b0',
                     u'tsi': u't\u0255',
                     u'w': u'\xd8'}

median_tl_to_ipa = {u'a': u'a',
                    u'ai': u'ai',
                    u'ainn': u'a\u0129',
                    u'ann': u'\xe3',
                    u'au': u'a\u028a',
                    u'aunn': u'a\u0169',
                    u'e': u'e',
                    u'enn': u'\u1ebd',
                    u'i': u'i',
                    u'ie': u'ie',
                    u'ia': u'ia',
                    u'iann': u'i\xe3',
                    u'iau': u'ia\u028a',
                    u'iaunn': u'ia\u0169',
                    u'inn': u'\u0129',
                    u'io': u'iə',
                    u'ionn': u'i\xf5',
                    u'ioo': u'i\u0254',
                    u'iu': u'iu',
                    u'iunn': u'i\u0169',
                    u'm': u'm',
                    u'ng': u'\u014b',
                    u'o': u'ə',
                    u'oi': u'oi',
                    u'onn': u'\xf5',
                    u'oo': u'\u0254',
                    u'oonn': u'\xf5',
                    u'u': u'u',
                    u'ua': u'ua',
                    u'uai': u'uai',
                    u'uainn': u'ua\u0129',
                    u'uann': u'u\xe3',
                    u'ue': u'ue',
                    u'ui': u'ui',
                    u'uinn': u'u\u0129',
                    u'unn': u'\u0169'}

final_tl_to_ipa = {None: u'\xd8', '': u'\xd8', u'm': u'm', u'n': u'n', u'ng': u'\u014b', 'r': 'r'}

ru_tl_to_ipa = {None: u'\xd8',
                '': u'\xd8',
                'h': u'\u0294',
                'k': u'k\u031a',
                'p': u'p\u031a',
                't': u't\u031a'}

py_pattern = u"""
(?P<syllabe>
(?P<initiale>zh|ch|sh|[ywbpmfdtnlgkhjqxrzcs])?  # y and w are not strictly speaking initals => postproc
(?P<mediane>[ui])?
(?P<tonale>[āēīōūǖáéíóúǘǎăěĕǐǒŏǔŭǚàèìòùǜaeiouüv])  # v stands of ü  accepted input that shall be normalised afterward
(?P<finale>ng|n|o|i|u)?
(?P<ton>[0-5])?'?)
"""
re_py = re.compile(py_pattern, re.U | re.I | re.VERBOSE)

tailo_tones_mark_to_number = {u'A\u0300': u'A3',
 u'A\u0301': u'A2',
 u'A\u0302': u'A5',
 u'A\u0304': u'A7',
 u'A\u030d': u'A8',
 u'E\u0300': u'E3',
 u'E\u0301': u'E2',
 u'E\u0302': u'E5',
 u'E\u0304': u'E7',
 u'E\u030d': u'E8',
 u'I\u0300': u'I3',
 u'I\u0301': u'I2',
 u'I\u0302': u'I5',
 u'I\u0304': u'I7',
 u'I\u030d': u'I8',
 u'M\u0300': u'M3',
 u'M\u0301': u'M2',
 u'M\u0302': u'M5',
 u'M\u0304': u'M7',
 u'M\u030d': u'M8',
 u'N\u0300': u'N3',
 u'N\u0301': u'N2',
 u'N\u0302': u'N5',
 u'N\u0304': u'N7',
 u'N\u030d': u'N8',
 u'O\u0300': u'O3',
 u'O\u0300\u0358': u'Ou3',
 u'O\u0301': u'O2',
 u'O\u0301\u0358': u'Ou2',
 u'O\u0302': u'O5',
 u'O\u0302\u0358': u'Ou5',
 u'O\u0304': u'O7',
 u'O\u0304\u0358': u'Ou7',
 u'O\u030d': u'O8',
 u'O\u030d\u0358': u'Ou8',
 u'O\u0358': u'Ou',
 u'U\u0300': u'U3',
 u'U\u0301': u'U2',
 u'U\u0302': u'U5',
 u'U\u0304': u'U7',
 u'U\u030d': u'U8',
 u'a\u0300': u'a3',
 u'a\u0301': u'a2',
 u'a\u0302': u'a5',
 u'a\u0304': u'a7',
 u'a\u030d': u'a8',
 u'e\u0300': u'e3',
 u'e\u0301': u'e2',
 u'e\u0302': u'e5',
 u'e\u0304': u'e7',
 u'e\u030d': u'e8',
 u'i\u0300': u'i3',
 u'i\u0301': u'i2',
 u'i\u0302': u'i5',
 u'i\u0304': u'i7',
 u'i\u030d': u'i8',
 u'm\u0300': u'm3',
 u'm\u0301': u'm2',
 u'm\u0302': u'm5',
 u'm\u0304': u'm7',
 u'm\u030d': u'm8',
 u'n\u0300': u'n3',
 u'n\u0301': u'n2',
 u'n\u0302': u'n5',
 u'n\u0304': u'n7',
 u'n\u030d': u'n8',
 u'o\u0300': u'o3',
 u'o\u0300\u0358': u'ou3',
 u'o\u0301': u'o2',
 u'o\u0301\u0358': u'ou2',
 u'o\u0302': u'o5',
 u'o\u0302\u0358': u'ou5',
 u'o\u0304': u'o7',
 u'o\u0304\u0358': u'ou7',
 u'o\u030d': u'o8',
 u'o\u030d\u0358': u'ou8',
 u'o\u0358': u'ou',
 u'u\u0300': u'u3',
 u'u\u0301': u'u2',
 u'u\u0302': u'u5',
 u'u\u0304': u'u7',
 u'u\u030d': u'u8',
 u'\xc0': u'A3',
 u'\xc1': u'A2',
 u'\xc2': u'A5',
 u'\xc8': u'E3',
 u'\xc9': u'E2',
 u'\xca': u'E5',
 u'\xcc': u'I3',
 u'\xcd': u'I2',
 u'\xce': u'I5',
 u'\xd2': u'O3',
 u'\xd2\u0358': u'Ou3',
 u'\xd3': u'O2',
 u'\xd3\u0358': u'Ou2',
 u'\xd4': u'O5',
 u'\xd4\u0358': u'Ou5',
 u'\xd9': u'U3',
 u'\xda': u'U2',
 u'\xdb': u'U5',
 u'\xe0': u'a3',
 u'\xe1': u'a2',
 u'\xe2': u'a5',
 u'\xe8': u'e3',
 u'\xe9': u'e2',
 u'\xea': u'e5',
 u'\xec': u'i3',
 u'\xed': u'i2',
 u'\xee': u'i5',
 u'\xf2': u'o3',
 u'\xf2\u0358': u'ou3',
 u'\xf3': u'o2',
 u'\xf3\u0358': u'ou2',
 u'\xf4': u'o5',
 u'\xf4\u0358': u'ou5',
 u'\xf9': u'u3',
 u'\xfa': u'u2',
 u'\xfb': u'u5',
 u'\u0100': u'A7',
 u'\u0101': u'a7',
 u'\u0112': u'E7',
 u'\u0113': u'e7',
 u'\u012a': u'I7',
 u'\u012b': u'i7',
 u'\u0143': u'N2',
 u'\u0144': u'n2',
 u'\u014c': u'O7',
 u'\u014c\u0358': u'Ou7',
 u'\u014d': u'o7',
 u'\u014d\u0358': u'ou7',
 u'\u016a': u'U7',
 u'\u016b': u'u7',
 u'\u01f8': u'N3',
 u'\u01f9': u'n3',
 u'\u1e3e': u'M2',
 u'\u1e3f': u'm2',
 u'\u207f': u'nn',
 u'\u030c': u'9'}



tailo_pattern = u"""
(?P<syllabe>
-?-?
(?P<initiale>tsh|ts|th|ng|ph|th|kh|[pbmtnlkghjs])?
((?P<mediane>[ui])?
(?P<tonale>[aeiou]+)|
(?P<mng>ng|n|m))
(?P<finale>nn|ng|nnh|[ptkhnmr])?)
(?P<ton>[1-9]?)
"""
# "(?:(p|b|ph|m|t|th|n|l|k|g|kh|ng|h|ts|j|tsh|s)?([aeiou+]+(?:nn|N)?|ng|m)(?:(ng|m|n|r)|(p|t|h|k))?([1-9])?)|(p|b|ph|m|t|th|n|l|k|g|kh|ng|h|tsi|tshi|si|ts|ji|j|tsh|s)-?-?");

re_tailo = re.compile(tailo_pattern, re.U | re.I | re.VERBOSE)


SinoSyllabe = namedtuple("SinoSyllabe", "initiale mediane tonale finale ton")

def dict_of_SinoSyllabe(s):
    return {"initiale": s.initiale if s.initiale is not None else "",
            "mediane":  s.mediane if s.mediane is not None else "",
            "tonale":   s.tonale if s.tonale is not None else "",
            "finale":   s.finale if s.finale is not None else "",
            "ton":      s.ton}

def detonalise_pinyin(tonale):
    if tonale[-1] in "12345":
        return (tonale[:-1],int(tonale[-1]))
    tonale = ud.normalize("NFD",tonale)
    for t, c in py_tons:
        if c in tonale:
            return (tonale.replace(c,""),t )
    return (tonale, 5)
 
def analyse_tailo(tl):
    # tone to number
    for k,v in tailo_tones_mark_to_number.iteritems():
        if k in tl:
            voyel = v[:-1]
            ton = v[-1]
            tl = "".join([tl.replace(k,voyel),ton])
    match = re_tailo.match(tl.lower())
    if not match:
        print tl
        raise ValueError(tl + " is not a valid tailo syllable")
    i = match.group("initiale")
    m = match.group("mediane")
    tl = match.group("tonale")
    mng = match.group("mng")
    f = match.group("finale")
    t = match.group("ton")
    if mng:
        tl = mng
    if not t :
        if f and f in ["p", "t", "k", "h"]:
            t = "4"
        else:
            t = "1"
    if False and i and i in ["j","s","ts","tsh"]:
        if m == "i" or (not m and tl[0] == "i"):
            i += "i"
    if f and f == "nn": # nasalisation
        f = None
        tl += "nn"
    if tl == u"o" and (f and f not in ["h", "r"]):
        tl = u"oo"
    if not i:
        i = ""
    if not m:
        m = ""
    if not tl:
        tl = ""
    if not f:
        f = ""
    s = SinoSyllabe(i, m, tl, f, t)
    return s



def romanise_hangul(hg, strict=True):
    if len(hg) != 1:
        if strict:
            raise ValueError(hg + " is not a single character") 
        else:
            return hg
    try:
        name = ud.name(hg)
        assert("HANGUL SYLLABLE" in name)
        latin = name[16:]
        return latin.lower()
    except:
        if strict:
            return ValueError(hg + " is not valid hangul")
        else:
            return hg




def analyse_hangul(word, sep='\t'):
    """ Split sino-syllable
        word: romanised syllable in korean
        
        return split sino-syllable 
    """
    word = romanise_hangul(word)
    patterns = rr
    res = []
    for item in patterns.nuclei:
        pattern = '(%s)' % item
        
        parts = re.split(pattern, word, 1)
        if len(parts) > 1:
            res = check_medial(parts, patterns.medials[0])
            res.append(0) 
            return SinoSyllabe(*res)
    raise ValueError(word + " is not valid romanised hangul")
    
def check_medial(syll_parts, medials, empty_char=''):
    """ Searching for medial in split sino-syllable
        
    """
    if not re.search(medials, syll_parts[0]):
        # no medial
        syll_parts.insert(1, empty_char)
    elif len(syll_parts[0]) == 1:
        # if the medial is not preceded by an onset, we consider that it fills both position, eg: y y a ng for 양
        res = re.split(medials, syll_parts[0])
        syll_parts[0] = res[1]
        syll_parts.insert(1, res[1])
    else:
        # typical onset-medial situation
        res = re.split(medials, syll_parts[0])
        syll_parts[0] = res[0]
        syll_parts.insert(1, res[1])
            
    return syll_parts



py_tons = [(1,u"\u0304"),(2,u"\u0301"),(3,u"\u0306"),(4,u"\u0300"),(3,u"\u030c")]

def detonalise_pinyin(tonale):
    if tonale[-1] in "12345":
        return (tonale[:-1],int(tonale[-1]))
    tonale = ud.normalize("NFD",tonale)
    for t, c in py_tons:
        if c in tonale:
            return (tonale.replace(c,""),t )
    return (tonale, 5)
        

def analyse_pinyin(py):
    match = re_py.match(py.lower())
    if not match:
        print py
        raise ValueError(py + " is not a valid pinyin syllable")
    i = match.group("initiale")
    m = match.group("mediane")
    tl = match.group("tonale")
    f = match.group("finale")
    t = match.group("ton")
    (tl,t2) = detonalise_pinyin(tl)
    if t and t2 != 5 and int(t) != t2:
        raise ValueError(py + "conflit de ton dans ce pinyin")
    else:
        if not t:
            t = t2
        else:
            t = int(t)
    if i == "y":
        if not m and tl != "i":
            m = 'i'
        if tl == 'u':
            m = u"ü"
        i = None
    if i == "w":
        if not m and tl != "u":
            m = 'u'
        i = None
    return SinoSyllabe(i if i else "", m if m else "", tl, f if f else "", t)

def normalise_pinyin(py):
    syls = [detonalise_pinyin(x[0]) for x in re_py.findall(py)]
    return "_".join(["%s%d" % x for x in syls]).lower()

def normalise_tailo(tl):
    nonone = lambda x: "" if x is None else x
    tl = re.sub("[,.]","", tl, flags=re.U)
    syls = re.split("[- ]+",tl, flags=re.U)
    syls = ["".join(map(nonone,analyse_tailo(x))) for x in syls if x != ""]
    return "_".join(syls).lower()
    
mapping_langues_analyse = {'mandarin': analyse_pinyin,
                           u'coréen': analyse_hangul,
                           u'hokkien': analyse_tailo}
mapping_langues_normalise = {'mandarin': normalise_pinyin,
                             u'coréen': lambda x: x,
                             'hokkien': normalise_tailo}

def get_normalisation_func(langue):
    if langue in mapping_langues_normalise:
        return mapping_langues_normalise[langue]
    else:
        return lambda x: x  # pas de mapping -> fonction d'identité


def get_analyseur_func(langue):
    if langue in mapping_langues_analyse:
        return mapping_langues_analyse[langue]
    else:
        return lambda x: None  # pas de mapping -> toujours None


def analyse_to_ipa(a):
    i = a.initiale
    m = a.mediane
    mt = median_tl_to_ipa[(m if m else "") + a.tonale]
    mt = (3 - len(mt)) * u'Ø' + mt
    f = a.finale
    ru = None 
    if i and i in ["j", "s", "ts", "tsh"] and (m == "i" or (m is None and a.tonale[0] == "i")):
        i += "i"
    i = initial_tl_to_ipa[i]
    if f and f[-1] in "ptkh":
        ru = f[-1]
        f = f[:-1]
    f = final_tl_to_ipa[f]
    ru = ru_tl_to_ipa[ru]
    t = a.ton
    return ".".join([i, mt, f, ru, str(t)])
