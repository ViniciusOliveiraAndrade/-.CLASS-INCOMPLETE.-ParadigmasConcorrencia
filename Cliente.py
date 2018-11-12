import socket #Importa o socket
import sys #Importa a biblioteca do sistema
import pickle
import threading

from Util import *

ENDERECO = 'localhost'
PORTACONECCAO = 25255
TAMANHODADOS = 4800

#***************************************************************************************************************
#Cliente

def criar_coneccao(local_host, local_porta): #função para criar a conecção com o servidor
	HOST = local_host #host 
	PORTA = local_porta #porta

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Cria um TCP/IP socket

	server_address = (HOST, PORTA) # clia a tupla de dados para liagação do socket para a porta

	print('HOST: Conectando com: {} Na porta: {}'.format(*server_address)) #Impressão de status de conecção

	sock.connect(server_address) #Cria a conecção com o servidor

	return sock

def receber_dados(sock,tamanhoDados, numero): #função para receber os dados compactados extrairlos
	data = sock.recv(tamanhoDados) # Recebe mensagem do usuario
	data = pickle.loads(data)
	print('\nHOST: Thread {} recebeu os dados:{!r}'.format(numero,data)) #imripme status
	return data

def enviar_dados(sock,dados,numero):#função para enviar os dados ja compactados
	print('HOST: Dados enviandos da Thread {}:{!r}'.format(numero,dados)) #Imprime status da mensagem a ser enviado
	dado = pickle.dumps(dados)
	sock.sendall(dado) #reenvia mensagem

def fechar_coneccao(sock): #Função para fechar a conecção
	print('HOST: Fechando conecção com o servidor') #imprime status de fechamento de cocencção
	sock.close() #Fecha a conecção 


def criar_cliente(): #Funcção para criar um cliente bease
	sock = criar_coneccao(ENDERECO, PORTACONECCAO)

	try:
		dados = receber_dados(sock,TAMANHODADOS)
		dados.sort()
		enviar_dados(sock,dados)
	finally:
		fechar_coneccao(sock)

#***************************************************************************************************************
#Thread

def ordenar_dados(sock,tamanhoDados ,numero):
	dados = receber_dados(sock,tamanhoDados, numero)
	dados.sort()
	enviar_dados(sock,dados,numero)





#***************************************************************************************************************


sock = criar_coneccao(ENDERECO,PORTACONECCAO)

try:
	t1 = threading.Thread(target = ordenar_dados, name = 'THREAD 1', args = (sock,TAMANHODADOS,'1'))
	t2 = threading.Thread(target = ordenar_dados, name = 'THREAD 2', args = (sock,TAMANHODADOS,'2'))
	t3 = threading.Thread(target = ordenar_dados, name = 'THREAD 3', args = (sock,TAMANHODADOS,'3'))
	
	t1.start()
	t2.start()
	t3.start()
finally:
	
	t1.join()
	t2.join()
	t3.join()

	fechar_coneccao(sock)
	