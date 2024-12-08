import sqlite3 as sql
import os

def connection_on():
    try:
        path = 'Data'
        destiny = os.path.join(path, 'database')
        os.makedirs(destiny, exist_ok=True)
        database = os.path.join(destiny, 'database.db')
        conn = sql.connect(database)

        return conn
    
    except PermissionError:
        return 'Without system permission'
    except Exception as e:
        return f"\033[31m[ERROR] = {e}\033[m"
    
def create_table(conn = connection_on()):
    try:
        cursor = conn.cursor()

        command_1 = '''
            CREATE TABLE IF NOT EXISTS Clientes(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL,
            senha TEXT NOT NULL,
            nascimento TEXT NOT NULL,
            foto BLOB);'''
        
        command_2 = '''
            CREATE TABLE IF NOT EXISTS Cursos(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER NOT NULL,
            titulo TEXT NOT NULL,
            comentario TEXT NOT NULL,
            FOREIGN KEY (cliente_id) REFERENCES clientes (id) ON DELETE CASCADE
            );'''
        
        cursor.execute(command_1)
        cursor.execute(command_2)
        conn.commit()

        return 'Created successfully'
        
    except sql.Error as e:
        return f"\033[31m[ERROR SQL] = {e}\033[m"
    except Exception as e:
        return f"\033[31m[ERROR] = {e}\033[m"
    
    finally:
        cursor.close()
        conn.close()

#start = create_table()
#print(start)