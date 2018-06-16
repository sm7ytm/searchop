#!/usr/bin/env python
# -*- coding:utf-8 -*-

""" Programmet kollar ett telefonnummer hos PTS huruvida det är ledigt eller vilken operatör det tillhör"""

import urllib2
from screen_util import clear       # Egen modul för att rensa skärmen


def search_op_by_number(nummer):        # Kolla vilken operatör som har numrettry:

    try:
        webbsida = urllib2.urlopen('http://api.pts.se/PTSNumberService/Pts_Number_Service.svc/pox/SearchByNumber?number=' + str(nummer))    # Öppna sidan och klistra ihop adressen med isbn-numret
        data = webbsida.read()
        return data

    except urllib2.HTTPError:
        clear()
        print '\n\tNågot blev fel, troligen hittades inte numret du sökte\n\n'


def is_available(nummer):           # Funktion för att kolla om ett specifikt nummer är ledigt

    try:
        webbsida = urllib2.urlopen('http://api.pts.se/PTSNumberService/Pts_Number_Service.svc/pox/IsNumberAvailable?number=' + str(nummer))
        data = webbsida.read()

        start = data.find('">') + 2
        slut = data.find('</Int>') - 5

        if data[start:slut] == '0':     # En nolla i retur visar att numret är ledigt
            return 'Ledigt'
        elif data[start:slut] == '1':
            return 'Upptaget'   # och en etta så är det upptaget
        else:
            return 'Fel'

    except urllib2.HTTPError:
        clear()
        print '\n\tNågot blev fel\n\n'


clear()
tfnum = raw_input('\tAnge nummer (xxxx-xxxxxx / xxx-xxxxxxx) : ')                # Fråga efter önskat nummer
nummer = tfnum[1:]

op_data = search_op_by_number(nummer)
op_start = op_data.find('<Name>') + 6       # Plocka ut start-index på texten
op_slut = op_data.find('</Name>')           # och slut index

ledigt = is_available(nummer)

clear()
print '\tOperatörsfråga\n'
print '\tNummer          : %s' % tfnum
print '\tOperatör        : ' + op_data[op_start:op_slut]
print '\tTillgänglighet  : %s' % ledigt
print '\n' * 3
