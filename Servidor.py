import socket
from _thread import *
import sys

server = "0.0.0.0"  # Debe ser la dirección IP del servidor
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Esperando una conexión, Servidor Iniciado")

# Esta es la posición inicial del objeto en el juego
positions = [50, 50]

def threaded_client(conn):
    conn.send(str.encode(str(positions)))
    reply = ""
    while True:
        try:
            data = eval(conn.recv(2048).decode())
            positions[0] = data[0]
            positions[1] = data[1]
            if not data:
                print("Desconectado")
                break
            else:
                reply = positions
                print("Recibido: ", data)
                print("Enviando : ", reply)
            conn.sendall(str.encode(str(reply)))
        except:
            break

    print("Conexión perdida")
    conn.close()

while True:
    conn, addr = s.accept()
    print("Conectado a:", addr)

    start_new_thread(threaded_client, (conn,))
