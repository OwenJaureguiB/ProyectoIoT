import Tkinter as tk

class App(Frame):
    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        self.quitButton = Button (self, text = "Close", command = self.quit)
        self.quitButton.grid()

if __name__ == "__main__":
    app = App()
    app.master.title("Administrador del Sistema")
    app.mainloop()
    pass