# coding:utf-8
import sys
import paramiko
from tkinter import *
import threading
import time

global root


def updateGUI(label, value):
    label['text'] = value


def getConnection(ip, username, password, port=22):
    """
     :param ip: 
     :param username:  
     :param password:  
     :param CMD:  
     :param port:  
     """
    ssh = paramiko.SSHClient()
    policy = paramiko.AutoAddPolicy()
    ssh.set_missing_host_key_policy(policy)
    ssh.connect(
        hostname=ip,
        port=port,
        username=username,
        password=password
    )

    print("+++++++++++++++++++++++start++++++++++++++++++++")
    print("[connect success] | ip : %s" % ip)

    return ssh
    # ssh.close()


def makeCommand(ssh, cm):
    stdin, stdout, stderr = ssh.exec_command(cm)
    time.sleep(0.5)
    result = stdout.read().decode()

    # error = stderr.read().decode()
    print("result: \n %s" % result)
    # if error != " ":
    #    print("error: \n %s"%error)
    print("+++++++++++++++++++++++done++++++++++++++++++++")


def RUN():
    main()


def main():
    ssh = getConnection('192.168.1.47', 'spiri', 'spiri-friend')
    COMMANDS_LIST = [
        'python3 GCS.py ARM',
        'python3 GCS.py DISARM',
        'python3 GCS.py LAND',
        'python3 GCS.py SQUARE',
        'python3 GCS.py CIRCLE',
        'python3 GCS.py HELIX',
        'python3 GCS.py LEMNISCATE'
    ]
    for i in COMMANDS_LIST:
        BUTTONS(ssh, i)


def BUTTONS(ssh, CM):
    Button(frame, text=CM.split(' ')[2], font=('Times', 12), width=15, height=1,
           command=lambda: makeCommand(ssh, CM)).pack(side='top')


'''def main(COMMANDS_LIST):
    thread_list = []
    for i in COMMANDS_LIST:
        thread = threading.Thread(target = BUTTONS, args = (ssh, i))
        
        thread_list.append(thread)
    for t in thread_list:
         thread.daemon = True
         t.start()
    for t in thread_list:
         t.join()'''


flag = 0
# The tkinter root object
root = Tk()
root.wm_title("microGCS - the worlds crummiest GCS")
root.geometry('800x600')
frame = Frame(root)
frame.pack()
b1 = Button(frame, text='Connection', font=('Times', 12), width=15, height=1, command=lambda: RUN())
b1.pack(side='top')

root.mainloop()
