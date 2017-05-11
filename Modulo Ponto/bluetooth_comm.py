# -*- coding: utf-8 -*-

import bluetooth
import os
import time
from threading import *

#Função que trata uma conexão bluetooth
def connection_handle(client, adress):
	print "Accepted connection from ", address

	#Recebe um byte que diz se o aplicativo e de passageiro ou da empresa ('1' - empresa, '2' - passageiro)
	client_type = client.recv(1)

	packageSize = 1024

	#Se oaplicativo eh da empresa, envia o log completo das paradas e realiza um backup interno
	if client_type == '1' : 
		file_name = "log.dat"
		f = open(file_name, "rb")
		file_size = os.path.getsize(file_name)
		print "Sending file to ", address, "start at", time.ctime()	
		client.send("%05d" % file_size)
	
		packet = 1
		while(packet):
			packet = f.read(packageSize)
			client.send(packet)	
		f.close()
		print "Finished sending to ", address, "at", time.ctime()
		client.close()
	
		file_name_backup = "log-backup.dat"
		file_backup = open(file_name_backup, "w")
		file_log = open(file_name, "r")
		data = file_log.read()
		file_backup.write(data)
		file_backup.close()
		file_log.close()
		file_log = open(file_name, "w")
		file_log.close()
	#Se é o aplicativo do usuário, apenas manda os dados das últimas paradas de cada linha
	elif client_type == '2':
		file_name = "paradas_recentes.dat"
		f = open(file_name, "rb")
		file_size = os.path.getsize(file_name)
		print "Sending file to ", address, "start at", time.ctime()	
		client.send("%05d" % file_size)
	
		packet = 1
		while(packet):
			packet = f.read(packageSize)
			client.send(packet)	
		f.close()
		print "Finished sending to ", address, "at", time.ctime()
		client.close()
	

		
		
		
	
	
server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
server_sock.bind(("",bluetooth.PORT_ANY))
server_sock.listen(1)

bluetooth.advertise_service(server_sock, "SiMO_admin_service",
                     service_classes=[bluetooth.SERIAL_PORT_CLASS],
                     profiles=[bluetooth.SERIAL_PORT_PROFILE])

print "Advertising"

while True:
	client_sock, address = server_sock.accept()
	new_client = Thread(target = connection_handle, args=(client_sock, address))
	new_client.start();

server_sock.close()
