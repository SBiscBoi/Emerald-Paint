from tkinter import *
from tkinter import filedialog, messagebox, colorchooser
from PIL import Image, ImageDraw
import PIL 

DEFAULT_CANVAS_WIDTH, DEFAULT_CANVAS_HEIGHT = 400, 400
WIDTH, HEIGHT = DEFAULT_CANVAS_WIDTH + 10, DEFAULT_CANVAS_HEIGHT + 10
DEFAULT_BG = (255, 255, 255) # White

class EmeraldPaintGUI:

    def __init__(self):
        self.root = Tk()
        self.root.title("Emerald Paint")
        self.root.iconbitmap("epIcon_256.ico")
        self.root.minsize(width=WIDTH, height=HEIGHT)
        self.root.bind("<Configure>", self.centerCanvas)

        self.brushWidth = 10.0 # initial brush width
        self.currentColor = "#000000" # initial brush color
        self.canvasWidth = DEFAULT_CANVAS_WIDTH
        self.canvasHeight = DEFAULT_CANVAS_HEIGHT

        # Menu bar
        self.menuBar = Menu(self.root)

        # File menu
        self.fileMenu = Menu(self.menuBar, tearoff=0)
        self.fileMenu.add_command(label="New Paint", command=self.clear) # Just clear for now since we don't yet check if the file being saved is new or not
        self.fileMenu.add_command(label="Save Paint", command=self.save)
        self.menuBar.add_cascade(label="File", menu=self.fileMenu)

        # Canvas menu
        self.canvasmenu = Menu(self.menuBar, tearoff=0)
        self.canvasmenu.add_command(label="Resize Canvas", command=self.resizeCanvas)
        self.menuBar.add_cascade(label="Canvas", menu=self.canvasmenu)

        # Brush menu
        self.brushmenu = Menu(self.menuBar, tearoff=0)
        self.brushmenu.add_command(label="Change Color", command=self.changeColor)
        # Brush Size will open a new small window, may change later
        self.brushmenu.add_cascade(label="Change Size", command=self.resizeBrush)
        self.menuBar.add_cascade(label="Brush", menu=self.brushmenu)
        
        self.root.config(menu=self.menuBar)

        self.canvas = Canvas(self.root, width=DEFAULT_CANVAS_WIDTH, height=DEFAULT_CANVAS_HEIGHT, bg=self.convinceRGB(DEFAULT_BG))
        self.canvas.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.canvas.pack()
        self.canvas.bind("<B1-Motion>", self.paint) # any mouse movement inside canvas or LMB will trigger the paint method

        self.image = PIL.Image.new("RGB", (DEFAULT_CANVAS_WIDTH, DEFAULT_CANVAS_HEIGHT), DEFAULT_BG)
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
    def resizeBrush(self):
        self.brushSizeWindow = Toplevel(self.root)
        self.brushSizeWindow.title("Change Brush Size")
        self.brushSizeWindow.geometry("140x30")
        self.brushSizeWindow.resizable(0,0)
        self.brushSizeWindow.attributes("-topmost", True)
        self.brushSizeWindow.attributes("-toolwindow", True)
        
        self.brushSizeLabel = Label(self.brushSizeWindow, text="Size:", height=4)
        self.brushSizeLabel.pack(side="left")
        
        self.brushSizeInput = Entry(self.brushSizeWindow, width=6)
        self.brushSizeInput.pack(side="left")
        self.brushSizeInput.insert(0, str(self.brushWidth))
        
        self.brushSizeSetButton = Button(self.brushSizeWindow, text="Submit", command=lambda: self.setBrushSize(self.brushSizeInput.get())) # verifty input is acceptable, set size
        self.brushSizeSetButton.pack(side="right")

    # Verifiy input and change brush size accordingly, close window
    def setBrushSize(self, newVal):
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

    # Center the canvas within root window
    def centerCanvas(self, event):
        self.canvas.place(relx=0.5, rely=0.5, anchor=CENTER)

    # Open window to input and change canvas size
    def resizeCanvas(self):
        self.canvasSizeWindow = Toplevel(self.root)
        self.canvasSizeWindow.title("Change Canvas Size")
        self.canvasSizeWindow.geometry("150x70")
        self.canvasSizeWindow.resizable(0,0)
        self.canvasSizeWindow.attributes("-topmost", True)
        self.canvasSizeWindow.attributes("-toolwindow", True)

        self.canvasSizeWindow.grid_rowconfigure(3)
        self.canvasSizeWindow.grid_columnconfigure(2)

        self.canvasSizeWLabel = Label(self.canvasSizeWindow, text="Width:", height=1)
        self.canvasSizeWLabel.grid(row=0, column=0, sticky="nsew", padx=20)

        self.canvasSizeWInput = Entry(self.canvasSizeWindow, width=6)
        self.canvasSizeWInput.grid(row=0, column=1, sticky="nsew")
        self.canvasSizeWInput.insert(0, str(self.canvasWidth))
                
        self.canvasSizeHLabel = Label(self.canvasSizeWindow, text="Height:", height=1)
        self.canvasSizeHLabel.grid(row=1, column=0, sticky="nsew")

        self.canvasSizeHInput = Entry(self.canvasSizeWindow, width=6)
        self.canvasSizeHInput.grid(row=1, column=1, sticky="nsew")
        self.canvasSizeHInput.insert(0, str(self.canvasHeight))

        self.canvasSizeSetButton = Button(self.canvasSizeWindow, text="Submit", command=lambda: self.setCanvasSize(self.canvasSizeWInput.get(), self.canvasSizeHInput.get())) # verifty input is acceptable, set size
        self.canvasSizeSetButton.grid(row=2, column=0, sticky="nsew", columnspan=2, padx=50)

    # Verify input, change window size if needed, resize canvas
    def setCanvasSize(self, width, height):
        try:
            width = int(width)
            height = int(height)
        except ValueError:
            messagebox.showerror("Canvas Resize Error", "Input must be a number.")
            self.canvasSizeWindow.destroy()

        answer = messagebox.askyesnocancel("Clear Warning", "WARNING: Resizing the canvas will clear the current painting.  Are you sure you want to resize?", parent=self.canvasSizeWindow)
        if answer != None:
            if answer:
                self.clear()
                # If window is smaller than canvas + padding, resize it
                print(self.root.winfo_width())
                print(width + 10)
                print(width + 10 > self.root.winfo_width())
                if width + 10 > self.root.winfo_width() or height + 10 > self.root.winfo_height():
                    self.root.minsize(width=width+10, height=height+10)
                self.canvas.config(width=width, height=height)
                self.image = PIL.Image.new("RGB", (width, height), DEFAULT_BG)
                self.draw = ImageDraw.Draw(self.image)
                self.centerCanvas(1) # takes in "event" but we can just toss garbage in here
            self.canvasSizeWindow.destroy() # should kill this child window as a result




EmeraldPaintGUI()
