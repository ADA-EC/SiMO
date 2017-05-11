#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy
import scipy.cluster.hierarchy as hcluster
import datetime
import glob, os
import time


# Grava a relação entre o nome do ponto e o MAC do módulo para a memória
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
# print pontos


# Para cada arquivo de log de um módulo realiza o clustering dos horários das paradas
os.chdir("simo")
for f in glob.glob("*.dat"):
	log_file = open(f, "r")
	stops_lists = {}
	# Gera um dicionário com chave o ID da linha e como valor uma lista com o horário das paradas
	for line in log_file:
		data = line.split(";")
		linha = data[0]
		mac = data[1]
		horario = data[2].split(" ")[1].split(":")
		seg_horario = int(horario[0])*3600 + int(horario[1])*60 + int(horario[2])
		curr_linha_stop_list = stops_lists.get(linha)
		if(curr_linha_stop_list == None):
			stops_lists[linha] = [seg_horario]
		else:
			curr_linha_stop_list.append(seg_horario)	
	log_file.close()

	
	os.chdir("..")
	directory = "media_paradas"
	try:
    		os.stat(directory)
	except:	
		os.mkdir(directory) 
	os.chdir(directory)

	mac_ponto = f[:17].upper()
	filename_paradas = pontos[mac_ponto] + "_media_paradas.csv"

	# Executa o algoritmo de agrupamento para cada linha
	file_stops = open(filename_paradas, "w") 
	thresh = 150
	for linha in stops_lists:
		stops = numpy.asarray([[float(i)] for i in stops_lists.get(linha)])
		#print stops
		clusters = hcluster.fclusterdata(stops, thresh, criterion='distance')
		num_sets = len(set(clusters))
		clusters = clusters.tolist()
	
		stops = stops_lists.get(linha)
		avg = [0] * num_sets
		num_elem = [0] * num_sets
		for i in range(len(stops)):
			index = clusters[i]-1
			avg[index] += stops[i]
			num_elem[index] += 1
			#print clusters[i], stops[i], num_elem[index], avg[index]
	
		for i in range(num_sets):
			avg[i] = avg[i]/num_elem[i]
		avg.sort()
	
		horario_parada = [0] * num_sets
		paradas = linha
		for i in range(num_sets):
			horario_parada[i] = str(avg[i]/3600) + ':' + str((avg[i] % 3600) / 60) + ':' + str(avg[i] % 60) 
			paradas += ';' + horario_parada[i]
		paradas += '\n'
		file_stops.write(paradas)
	
	file_stops.close()

	os.chdir("..")
	os.chdir("simo")
