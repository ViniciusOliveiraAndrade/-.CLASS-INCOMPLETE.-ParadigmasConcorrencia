import socket #Importa o socket
import sys #Importa a biblioteca do sistema
import pickle
import threading

from Util import *

ENDERECO = 'localhost'
PORTACONECCAO = 25255
TAMANHODADOS = 4800
DADOSENVIAR = criar_dados(9,10)

#***************************************************************************************************************
#Servidor
def criar_coneccao(local_host, local_porta):
	HOST = local_host #host 
	PORTA = local_porta #porta

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Cria um TCP/IP socket

	server_address = (HOST, PORTA) # clia a tupla de dados para liagação do socket para a porta

	print('\nSERVER: Iniciando o servidor em: "{}" Na porta: "{}"\n'.format(*server_address)) #Impressão de status de inicialização

	sock.bind(server_address) #Cria a liagação ou inicia o socket no endereço e na porta 

	sock.listen(3) #ouvi a conecção com o  host, torna o socket em um servidor

	return sock

def pegar_usuario(sock): #função para receber o Usuario da conecção
	
	print('SERVER: Esperando por uma conecção') # imprime status de espera
	connection, client_address = sock.accept() # Espera por uma conecção com o host, e retorna se conectou e o endereço
	
	return connection, client_address

def receber_dados(connection,tamanhoDados, host): #função para receber os dados compactados extrairlos
	data = connection.recv(tamanhoDados) # Recebe mensagem do usuario
	data = pickle.loads(data)
	print('\nSERVER: Dados :{!r}. Recebido do HOST {}'.format(data,host)) #imripme status
	return data
	
def enviar_dados(connection,dados, host):#função para enviar os dados ja compactados
	print('SERVER: Dados enviandos {!r} para o HOST {}.'.format(dados,host)) #Imprime status da mensagem a ser enviado
	dado = pickle.dumps(dados)
	connection.sendall(dado) #reenvia mensagem

def fechar_coneccao(con):
	print("SERVER: Fechando e limpando conecção para proximo HOST")
	con.close()# fecha a conecção

def criar_server():
	sock = criar_coneccao(ENDERECO,PORTACONECCAO)
	con, endereco = pegar_usuario(sock)
	try:
		print('SERVER: Conectado com', endereco) # Imime status de conecção
		matriz = criar_dados(10,10)
		enviar_dados(con,matriz[0])
		enviar_dados(con,matriz[1])
		enviar_dados(con,matriz[2])

		dados = receber_dados(con,TAMANHODADOS)
		dados = receber_dados(con,TAMANHODADOS)
		dados = receber_dados(con,TAMANHODADOS)
		if dados: #se tiver dados entra
			pass
		else:
			print('SERVER: não recebeu msg do usuário', endereco) #imprime status
	finally:
		fechar_coneccao(con)

#***************************************************************************************************************
#Thread

def getDado():
	return DADOSENVIAR.pop()

def usuario(sock, nome):
	con, endereco = pegar_usuario(sock)
	try:
		print('\nSERVER: Conectado com o HOTS {} no endereço: {}'.format(nome,endereco)) # Imime status de conecção

		dados_enviados = 0
		while dados_enviados < 3:
			enviar_dados(con,getDado(),nome)
			dados_enviados += 1
		
		dados_recebidos = 0
		while dados_recebidos < 3:
			dados = receber_dados(con,TAMANHODADOS, nome)
			if dados: #se tiver dados entra
				pass
			else:
				print('SERVER: Não recebeu dados do HOST {} no endereço: {}'.format(nome, endereco)) #imprime status
			dados_recebidos += 1
	finally:
		fechar_coneccao(con)

#***************************************************************************************************************

# criar_server()

sock = criar_coneccao(ENDERECO,PORTACONECCAO)
lista_hosts = []
numero_hosts = 0

while numero_hosts < 3:
	t = threading.Thread(target = usuario, name = 'THREAD {}'.format(numero_hosts), args = (sock,'{}'.format(numero_hosts)))
	lista_hosts.append(t)
	t.start()
	numero_hosts += 1

# for t in lista_hosts:
# 	t.join()

