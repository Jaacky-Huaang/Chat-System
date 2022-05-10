

import time
import socket
import select
import sys
import string
import indexer
import json
import pickle as pkl
from chat_utils import *
import chat_group as grp
import os
import random


class Server:
    def __init__(self):
        self.new_clients = []  # list of new sockets of which the user id is not known
        self.logged_name2sock = {}  # dictionary mapping username to socket
        self.logged_sock2name = {}  # dict mapping socket to user name
        self.all_sockets = []
        self.group = grp.Group()
        # start server
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(SERVER)
        self.server.listen(5)
        self.all_sockets.append(self.server)
        # initialize past chat indices
        self.indices = {}
        # sonnet
        # self.sonnet_f = open('AllSonnets.txt.idx', 'rb')
        # self.sonnet = pkl.load(self.sonnet_f)
        # self.sonnet_f.close()
        self.sonnet = indexer.PIndex("AllSonnets.txt")
        self.last_msg=None

        #####_________________⭐️⭐️⭐️Implemented for Secure Messaging⭐️⭐️⭐️______________
        self.base=6
        self.clock=11
        #####_________________⭐️⭐️⭐️Implemented for Secure Messaging⭐️⭐️⭐️______________


    def new_client(self, sock):
        # add to all sockets and to new clients
        print('new client...')
        sock.setblocking(0)
        self.new_clients.append(sock)
        self.all_sockets.append(sock)

    def login(self, sock):
        # read the msg that should have login code plus username
        try:
            msg = json.loads(myrecv(sock))
            print("login:", msg)
            if len(msg) > 0:

                if msg["action"] == "login":
                    name = msg["name"]

                    if self.group.is_member(name) != True:
                        # move socket from new clients list to logged clients
                        self.new_clients.remove(sock)
                        # add into the name to sock mapping
                        self.logged_name2sock[name] = sock
                        self.logged_sock2name[sock] = name
                        # load chat history of that user
                        if name not in self.indices.keys():
                            try:
                                self.indices[name] = pkl.load(
                                    open(name+'.idx', 'rb'))
                            except IOError:  # chat index does not exist, then create one
                                self.indices[name] = indexer.Index(name)
                        print(name + ' logged in')
                        self.group.join(name)
                        mysend(sock, json.dumps(
                            {"action": "login", "status": "ok"}))
                    else:  # a client under this name has already logged in
                        mysend(sock, json.dumps(
                            {"action": "login", "status": "duplicate"}))
                        print(name + ' duplicate login attempt')
                else:
                    print('wrong code received')
            else:  # client died unexpectedly
                self.logout(sock)
        except:
            self.all_sockets.remove(sock)

    def logout(self, sock):
        # remove sock from all lists
        name = self.logged_sock2name[sock]
        pkl.dump(self.indices[name], open(name + '.idx', 'wb'))
        del self.indices[name]
        del self.logged_name2sock[name]
        del self.logged_sock2name[sock]
        self.all_sockets.remove(sock)
        self.group.leave(name)
        sock.close()
    #😈😈😈😈😈😈😈😈😈😈😈😈😈😈😈😈😈😈😈😈存一下上一条exchange的消息
    def set_history(self,msg):
        self.last_msg=msg
    #😈😈😈😈😈😈😈😈😈😈😈😈😈😈😈😈😈😈😈😈
# ==============================================================================
# main command switchboard
# ==============================================================================
    def handle_msg(self, from_sock):
        # read msg code
        msg = myrecv(from_sock)
        msg = json.loads(msg)
        
        if len(msg) > 0:


            #####_________________⭐️⭐️⭐️Implemented for Secure Messaging⭐️⭐️⭐️______________
            if msg["action"]=="produce_public_private":
                from_name=self.logged_sock2name[from_sock]
                to_name=msg["target"]
                to_sock=self.logged_name2sock[to_name]
                mysend(to_sock, json.dumps(
                        {"action": "produce_public_private", 
                        "target": from_name, "from": from_name,"message":msg["message"]}))
            elif msg["action"]=="produce_shared_keys":
                from_name=self.logged_sock2name[from_sock]
                to_name=msg["target"]
                to_sock=self.logged_name2sock[to_name]
                mysend(to_sock, json.dumps(
                        {"action": "produce_shared_keys", 
                        "target": from_name, "from": from_name,"message":msg["message"]}))
            #####_________________⭐️⭐️⭐️Implemented for Secure Messaging⭐️⭐️⭐️______________


            # ==============================================================================
            # handle connect request
            # ==============================================================================
            
            if msg["action"] == "connect":
                to_name = msg["target"]
                from_name = self.logged_sock2name[from_sock]
                if to_name == from_name:
                    msg = json.dumps({"action": "connect", "status": "self"})
                # connect to the peer
                elif self.group.is_member(to_name):
                    to_sock = self.logged_name2sock[to_name]
                    self.group.connect(from_name, to_name)
                    the_guys = self.group.list_me(from_name)
                    msg = json.dumps(
                        {"action": "connect", "status": "success"})
                    for g in the_guys[1:]:
                        to_sock = self.logged_name2sock[g]
                        mysend(to_sock, json.dumps(
                            {"action": "connect", "status": "request", "from": from_name}))
                else:
                    msg = json.dumps(
                        {"action": "connect", "status": "no-user"})
                mysend(from_sock, msg)

# ==============================================================================
# handle messeage exchange: one peer for now. will need multicast later
# ==============================================================================
            elif msg["action"] == "exchange":
                #😈😈😈😈😈😈😈😈😈😈😈😈这一段reliable messaging的和原代码是混在一起的
                self.set_history(msg)
                
                from_name = self.logged_sock2name[from_sock]
                the_guys = self.group.list_me(from_name)
                #said = msg["from"]+msg["message"]
                said2 = text_proc(msg["message"], from_name)
                self.indices[from_name].add_msg_and_index(said2)
                
                #Simulating a bad server that produces wrong messages
                unreliable_msg=''
                rate=0.4
                for thing in msg["message"][:-1]:
                    print(thing)
                    error_prob=random.random()
                    print(error_prob)
                    if error_prob<=rate:
                        mark=random.randint(1,255)
                    else:
                        mark=ord(thing)
                    new_thing=chr(mark)
                    print(new_thing)
                    unreliable_msg+=new_thing
                unreliable_msg=unreliable_msg+msg["message"][-1]
                
                
                for g in the_guys[1:]:
                    to_sock = self.logged_name2sock[g]
                    self.indices[g].add_msg_and_index(said2)
                    mysend(to_sock, json.dumps(
                        {"action": "exchange", "from": msg["from"], 
                         "message": unreliable_msg}))
            
            elif msg["action"] == "resend":
                from_name = self.logged_sock2name[from_sock]
                to_sock = self.logged_name2sock[from_name]

                unreliable_msg=''
                rate=0.0
                print(self.last_msg)
                for thing in self.last_msg["message"][:-1]:
                    print(thing)
                    error_prob=random.random()
                    print(error_prob)
                    if error_prob<=rate:
                        mark=random.randint(1,255)
                    else:
                        mark=ord(thing)
                    new_thing=chr(mark)
                    print(new_thing)
                    unreliable_msg+=new_thing
                    
                self.last_msg["message"]=unreliable_msg+self.last_msg["message"][-1]
                
                mysend(to_sock, json.dumps(
                        {"action": "exchange", "from": self.last_msg["from"], 
                        "message": self.last_msg["message"]}))
            #😈😈😈😈😈😈😈😈😈😈😈😈
# ==============================================================================
#                 listing available peers
# ==============================================================================
            elif msg["action"] == "list":
                from_name = self.logged_sock2name[from_sock]
                msg = self.group.list_all()
                mysend(from_sock, json.dumps(
                    {"action": "list", "results": msg}))
# ==============================================================================
#             retrieve a sonnet
# ==============================================================================
            elif msg["action"] == "poem":
                poem_indx = int(msg["target"])
                from_name = self.logged_sock2name[from_sock]
                print(from_name + ' asks for ', poem_indx)
                poem = self.sonnet.get_poem(poem_indx)
                poem = '\n'.join(poem).strip()
                print('here:\n', poem)
                mysend(from_sock, json.dumps(
                    {"action": "poem", "results": poem}))
# ==============================================================================
#                 time
# ==============================================================================
            elif msg["action"] == "time":
                ctime = time.strftime('%d.%m.%y,%H:%M', time.localtime())
                mysend(from_sock, json.dumps(
                    {"action": "time", "results": ctime}))
# ==============================================================================
#                 search
# ==============================================================================
            elif msg["action"] == "search":
                term = msg["target"]
                from_name = self.logged_sock2name[from_sock]
                print('search for ' + from_name + ' for ' + term)
                # search_rslt = (self.indices[from_name].search(term))
                search_rslt = '\n'.join(
                    [x[-1] for x in self.indices[from_name].search(term)])
                print('server side search: ' + search_rslt)
                mysend(from_sock, json.dumps(
                    {"action": "search", "results": search_rslt}))
# ==============================================================================
# the "from" guy has had enough (talking to "to")!
# ==============================================================================
            elif msg["action"] == "disconnect":
                from_name = self.logged_sock2name[from_sock]
                the_guys = self.group.list_me(from_name)
                self.group.disconnect(from_name)
                the_guys.remove(from_name)
                if len(the_guys) == 1:  # only one left
                    g = the_guys.pop()
                    to_sock = self.logged_name2sock[g]
                    mysend(to_sock, json.dumps({"action": "disconnect"}))

        
# ==============================================================================
#                 the "from" guy really, really has had enough
# ==============================================================================


        else:
            # client died unexpectedly
            self.logout(from_sock)

# ==============================================================================
# main loop, loops *forever*
# ==============================================================================
    def run(self):
        print('starting server...')
        while(1):
            read, write, error = select.select(self.all_sockets, [], [])
            print('checking logged clients..')
            for logc in list(self.logged_name2sock.values()):
                if logc in read:
                    self.handle_msg(logc)
            print('checking new clients..')
            for newc in self.new_clients[:]:
                if newc in read:
                    self.login(newc)
            print('checking for new connections..')
            if self.server in read:
                # new client request
                sock, address = self.server.accept()
                self.new_client(sock)


def main():
    server = Server()
    server.run()
    os.system("python SnakeServer.py")


if __name__ == "__main__":
    main()
