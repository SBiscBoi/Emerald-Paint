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

        self.brushWidth = 10.0 # initial brush width
        self.currentColor = "#000000" # initial brush color

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
        # Brush Size will open a new small window, may change later
        self.brushmenu.add_cascade(label="Change Size", command=self.changeBrushSize)
        self.menuBar.add_cascade(label="Brush", menu=self.brushmenu)
        
        self.root.config(menu=self.menuBar)

        self.canvas = Canvas(self.root, width=WIDTH-10, height=HEIGHT-10, bg=self.convinceRGB(DEFAULT_BG))
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

    # Ask if the uder wants to save, then clear the canvas and image
    def clear(self):
        answer = messagebox.askyesnocancel("New Paint", "Would you like to save before clearing?", parent=self.root)
        if answer is not None:
            if answer:
                self.save()
            self.canvas.delete("all")
            self.draw.rectangle([0, 0, 10000, 10000], fill=DEFAULT_BG) #draw a huge rectengle to "clear"

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

    # Open the window to change brush size
    def changeBrushSize(self):
        self.brushSizeWindow = Toplevel(self.root)
        self.brushSizeWindow.title("Change Brush Size")
        self.brushSizeWindow.geometry("125x30")
        self.brushSizeWindow.resizable(0,0)
        self.brushSizeWindow.attributes("-topmost", True)
        
        self.brushSizeLabel = Label(self.brushSizeWindow, text="Size:", height=4)
        self.brushSizeLabel.pack(side="left")
        
        self.brushSizeInput = Entry(self.brushSizeWindow, width=6)
        self.brushSizeInput.pack(side="left")
        self.brushSizeInput.insert(0, str(self.brushWidth))
        
        self.brushSizeSetButton = Button(self.brushSizeWindow, text="Submit", command=lambda: self.setBrushSize(self.brushSizeInput.get())) # verifty input is acceptable, set size
        self.brushSizeSetButton.pack(side="right")

    # Verifiy input and change brush size accordingly, close window
    def setBrushSize(self, newVal):
        print(newVal)
        if newVal != None:
            try:
                newVal = float(newVal)
                if newVal < 1 or newVal > 100: #check if out of range
                    messagebox.showerror("Brush Size Error","Brush Size must be between 1 and 100")
                else:
                    self.brushWidth = newVal
            except ValueError:
                messagebox.showerror("Brush Size Error", "Brush Size must be a number")
        self.brushSizeWindow.destroy()

    # Open a window when the user wants to exit the program to make sure the user does not exit without saving unless explicitly requesting to do so.
    def onClosing(self):
        answer = messagebox.askyesnocancel("Quit", "Would you like to save before exiting?", parent=self.root)
        if answer is not None:
            if answer:
                self.save()
            self.root.destroy()
            exit(0)

    # convert RGB 3-int tuple to tkinter friendly color code
    def convinceRGB(self, rgb):
        return "#%02x%02x%02x" % rgb



EmeraldPaintGUI()
