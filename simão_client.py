import socket
import time

# Configurações do Destino (Onde o robô está?)
# Substitua pelo IP real do robô na rede (ex: '192.168.1.100')
IP_ROBO = "192.168.0.220" 
PORTA_ROBO = 5005

# 1. Cria o Socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

comandos = ["FRENTE", "FRENTE", "ESQUERDA", "PARAR"]

print(f"IHM iniciada. Enviando dados para {IP_ROBO}:{PORTA_ROBO} via UDP...")

try:
    for cmd in comandos:
        # Precisamos codificar a string para bytes antes de enviar pela rede
        mensagem_bytes = cmd.encode('utf-8')
        
        # 2. Arremessa os dados (Send To)
        sock.sendto(mensagem_bytes, (IP_ROBO, PORTA_ROBO))
        print(f"Enviado: {cmd}")
        
        time.sleep(1) # Simula o usuário apertando botões

except Exception as e:
    print(f"Erro ao enviar: {e}")
finally:
    sock.close()