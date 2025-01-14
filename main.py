#CLASSES ==========================================================================================================================================================================================

from classes import Sudoku
from classes import Jogador
from classes import Tentativa

#BANCO DE DADOS ==========================================================================================================================================================================================

import sqlite3 as lite
from banco import conexao

#VARIÁVEIS BASE ==========================================================================================================================================================================================
users = []
sudokus = []

#FUNÇÕES ==========================================================================================================================================================================================

#CRUD =========================================================================================================================

#viewUsers =================================================================
def viewUser(user):
    view = []
    with conexao:
        cur = conexao.cursor()
        querry = "SELECT * FROM users WHERE user=?"
        cur.execute(querry, (user,))
        informacoes = cur.fetchall()
        for i in informacoes:
            view.append(i)
    return view

#updateUser =================================================================
def updateUser(i):
    with conexao:
        cur = conexao.cursor()
        querry = "UPDATE users SET user=? WHERE user=?"
        cur.execute(querry, i)

#updateUserJogos =================================================================
def updateUserJogos(i):
    with conexao:
        cur = conexao.cursor()
        querry = "UPDATE users SET qntdJogos=? WHERE user=?"
        cur.execute(querry, i)

#updateUserVit =================================================================
def updateUserVit(i):
    with conexao:
        cur = conexao.cursor()
        querry = "UPDATE users SET vit=? WHERE user=?"
        cur.execute(querry, i)
#updateUserDer =================================================================
def updateUserDer(i):
    with conexao:
        cur = conexao.cursor()
        querry = "UPDATE users SET der=? WHERE user=?"
        cur.execute(querry, i)

#deleteUsers =================================================================
def deleteUser(user):
    with conexao:
        cur = conexao.cursor()
        querry = "DELETE FROM users WHERE user=?"
        cur.execute(querry, (user,))
    return 'break'

#Restante =========================================================================================================================

#Novo Sudoku =================================================================
def novoSudoku(sudoku):
    
    users[0].qntdJogos += 1
    updateUserJogos([users[0].qntdJogos, users[0].user])
    sudokus[0].status = 0
    tentativa = Tentativa(0)
    x = 0

    while sudoku.conferirSudoku() == False:
        for linha in sudoku.matriz:
            print(linha)

        print('Para sair, digite qualquer letra.')
        print('Para editar a nova posição, insira o eixo X e o eixo Y.')
        try:
            linha = int(input('Linha: '))-1
            coluna = int(input('coluna Y: '))-1
            num = int(input('Novo Número: '))
        except ValueError:
            print('Não foi inserido um número! Saindo do Sudoku!')
            users[0].der += 1
            updateUserDer([users[0].der, users[0].user])
            x += 1
            break

        if sudoku.conferirInserir(linha, coluna, num) == False:
            print('Não é possível inserir o número nesta posição!')
            print('Ação Cancelada!')
        else:
            sudoku.matriz[linha][coluna] = num
            print('Número Inserido!')
        print('')

    if x == 1:
        return
    
    print('Sudoku Resolvido!!!')
    tentativa.status = 1
    sudokus[0].status = 1
    users[0].vit += 1
    updateUserVit([users[0].vit, users[0].user])



    return

#Jogador =================================================================
def acessarJogador(userX):
    print('''
O que você deseja fazer com o jogador?
          Para Deletar, digite "DELETAR";
          Para Editar, digite "EDITAR";
          Para Visualizar, digite "VISUALIZAR".''')
    opcao = input('')

    if opcao.upper() == 'DELETAR':
        print('Você tem certeza? (sim/não)')
        escolha = input('')
        if escolha.upper() == 'SIM':
            return deleteUser(userX)
        elif escolha.upper() == 'NÃO':
            print('Ação Cancelada!')
        else:
            print('Opção Inválida!')
        return

    elif opcao.upper() == 'EDITAR':
        novoUser = input('Insira o novo nome do jogador: ')
        return updateUser([novoUser, userX])
    
    elif opcao.upper() == 'VISUALIZAR':
        view = viewUser(userX)
        print(f'''
Nome: {view[0][0]}
Quantidade de Jogos: {view[0][1]}
Vitórias: {view[0][2]}
Derrotas: {view[0][3]}''')
        return
    else:
        print('Opção Inválida!')
    return

#BASE ==========================================================================================================================================================================================

print('''
Seja bem-vindo ao Sudoku!
Para jogar, você deve criar ou acessar um usuário: ''')

user = input('')
if viewUser(user) != []:
    print('Usuário acessado!')
    jogador = viewUser(user)[0]
    users.append(Jogador(jogador[0], int(jogador[1]), int(jogador[2]), int(jogador[3])))
else:
    users.append(Jogador(user, 0, 0, 0))
    users[0].insertJogador()
    print('Usuário novo cadastrado!')

while True:
    print('''
Para seguir adiante, digite uma das opções:
          Para criar um novo sudoku, digite: "novo";
          Para acessar o jogador, digite "jogador";
          Para sair, digite "sair".
        ''')
    opcao = input('')

    if opcao.upper() == 'NOVO':
        sudoku = Sudoku(0)
        sudoku.gerarSudoku()
        sudokus.append(sudoku)
        try:
            num = int(input('Insira a quantidade de números que serão retirados: '))
        except ValueError:
            print('Valor Inválido!')
            continue
        
        sudoku.removerNumeros(num)

        novoSudoku(sudoku)
        
    elif opcao.upper() == 'JOGADOR':
        if acessarJogador(user) == 'break':
            break
    elif opcao.upper() == 'SAIR':
        break
    else:
        print('Opção Inválida!')