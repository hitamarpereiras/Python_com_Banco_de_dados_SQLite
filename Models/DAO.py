from Models import connect_db as cdb
import os
from PIL import Image
from io import BytesIO

class UserDAO:
    def __init__(self, name, email, password, date_birth, picture, course, comment):
        self.name = name.strip()
        self.email = email.strip()
        self.password = password.strip()
        self.date = date_birth
        self.picture = picture
        self.course = course
        self.comment = comment

    def is_valid(self):
        if '@' not in self.email:
            return False, 'Invalid email!'
        if len(self.password) < 8:
            return False, 'Password must be 8 characters long'
        if '/' not in self.date:
            return False, 'Invalid Date!'
        if not self.picture:
            return False, 'Invalid profile photo!'
        if not self.course:
            return False, 'Choose a course!'
        else:
            return True, None
        
def add_client(client: UserDAO):
    try:
        conn = cdb.connection_on()
        cursor = conn.cursor()
        cursor.execute('PRAGMA foreign_key = on')

        with open(client.picture, mode='rb') as bytes:
            photo = bytes.read()

        command_1 = "INSERT INTO Clientes (nome, email, senha, nascimento, foto) VALUES (?, ?, ?, ?, ?);"

        command_2 = "INSERT INTO Cursos (cliente_id, titulo, comentario) VALUES (?, ?, ?);"

        cursor.execute(command_1, (client.name, client.email, client.password, client.date, photo))
        user_id = cursor.lastrowid
        cursor.execute(command_2, (user_id, client.course, client.comment))
        conn.commit()

        return True, f"{client.name}, registered successfully!"

    except Exception as e:
        print(e)
        return False, f"[ERROR] = {e}"
    
    finally:
        cursor.close()
        conn.close()

def search_client(client_id):
    try:
        conn = cdb.connection_on()
        cursor = conn.cursor()
        cursor.execute('PRAGMA foreign_key = on')

        command = "SELECT * FROM Clientes WHERE id = ?"
        cursor.execute(command, (client_id,))

        """ Vai criar um caminho pra salvar as imagens """
        client = cursor.fetchone()
        path = 'Data'
        folder = os.path.join(path, 'profiles')
        os.makedirs(folder, exist_ok=True)

        if client:
            img = Image.open(BytesIO(client[5]))
            img.save(os.path.join(folder, f"photo_{client_id}.jpg"), "JPEG")
            return client, f"photo_{client_id}.jpg"
        else:
            return False, "Not found! :("

    except Exception as e:
        print(e)
        return f"[ERROR] = {e}"
    
    finally:
        cursor.close()
        conn.close()

def update_client(cliente: UserDAO):
    try:
        conn = cdb.connection_on()
        cursor = conn.cursor()
        cursor.execute('PRAGMA foreign_key = on')

        command = ""
    except Exception as e:
        return f"[ERROR] = {e}"