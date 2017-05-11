# -*- coding: utf-8 -*-

import time
import glob, os
import datetime


#Classe que representa uma parada
#	Atributos:
#		linha: Nome da linha
#		ponto: Nome do ponto
#		mac_onibus: Endereço MAC do beacon que estava no onibus
#		mac_ponto: Endereço MAC do modulo bluetooth do ponto
#		chegada: Data e hora de chegada do onibus no ponto
#		partida: Data e hora de partida do onibus do ponto
#	Metodos:
#		__init__: Construtor da classe, apenas inicializa os atributos
#		__str__: Sobrescreve o metodo str() padrao
#		toCsv:	Retorna uma string com os atributos separados por virgula	
class Parada(object) :

	def __init__(self):
		self.linha = ""
		self.ponto  = ""
		self.mac_onibus = ""
		self.mac_ponto = ""
		self.chegada = ""
		self.partida = ""

	def __str__(self):
		return "-----------------\n" \
				+ "Linha: " + self.linha + "\n" \
				+ "Ponto: " + self.ponto + "\n" \
				+ "MAC do onibus: " + self.mac_onibus + "\n" \
				+ "MAC do ponto: "+ self.mac_ponto + "\n" \
				+ "Chegada: " + self.chegada.strftime("%Y-%m-%d %H:%M:%S") + "\n" \
				+ "Partida: " + self.partida.strftime("%Y-%m-%d %H:%M:%S")

	def toCsv(self):
		return  self.ponto + "," + self.mac_ponto + "," + self.mac_onibus + "," + self.chegada.strftime("%H:%M:%S") + "," + self.partida.strftime("%H:%M:%S") + "\n"


#Convete uma string no formato Ano-mes-dia Hora-minuto-segundo para uma variavel do tipo datetime
def str2datetime(string) :
	return datetime.datetime.strptime(string, "%Y-%m-%d %H:%M:%S")

#Carrega os pontos do arquivo .dat e cria um dicionario indexado pelo MAC do ponto
pontos = {}
file_pontos = open("pontos.dat", "r")
for l in file_pontos :
	print l
	line = l.replace("\n","") 
	if line == "" :
		continue
	fields = line.split(";")
	print fields
	pontos[fields[1].upper()] = fields[0]
print pontos


#Abre todos os logs obtidos dos pontos (na pasta simo) e convete todos os registros para a classe "Parada"
os.chdir("simo")

paradas = []
for f in glob.glob("*.dat"):
	mac_ponto = f[:17].upper()
	print mac_ponto
	ponto = pontos[mac_ponto]
	
	print f
	log_file = open(f, "r") 

	for l in log_file:
		line = l.replace("\n", "")
		print l
		fields = line.split(";")
		print fields
		p = Parada()
		p.linha = fields[0]
		p.mac_onibus = fields[1]
		p.chegada = str2datetime(fields[2]) 
		p.partida = str2datetime(fields[3])
		p.mac_ponto = mac_ponto
		p.ponto = ponto
	
		paradas.append(p)
		print str(p)


#Filtra as paradas por linha e data
filtro = {}
for p in paradas:
	linha_data = (p.linha, p.chegada.strftime("%Y-%m-%d"))
	if filtro.get(linha_data) == None :
		filtro[linha_data] = []
	filtro[linha_data].append(p)

os.chdir("..")

#Salva os dados filtrados na pasta "csv_linha"
directory = "csv_linha"
try:
    os.stat(directory)
except:	
	os.mkdir(directory) 

os.chdir(directory)

cabecalho = "Ponto,MAC_Ponto,MAC_Onibus,Hor_Chegada,Hor_Partida\n"
for linha_data in filtro:
	csv_file = open(linha_data[0] + " " + linha_data[1] + ".csv", "a")
	csv_file.write(cabecalho)
	for p in filtro[linha_data] :
		csv_file.write(p.toCsv())
	csv_file.close()


	
#print paradas
	
		
	
