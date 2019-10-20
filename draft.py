import tkinter as tk
from datetime import datetime
import re
import PIL
from Pillow import*

class LoadImage:
    def loadImage(self):

class Users:
    def __init__(self):
        self.users = {}
    def addUser(self, userName, password):
        newUser = User(userName, password)
        self.users.add(newUser)
class User:
    def __init__(self, userName, password):
        self.userName = userName
        self.password = password
        self.messages = dict() # recipientUser : messageList
        self.friendsList = {}

    def addFriend(self, otherUser):
        self.friendsList.add(otherUser)

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
        self._frame = None
        self.switch_frame(CreateAccount)
        self.users = Users()
    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

class CreateAccount(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        label = tk.Label(self, text = "WELCOME TO OPTIN")
        label.pack()
        topFrame = tk.Frame(self)
        topFrame.pack(side = "top")
        middleFrame = tk.Frame(self)
        middleFrame.pack()
        bottomFrame = tk.Frame(self)
        bottomFrame.pack(side = "bottom")
        self.username = tk.Label(topFrame, text = "Username")
        self.username.grid(row=0, stick = "E")

        self.usernameEntry = tk.Entry(topFrame)
        self.usernameEntry.grid(row = 0, column = 1)

        self.password = tk.Label(topFrame, text = "Password")
        self.password.grid(row=1, stick = "E")

        self.passwordEntry = tk.Entry(topFrame)
        self.passwordEntry.grid(row = 1, column = 1)

        self.passwordConfirmed = tk.Label(topFrame, text = "Password")
        self.passwordConfirmed.grid(row=2, stick = "E")

        """if (self.passwordConfirmedEntry != self.passwordEntry):
            label = tk.Label(self, text = "Unmatched Password")
            label.grid(row = 5, column = 1)

            master.switch_frame(CreateAccount)"""
        self.passwordConfirmedEntry = tk.Entry(topFrame)
        self.passwordConfirmedEntry.grid(row = 2, column = 1)

        c = tk.Checkbutton(topFrame, text = "Agree to OptIn's Contracting Rules")
        c.grid(columnspan = 2)

        tk.createAccountButton = tk.Button(topFrame, text = "I Opt In!", command = lambda: self.createAccountPressed(master, self.usernameEntry, self.passwordEntry))
        tk.createAccountButton.grid(row = 4, stick = "E")
    def createAccountPressed(self, master, userName, password):
        master.users.addUser(userName, password)
class LoginPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        label = tk.Label(self, text = "WELCOME TO OPTIN")
        label.pack() #just pack it in somewhere
        topFrame = tk.Frame(self)
        topFrame.pack(side = "top")
        middleFrame = tk.Frame(self)
        middleFrame.pack()
        bottomFrame = tk.Frame(self)
        bottomFrame.pack(side = "bottom")

        self.username = tk.Label(topFrame, text = "Username")
        self.username.grid(row=0, stick = "E")

        self.usernameEntry = tk.Entry(topFrame)
        self.usernameEntry.grid(row = 0, column = 1)

        self.password = tk.Label(topFrame, text = "Password")
        self.password.grid(row=1, stick = "E")

        self.passwordEntry = tk.Entry(topFrame)
        self.passwordEntry.grid(row = 1, column = 1)

        c = tk.Checkbutton(topFrame, text = "Keep me logged in")
        c.grid(columnspan = 2)

        tk.login_button = tk.Button(topFrame, text = "I Opt In!", command = lambda: master.switch_frame(MenuPage))
        tk.login_button.grid(row = 3, stick = "E")


class MenuPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        topFrame = tk.Frame(self)
        topFrame.pack(side = "top")
        bottomFrame = tk.Frame(self)
        bottomFrame.pack(side = "bottom")

        button1 = tk.Button(topFrame, text = "List of friends", fg = "red")
        button2 = tk.Button(topFrame, text = "Camera", fg = "blue")
        button3 = tk.Button(topFrame, text = "Your QR", fg = "green")

        button1.pack(side = "left")
        button2.pack(side = "left")
        button3.pack(side = "left")

class FriendsPage(tk.Frame):
    def __init__(self, root, controller):
        tk.Frame.__init__(self, root)
        self.controller = controller
        topFrame = tk.Frame(root)
        topFrame.pack(side = "top")

        label = tk.Label(topFrame, text = "Message", fg = "purple")
        label.grid(row = 0, column = 0)
        message_entry = tk.Entry(topFrame)
        message_entry.grid(row=0, column = 1)


if __name__ == "__main__":
    app = OptIn()
    app.mainloop()
