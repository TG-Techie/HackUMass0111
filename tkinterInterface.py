import re
import tkinter as tk
from datetime import datetime
import json

class User:

    def __init__(self, userName, password):

        self.username = userName
        self.password = password
        self.messages = dict() # recipientUser : messageList
        self.friendsList = {}
        self.qr = None

    def addFriend(self, otherUser):
        self.friendsList.append(otherUser)

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

    def __repr__(self):
        s = str(self.sender.userName) + "\n"
        s += str(self.recipient.userName) + "\n ----- \n"
        s += self.message + "\n ----- \n"
        s += str(self.timeStamp) + "\n"
        return s


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
    def getUsers(self):
        return self.users
    def getUsersObject(self):
        return self.usersObject
    def addUser(self, username, password):
        self.users[username] = password
        newUser = User(username, password)
        self.usersObject[username] = newUser
        return newUser
    def switch_frame(self, frame_class, args = []):

        """Destroys current frame and replaces it with a new one."""
        if len(args) == 0 or frame_class == DashboardScreen:
            new_frame = frame_class(self)
        else:
            if frame_class == LoginScreen:
                new_frame = frame_class(self, args[0], args[1], args[2])
            elif frame_class == SignedUpScreen:
                new_frame = frame_class(self, args[0], args[1], args[2])
        if self._frame is not None:
            self._frame.destroy()

        self._frame = new_frame
        self._frame.pack()


class LoginScreen(tk.Frame):
    # define some states

    def __init__(self, controller, loggedIn=False, wrongpass=False, accountNotFound=False):
        tk.Frame.__init__(self, controller)
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
            topFrame = tk.Frame(self)
            topFrame.pack(side = "top")
            middleFrame = tk.Frame(self)
            middleFrame.pack()
            bottomFrame = tk.Frame(self)
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
                self.controller.switch_frame(DashboardScreen, args)
            else:
                self.wrongpass = True
                args = [self.loggedIn, self.wrongpass, self.accountNotFound]
                self.controller.switch_frame(LoginScreen, args)
    def signedUpPressed(self):
        self.controller.switch_frame(SignedUpScreen)
        return


class SignedUpScreen(tk.Frame):
    def __init__(self, controller, signedUp=False, wrongpass=False, existed = False):
        tk.Frame.__init__(self, controller)
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
            topFrame = tk.Frame(self)
            topFrame.pack(side = "top")
            middleFrame = tk.Frame(self)
            middleFrame.pack()
            bottomFrame = tk.Frame(self)
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
            self.controller.currentUser = self.controller.addUser(username, password)
            print(self.controller.currentUser.username)
            with open("users.json", "w") as jsonFile:
                json.dump(self.controller.users, jsonFile)
            self.controller.switch_frame(DashboardScreen)

class DashboardScreen(tk.Frame):
    #something else, you get the idea
    # so the point of extending Screen that Screen kinda acts as an interface, and I feel like I will want to do something
    # collectively with a Screen array or something. But even if not, it just feels more comfortable and structured to do
    def __init__(self, controller):
        tk.Frame.__init__(self)
        self.controller = controller
        #State variables
        self.draw()
    def draw(self):
        topFrame = tk.Frame(self)
        topFrame.pack(side = "top")
        bottomFrame = tk.Frame(self)
        bottomFrame.pack(side = "bottom")

        print("blah" + str(self.controller.currentUser.username))
        label = tk.Label(topFrame, text = "Welcome " + str(self.controller.currentUser.username) + "!")
        label.pack(side = "top")

        button1 = tk.Button(topFrame, text = "List of friends", fg = "red", command = lambda: self.listOfFriendsPressed())
        button2 = tk.Button(topFrame, text = "Your QR", fg = "green", command = lambda: self.qrPressed())

        button1.pack(side = "left")
        button2.pack(side = "left")

    def listOfFriendsPressed(self):
        self.controller.switch_frame(FriendsScreen)
    def qrPressed(self):
        self.controller.switch_frame(qrFrame)
class qrFrame(tk.Frame):
    pass

class FriendsScreen(tk.Frame):
    def __init__(self, controller):
        tk.Frame.__init__(self)
        self.controller = controller
        self.draw()

    def draw(self):
        friendsList = self.controller.currentUser.friendsList
        count = 0
        topFrame = tk.Frame(self)
        topFrame.pack(side = "top")
        for friend in friendsList:
            button = tk.Button(topFrame, text = friend.username, command = lambda : self.controller.switch_frame(MessageScreen, friend))
            button.grid(row =count, column = 1)
            count += 1
    def updateFriend_main(self, otherUserName, otherKey):
        friendsList = self.controller.currentUser.friendsList
        for friend in friendsList:
            if friend.username == otherUserName:
                friend.qr = otherKey
                ##NEED TO SAVE ALL DATA EVERY TIME WE UPDATE INFO including signUp, updateFriend
                self.controller.saveInfo()
                return
        friend = self.controller.usersObject.get(otherUserName)
        self.currentUser.addFriend(friend)

class MessageScreen(tk.Frame):
    def __init__(self, friend):
        pass
if __name__ == "__main__":
    app = OptIn()
    app.mainloop()