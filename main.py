from tkinter import *
from PIL import Image, ImageDraw
import PIL

WIDTH, HEIGHT = 400, 400
CENTER_HORIZONTAL = WIDTH // 2
DEFAULT_COLOR = (255, 255, 255) # White

class EmeraldPaintGUI:

    def __init__(self):
        self.root = Tk()
        self.root.title("Emerald Paint")

        self.brushWidth = 10
        self.currentColor = "#000000"

        self.canvas = Canvas(self.root, width=WIDTH-10, height=HEIGHT-10, bg="white")
        self.canvas.pack()
        self.canvas.bind("<B1-Motion>", self.paint) # any mouse movement inside canvas or LMB will trigger the paint method

        self.image = PIL.Image.new("RGB", (WIDTH, HEIGHT), DEFAULT_COLOR)
        self.draw = ImageDraw.Draw(self.image)

        self.buttonFrame = Frame(self.root)
        self.buttonFrame.pack(fill=X)

        self.buttonFrame.columnconfigure(0, weight=1)
        self.buttonFrame.columnconfigure(1, weight=1)
        self.buttonFrame.columnconfigure(2, weight=1)

        self.clearButton = Button(self.buttonFrame, text="Clear", command=self.clear)
        self.clearButton.grid(row=0, column=0, sticky=W+E)

        self.saveButton = Button(self.buttonFrame, text="Save", command=self.save)
        self.saveButton.grid(row=0, column=1, sticky=W+E)

        # TODO: Make a slider for the brush size
        #self.clearButton = Button(self.buttonFrame, text="Clear", command=self.clear)
        #self.clearButton.grid(row=1, column=1, sticky=W+E)
        
        # IDEA: make this a color-picker style element 
        self.changeColorButton = Button(self.buttonFrame, text="Change Color", command=self.changeColor)
        self.changeColorButton.grid(row=0, column=2, sticky=W+E)

        self.root.protocol("WM_DELETE_WINDOW", self.onClosing)
        self.root.attributes("-topmost", True)
        self.root.mainloop()


    def paint(self):
        pass

    def clear(self):
        pass

    def save(self):
        pass

    def changeColor(self):
        pass

    def onClosing(self):
        pass


EmeraldPaintGUI()
