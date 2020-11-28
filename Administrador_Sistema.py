from tkinter import *

class App(Frame):
    def __init__(self, master = None):
        Frame.__init__(self, master)
        top=self.winfo_toplevel()
        self.usuario = "yo"
        self.contra  = "Prueba"
        self.grid()
        self.createWidgets()
        self.login()

    def createWidgets(self):
        self.user  = Label(self,text="User:")
        self.user_ = Entry(self)
        self.pasword  = Label(self,text="Pasword:")
        self.pasword_ = Entry(self,show='*',exportselection=0)
        self.loginButton = Button(self,text="Login",command=self.checkLog)
        self.quitButton  = Button(self,text="Close",command=self.quit)
    
    def login(self):
        self.user.grid()
        self.user_.grid(row=0,column=1)
        self.pasword.grid()
        self.pasword_.grid(row=1,column=1)
        self.loginButton.grid(columnspan=2,sticky=N+S+E+W)
        self.quitButton.grid(column=1, sticky=E)

    def checkLog(self):
        pw = self.pasword_.get()
        us = self.user_.get()
        if(len(pw) == 0 or len(us) == 0):
            print("Datos incompletos")
        elif(self.contra == pw and self.usuario == us):
            print("Correcto")
        else:
            print("Incorrecto")
            self.user_.delete(0,last=len(us))
            self.pasword_.delete(0,last=len(pw))

app = App()
app.master.title("Administrador del Sistema")
app.mainloop()