from random import randint

def criar_dados(LINHAS,COLUNAS):
	dados = []
	while len(dados) != LINHAS:
		linha = []
		while len(linha) != COLUNAS:
			numero = randint(0, 100)
			if numero not in linha:
				linha.append(numero)
		dados.append(linha)
	return dados


def imprime_dados(dados):
	for dado in dados:
		print(" ".join(str(dado)))