from tkinter import *

class App(Frame):
    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        self.quitButton = Button (self, text = "Close", command = self.quit)
        self.quitButton.grid()

app = App()
app.master.title("Administrador del Sistema")
app.mainloop()