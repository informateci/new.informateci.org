__author__ = 'mandrake'

import re
import utils.web

_examptn = "<font face=[^>]+>([^<]+)</font>[^<]*</td><td>[^<]*<input.*value=\"([\d]+)\""
_appelloptn = "<input type=\"hidden\" name=\"appello\" value=\"([\d]+)\">"
_studentptn = "<tr><td class=\"cella_sfondo\">[^<]*</td>[^<]*<td class=\"cella_sfondo\">([\d]+)</td>[^<]*" + \
"<td class=\"cella_sfondo\">([\w]+)</td>[^<]*<td class=\"cella_sfondo\">([\w]+)</td>[^<]*" + \
"<td class=\"cella_sfondo\">([^<]*)</td>[^<]*<td>[^&]*&nbsp;"

_exdataptn = "<tr><td[^>]+>[\r\n]+([\d]+)</td>[\r\n]+<td[^>]+>[\r\n]+([\d/]+)</td><td[^>]+>[\r\n]+([\d\.]+)</td><td[^>]+>[\r\n]+([a-zA-Z0-9,\s]+)</td>[\r\n]+<td>"


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


def cerca(nome, cognome, course):
    l = parse_exam_names(course, 2013)
    for exam in l:
        m = parse_students(course, 2013, exam[2], exam[1])
        for s in m:
            # print s[1].lower(), s[2].lower()
            if nome.lower().strip() == s[1].lower().strip() and cognome.lower().strip() == s[2].lower().strip():
                toprint = "Esame: %s, Matricola: %s, Nome: %s, Cognome: %s" % (exam[0], s[0], s[1], s[2])
                print toprint


class Appello:
    def __init__(self, codice='', nome='', data='', ora='', aula='', nappello=-1, avvisi=''):
        self.codice = codice
        self.nome = nome
        self.data = data
        self.ora = ora
        self.aula = aula
        self.nappello = nappello
        self.avvisi = avvisi


class WebUnipi:
    def __init__(self):
        pass

    def get_compitini(self):
        pass

    def get_appelli(self, year=2014):
        return parse_exam_names(course='inf31', year=year) + parse_exam_names('wif18', year=year)