import socket

# Configurações do Servidor
IP = "192.168.0.220"
PORTA = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((IP, PORTA))

print(f"Placa da cabeça aguardando comandos na porta {PORTA}...")

try:
    while True:
        # 1. Recebe o pacote encapsulado em bytes
        dados_bytes, endereco_origem = sock.recvfrom(1024)
        
        # 2. Desencapsula (Decodifica para string e remove o \r\n do final)
        pacote_str = dados_bytes.decode('ascii').strip()
        print(f"Recebido raw: {repr(pacote_str)}")
        
        # 3. Faz o parsing dos dados separando por vírgula
        partes = pacote_str.split(',')
        
        if len(partes) == 4 and partes[0] == '10' and partes[1] == 'M':
            # Extrai e garante que são inteiros (o Python lida nativamente com int32)
            try:
                eixo_x = int(partes[2])
                eixo_y = int(partes[3])
                
                print(f"Comando válido -> Mover X: {eixo_x}, Y: {eixo_y}")
                
                # Monta o pacote de Resposta de Sucesso (Ack)
                resposta = "10,M,A\r\n"
                
            except ValueError:
                print("Erro: X ou Y não são números inteiros válidos.")
                # Monta o pacote de Resposta de Erro (Nack)
                resposta = "10,M,N\r\n"
        else:
            print("Erro: Pacote fora do padrão ou endereço incorreto.")
            resposta = "10,M,N\r\n"
            
        # 4. Envia a resposta de volta para a IHM
        sock.sendto(resposta.encode('ascii'), endereco_origem)

except KeyboardInterrupt:
    print("\nEncerrando servidor.")
finally:
    sock.close()