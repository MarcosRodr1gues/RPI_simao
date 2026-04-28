import socket
import threading
import queue
import time

# Configurações de Rede
IP_ROBO = "192.168.0.220"
PORTA_ROBO = 5005

# 1. Cria uma Fila segura para as Threads conversarem
fila_de_comandos = queue.Queue()

# 2. Define o comportamento da Thread de Rede
def worker_de_rede():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(1.0) # Timeout de 1 seg
    
    print("[REDE] Iniciada e aguardando comandos na fila...")
    
    while True:
        # Pega o próximo comando da fila (trava aqui até aparecer um comando)
        comando = fila_de_comandos.get() 
        
        if comando == "DESLIGAR":
            print("[REDE] Encerrando conexão.")
            break
            
        try:
            # Envia o comando
            sock.sendto(comando.encode('ascii'), (IP_ROBO, PORTA_ROBO))
            
            # Aguarda o Ack
            dados, _ = sock.recvfrom(1024)
            resposta = dados.decode('ascii').strip()
            
            if "A" in resposta:
                print(f"[REDE] Sucesso (Ack recebido para: {repr(comando)})")
            else:
                print(f"[REDE] Falha (Nack ou erro para: {repr(comando)})")
                
        except socket.timeout:
            print(f"[REDE] ALERTA: Timeout! Robô não respondeu ao comando {repr(comando)}")
        
        # Avisa a fila que terminou a tarefa
        fila_de_comandos.task_done()

# 3. Inicia a Thread de Rede em background (daemon=True faz ela fechar com o programa)
thread_rede = threading.Thread(target=worker_de_rede, daemon=True)
thread_rede.start()

# ==========================================
# 4. THREAD PRINCIPAL (Simulando a sua IHM)
# ==========================================
print("[IHM] Interface iniciada e rodando lisa!")

try:
    # A interface gráfica não precisa se preocupar com sockets, 
    # ela só "joga" os comandos na fila e volta a fazer o que estava fazendo.
    
    print("[IHM] Enviando comando Movimento 1")
    fila_de_comandos.put("10,M,500,-200\r\n")
    
    time.sleep(0.5) # O usuário esperou meio segundo
    
    print("[IHM] Enviando comando Movimento 2")
    fila_de_comandos.put("10,M,-1500,0\r\n")
    
    # Mantém a Thread Principal viva simulando a IHM rodando...
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("\n[IHM] Fechando programa...")
    fila_de_comandos.put("DESLIGAR") # Manda a thread de rede se fechar