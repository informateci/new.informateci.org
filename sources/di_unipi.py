from utils.cache import cached_in

__author__ = 'mandrake'

import re
import utils.web
import BeautifulSoup
from enum import Enum


class AppelloOrCompitino(Enum):
    Appello = 0
    Compitino = 1

    @classmethod
    def to_string(cls, val):
        for k, v in vars(cls).iteritems():
            if v == val:
                return k


class IstanzaEsame:

    def __init__(self, n_appello=-1, n_compitino=-1, app_or_comp=None, id_esame_aa=-1, cdl='', data_inizio=None,
                 ora_inizio=None, aule=[], sigla='', nome=''):
        self.n_appello = n_appello
        self.n_compitino = n_compitino
        self.app_or_comp = app_or_comp
        self.id_esame_aa = id_esame_aa
        self.cdl = cdl
        self.data_inizio = data_inizio
        self.ora_inizio = ora_inizio
        self.aule = aule
        self.sigla = sigla
        self.nome = nome

    def get_dict_repr(self):
        return {
            'n_appello': self.n_appello,
            'n_compitino': self.n_compitino,
            'app_or_comp': self.app_or_comp,
            'id_esame_aa': self.id_esame_aa,
            'cdl': self.cdl,
            'data_inizio': self.data_inizio,
            'ora_inizio': self.ora_inizio,
            'aule': self.aule,
            'sigla': self.sigla,
            'nome': self.nome
        }


class StudenteIscritto:

    def __init__(self, nome='', cognome='', matricola='', commenti=''):
        self.nome = nome
        self.cognome = cognome
        self.matricola = matricola
        self.commenti = commenti

    def get_dict_repr(self):
        return {
            'nome': self.nome,
            'cognome': self.cognome,
            'matricola': self.matricola,
            'commenti': self.commenti
        }


@cached_in(expire=60)
def parse_istanze_esame(course, year):
    ret = []
    for i in (range(1, 7) + [10, 20, 30, 40]):
        # Scrapo tutti gli esami di un dato appello
        url = "http://compass2.di.unipi.it/didattica/%s/share/orario/Appelli/" % course +\
            "appelli.asp?letter=&ycourse=&course=%s&year=%d&start=%d&end=%d" % \
            (course, int(year), i, i)
        bs = BeautifulSoup.BeautifulSoup(utils.web.url2html(url))
        t = bs.findAll('table')[2]
        for tr in t.findAll('tr'):
            valid = True

            try:
                sigla = tr.findAll('td')[0].findAll('font')[0].contents[0]
                nome = tr.findAll('td')[1].findAll('font')[0].contents[0].replace('\r\n', ' ').strip()
                id_esame_aa = tr.findAll('td')[2].findAll('input')[0].get('value')
                # TODO: vado a cercare data, ora e aule
                dat_url = "http://compass2.di.unipi.it/didattica/inf31/share/orario/Appelli/appelliret.asp?start=%d&end=%d&chk=%d" %\
                           (i, i, int(id_esame_aa))
                dat_bs = BeautifulSoup.BeautifulSoup(utils.web.url2html(dat_url))
                dat_tds = dat_bs.findAll('table')[2].findAll('tr')[3].findAll('td')
                print dat_tds
                print
                try:
                    data_inizio = dat_tds[1].contents[0].replace('\r\n', '')
                    ora_inizio = dat_tds[2].contents[0].replace('\r\n', '')
                    aule = [x.strip() for x in dat_tds[3].contents[0].split(',')]
                except Exception:
                    data_inizio = ''
                    ora_inizio = ''
                    aule = []
            except Exception:
                valid = False

            if valid:
                if i < 9:
                    ret.append(
                        IstanzaEsame(nome=nome, sigla=sigla, n_appello=i, app_or_comp=AppelloOrCompitino.Appello,
                                     id_esame_aa=id_esame_aa, data_inizio=data_inizio, ora_inizio=ora_inizio,
                                     aule=aule).get_dict_repr()
                    )
                else:
                    ret.append(
                        IstanzaEsame(nome=nome, sigla=sigla, n_compitino=i, app_or_comp=AppelloOrCompitino.Compitino,
                                     id_esame_aa=id_esame_aa, data_inizio=data_inizio, ora_inizio=ora_inizio,
                                     aule=aule).get_dict_repr()
                    )

    return ret


'''
#########################################################################

                   OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOLD

#########################################################################
'''

_examptn = "<font face=[^>]+>([^<]+)</font>[^<]*</td><td>[^<]*<input.*value=\"([\d]+)\""
_appelloptn = "<input type=\"hidden\" name=\"appello\" value=\"([\d]+)\">"
_studentptn = "<tr><td class=\"cella_sfondo\">[^<]*</td>[^<]*<td class=\"cella_sfondo\">([\d]+)</td>[^<]*" + \
"<td class=\"cella_sfondo\">([\w]+)</td>[^<]*<td class=\"cella_sfondo\">([\w]+)</td>[^<]*" + \
"<td class=\"cella_sfondo\">([^<]*)</td>[^<]*<td>[^&]*&nbsp;"

_exdataptn = "<tr><td[^>]+>[\r\n]+([\d]+)</td>[\r\n]+<td[^>]+>[\r\n]+([\d/]+)</td><td[^>]+>[\r\n]+([\d\.]+)</td><td[^>]+>[\r\n]+([a-zA-Z0-9,\s]+)</td>[\r\n]+<td>"


def cerca(nome, cognome, course):
    l = parse_exam_names(course, 2013)
    for exam in l:
        m = parse_students(course, 2013, exam[2], exam[1])
        for s in m:
            # print s[1].lower(), s[2].lower()
            if nome.lower().strip() == s[1].lower().strip() and cognome.lower().strip() == s[2].lower().strip():
                toprint = "Esame: %s, Matricola: %s, Nome: %s, Cognome: %s" % (exam[0], s[0], s[1], s[2])
                print toprint


def parse_students(course, year, no, exam):
    ret = []
    appellore = re.compile(_appelloptn)
    studentre = re.compile(_studentptn)
    url = "http://compass2.di.unipi.it/didattica/%s/share/orario/Appelli/" % course \
         + "appelliret.asp?letter=&ycourse=&course=%s&year=%d&start=%d&end=%d&chk=%s" % \
         (course, year, no, no, exam)
    h = utils.web.url2html(url)
    matches = appellore.finditer(h)
    try:
        m = matches.next()
    except StopIteration:
        return []
    url = "http://compass2.di.unipi.it/didattica/inf31/share/orario/Appelli/lista.asp?action=list&appello=%s" \
        % m.group(1)

    h = utils.web.url2html(url)
    matches = studentre.finditer(h)
    ok = True
    while ok:
        try:
            m = matches.next()
            ret.append([m.group(1), m.group(2), m.group(3), m.group(4)])
            #print m.group(1), m.group(2), m.group(3), "Note:", m.group(4)
        except StopIteration:
            ok = False

    return ret


def parse_exam_data(istart, iend, id):
    ptnre = re.compile(_exdataptn)
    url = "http://compass2.di.unipi.it/didattica/inf31/share/orario/Appelli/appelliret.asp?start=%d&end=%d&chk=%d"\
        % (istart, iend, id)
    h = utils.web.url2html(url)
    print url
    return ptnre.findall(h)

def parse_exam_names(course, year):
    print 'parse_exam_names'
    examre = re.compile(_examptn)
    ret = []

    for i in range(1, 7):
        url = "http://compass2.di.unipi.it/didattica/%s/share/orario/Appelli/" % course +\
            "appelli.asp?letter=&ycourse=&course=%s&year=%d&start=%d&end=%d" % \
            (course, year, i, i)
        print url
        h = utils.web.url2html(url)
        matches = examre.finditer(h)
        ok = True
        while ok:
            try:
                m = matches.next()
                ret.append([utils.web.unescape(m.group(1)).strip().replace('\r\n-', ' -'), m.group(2), i, parse_exam_data(i, i, int(m.group(2)))])
            except StopIteration:
                ok = False

    return ret


class Appello:
    def __init__(self, codice='', nome='', data='', ora='', aula='', nappello=-1, avvisi=''):
        self.codice = codice
        self.nome = nome
        self.data = data
        self.ora = ora
        self.aula = aula
        self.nappello = nappello
        self.avvisi = avvisi


class DiUnipi:
    def __init__(self):
        pass

    def get_compitini(self):
        pass

    def get_appelli(self, year=2014):
        return parse_exam_names(course='inf31', year=year) + parse_exam_names('wif18', year=year)
