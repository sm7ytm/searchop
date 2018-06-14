#!/usr/bin/env python
# -*- coding:utf-8 -*-

""" Programmet kollar ett telefonnummer hos PTS huruvida det är ledigt eller vilken operatör det tillhör"""

import urllib2
from screen_util import clear		# Egen modul för att rensa skärmen


def search_op_by_number(nummer):		# Kolla vilken operatör som har numret

	print '\tOperatörsfråga\n'
	print '\n\tFrågan körs, vänligen vänta'
	try:
		webbsida = urllib2.urlopen('http://api.pts.se/PTSNumberService/Pts_Number_Service.svc/pox/SearchByNumber?number=' + str(nummer))	# Öppna sidan och klistra ihop adressen med isbn-numret
		data = webbsida.read()
	
		start = data.find('<Name>') + 6		# Plocka ut start-index på texten
		slut = data.find('</Name>')			# och slut index
		
		clear()		
		print '\tOperatörsfråga\n'
		print '\n\tNummer  : %s' % tfnum
		print '\tOperatör: ' + data[start:slut]
		print '\n' * 3								 
			
	except urllib2.HTTPError:
		clear()
		print '\n\tNågot blev fel, troligen hittades inte numret du sökte\n\n'	



def is_avaiable(nummer):			# Funktion för att kolla om ett specifikt nummer är ledigt

	print '\tTillgänglighetsfråga\n'
	print '\n\tFrågan körs, vänligen vänta'
	try:
		webbsida = urllib2.urlopen('http://api.pts.se/PTSNumberService/Pts_Number_Service.svc/pox/IsNumberAvailable?number=' + str(nummer))		
		data = webbsida.read()
		
		start = data.find('">') + 2
		slut = data.find('</Int>') - 5
		
		clear()
		print '\tTillgänglighetsfråga\n'
		
		print '\n\tNummer  : %s' % tfnum
	
		
		if data[start:slut] == '0':		# En nolla i retur visar att numret är ledigt
			print '\tNumret är ledigt'
		elif data[start:slut] == '1':
			print '\tNumret är upptaget'	# och en etta så är det upptaget
		else:
			print '\tNågot blev fel, kan vara felformat prova riktnummer utan nolla och bindestreck mellan rikt och abbonentdel' # övriga fel anges av -1 men behövs inte
		
		print '\n' * 3								 
			
	except urllib2.HTTPError:
		clear()
		print '\n\tNågot blev fel\n\n'	
		
clear()		
tfnum = raw_input('\tAnge det telefonnummer du vill fråga på: ')				# Fråga efter önskat nummer
nummer = tfnum[1:]

clear()		
svar = raw_input('\tVälj (L)edigt eller (O)peratör: ')

clear()


if svar == 'l':
	clear()	
	is_avaiable(nummer)
elif svar == 'o':
	clear()	
	search_op_by_number(nummer)
else:
	print '\tFel val'
	