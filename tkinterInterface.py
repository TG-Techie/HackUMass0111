import re
import tkinter as tk
from datetime import datetime
import json
import os

import scanner

class frame(tk.Frame):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, height = 150, width = 300, **kwargs)

class User:

    def __init__(self, userName, password):

        self.username = userName
        self.password = password
        self.messages = dict() # recipientUser : messageList
        self.friendsList = {}
        self.qr = None

    def addFriend(self, otherUser):
        self.friendsList[otherUser.username] = otherUser

    def removeFriend(self, otherUser):

        self.friendsList.pop(otherUser)

    def sendMessage(self, message, recipient):

        newMessage = Message(message, self, recipient)
        self.messages[recipient] = self.messages.get(recipient, []).append(newMessage)

    def seeExchange(self, otherUser):

        s = otherUser.userName
        exchange = self.messages.get(otherUser)
        for message in exchange:
            s += message
        return s

    def getFriendList(self):

        return self.friendsList


class Message:

    def __init__(self, message, sender, recipient):
        self.message = message
        self.sender = sender
        self.recipient = recipient
        self.timeStamp = datetime.now()

    def __str__(self):
        return  str(self.sender.username) + " ->" + str(self.recipient.username)\
        +'@'+str(self.timeStamp).split(' ')[1].split('.')[0]+':\n'\
        +self.message + "\n ----- \n"



class OptIn(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)

        with open("users.json", "r") as jsonFile:
            self.users = json.load(jsonFile)

        self.usersObject = dict()
        for username, password in self.users.items():
            self.usersObject[username] = User(username, password)
        self._frame = None
        self.switch_frame(LoginScreen)
        self.currentUser = None;
        self.recipient = None
    def saveInfo(self):
        with open("users.json", "w") as jsonFile:
            json.dump(self.controller.users, jsonFile)

        self.users = dict()

        self._frame = None
        self.switch_frame(SignedUpScreen)


    def getUsers(self):
        return self.users
    def getUsersObject(self):
        return self.usersObject
    def addUser(self, username, password):
        self.users[username] = password
        self.usersObject[username] = User(username, password)

    def switch_frame(self, frame_class, args  = []):

        """Destroys current frame and replaces it with a new one."""
        if len(args) == 0 or frame_class == DashboardScreen:
            new_frame = frame_class(self)
        else:
            #if frame_class == LoginScreen:
                new_frame = frame_class(self, *args)
            #elif frame_class == SignedUpScreen:
                #new_frame = frame_class(self, args[0], args[1], args[2])
        if self._frame is not None:
            self._frame.destroy()

        self._frame = new_frame
        self._frame.pack()
"""
    def mainloop(self):
        while True:
            tk.update_idletasks()
            tk.update_tasks()
            for func in self.func_loops.items():
                func()
"""


class LoginScreen(frame):
    # define some states

    def __init__(self, controller, loggedIn=False, wrongpass=False, accountNotFound=False):
        frame.__init__(self, controller)
        #State variables
        self.loggedIn = loggedIn #This happens when 1.password is wrong 2.havent logged in yet
        self.wrongpass = wrongpass
        self.accountNotFound = accountNotFound
        self.controller = controller

        self.draw()

    def draw(self):
        if (self.loggedIn == False):
            """SET UP"""
            label = tk.Label(self, text = "WELCOME TO OPTIN")
            label.pack()
            topFrame = frame(self)
            topFrame.pack(side = "top")
            middleFrame = frame(self)
            middleFrame.pack()
            bottomFrame = frame(self)
            bottomFrame.pack(side = "bottom")

            """LOG IN INFO"""
            username = tk.Label(topFrame, text = "Username")
            username.grid(row=0, stick = "E")

            users = self.controller.getUsers()

            def usernameEnter(event):
                if (users.get(username) == -1):
                    self.accountNotFound = True
                    args = [self.loggedIn, self.wrongpass, self.accountNotFound]
                    self.controller.switch_frame(LoginScreen, args)

            usernameEntry = tk.Entry(topFrame)
            usernameEntry.grid(row = 0, column = 1)
            self.controller.bind('<Return>', usernameEnter)


            password = tk.Label(topFrame, text = "Password")
            password.grid(row=1, stick = "E")

            passwordEntry = tk.Entry(topFrame)
            passwordEntry.grid(row = 1, column = 1)


            if (self.accountNotFound == True):
                accountNotFoundLabel = tk.Label(text = "Account Not Found!")
                accountNotFoundLabel.pack()

            if (self.wrongpass == True):
                wrongPassLabel = tk.Label(text = "Wrong Password")
                wrongPassLabel.pack()

            loginButton = tk.Button(topFrame, text = "I Opt In!", command = lambda: self.loggedInPressed(usernameEntry.get(), passwordEntry.get()))
            loginButton.grid(row = 4, stick = "E")

            signedUpLabel = tk.Label(topFrame, text = "Haven't had account? Sign Up!")
            signedUpLabel.grid(row = 5, stick = "E")

            signedUpButton = tk.Button(topFrame, text = "Sign Up", command = lambda: self.signedUpPressed())
            signedUpButton.grid(row = 6, stick = "E")
        return
    def loggedInPressed(self, username, password):

        if ((username is None) or (password is None)):
            args = [self.loggedIn, self.wrongpass, self.accountNotFound]
            self.controller.switch_frame(LoginScreen, args)
            return
        else:
            users = self.controller.getUsers()
            if len(users) == 0:
                self.accountNotFound = True
                args = [self.loggedIn, self.wrongpass, self.accountNotFound]
                self.controller.switch_frame(LoginScreen, args)
                return
            if users.get(username) == password:
                self.loggedIn = True
                self.controller.currentUser = self.controller.usersObject.get(username)
                self.controller.addUser(username, password)
                with open("users.json", "w") as jsonFile:
                    json.dump(self.controller.users, jsonFile)
                self.controller.switch_frame(DashboardScreen)
            else:
                self.wrongpass = True
                args = [self.loggedIn, self.wrongpass, self.accountNotFound]
                self.controller.switch_frame(LoginScreen, args)
    def signedUpPressed(self):
        self.controller.switch_frame(SignedUpScreen)
        return


class SignedUpScreen(frame):
    def __init__(self, controller, signedUp=False, wrongpass=False, existed = False):
        frame.__init__(self, controller)
        #State variables
        self.signedUp = signedUp #This happens when 1.password is wrong 2.havent logged in yet
        self.unmatched = wrongpass
        self.existed = existed
        self.controller = controller
        self.draw()

    def draw(self):
        if (self.signedUp == False):
            """SET UP"""
            label = tk.Label(self, text = "WELCOME TO OPTIN")
            label.pack()
            topFrame = frame(self)
            topFrame.pack(side = "top")
            middleFrame = frame(self)
            middleFrame.pack()
            bottomFrame = frame(self)
            bottomFrame.pack(side = "bottom")

            """LOG IN INFO"""
            username = tk.Label(topFrame, text = "Username")
            username.grid(row=0, stick = "E")

            users = self.controller.getUsers()
            def usernameEnter(event):
                if (users.get(username) != 1):
                    self.existed = True
                    args = [self.signedUp, self.unmatched, self.existed]
                    self.controller.switch_frame(LoginScreen, args)

            usernameEntry = tk.Entry(topFrame)
            usernameEntry.grid(row = 0, column = 1)
            self.controller.bind('<Return>', usernameEntry)


            password = tk.Label(topFrame, text = "Password")
            password.grid(row=1, stick = "E")


            passwordEntry = tk.Entry(topFrame)
            passwordEntry.grid(row = 1, column = 1)

            passwordConfirmedEntry = tk.Entry(topFrame)
            passwordConfirmedEntry.grid(row = 2, column = 1)


            def passwordEnter(event):
                if (passwordConfirmedEntry.get() != passwordEntry.get()):
                    self.unmatched = True
                    args = [self.signedUp, self.unmatched, self.existed]
                    self.controller.switch_frame(SignedUpScreen, args)

            self.controller.bind('<Return>', passwordEnter)

            if (self.unmatched == True):
                wrongPassLabel = tk.Label(text = "Unmatched Password")
                wrongPassLabel.pack()

            loginButton = tk.Button(topFrame, text = "I Opt In!", command = lambda: self.loggedInPressed(usernameEntry.get(), passwordEntry.get()))
            loginButton.grid(row = 4, stick = "E")
        return

    def loggedInPressed(self, username, password):

        if ((username is None) or (password is None)):
            args = [self.signedUp, self.wrongpass, self.existed]
            self.controller.switch_frame(LoginScreen, args)
            return
        else:
            self.controller.addUser(username, password)
            with open("users.json", "w") as jsonFile:
                json.dump(self.controller.users, jsonFile)
            self.controller.switch_frame(DashboardScreen)

class DashboardScreen(frame):
    #something else, you get the idea
    # so the point of extending Screen that Screen kinda acts as an interface, and I feel like I will want to do something
    # collectively with a Screen array or something. But even if not, it just feels more comfortable and structured to do
    def __init__(self, controller):
        frame.__init__(self)
        self.controller = controller
        #State variables
        self.draw()
    def draw(self):
        topFrame = frame(self)
        topFrame.pack(side = "top")
        bottomFrame = frame(self)
        bottomFrame.pack(side = "bottom")

        print("blah" + str(self.controller.currentUser.username))
        label = tk.Label(topFrame, text = "Welcome " + str(self.controller.currentUser.username) + "!")
        label.pack(side = "top")

        button1 = tk.Button(topFrame, text = "List of friends", fg = "red", command = lambda: self.listOfFriendsPressed())

        button1.pack(side = "left")

    def listOfFriendsPressed(self):
        self.controller.switch_frame(FriendsScreen)
    def qrPressed(self):
        self.controller.switch_frame(qrFrame)

class FriendsScreen(frame):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.draw()

    def friend_exchange(self):
        scanner.exchange(self.controller.currentUser.username, self.updateFriend)
        self.controller.switch_frame(FriendsScreen)

    def draw(self):
        button2 = tk.Button(self, text = "Add Contact", fg = "green", command = self.friend_exchange)
        button2.pack(side = "left")

        friendsList = self.controller.currentUser.friendsList
        count = 0
        topFrame = frame(self)
        topFrame.pack(side = "top")
        for friendname, friend in friendsList.items():
            button = tk.Button(topFrame, text = friendname, command = lambda : self.controller.switch_frame(MessageScreen, (friend,)))
            button.grid(row =count, column = 1)
            count += 1

    def updateFriend(self, otherUserName, otherKey):
        b = tk.Button(self, text = "Dashboard", command = lambda: self.controller.switch_frame(DashboardScreen))
        b.pack()
        friendsList = self.controller.currentUser.friendsList
        for friend in friendsList:
            if friend.username == otherUserName:
                friend.qr = otherKey
                self.controller.saveInfo()
                return
        friend = self.controller.usersObject.get(otherUserName)
        if friend == None:
            raise Exception('User specified does not exist')
        self.controller.currentUser.addFriend(friend)

class MessageScreen(frame):
    def __init__(self, controller, friend):
        super().__init__()
        self.controller = controller
        self.friend = friend
        self.draw(friend)

    def draw(self, friend):
        print("!MessageScreen draw func start")

        topFrame = frame(self)
        topFrame.pack(side = "top")
        currentUser = self.controller.currentUser

        if self.friend.username not in currentUser.messages.keys():
            currentUser.messages[self.friend.username] = []
        messageList = currentUser.messages[self.friend.username]

        print(id(messageList))
        for message in messageList:
            print('messages foiund and packing:', str(message) )
            label = tk.Label(self, text = str(message))
            label.pack()

        newMessage = tk.Label(topFrame, text = "Message")
        newMessage.pack()

        newMessageEntry = tk.Entry(topFrame)
        newMessageEntry.pack()




        def send():
            newMessageObject = Message(newMessageEntry.get(), currentUser, friend)
            print('newMessageObject\n', newMessageObject)

            #adds msg to current usr's list
            #self.controller.currentUser.messages.get(friend.username, []).append(newMessageObject)
            messageList.append(newMessageObject)

            self.send(newMessageObject, friend)
            self.controller.switch_frame(MessageScreen, [self.friend])

        sendButton = tk.Button(self, text = "SEND", command = send )
        sendButton.pack()

        b = tk.Button(self, text = "Dashboard", command = lambda: self.controller.switch_frame(DashboardScreen))
        b.pack()
        print("!MessageScreen draw func END")


    def plaintext_to_cipherbytes(self, plaintext, otp):
        plainbytes = plaintext.encode('ascii')
        len_plainbytes: int = len(plainbytes)
        if len_plainbytes > len(otp):
            raise Exception('Not enough one-time pad left to encrypt')
        otp_part = otp[0:len_plainbytes]
        cipherbytes = bytearray(len_plainbytes + 1)
        carry = 0
        for i in range(len_plainbytes):
            sumbyte = plainbytes[i] + otp_part[i] + carry
            if sumbyte >= 256:
                carry = 1
                sumbyte = sumbyte % 256
            else:
                carry = 0
            cipherbytes[i] = sumbyte
        cipherbytes[len_plainbytes] = carry
        return cipherbytes


    def send(self, message, friend):
        print("Sending message:\n'''" + str(message),"'''")
        #print("Message sent to server as: " + self.plaintext_to_cipherbytes(message.message, os.urandom(len(str(message)))).decode('utf-8'))




if __name__ == "__main__":
    app = OptIn()
    app.mainloop()
