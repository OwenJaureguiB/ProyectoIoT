import os
import cv2
import numpy as np
from PIL import Image as image
import firebase_admin
from tkinter import *
from firebase_admin import credentials, db, storage

class App(Frame):
    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.grid()
        self.firebaseConnection()
        self.createWidgets()
        self.login()

    def firebaseConnection(self):
        cred = credentials.Certificate("controlacceso-iot-firebase-adminsdk-s0oyr-e0fd69aa2b.json")
        firebase_admin.initialize_app(cred, {"databaseURL":"https://controlacceso-iot.firebaseio.com/","storageBucket": "controlacceso-iot.appspot.com"})
        self.bucket = storage.bucket()

    def createWidgets(self):
        self.user  = Label(self,text="Usuario:")
        self.user_ = Entry(self)
        self.pasword  = Label(self,text="Contraseña:")
        self.pasword_ = Entry(self,show='*',exportselection=0)
        self.nombre  = Label(self,text="Nombre:")
        self.nombre_ = Entry(self)
        self.apellido  = Label(self,text="Apellido:")
        self.apellido_ = Entry(self)
        self.usuarios = Label(self,text="Usuarios")
        self.acceso = Label(self,text="Acceso Permitido")
        self.loginButton = Button(self,text="Login",command=self.checkLog)
        self.quitButton  = Button(self,text="Close",command=self.quit)
        self.newUser = Button(self,text="Crear nuevo usuario",command=self.createUser)
        self.removeUser = Button(self,text="Borrar usuarios",command=self.delUser)
        self.adminUsers = Button(self,text="Administrar permisos",command=self.access)
        self.agregarPerm = Button(self,text="Ver Habitacion",command=self.agregarPermiso)
        self.giveAcc = Button(self,text="Otorgar Permiso",command=self.giveAccess)
        self.removeAcc = Button(self,text="Remover Permiso",command=self.removeAccess)
        self.SetUser = Button(self,text="Crear Usuario",command=self.getUserData)
        self.yScroll = Scrollbar(self, orient=VERTICAL)
        self.listaRooms = Listbox(self,selectmode=SINGLE,yscrollcommand=self.yScroll.set,width=40)
        self.yScroll2 = Scrollbar(self, orient=VERTICAL)
        self.usuarios_sin_permiso = Listbox(self,selectmode=MULTIPLE,yscrollcommand=self.yScroll2.set,width=40)
        self.yScroll3 = Scrollbar(self, orient=VERTICAL)
        self.usuarios_con_permiso = Listbox(self,selectmode=MULTIPLE,yscrollcommand=self.yScroll3.set,width=40)

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
        if(len(pw) == 0 or len(us) == 0 and False):
            print("Datos incompletos")
        elif(self.admin["Pasword"] == pw and self.admin["Usuario"] == us or True):
            print("Correcto")
            self.administrar()
        else:
            print("Incorrecto")
            self.user_.delete(0,last=len(us))
            self.pasword_.delete(0,last=len(pw))

    def administrar(self):
        self.dbRooms = db.reference("Habitacion")
        self.rooms = self.dbRooms.get()
        self.dbUsers = db.reference("Usuarios")
        self.users = self.dbUsers.get()
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

    def forgetLog(self):
        self.newUser.grid_forget()
        self.removeUser.grid_forget()
        self.adminUsers.grid_forget()

    def createUser(self):
        self.forgetLog()
        self.nombre.grid(row=0)
        self.nombre_.grid(row=0,column=1)
        self.apellido.grid(row=1)
        self.apellido_.grid(row=1,column=1)
        self.SetUser.grid(row=2,columnspan=2,sticky=N+S+E+W)
        self.quitButton.grid_forget()
        self.quitButton.grid(row=3,column=1,sticky=E)
        
    def getUserData(self):
        self.lectura()
        self.train()
        blob = self.bucket.blob("trainer.yml")
        blob.upload_from_filename("trainer/trainer.yml")
        newUser = "Usuario" + str(len(self.users))
        permisos = {}
        for i in range(len(self.rooms)):
            permisos["Permiso"+str(i)]=False
        self.dbUsers.child(newUser).set({"Nombre":self.nombre_.get(), 
                     "Apellido":self.apellido_.get(),
                     "Permisos":permisos}
        )

    def delUser(self):
        print(self.users)

    def access(self):
        self.forgetLog()
        self.yScroll.grid( row=0, column=1, sticky=N+S )
        self.listaRooms.grid( row=0, column=0, sticky=N+S+E+W )
        self.yScroll["command"] = self.listaRooms.yview
        self.agregarPerm.grid(row=1, columnspan=2,sticky=N+S+E+W)
        for room in range(len(self.rooms)):
            self.listaRooms.insert(room,self.rooms[room]["Nombre"])

    def agregarPermiso(self):
        self.tabla = [[],[]]
        self.listaRooms.grid_forget()
        self.yScroll.grid_forget()
        self.agregarPerm.grid_forget()
        self.usuarios.grid(row=0)
        self.acceso.grid(row=0,column=2)
        self.habitacion = self.listaRooms.curselection()[0]
        self.listaRooms.delete(0,END)
        self.yScroll2.grid(row=1, column=1, sticky=N+S)
        self.usuarios_sin_permiso.grid(row=1, column=0, sticky=N+S+E+W)
        self.yScroll2["command"] = self.usuarios_sin_permiso.yview
        self.yScroll3.grid( row=1, column=3, sticky=N+S )
        self.usuarios_con_permiso.grid( row=1, column=2, sticky=N+S+E+W)
        self.yScroll3["command"] = self.usuarios_con_permiso.yview
        self.giveAcc.grid(row=2,sticky=N+S+E+W)
        self.removeAcc.grid(row=2,column=2,sticky=N+S+E+W)
        self.llaves = list(self.users.keys())
        for user in range(len(self.llaves)):
            codigo = self.users[self.llaves[user]]["Nombre"] + " " + self.users[self.llaves[user]]["Apellido"]
            if(self.users[self.llaves[user]]["Permisos"]["Permiso"+str(self.habitacion)]):
                self.tabla[1].append(self.llaves[user])
                self.usuarios_con_permiso.insert(user,codigo)
            else:
                self.tabla[0].append(self.llaves[user])
                self.usuarios_sin_permiso.insert(user,codigo)

    def giveAccess(self):
        cont=0
        for index_ in self.usuarios_sin_permiso.curselection():
            index = index_-cont
            self.usuarios_con_permiso.insert(END,self.usuarios_sin_permiso.get(index))
            self.tabla[1].append(self.tabla[0][index])
            self.dbUsers.child(self.tabla[0][index]+"/Permisos/Permiso"+str(self.habitacion)).set(True)
            self.usuarios_sin_permiso.delete(index)
            self.tabla[0].pop(index)
            cont += 1

    def removeAccess(self):
        cont=0
        for index_ in self.usuarios_con_permiso.curselection():
            index = index_-cont
            self.usuarios_sin_permiso.insert(END,self.usuarios_con_permiso.get(index))
            self.tabla[0].append(self.tabla[1][index])
            self.dbUsers.child(self.tabla[1][index]+"/Permisos/Permiso"+str(self.habitacion)).set(False)
            self.usuarios_con_permiso.delete(index)
            self.tabla[1].pop(index)
            cont += 1

    def lectura(self):
        cam = cv2.VideoCapture(0)
        cam.set(3, 640) # set video width
        cam.set(4, 480) # set video height

        face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

        # For each person, enter one numeric face id
        face_id = len(self.users)

        print("\n [INFO] Initializing face capture. Look the camera and wait ...")
        # Initialize individual sampling face count
        count = 0

        while(True):

            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_detector.detectMultiScale(gray, 1.3, 5)

            for (x,y,w,h) in faces:

                cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)     
                count += 1

                # Save the captured image into the datasets folder
                cv2.imwrite("dataset/User." + str(face_id) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])
                #blob = self.bucket.blob(str(face_id)+"/User." + str(face_id) + '.' + str(count) + ".jpg")
                #blob.upload_from_filename("dataset/User." + str(face_id) + '.' + str(count) + ".jpg")
                cv2.imshow('image', img)

            k = cv2.waitKey(100) & 0xff # Press 'ESC' for exiting video
            if k == 27:
                break
            elif count >= 30: # Take 30 face sample and stop video
                break

        # Do a bit of cleanup
        print("\n [INFO] Exiting Program and cleanup stuff")
        cam.release()
        cv2.destroyAllWindows()

    def getImagesAndLabels(self,path):

        imagePaths = [os.path.join(path,f) for f in os.listdir(path)]     
        faceSamples=[]
        ids = []

        for imagePath in imagePaths:

            PIL_img = image.open(imagePath).convert('L') # convert it to grayscale
            img_numpy = np.array(PIL_img,'uint8')

            id = int(os.path.split(imagePath)[-1].split(".")[1])
            faces = self.detector.detectMultiScale(img_numpy)

            for (x,y,w,h) in faces:
                faceSamples.append(img_numpy[y:y+h,x:x+w])
                ids.append(id)

        return faceSamples,ids

    def train(self):
        path = 'dataset'

        recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

        print ("\n [INFO] Training faces. It will take a few seconds. Wait ...")
        faces,ids = self.getImagesAndLabels(path)
        recognizer.train(faces, np.array(ids))

        # Save the model into trainer/trainer.yml
        recognizer.write('trainer/trainer.yml') # recognizer.save() worked on Mac, but not on Pi

        # Print the numer of faces trained and end program
        print("\n [INFO] {0} faces trained. Exiting Program".format(len(np.unique(ids))))

app = App()
app.master.title("Administrador del Sistema")
app.mainloop()