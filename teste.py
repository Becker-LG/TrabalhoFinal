import random

class Sudoku:
    def __init__(self, lista1=None, lista2=None, lista3=None, lista4=None, lista5=None, lista6=None, lista7=None, lista8=None, lista9=None):
        # A matriz é uma lista de listas que representa o tabuleiro do Sudoku
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
        self.sudoku = []

    def conferirSudoku(self):
        # Função para verificar se o Sudoku está correto
        return self._linhas_validas() and self._colunas_validas() and self._subgrades_validas()

    def _linhas_validas(self):
        # Verifica se todas as linhas contêm os números de 1 a 9 sem repetições
        for linha in self.matriz:
            if sorted(linha) != list(range(1, 10)):
                return False
        return True

    def _colunas_validas(self):
        # Verifica se todas as colunas contêm os números de 1 a 9 sem repetições
        for coluna in range(9):
            if sorted(self.matriz[linha][coluna] for linha in range(9)) != list(range(1, 10)):
                return False
        return True

    def _subgrades_validas(self):
        # Verifica se cada subgrade 3x3 contém os números de 1 a 9 sem repetições
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
        
        #Tive que pesquisar para conseguir utilizar o método de backtracking
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
        self.sudoku = self.matriz

    def conferirInserir(self, linha, coluna, num):
        # Verifica se 'num' pode ser inserido na posição [linha][coluna]
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
        # Remove uma quantidade específica de números aleatórios da grade para criar um desafio
        posicoes = []
        for linha in range(9):
            for coluna in range(9):
                posicoes.append((linha, coluna))
        random.shuffle(posicoes)
        for linha, coluna in posicoes[:quantidade]:
            self.sudoku[linha][coluna] = 0

# Exemplo de uso
sudoku = Sudoku()
sudoku.gerarSudoku()
sudoku.removerNumeros(40)

for linha in sudoku.matriz:
    print(linha)
print('')
for linha in sudoku.sudoku:
    print(linha)


# Exemplo de uso
sudoku_exemplo = Sudoku(
    [5, 3, 4, 6, 7, 8, 8, 1, 2],
    [6, 7, 2, 1, 9, 5, 3, 4, 8],
    [1, 9, 8, 3, 4, 2, 5, 6, 7],
    [8, 5, 9, 7, 6, 1, 4, 2, 3],
    [4, 2, 6, 8, 5, 3, 7, 9, 1],
    [7, 1, 3, 9, 2, 4, 8, 5, 6],
    [9, 6, 1, 5, 3, 7, 2, 8, 4],
    [2, 8, 7, 4, 1, 9, 6, 3, 5],
    [3, 4, 5, 2, 8, 6, 1, 7, 9]
)

#for linha in sudoku_exemplo.matriz:
#    print(linha)
#sudoku_exemplo.removerNumeros(20)
#
#print('')
#
#for linha in sudoku_exemplo.matriz:
#    print(linha)
#
#print('')
#
#for linha in sudoku_exemplo.sudoku:
#    print(linha)

print("Sudoku está correto:", sudoku.conferirSudoku())
