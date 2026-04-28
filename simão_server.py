import socket

# Configurações do Robô
IP_ROBO = "192.168.0.220" # Escuta em todas as interfaces de rede do robô
PORTA = 5005

# 1. Cria o Socket UDP
# AF_INET = IPv4 | SOCK_DGRAM = Protocolo UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 2. Faz o 'Bind' (Abre a porta física no sistema operacional)
sock.bind((IP_ROBO, PORTA))

print(f"Robô aguardando comandos UDP na porta {PORTA}...")

try:
    while True:
        dados, endereco_origem = sock.recvfrom(1024)
        
        # Os dados chegam em bytes, precisamos decodificar para texto
        comando = dados.decode('utf-8')
        
        print(f"Comando recebido: '{comando}' veio da IHM no IP: {endereco_origem}")
        

except KeyboardInterrupt:
    print("\nDesligando receptor do robô.")
finally:
    sock.close()