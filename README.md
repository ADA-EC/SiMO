                                             # SiMO
Códigos do projeto SiMO (Sistema de Monitoramento de Onibus) do grupo ADA para o concurso Be An Icon

# Instalação

O grupo utilizou o Ubuntu 14.04 para a criaçãos dos códigos.
Para executá-los, é necessário instalar a biblioteca bluez para python com a seguinte linhas de código:

sudo apt-get install python-bluez

sudo apt-get install python-numpy

sudo apt-get install python-scipy


# Arquitetura

	O sistema é composto de 4 partes principais sendo elas: módulo de processamento do ponto de ônibus, linhas de ônibus com beacons identificadores, aplicativos de celular para o usuário e o administrador e o processamento em um servidor de processamento central dos arquivos de log.

	Módulo de processamento do ponto de ônibus
		"simo.py" é responsável  pela identificação dos beacons (ônibus) e salvar as paradas em um log, também é responsável por manter o log de últimas paradas atualizados.
		"blescan.py" é uma biblioteca responsável por escanear os beacons próximos
		"log.dat" é o arquivo de log das paradas de ônibus realizadas naquele ponto
		"linhas.dat" é um arquivo que associa um endereço MAC de um beacon a uma linha de ônibus
		"paradas_recentes.dat" é um arquivo que salva apenas as  ultimas paradas de cada linha no ponto em questão (informação que será enviada para o usuário
		"bluetooth_comm.py" faz a comunicação do raspberry do ponto com os aplicativos de celular, tanto para enviar os ultimos ônibus
	
	Aplicativos: Existem dois aplicativos, um para o passageiro, que recebe apenas os últimos ônibus que passaram no ponto em que ele se conectou, e um para o administrador, que resgata todo o registro de paradas do ponto

	Servidor de processamento central
		"log2csv.py" realiza a leitura de todos os arquivos de log coletados e organiza em arquivos csv para cada dia de cada linha de onibus permitindo assim a análise dos dados por programas de planilhas.
		"clustering_stops.py" realiza a leitura dos arquivos de log de cada ponto e gera umas estimativa dos horário em que cada linha passa no ponto.
		"pontos.dat" é um arquivo que relaciona um ponto ao endereço MAC de seu módulo

	
# Implementação
	A maior parte do projeto é feita em python, com exceção dos aplicativos, onde utilizamos o MIT App Inventor 2

# Execução
	Para ativar as funcionalidades do modulo do ponto de onibus devem ser executadas as seguintes linhas de código:
		sudo python simo.py
		python bluetooth_comm.py
		
	Para organizar as informaçoes coletadas a partir do servidor central é preciso executar a seguinte linha de codigo:
		python log2csv.py
		python clustering_stops.py
		
	Os aplicativos devem ser utilizados em dispositivos android que deve ser confiigurado para permitir a instalação de aplicativos de fontes não confiáveis, então basta o download do .apk no smartphone e executá-lo.
