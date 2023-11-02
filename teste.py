import socket
import threading

# Endereço IP e porta para o servidor
host = '10.113.60.204'  # Endereço IP do servidor
porta = 12345  # Porta do servidor

# Lista de amigos
lista_amigos = {
    'alanna': '10.113.60.204',
    'xandao': '10.113.60.230',
    'flavio': '10.113.60.221',
    'guilherme':'10.113.60.202'
}

# Cria um objeto socket UDP
socket_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Liga o socket ao endereço e porta especificados
socket_server.bind((host, porta))

print(f"Servidor UDP aguardando mensagens em {host}:{porta}")

# Função para receber mensagens
def receber_mensagens():
    while True:
        try:
            # Recebe os dados e o endereço do remetente
            dados, endereco = socket_server.recvfrom(1024)  # Tamanho do buffer é 1024 bytes

            mensagem = dados.decode('utf-8')
            print(f"Recebido de {endereco[0]}:{endereco[1]}: {mensagem}")

        except UnicodeDecodeError:
            print(f"Recebido de {endereco[0]}:{endereco[1]}: Erro de decodificação (não UTF-8)")

# Inicializa uma thread para receber mensagens
thread_recebimento = threading.Thread(target=receber_mensagens)
thread_recebimento.daemon = True
thread_recebimento.start()

# Função para enviar mensagens
def enviar_mensagens():
    cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    while True:
        nome_amigo = input("Digite o nome da pessoa para enviar mensagem: ")
        if nome_amigo == "/sair":
            print("Encerrando o programa...")
            print("Fechando portas de escuta:")
            thread_recebimento.join()
            break
        elif nome_amigo in lista_amigos:
            destino_ip = lista_amigos[nome_amigo]
            mensagem = input("Digite a mensagem a ser enviada: ")
            cliente_socket.sendto(mensagem.encode('utf-8'), (destino_ip, porta))
        else:
            print("Nome de amigo inválido. Tente novamente.")

# Inicializa uma thread para enviar mensagens
thread_envio = threading.Thread(target=enviar_mensagens)
thread_envio.start()

# Aguarda as threads finalizarem
thread_envio.join()
print("Threads encerradas.")
# Feche o socket (isso nunca será executado no loop acima)
socket_server.close()
print("Socket encerrado. Bye Bye")