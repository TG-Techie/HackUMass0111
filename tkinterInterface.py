import re
import tkinter as tk
from datetime import datetime
import scanner

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
        self.users = dict()

        self.func_loops = {}
        #FIXME loged_in_username
        self._frame = None
        self.switch_frame(SignedUpScreen)
        #self.new_qr_frame( scanner.bitmap.string_to_bitmap('as;lghkjsfghk'))

    def getUsers(self):
        return self.users

    def addUser(self, username, password):
        self.users[username] = User(username, password)

    def switch_frame(self, frame_class, args = []):

        """Destroys current frame and replaces it with a new one."""
        if len(args) == 0:
            new_frame = frame_class(self)
        else:
            if frame_class == LoginScreen:
                new_frame = frame_class(self, args[0], args[1], args[2])
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


class LoginScreen(tk.Frame):
    # define some states

    def __init__(self, controller, loggedIn=False, wrongpass=False, accountNotFound=False):
        tk.Frame.__init__(self, controller)
        #State variables
        self.loggedIn = loggedIn #This happens when 1.password is wrong 2.havent logged in yet
        self.wrongpass = wrongpass
        self.accountNotFound = accountNotFound
        self.controller = controller
        print(self.controller.users)
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
            if users.get(username).password == password:
                self.loggedIn = True
                args = [self.loggedIn, self.wrongpass, self.accountNotFound]
                self.controller.switch_frame(DashboardScreen, args)
            else:
                self.wrongpass = True
                args = [self.loggedIn, self.wrongpass, self.accountNotFound]
                self.controller.switch_frame(LoginScreen, args)
    def signedupPressed(self):
        self.controller.switch_frame(SignedUpScreen)


class SignedUpScreen(tk.Frame):

    def __init__(self, controller):
        super().__init__(controller)

        try:
            name = controller.loged_in_username
        except:
            name = "ANON"
        b = tk.Button(text="add contact", command = lambda *args: scanner.exchange(name) )
        b.pack()

class DashboardScreen(tk.Frame):
    #something else, you get the idea
    # so the point of extending Screen that Screen kinda acts as an interface, and I feel like I will want to do something
    # collectively with a Screen array or something. But even if not, it just feels more comfortable and structured to do
    pass


        #w.pack()


if __name__ == "__main__":
    app = OptIn()
    app.mainloop()
