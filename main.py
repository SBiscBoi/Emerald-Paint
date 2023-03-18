from tkinter import *
from tkinter import filedialog, messagebox, colorchooser
from PIL import Image, ImageDraw
import PIL 

WIDTH, HEIGHT = 400, 400
CENTER_HORIZONTAL = WIDTH // 2
DEFAULT_BG = (255, 255, 255) # White

class EmeraldPaintGUI:

    def __init__(self):
        self.root = Tk()
        self.root.title("Emerald Paint")
        self.root.iconbitmap("epIcon_256.ico")

        self.brushWidth = 10
        self.currentColor = "#000000"

        # Menu bar
        self.menuBar = Menu(self.root)

        # File menu
        self.fileMenu = Menu(self.menuBar, tearoff=0)
        self.fileMenu.add_command(label="New Paint", command=self.clear) # Just clear for now since we don't yet check if the file being saved is new or not
        self.fileMenu.add_command(label="Save Paint", command=self.save)
        self.menuBar.add_cascade(label="File", menu=self.fileMenu)

        # Brush menu
        self.brushmenu = Menu(self.menuBar, tearoff=0)
        self.brushmenu.add_command(label="Change Color", command=self.changeColor)
        self.menuBar.add_cascade(label="Brush", menu=self.brushmenu)

        self.root.config(menu=self.menuBar)

        # ********Test GUI************
        # self.buttonFrame = Frame(self.root)
        # self.buttonFrame.pack(fill=X)
 
        # self.buttonFrame.columnconfigure(0, weight=1)
        # self.buttonFrame.columnconfigure(1, weight=1)
        # self.buttonFrame.columnconfigure(2, weight=1)

        # self.clearButton = Button(self.buttonFrame, text="Clear", command=self.clear)
        # self.clearButton.grid(row=0, column=0, sticky=W+E)

        # self.saveButton = Button(self.buttonFrame, text="Save", command=self.save)
        # self.saveButton.grid(row=0, column=1, sticky=W+E)

        # # TODO: Make a slider for the brush size
        # #self.clearButton = Button(self.buttonFrame, text="Clear", command=self.clear)
        # #self.clearButton.grid(row=1, column=1, sticky=W+E)

        # self.changeColorButton = Button(self.buttonFrame, text="Change Color", command=self.changeColor)
        # self.changeColorButton.grid(row=0, column=2, sticky=W+E)

        self.canvas = Canvas(self.root, width=WIDTH-10, height=HEIGHT-10, bg="white")
        self.canvas.pack()
        self.canvas.bind("<B1-Motion>", self.paint) # any mouse movement inside canvas or LMB will trigger the paint method

        self.image = PIL.Image.new("RGB", (WIDTH, HEIGHT), DEFAULT_BG)
        self.draw = ImageDraw.Draw(self.image)


        self.root.protocol("WM_DELETE_WINDOW", self.onClosing)
        self.root.attributes("-topmost", True)
        self.root.mainloop()

    # Draw Circles where the mouse currently is based on the color and brush width.
    def paint(self, event):
        x1, y1 = (event.x - 1), (event.y - 1) 
        x2, y2 = (event.x + 1), (event.y + 1)
        self.canvas.create_oval(x1, y1, x2, y2, outline=self.currentColor, fill=self.currentColor, width=self.brushWidth)
        self.draw.ellipse([x1, y1, x2 + self.brushWidth, y2 + self.brushWidth], outline=self.currentColor, fill=self.currentColor, width=self.brushWidth)

    # Clear the canvas and image
    def clear(self):
        self.canvas.delete("all")
        self.draw.rectangle([0, 0, 10000, 10000], fill="white") #draw a huge rectengle to "clear"

    # Save the artwork to new file
    def save(self):
        filename = filedialog.asksaveasfilename(initialfile="ep_untitled.png", 
                                                defaultextension=".png", 
                                                filetypes=[("PNG", ".png"), ("JPG", ".jpg")]) # may support other formats in the future
        if filename != "":
            self.image.save(filename)

    # Change the current brush color
    def changeColor(self):
        _, chosenColor = colorchooser.askcolor(title="Color Selector") #Returns RGB and Hex, hex will be used only.
        
        if chosenColor != None:
            self.currentColor = chosenColor

    # Open a window when the user wants to exit the program to make sure the user does not exit without saving unless explicitly requesting to do so.
    def onClosing(self):
        answer = messagebox.askyesnocancel("Quit", "Would you like to save before exiting?", parent=self.root)
        if answer is not None:
            if answer:
                self.save()
            self.root.destroy()
            exit(0)


EmeraldPaintGUI()
