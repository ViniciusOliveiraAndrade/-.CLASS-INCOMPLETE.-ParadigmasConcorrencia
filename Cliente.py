import socket #Importa o socket
import sys #Importa a biblioteca do sistema
import pickle
from Util import *

ENDERECO = 'localhost'
PORTACONECCAO = 25256
TAMANHODADOS = 4800

def criar_coneccao(local_host, local_porta):
	HOST = local_host #host 
	PORTA = local_porta #porta

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Cria um TCP/IP socket

	server_address = (HOST, PORTA) # clia a tupla de dados para liagação do socket para a porta

	print('HOST: Conectando com: {} Na porta: {}'.format(*server_address)) #Impressão de status de conecção

	sock.connect(server_address) #Cria a conecção com o servidor

	return sock

def receber_dados(sock,tamanhoDados): #função para receber os dados compactados extrairlos
	data = sock.recv(tamanhoDados) # Recebe mensagem do usuario
	data = pickle.loads(data)
	print('\nHOST: Dados recebidos :{!r}'.format(data)) #imripme status
	return data

def enviar_dados(sock,dados):#função para enviar os dados ja compactados
	print('HOST: Dados enviandos {!r}'.format(dados)) #Imprime status da mensagem a ser enviado
	dado = pickle.dumps(dados)
	sock.sendall(dado) #reenvia mensagem

def fechar_coneccao(sock):
	print('HOST: Fechando conecção com o servidor') #imprime status de fechamento de cocencção
	sock.close() #Fecha a conecção 


def criar_cliente():
	sock = criar_coneccao(ENDERECO, PORTACONECCAO)

	try:
		dados = receber_dados(sock,TAMANHODADOS)
		dados.sort()
		enviar_dados(sock,dados)
	finally:
		fechar_coneccao(sock)

#***************************************************************************************************************


criar_cliente()