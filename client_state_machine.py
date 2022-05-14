
from chat_utils import *
import json
import secrets
import os
import random

class ClientSM:

    def __init__(self, s):
        self.state = S_OFFLINE
        self.peer = ''
        self.me = ''
        self.out_msg = ''
        self.s = s
        

        #####_________________⭐️⭐️⭐️Implemented for Secure Messaging👇⭐️⭐️⭐️______________
        # To give user a private key when login
        #self.private_key=secrets.randbits(17)
        self.private_key=random.randint(1,25)
        # The base of the public-private number. Requirement: base is the primitive root of the clock_key
        self.base=6
        # The clock to be divided. Requirement: prime
        self.clock=11
        #The shared key, undecided yet
        self.shared_key=None
        self.public_private_key=self.base**self.private_key%self.clock
        #####_________________⭐️⭐️⭐️Implemented for Secure Messaging👆⭐️⭐️⭐️______________


    #🌈🌈🌈🌈🌈🌈🌈🌈🌈🌈🌈🌈🌈🌈🌈🌈🌈 Online Gaming Part ! 🌈🌈🌈🌈🌈🌈🌈🌈🌈🌈🌈🌈🌈🌈🌈🌈🌈    

    def start_game(self):
        
        os.system("python Snake.py")

  
#####_________________⭐️⭐️⭐️Implemented for Secure Messaging⭐️⭐️⭐️______________

    def get_public_private_key(self):
         return self.base**self.private_key%self.clock
    
    def get_shared_key(self,public_private_key):
        #public_private_key**self.private_key%self.clock
        #self.shared_key=public_private_key**self.private_key%self.clock
        return public_private_key**self.private_key%self.clock
    
    def encode(self,msg):
        encoded_msg=''
        
        for i in msg:
            # use the built-in method ord()and chr() 
            # to convert letters into digits and mess up the original message
            print(i,ord(i))
            print(ord(i)+self.shared_key)
            encoded_msg+=chr(ord(i)+self.shared_key)
        return encoded_msg

    def decode(self,encoded_msg):
        decoded_msg=''
        for i in encoded_msg:
            # the reversed operation of encode
            print(i,ord(i))
            print(ord(i)-self.shared_key)
            print(chr(ord(i)-self.shared_key))
            decoded_msg+=chr(ord(i)-self.shared_key)
        return decoded_msg

#####_________________⭐️⭐️⭐️Implemented for Secure Messaging⭐️⭐️⭐️______________

    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state

    def set_myname(self, name):
        self.me = name

    def get_myname(self):
        return self.me

    def connect_to(self, peer):
        msg = json.dumps({"action":"connect", "target":peer})
        mysend(self.s, msg)
        response = json.loads(myrecv(self.s))
        if response["status"] == "success":
            self.peer = peer
            self.out_msg += 'You are connected with '+ self.peer + '\n'
            return (True)
        elif response["status"] == "busy":
            self.out_msg += 'User is busy. Please try again later\n'
        elif response["status"] == "self":
            self.out_msg += 'Cannot talk to yourself (sick)\n'
        else:
            self.out_msg += 'User is not online, try again later\n'
        return(False)

    def disconnect(self):
        msg = json.dumps({"action":"disconnect"})
        mysend(self.s, msg)
        self.out_msg += 'You are disconnected from ' + self.peer + '\n'
        self.peer = ''

    def proc(self, my_msg, peer_msg):
        self.out_msg = ''
#==============================================================================
# Once logged in, do a few things: get peer listing, connect, search
# And, of course, if you are so bored, just go
# This is event handling instate "S_LOGGEDIN"
#==============================================================================
        if self.state == S_LOGGEDIN:
            # todo: can't deal with multiple lines yet
            if len(my_msg) > 0:

                if my_msg == 'q':
                    self.out_msg += 'See you next time!\n'
                    self.state = S_OFFLINE

                elif my_msg == 'time':
                    mysend(self.s, json.dumps({"action":"time"}))
                    time_in = json.loads(myrecv(self.s))["results"]
                    self.out_msg += "Time is: " + time_in

                elif my_msg == 'who':
                    mysend(self.s, json.dumps({"action":"list"}))
                    logged_in = json.loads(myrecv(self.s))["results"]
                    self.out_msg += 'Here are all the users in the system:\n'
                    self.out_msg += logged_in
#🌈🌈🌈🌈🌈🌈🌈🌈🌈🌈🌈🌈🌈🌈🌈🌈🌈 Online Gaming Part ! 🌈🌈🌈🌈🌈🌈🌈🌈🌈🌈🌈🌈🌈🌈🌈🌈🌈              
                elif my_msg=="game":
                    self.state=S_GAMING
                    self.start_game()
#🌈🌈🌈🌈🌈🌈🌈🌈🌈🌈🌈🌈🌈🌈🌈🌈🌈 Online Gaming Part ! 🌈🌈🌈🌈🌈🌈🌈🌈🌈🌈🌈🌈🌈🌈🌈🌈🌈 
                elif my_msg[0] == 'c':
                    peer = my_msg[1:]
                    peer = peer.strip()
                    if self.connect_to(peer) == True:
                        self.state = S_CHATTING
                        self.out_msg += 'Connect to ' + peer + '. Chat away!\n\n'
                        self.out_msg += '-----------------------------------\n'
#####_________________⭐️⭐️⭐️Implemented for Secure Messaging⭐️⭐️⭐️______________
                        
                        mysend(self.s, json.dumps(
                             {"action":"produce_public_private","target":self.peer,
                             "message":self.public_private_key}))
#####_________________⭐️⭐️⭐️Implemented for Secure Messaging⭐️⭐️⭐️______________
                    
                    
                    else:
                        self.out_msg += 'Connection unsuccessful\n'

                elif my_msg[0] == '?':
                    term = my_msg[1:].strip()
                    mysend(self.s, json.dumps({"action":"search", "target":term}))
                    search_rslt = json.loads(myrecv(self.s))["results"].strip()
                    if (len(search_rslt)) > 0:
                        self.out_msg += search_rslt + '\n\n'
                    else:
                        self.out_msg += '\'' + term + '\'' + ' not found\n\n'

                elif my_msg[0] == 'p' and my_msg[1:].isdigit():
                    poem_idx = my_msg[1:].strip()
                    mysend(self.s, json.dumps({"action":"poem", "target":poem_idx}))
                    poem = json.loads(myrecv(self.s))["results"]
                    # print(poem)
                    if (len(poem) > 0):
                        self.out_msg += poem + '\n\n'
                    else:
                        self.out_msg += 'Sonnet ' + poem_idx + ' not found\n\n'

                else:
                    self.out_msg += menu

            if len(peer_msg) > 0:
                peer_msg = json.loads(peer_msg)
                if peer_msg["action"] == "connect":
                    self.peer = peer_msg["from"]
                    self.out_msg += 'Request from ' + self.peer + '\n'
                    self.out_msg += 'You are connected with ' + self.peer
                    self.out_msg += '. Chat away!\n\n'
                    self.out_msg += '------------------------------------\n'
                    self.state = S_CHATTING

#==============================================================================
# Start chatting, 'bye' for quit
# This is event handling instate "S_CHATTING"
#==============================================================================
        elif self.state == S_CHATTING:


            if len(my_msg) > 0:  
                if my_msg == 'bye':
                    self.disconnect()
                    self.state = S_LOGGEDIN
                    self.peer = ''   
                elif my_msg=="game":
                    self.state=S_GAMING
                    mysend(self.s, json.dumps({"action":"game"}))
                    self.start_game()

                #self.shared_key=self.get_shared_key(self.public_private_key)
                
                print("This is the encoded msg:",my_msg)
                print("This is the shared key: ",self.shared_key)
                
                sum=0
                for thing in my_msg:
                    mark=ord(thing)
                    sum+=mark
                checksum=str(sum)[-1]
                my_msg+=checksum
                
                my_msg=self.encode(my_msg)

                mysend(self.s, json.dumps(
                    {"action":"exchange", "from":"[" + self.me + "]", 
                    "message":my_msg}))
                print("This is the encoded message with sum: "+my_msg)

#========================self/peer======================== 

            if len(peer_msg) > 0:    # peer's stuff, coming in
                peer_msg = json.loads(peer_msg)

                if peer_msg["action"] == "connect":
                    self.out_msg += "(" + peer_msg["from"] + " joined)\n"

                #####_________________⭐️⭐️⭐️Implemented for Secure Messaging⭐️⭐️⭐️______________
                # send self's ppkey for peers to get shared key
                elif peer_msg["action"]=="produce_public_private":
                    
                    ppkey=self.get_public_private_key()
                    print("This is ppkey:",ppkey)
                    mysend(self.s, json.dumps(
                            {"action":"produce_shared_keys","target":self.peer,
                            "message":ppkey}))
                    # Below this line, self.public_private_key
                    # is the one received from peers
                    # self.public_private_key=int(peer_msg["message"])
                    self.shared_key=self.get_shared_key(int(peer_msg["message"]))
                    print("This is shared key:",self.shared_key)
                    self.out_msg += "Your messages have been encoded thanks to Jacky!\n"
                    self.out_msg += "\n"
                    self.out_msg += '------------------------------------\n'
                
                # get peer's ppkey to produce shared key for self
                elif peer_msg["action"]=="produce_shared_keys":
                    
                    #self.public_private_key=int(peer_msg["message"])
                    self.shared_key=self.get_shared_key(int(peer_msg["message"]))
                    print("This is shared key:",self.shared_key)
                    self.out_msg += "Your messages have been encoded thanks to Jacky!\n"
                    self.out_msg += "\n"
                    self.out_msg += '------------------------------------\n'
                #####_________________⭐️⭐️⭐️Implemented for Secure Messaging⭐️⭐️⭐️______________


                elif peer_msg["action"] == "disconnect":
                    self.state = S_LOGGEDIN
                    self.out_msg='You are disconnected from ' + self.peer + '\n'
                    self.peer=''
                
                else:
                    #####_________________⭐️⭐️⭐️Implemented for Secure Messaging⭐️⭐️⭐️______________
                    # self.public_private_key=self.get_public_private_key()
                    # self.shared_key=self.get_shared_key(self.get_public_private_key())
                    print("This is shared key: ",self.shared_key)
                    encoded_msg=peer_msg["message"]
                    print("This is the encoded message from peer with sum: "+peer_msg["message"])

                    decoded_msg=self.decode(encoded_msg)
                    print("This is the decoded_msg: ",decoded_msg)
                    #####_________________⭐️⭐️⭐️Implemented for Secure Messaging⭐️⭐️⭐️______________
                    #😈😈😈😈😈😈😈😈😈😈😈😈
                    check_sum=int(decoded_msg[-1])

                    sum=0
                    
                    for thing in decoded_msg[:-1]:
                        
                        mark=ord(thing)
                        sum+=mark
                    print(sum)
                    print(check_sum)
                    if int(str(sum)[-1])==check_sum:
                        self.out_msg += peer_msg["from"] + decoded_msg[:-1]
                    else:
                        
                       mysend(self.s, json.dumps({"action":"resend"}))
                    #😈😈😈😈😈😈😈😈😈😈😈😈

                    

                    

            # Display the menu again
            if self.state == S_LOGGEDIN:
                self.out_msg += menu
#==============================================================================
# invalid state
#==============================================================================
        else:
            self.out_msg += 'How did you wind up here??\n'
            print_state(self.state)

        return self.out_msg
