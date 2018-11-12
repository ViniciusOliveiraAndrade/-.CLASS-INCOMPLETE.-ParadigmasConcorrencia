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

	print('SERVER: Iniciando o servidor em: "{}" Na porta: "{}"\n'.format(*server_address)) #Impressão de status de inicialização

	sock.bind(server_address) #Cria a liagação ou inicia o socket no endereço e na porta 

	sock.listen(1) #ouvi a conecção com o  host, torna o socket em um servidor

	return sock

def pegar_usuario(sock):
	
	print('SERVER: Esperando por uma conecção') # imprime status de espera
	connection, client_address = sock.accept() # Espera por uma conecção com o host, e retorna se conectou e o endereço
	
	return connection, client_address

def receber_dados(connection,tamanhoDados): #função para receber os dados compactados extrairlos
	data = connection.recv(tamanhoDados) # Recebe mensagem do usuario
	data = pickle.loads(data)
	print('\nSERVER: Dados recebidos :{!r}'.format(data)) #imripme status
	return data
	
def enviar_dados(connection,dados):#função para enviar os dados ja compactados
	print('SERVER: Dados enviandos {!r}'.format(dados)) #Imprime status da mensagem a ser enviado
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

		dados = receber_dados(con,TAMANHODADOS)
		if dados: #se tiver dados entra
			pass
		else:
			print('SERVER: não recebeu msg do usuário', endereco) #imprime status
	finally:
		fechar_coneccao(con)

#***************************************************************************************************************

criar_server()