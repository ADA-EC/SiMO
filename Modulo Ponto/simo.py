 # -*- coding: utf-8 -*-

import bluetooth._bluetooth as bluez
import blescan
import time
import datetime
from threading import Thread

#Classe responsavel por escanear os beacons proximose resgatar as informações relevantes sobre o beacon
class Scanner():
	def __init__(self, deviceId = 0, loops = 1):
		self.deviceId = deviceId
		self.loops = loops
		try:
			self.sock = bluez.hci_open_dev(self.deviceId)   #Abre uma conexao com o bluetooth
			blescan.hci_le_set_scan_parameters(self.sock)   #Configura os paramentos para o escaneamento
			blescan.hci_enable_le_scan(self.sock)			#Escaneia dispositivos proximos
		except Exception, e:
			print e   

	def scan(self):
		return blescan.parse_events(self.sock, self.loops)

#Classe Beacon: Contem as informações sobre o beacon que foi detectado
class Beacon():
	def __init__(self, mac, uuid, major, minor, rssi, msrd_pwr):
		self.mac = mac
		self.uuid = uuid
		self.major = major
		self.minor = minor
		self.rssi = rssi
		self.msrd_pwr =  msrd_pwr
		print "Hello World"
	def __str__(self):
		return "MAC: " + self.mac +"\nUUID: " + self.uuid + "\nMajor: " + self.major + "\nMinor: " + self.minor + "\nRSSI: " + self.rssi + "\nMeaseured Power: " + self.msrd_pwr

#Checa de tempos em tempos se deixou de detectar um beacon para salvar o horário de partida no log
def check_current_stops():
	while True:
		mac_lst = []
		for l in log:
			stop = log.get(l)
			print stop
			if time.time() - stop[1] > 5:
				print "Salvo parada " + l
				mac_lst.append(l)

		f = open("log.dat", "a")		
		for l in mac_lst:
			linha = linhas_lst.get(l)
			stop = log.get(l)	
			st = linha + ";" + l + ";"
			horario = datetime.datetime.fromtimestamp(stop[0]).strftime('%Y-%m-%d %H:%M:%S')
			st += horario + ";" 
			st += datetime.datetime.fromtimestamp(stop[1]).strftime('%Y-%m-%d %H:%M:%S') + "\n"
			f.write(st)
			linha_recente[linha] = horario
			del log[l]
		f.close()

		data = ""
		for id_linha in linha_recente:
			horario = linha_recente.get(id_linha)
			data += id_linha + ";" + horario + "\n"

		file_paradas_recentes = open("paradas_recentes.dat", "w")
		file_paradas_recentes.write(data)
		file_paradas_recentes.close()
						
			
		time.sleep(10)

#Cria um dicionario associando cada MAC ao codigo de uma linha
file_linhas = open("linhas.dat", "r")
linhas_lst = {}
linha_recente = {}
for line in file_linhas:
	fields = line.split(";")
	linha_id = fields[1].replace("\n", "")
	linhas_lst[fields[0]] = linha_id
	if(linha_recente.get(linha_id) == None):
		linha_recente[linha_id] = ""
print linhas_lst
print linha_recente

flag = False 
scanner = Scanner(loops=2)
curr_beacon = None
beacon_lst= {}
log = {}
thread = Thread(target = check_current_stops)
thread.start()
#Identifica os beacons proximo e salva no log
while True:
	for beacon in scanner.scan():
		fields = beacon.split(",")

		curr_beacon = beacon_lst.get(fields[0])
		if curr_beacon == None:
			beacon_lst[fields[0]] = Beacon(fields[0], fields[1], fields[2], fields[3], fields[5], fields[4])
		else:
			curr_beacon.rssi = fields[5]

		curr_stop = log.get(fields[0])
		if curr_stop == None :
			log[fields[0]] = [time.time(), time.time()]
		else:
			curr_stop[1] = time.time()
 
		print str(curr_beacon)

