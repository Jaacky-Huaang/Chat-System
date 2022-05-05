import socket
import sys
from chat_utils import *
import client_state_machine as csm
from GUI import *


class Client:
    def __init__(self, args):
        self.args = args

    def quit(self):
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()

    def init_chat(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        svr = SERVER if self.args.d == None else (self.args.d, CHAT_PORT)
        self.socket.connect(svr)
        self.sm = csm.ClientSM(self.socket)
        self.gui = GUI(self.send, self.recv, self.sm, self.socket)

    def shutdown_chat(self):
        return

    def send(self, msg):
        mysend(self.socket, msg)

    def recv(self):
        return myrecv(self.socket)

    def run_chat(self):
        self.init_chat()
        self.gui.run()
        print("gui is off")
        self.quit()
#-------------------login with password------------------
    def register_user(self,user,key):
        msg = json.dumps({'action':'register','name':user,'password':key})
        self.send(msg)
        response = json.loads(self.recv())
        if response['status'] == 'duplicate':
            return '0'
        elif response['status'] == 'ok':
            return 'ok'
        
    def verify_user(self,user,key):
        msg=json.dumps({'action':'login','name':user,'password':key})
        self.send(msg)
        response = json.loads(self.recv())
        if response['status']=='ok':
            self.name=user
            return 'ok'
        elif response['status']=='notregister':
            return '1'
        elif response['status']=='wrongpassword':
            return '2'
        elif response['status']=='duplicate':
            return '3'
            
