from tkinter import *

bg_color= "#dfe0e5"
root=Tk()
root.title("Paint")
root.geometry("1100x600")
root.config(bg=bg_color)
previous_point=[0,0]
current_point=[0,0]
color="black"
thickness=1

def pencil (event):
    global previous_point
    global current_point
    x= event.x
    y= event.y
    current_point=[x,y]
    if previous_point!= [0,0]:
        canvas.create_line(previous_point[0], previous_point[1], current_point[0], current_point[1], fill=color, width=thickness)
    previous_point=current_point
    if event.type=="5":
        previous_point=[0,0]
    #canvas.create_oval(x, y, x+1, y+1, fill="black", width=5)
    

frame1 = Frame(root, height=150, width=1100,bg="White")
frame1.grid(row=0,column=0,sticky=NW)
  
utils = Frame(frame1, height=150, width=150,bg="Black")
utils.grid(row=0,column=0)

pencilButton=Button(utils, text="Pencil", width=10)
pencilButton.grid(row=0,column=0)

eraserButton=Button(utils, text="Eraser", width=10)
eraserButton.grid(row=1,column=0)

toolsLabel = Label(utils, text="Tools", width=11)
toolsLabel.grid(row=2,column=0)

frame2 = Frame(root, height=450, width=1100,bg="White")
frame2.grid(row=1,column=0)

canvas= Canvas(frame2, bg="White", width=1100, height=450)
canvas.grid(row=0,column=0)
root.resizable(False,False)

canvas.bind("<B1-Motion>", pencil)
canvas.bind("<ButtonRelease-1>", pencil)


root.mainloop()