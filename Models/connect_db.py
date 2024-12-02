import os
import sqlite3 as sql
from time import sleep

def __CREATE_CONECTION__():
    try:
        PATH = 'Data'
        os.makedirs(PATH, exist_ok=True)
        bd = os.path.join(PATH, 'database.db')
        connect_db = sql.connect(bd)

        return connect_db

    except PermissionError:
        return 'Erro de permissao!'
    except Exception as e:
        return f"{e}"

def create_tables():
    connect = __CREATE_CONECTION__()
    if not connect:
        return 'Erro de conexao'
    try:
        cursor = connect.cursor()
        
        command_1 = """
            CREATE TABLE IF NOT EXISTS Cliente(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cpf INTEGER NOT NULL,
                nome TEXT NOT NULL,
                email TEXT NOT NULL,
                nascimento TEXT NOT NULL,
                id_imagem INTEGER,
                FOREIGN KEY (id_imagem) REFERENCES Imagens (id));"""
        
        command_2 = """
            CREATE TABLE IF NOT EXISTS Imagens(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dados BLOB);"""
        
        cursor.execute(command_2)
        cursor.execute(command_1)
        connect.commit()

        return 'Processo concluido com sucesso!'
    except sql.Error as e:
        return f"ERRO = {e}"
    
    finally:
        if connect:
            cursor.close()
            connect.close()

print(create_tables())