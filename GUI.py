
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 13:36:58 2021
@author: bing
"""
#This is a test!!！
# import all the required  modules
import threading
import select
from tkinter import *
from tkinter import font
from tkinter import ttk
from chat_utils import *
import json
from tkinter import messagebox

# GUI class for the chat


class GUI:
    # constructor method
    def __init__(self, send, recv, sm, s):
        # chat window which is currently hidden
        self.Window = Tk()
        self.Window.withdraw()
        self.send = send
        self.recv = recv
        self.sm = sm
        self.socket = s
        self.my_msg = ""
        self.system_msg = ""

    def login(self):
        # login window
        self.login = Toplevel()
        # set the title
        self.login.title("Login")
        self.login.resizable(width=False,
                             height=False)
        self.login.configure(width=400,
                             height=300)
        # create a Label
        self.pls = Label(self.login,
                         text="Please login to continue",
                         justify=CENTER,
                         font="Helvetica 14 bold")

        self.pls.place(relheight=0.15,
                       relx=0.2,
                       rely=0.07)
        # create a Label
        self.labelName = Label(self.login,
                               text="Name: ",
                               font="Helvetica 12")

        self.labelName.place(relheight=0.2,
                             relx=0.1,
                             rely=0.2)

        # create a entry box for
        # tyoing the message
        self.entryName = Entry(self.login,
                               font="Helvetica 14")

        self.entryName.place(relwidth=0.4,
                             relheight=0.12,
                             relx=0.35,
                             rely=0.2)

        # set the focus of the curser
        self.entryName.focus()
        
        
#***************START***OF***PASSWORD*************************************
        self.labelPassword = Label(self.login,
                               text="Password: ",
                               font="Helvetica 12")

        self.labelPassword.place(relheight=0.2,
                             relx=0.1,
                             rely=0.43)
        
        self.entryPassword = Entry(self.login,
                                   font="Helvetica 14")
        self.entryPassword.place(relwidth=0.4,
                             relheight=0.12,
                             relx=0.35,
                             rely=0.43)

        
        #self.entryPassword.focus()
        
        #self.Check(self.entryName.get(), self.entryPassword.get())
#----------------------------end of password----------------------
        # create a Continue Button
        # along with action
        self.go = Button(self.login,
                         text="CONTINUE",
                         font="Helvetica 14 bold",
                         command=lambda: self.goAhead((self.entryName.get(),self.entryPassword.get())))

        self.go.place(relx=0.15,
                      rely=0.64)
#***************Password*************************************       
        self.regi = Button(self.login,
                         text="REGISTER",
                         font="Helvetica 14 bold",
                         command=lambda: self.Register((self.entryName.get(),self.entryPassword.get())))
        
        self.regi.place(relx=0.45,
                      rely=0.64)
#*****************end of password*********************************        
        
        self.Window.mainloop()
        
#************ A Function for Password *************************      
    def Register(self,nameAndPswd):
        nm=nameAndPswd[0]
        pswd=nameAndPswd[1]
        #print(nm,pswd)
        
        if nm == '' or pswd == '':
            messagebox.showwarning(
                title='Invalid input', message='User name or password is empty')
            #return
        
        else:
            msg = json.dumps({'action':'register','name':nm,'password':pswd})
            self.send(msg)
            response = json.loads(self.recv())
            #print(response)
            #result = self.register_user(nm,pswd)
            if response['status'] == 'duplicate':
                messagebox.showerror(
                    title='Error', message='You have already logged in. No need to register.')
            elif response['status'] == 'ok':
                messagebox.showinfo('Success','You have successfully registered!')
                
                
#*******************Something added below for password*******************              
 
    def goAhead(self, nameAndPswd):
        name=nameAndPswd[0]
        pswd=nameAndPswd[1]
        if len(name) > 0:
            msg = json.dumps({"action": "login", "name": name,'password':pswd})
            self.send(msg)
            response = json.loads(self.recv())
            #print(response)
            if response["status"] == 'ok':
                self.login.destroy()
                self.sm.set_state(S_LOGGEDIN)
                self.sm.set_myname(name)
                self.layout(name)
                self.textCons.config(state=NORMAL)
                # self.textCons.insert(END, "hello" +"\n\n")
                self.textCons.insert(END, menu + "\n\n")
                self.textCons.config(state=DISABLED)
                self.textCons.see(END)
                process = threading.Thread(target=self.proc)
                process.daemon = True
                process.start()
            elif response['status'] == 'notregister':
                messagebox.showerror(
                    title='Error',message='User name does not exist.')
                
            elif response['status'] == 'duplicate':
                messagebox.showerror(
                    title='Error',message='You already logged in.')
            elif response['status'] == 'wrongpassword':
                messagebox.showerror(
                    title='Error',message='User name or password is wrong.')
 #***************************************************               
                # while True:
                #     self.proc()
        # the thread to receive messages
        

    # The main layout of the chat
    def layout(self, name):

        self.name = name
        # to show chat window
        self.Window.deiconify()
        self.Window.title("CHATROOM")
        self.Window.resizable(width=False,
                              height=False)
        self.Window.configure(width=470,
                              height=550,
                              bg="#17202A")
        self.labelHead = Label(self.Window,
                               bg="#17202A",
                               fg="#EAECEE",
                               text=self.name,
                               font="Helvetica 13 bold",
                               pady=5)

        self.labelHead.place(relwidth=1)
        self.line = Label(self.Window,
                          width=450,
                          bg="#ABB2B9")

        self.line.place(relwidth=1,
                        rely=0.07,
                        relheight=0.012)

        self.textCons = Text(self.Window,
                             width=20,
                             height=2,
                             bg="#17202A",
                             fg="#EAECEE",
                             font="Helvetica 14",
                             padx=5,
                             pady=5)

        self.textCons.place(relheight=0.745,
                            relwidth=1,
                            rely=0.08)

        self.labelBottom = Label(self.Window,
                                 bg="#ABB2B9",
                                 height=80)

        self.labelBottom.place(relwidth=1,
                               rely=0.825)

        self.entryMsg = Entry(self.labelBottom,
                              bg="#2C3E50",
                              fg="#EAECEE",
                              font="Helvetica 13")

        # place the given widget
        # into the gui window
        self.entryMsg.place(relwidth=0.74,
                            relheight=0.06,
                            rely=0.008,
                            relx=0.011)

        self.entryMsg.focus()

        # create a Send Button
        self.buttonMsg = Button(self.labelBottom,
                                text="Send",
                                font="Helvetica 10 bold",
                                width=20,
                                bg="#ABB2B9",
                                command=lambda: self.sendButton(self.entryMsg.get()))

        self.buttonMsg.place(relx=0.77,
                             rely=0.008,
                             relheight=0.06,
                             relwidth=0.22)

        self.textCons.config(cursor="arrow")

        # create a scroll bar
        scrollbar = Scrollbar(self.textCons)

        # place the scroll bar
        # into the gui window
        scrollbar.place(relheight=1,
                        relx=0.974)

        scrollbar.config(command=self.textCons.yview)

        self.textCons.config(state=DISABLED)

    # function to basically start the thread for sending messages

    def sendButton(self, msg):
        # self.textCons.config(state=DISABLED)
        self.my_msg = msg
        # print(msg)
        self.entryMsg.delete(0, END)
        self.textCons.config(state=NORMAL)
        self.textCons.insert(END, msg + "\n")
        self.textCons.config(state=DISABLED)
        self.textCons.see(END)
 #------------------file button-----------------       
    '''def fileButton(self, msg):
        self.file = Toplevel()
        # set the title
        self.file.title("File")
        self.file.resizable(width=False,
                             height=False)
        self.file.configure(width=400,
                             height=300)
        
        self.labelFile = Label(self.file,
                               text="File: ",
                               font="Helvetica 12")
        self.labelFile.place(relheight=0.2,
                             relx=0.1,
                             rely=0.2)
        self.entryFile = Entry(self.file,
                               font="Helvetica 14")
        self.entryFile.place(relwidth=0.4,
                             relheight=0.12,
                             relx=0.35,
                             rely=0.2)'''
        # create a Label
  #-----------------------------------------------------------      

    def proc(self):
        # print(self.msg)
        while True:
            read, write, error = select.select([self.socket], [], [], 0)
            peer_msg = []
            # print(self.msg)
            if self.socket in read:
                peer_msg = self.recv()
            if len(self.my_msg) > 0 or len(peer_msg) > 0:
                # print(self.system_msg)
                self.system_msg = self.sm.proc(self.my_msg, peer_msg)
                self.my_msg = ""
                self.textCons.config(state=NORMAL)
                self.textCons.insert(END, self.system_msg + "\n\n")
                self.textCons.config(state=DISABLED)
                self.textCons.see(END)

    def run(self):
        self.login()
 
            
            #----------------------------------------------
# create a GUI class object
if __name__ == "__main__":
    # g = GUI()
    pass
