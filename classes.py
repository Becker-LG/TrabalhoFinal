import random
import sqlite3 as lite
from banco import conexao

#SUDOKU =========================================================================================================================
class Sudoku:
    def __init__(self, status, lista1=None, lista2=None, lista3=None, lista4=None, lista5=None, lista6=None, lista7=None, lista8=None, lista9=None):
        self.matriz = [
            lista1 or [0] * 9,
            lista2 or [0] * 9,
            lista3 or [0] * 9,
            lista4 or [0] * 9,
            lista5 or [0] * 9,
            lista6 or [0] * 9,
            lista7 or [0] * 9,
            lista8 or [0] * 9,
            lista9 or [0] * 9,
        ]
        self.status = status

    def conferirSudoku(self):

        #verificando linhas
        for linha in self.matriz:
            if sorted(linha) != list(range(1, 10)):
                return False
        
        #verificando colunas
        for coluna in range(9):
            valoresColuna = []
            for linha in range(9):
                valoresColuna.append(self.matriz[linha][coluna])
            if sorted(valoresColuna) != list(range(1, 10)):
                return False

        #verificando quadrante
        for linha in range(0, 9, 3):
            for coluna in range(0, 9, 3):
                elementos = []
                for linha2 in range(linha, linha + 3):
                    for coluna2 in range(coluna, coluna + 3):
                        elementos.append(self.matriz[linha2][coluna2])
                if sorted(elementos) != list(range(1, 10)):
                    return False

        return True
    
    def gerarSudoku(self):
        def preencherGrade():
            for linha in range(9):
                for coluna in range(9):
                    if self.matriz[linha][coluna] == 0:
                        random.shuffle(numeros)
                        for num in numeros:
                            if self.conferirInserir(linha, coluna, num):
                                self.matriz[linha][coluna] = num
                                if preencherGrade():
                                    return True
                                self.matriz[linha][coluna] = 0
                        return False
            return True

        numeros = list(range(1, 10))
        preencherGrade()

    def conferirInserir(self, linha, coluna, num):
        if num in self.matriz[linha]:
            return False
        for i in range(9):
            if self.matriz[i][coluna] == num:
                return False
        subgradeLinha = 3 * (linha // 3)
        subgradeColuna = 3 * (coluna // 3)
        for i in range(subgradeLinha, subgradeLinha + 3):
            for j in range(subgradeColuna, subgradeColuna + 3):
                if self.matriz[i][j] == num:
                    return False
        return True
    
    def removerNumeros(self, quantidade):
        posicoes = [(linha, coluna) for linha in range(9) for coluna in range(9)]
        random.shuffle(posicoes)
        for i in range(quantidade):
            linha, coluna = posicoes[i] 
            self.matriz[linha][coluna] = 0 

#JOGADOR =========================================================================================================================
class Jogador:
    def __init__(self, user, qntdJogos, vit, der):
        self.__user = user
        self.qntdJogos = qntdJogos
        self.vit = vit
        self.der = der

    @property
    def user(self):
        return self.__user
    @user.setter
    def user(self, novo):
        self.__user = novo

    
    def insertJogador(self):
        with conexao:
            cur = conexao.cursor()
            query = f'''INSERT INTO users (user, qntdJogos, vit, der) 
                                        VALUES(?, ?, ?, ?)'''
            cur.execute(query, [self.__user, self.qntdJogos, self.vit, self.der])

#TENTATIVAS =========================================================================================================================
class Tentativa:
    def __init__(self, status):
        self.__status = status

    @property
    def status(self):
        return self.__status
    @status.setter
    def status(self, novo):
        self.__status = novo
