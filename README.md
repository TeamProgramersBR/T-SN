T²SN -- network explanation

https://teamprogramersbr.github.io/T-SN/

pwned by : hide and seek
-----------------------------

 - T²SN -

 Use com: ttsn.py -t target_host -p port
 
 -l --listen interceptar conexões de [host:port]
 
 -e --execute=arquivo  executa o arquivo em cima da conexão 
 
 -c --command  executa um shell
 
 -u --upload=destino manda um arquivo ao alvo

<a href="https://github.com/TeamProgramersBR/T-SN.git">
<img src="http://batidaoautomotivo.com.br/wp-content/uploads/2015/08/Botao-Download.png" alt="alt tag" style="max-width:100%;">
 </a>
 
 
 
 
 Exemplos:

 ttsn.py  -t 192.168.0.1 -p 5555 -l -c

 ttsn.py -t 192.158.0.1 -p 5555 -l -u=c:\\target.exe

 ttsn.py -t 192.168.0.1 -p 5555 -l -e=\"cat /etc/passwd\"

 echo 'VIRUS TOTAL E UM LIXO' | ./ttsn.py -t 192.168.0.1 -p 135
    
