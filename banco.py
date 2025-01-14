import sqlite3 as lite

con = lite.connect('sudoku.db')

with con:
    cur = con.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user VARCHAR(45) PRIMARY KEY NOT NULL,
        qntdJogos INT NOT NULL,
        vit INT NOT NULL,
        der INT NOT NULL
    )
    ''')

conexao = lite.connect('sudoku.db')