from tkinter import *
import firebase_admin
from firebase_admin import credentials, db, storage, firestore

class App(Frame):
    def __init__(self, master = None):
        Frame.__init__(self, master)
        top=self.winfo_toplevel()
        self.grid()
        self.firebaseConnection()
        self.createWidgets()
        self.login()

    def firebaseConnection(self):
        cred = credentials.Certificate("controlacceso-iot-firebase-adminsdk-s0oyr-e0fd69aa2b.json")
        firebase_admin.initialize_app(cred, {"databaseURL":"https://controlacceso-iot.firebaseio.com/"})

    def createWidgets(self):
        self.user  = Label(self,text="Usuario:")
        self.user_ = Entry(self)
        self.pasword  = Label(self,text="Contraseña:")
        self.pasword_ = Entry(self,show='*',exportselection=0)
        self.loginButton = Button(self,text="Login",command=self.checkLog)
        self.quitButton  = Button(self,text="Close",command=self.quit)
        self.newUser = Button(self,text="Crear nuevo usuario",command=self.createUser)
        self.removeUser = Button(self,text="Borrar usuarios",command=self.delUser)
        self.adminUsers = Button(self,text="Administrar permisos",command=self.access)
    
    def login(self):
        self.admin = db.reference("Admin").get()
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
        elif(self.admin["Pasword"] == pw and self.admin["Usuario"] == us):
            print("Correcto")
            self.administrar()
        else:
            print("Incorrecto")
            self.user_.delete(0,last=len(us))
            self.pasword_.delete(0,last=len(pw))

    def administrar(self):
        self.dbUsers = db.reference("Usuarios")
        self.dbRooms = db.reference("Habitacion")
        self.users = self.dbUsers.get()
        self.rooms = self.dbRooms.get()
        self.user.grid_forget()
        self.user_.grid_forget()
        self.pasword.grid_forget()
        self.pasword_.grid_forget()
        self.loginButton.grid_forget()
        self.quitButton.grid_forget()
        self.newUser.grid(row=1,columnspan=2,sticky=N+S+E+W)
        self.removeUser.grid(row=2,columnspan=2,sticky=N+S+E+W)
        self.adminUsers.grid(row=3,columnspan=2,sticky=N+S+E+W)
        self.quitButton.grid(column=1, sticky=E)

    def createUser(self):
        execfile("01_face_dataset.py")

    def delUser(self):
        print(self.users)

    def access(self):
        self.newUser.grid_forget()
        self.removeUser.grid_forget()
        self.adminUsers.grid_forget()
        print(self.rooms)

app = App()
app.master.title("Administrador del Sistema")
app.mainloop()