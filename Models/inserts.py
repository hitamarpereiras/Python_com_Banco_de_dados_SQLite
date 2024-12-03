from .connect_db import __CREATE_CONECTION__ 
from io import BytesIO
from PIL import Image
import os

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
    
""" INSERIR VALORES """     
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
        
""" INSERIR IMAGEM DO PERIL """
def save_image_profile(dados):
    connect = __CREATE_CONECTION__()
    cursor = connect.cursor()

    try:
        with open(dados, mode='rb') as file:
            data = file.read()

        commandSQL = "INSERT INTO Imagens (dados) VALUES (?);"

        cursor.execute(commandSQL, (data,))
        connect.commit()

    except Exception as e:
        return  f"Erro IMG = {e}"

    finally:
        if connect:
            cursor.close()
            connect.close()

""" UPDATE CLIENTE """
def update_client(cliente: Client):
    connect = __CREATE_CONECTION__()
    cursor = connect.cursor()

    try:
        commandSQL = """
            UPDATE Cliente (cpf, nome, email, nascimento)
            VALUES (?, ?, ?, ?);
            """
        cursor.execute(commandSQL, cliente.cpf, cliente.nome, cliente.email, cliente.dt_nascimento)
        connect.commit()

    except Exception as e:
        return f"Error = {e}"
    finally:
        cursor.close()
        connect.close()

# Procurar Clientes
def search_client(id):
    connect = __CREATE_CONECTION__()
    cursor = connect.cursor()
    cursor.execute('PRAGMA foreign_key = on')
    try:
        comamndSQL = "SELECT * FROM Cliente WHERE id = ?"  
        cursor.execute(comamndSQL, (id,))

        cliente =  cursor.fetchone()
        if cliente:
            return cliente
        else:
            return "Nao encontrado!"
        
    except Exception as e:
        return f"ERROR = {e}"
    finally:
        cursor.close()
        connect.close()

# converter dados e salvar
def convert_binary_to_image(id,img_data):
    try:
        # Converte os dados binários em imagem 
        img = Image.open(BytesIO(img_data))
        path = 'Data'
        destani = os.path.join(path, 'profiles')
        os.makedirs(destani, exist_ok=True)
        # Salvar como arquivo para testes
        img.save(os.path.join(destani, f"profile{id}.jpg"), "JPEG")
        return f"profile{id}.jpg"
    
    except Exception as e:
        print(f"Erro ao converter dados binários para imagem: {e}")
        return None
    
# Buscar fotoo de perfil
def search_image(id):
    connect = __CREATE_CONECTION__()
    cursor = connect.cursor()
    
    try:
        comamndSQL = "SELECT * FROM Imagens WHERE id = ?"
        cursor.execute(comamndSQL, (id,))

        img =  cursor.fetchone()
        if img:
            imgd = convert_binary_to_image(id, img[1])
            return imgd
        else:
            return False
        
    except Exception as e:
        return f"ERROR = {e}"
    finally:
        cursor.close()
        connect.close()
