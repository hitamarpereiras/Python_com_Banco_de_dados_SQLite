from .connect_db import __CREATE_CONECTION__ 

class Client:
    def __init__(self, cpf, nome, email, dt_nascimento) -> None:
        self.cpf = cpf
        self.nome = nome.strip()
        self.email = email.strip()
        self.dt_nascimento = dt_nascimento

    def is_valid(self):
        if len(self.cpf) != 11:
            return False, 'CPF Invalido!'
        if '@' not in self.email:
            return False, 'Email Invalido!'
        if '/' not in self.dt_nascimento:
            return False, 'Data de Nascimento incorreta!'
        return True, None
        
def insert_values(client: Client):
    connect = __CREATE_CONECTION__() 
    cursor = connect.cursor()

    try:
        commandSQL = '''
            INSERT INTO Cliente(cpf, nome, email, nascimento) 
            VALUES (?, ?, ?, ?);'''

        cursor.execute(commandSQL, (client.cpf, client.nome, client.email, client.dt_nascimento))
        connect.commit()
            
        return 'Cliente inserido com sucesso!'

    except Exception as e:
        return f"ERRO = {e}"
    
    finally:
        if connect:
            cursor.close()
            connect.close()
        

def save_image_profile(dados):
    connect = __CREATE_CONECTION__()
    cursor = connect.cursor()

    try:
        commandSQL = "INSERT INTO Imagens (dados) VALUES (?);"

        cursor.execute(commandSQL, (dados,))
        connect.commit()

    except Exception as e:
        print(f"Erro IMG = {e}")

    finally:
        if connect:
            cursor.close()
            connect.close()