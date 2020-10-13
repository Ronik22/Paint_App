from tkinter import *
from tkinter import ttk, colorchooser
import PIL
from PIL import Image, ImageDraw

import pyautogui
import time

b1 = "up"
xold, yold = None, None
background="white"
foreground="black"
penwidth=3
brushtype="round"

root = Tk()
root.title("Paint Application")
root.geometry('800x800')
root.minsize(800,800)


def save(): 
    # inaccurate drawings and saves a 1920x1080 png in white background
    filename = 'image1.png'
    image1.save(filename)
    
def save2():
    # accurate but works for 1920x1080 screens while running the app as a maximized window
    from PIL import ImageGrab
    image = ImageGrab.grab(bbox=(150,60,1920,1020))
    image.save('image2.png')

def exitWindow():
    exit()

def penfunc():  
    global brushtype
    brushtype="round"

def brushfunc():
    global brushtype
    brushtype="projecting"

def change_fg():  #changing the pen color
    global foreground
    foreground=colorchooser.askcolor(color=foreground)[1]
    brush_cpic1.config(bg=foreground)

def change_bg():  #changing the background color of the canvas
    global background
    background=colorchooser.askcolor(color=background)[1]
    brush_cpic2.config(bg=background)
    drawing_area.config(bg=background)

def brush_sizechange(event):
    global penwidth
    penwidth=slider.get()
    slider_label.config(text="Width: "+str(int(penwidth)))
    
def b1down(event):
    global b1
    b1 = "down"          

def b1up(event):
    global b1, xold, yold
    b1 = "up"
    xold = None           
    yold = None

def motion(event):
    if b1 == "down":
        global xold, yold
        if xold is not None and yold is not None:
            event.widget.create_line(xold,yold,event.x,event.y,smooth=TRUE,fill=foreground,width=penwidth,capstyle=brushtype)
            draw.line((xold, yold, event.x, event.y),fill=foreground,width=int(penwidth),joint='curve')

        xold = event.x
        yold = event.y
    


####### toolbar menu ######
main_menu=Menu(root,bg="#cedbff",tearoff=0)


file_menu=Menu(main_menu,tearoff=0)
file_menu.add_command(label='Help')
file_menu.add_command(label='Save drawing 1',command = lambda : save())
file_menu.add_command(label='Save drawing 2',command = lambda : save2())

main_menu.add_cascade(label='Options', menu = file_menu)
main_menu.add_command(label='About')
main_menu.add_command(label='Exit',command=exitWindow)
root.config(menu=main_menu)

####### tools #######
tools_area = Frame(master=root,bg="#1F7DFF",width=100)      
tools_area.pack(side=LEFT,fill=Y)

tool_selc = LabelFrame(master=tools_area,bg="#1F7DFF",fg="#fff",labelanchor='n',relief=GROOVE,bd=1)   
tool_selc.pack(anchor="center",padx=10,pady=20)
pen = Button(master=tool_selc, width=8, height=1,relief=FLAT,text="PEN",command=penfunc)
pen.pack(padx=12,pady=10,anchor="center")
eraser = Button(master=tool_selc, width=8, height=1,relief=FLAT,text="ERASER",state=DISABLED)
eraser.pack(padx=12,pady=10,anchor="center")
paintbrush = Button(master=tool_selc, width=8, height=1,relief=FLAT,text="BRUSH",command=brushfunc)
paintbrush.pack(padx=12,pady=10,anchor="center")

brush = LabelFrame(master=tools_area,bg="#1F7DFF",fg="#fff",text="FOREGROUND",labelanchor='n',relief=GROOVE,bd=1)   
brush.pack(anchor="center",padx=10,pady=20)
brush_cpic1 = Button(master=brush, width=8, height=2,relief=FLAT,command=change_fg,bg=foreground)
brush_cpic1.pack(padx=12,pady=10,anchor="center")

brush = LabelFrame(master=tools_area,bg="#1F7DFF",fg="#fff",text="BACKGROUND",labelanchor='n',relief=GROOVE,bd=1)   
brush.pack(anchor="center",padx=10,pady=20)
brush_cpic2 = Button(master=brush, width=8, height=2,relief=FLAT,command=change_bg,bg=background)
brush_cpic2.pack(padx=12,pady=10,anchor="center")

slider = ttk.Scale(master=tools_area,from_= 3, to = 50,orient=HORIZONTAL,command=brush_sizechange) 
slider.pack(side=BOTTOM,padx=12,pady=20)

slider_label=Label(master=tools_area,text="Width: "+str(penwidth))
slider_label.pack(side=BOTTOM)

drawing_area = Canvas(master=root,bg=background,cursor="hand2")
drawing_area.pack(fill=BOTH,expand=True)

drawing_area.bind("<Motion>", motion)
drawing_area.bind("<ButtonPress-1>", b1down)
drawing_area.bind("<ButtonRelease-1>", b1up)

image1 = PIL.Image.new('RGB', (1920, 1080), background)
draw = ImageDraw.Draw(image1)

root.mainloop()