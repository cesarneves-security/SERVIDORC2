# Servidor C2 com SSL
---
#SERVIDOR C2
Este é um projeto de servidor C2 (Command and Control) com suporte a SSL, desenvolvido em Python, que permite a comunicação segura entre um servidor e seus clientes para execução remota de comandos. O objetivo deste projeto é educacional e deve ser utilizado com ética e responsabilidade em ambientes controlados.

## Funcionalidades
- **Comunicação Segura com SSL**: O servidor e o cliente utilizam SSL para criptografar as comunicações, garantindo segurança contra interceptação de dados.
- **Execução Remota de Comandos**: O servidor envia comandos ao cliente, que os executa e retorna o resultado.
- **Transferência de Arquivos**: O cliente pode enviar arquivos ao servidor quando solicitado.
- **Função de Autodestruição**: O cliente possui uma função `selfdestruct`, que remove o próprio arquivo.
- **Coleta de Informações do Cliente**: O cliente coleta e envia informações sobre o sistema ao servidor, incluindo IP, nome de usuário, sistema operacional, entre outros.

## Estrutura do Projeto
- `__cliente__.py`: Código do cliente que se conecta ao servidor, recebe e executa comandos.
- `__server__.py`: Código do servidor que gerencia conexões, envia comandos e recebe dados dos clientes.
- `server.crt` e `server.key`: Certificados SSL usados para autenticar e criptografar a conexão.

## Como Usar
1. Clone o repositório:
```bash
git clone https://github.com/cesarneves-security/SERVIDORC2.git
```
2. Navegue até o diretório do projeto:
```bash
cd SERVIDORC2
```
3. Executar o Cliente:
```bash
python3 __cliente__.py
```
4. Executar o Server:
```bash
python3 __server__.py
```
3. Criar executavel .exe
```bash
pyinstaller --onefile __server__.py ou __cliente__.py
```

### Pré-requisitos
1. **Python 3.x**: Certifique-se de ter o Python 3.x instalado no sistema.
2. **Certificados SSL**: Gere um certificado e uma chave SSL para configurar a comunicação segura entre o cliente e o servidor. Exemplo de comando:
   ```bash
   openssl req -new -x509 -keyout server.key -out server.crt -days 365 -nodes

### Contribuição
Se você encontrar algum problema ou tiver sugestões de melhoria, sinta-se à vontade para abrir uma issue ou enviar um pull request