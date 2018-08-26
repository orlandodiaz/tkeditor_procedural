# Copyright 2018 Orlando Reategui Diaz

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.

################################# NOTES #######################################
# This a procedural-based tkinter text editor made as an exercise
import subprocess
from tkinter import filedialog
from tkinter import *
from tkinter import StringVar
import sys
from PIL import Image, ImageTk
import os

############################### ACTIONS #######################################
file = None
def open_file(*args):
    global file

    # Open file dialog and get path of selected
    filename = filedialog.askopenfilename(
    filetypes =[("All Files","*.*"),("Text Documents","*.txt")])

    if filename:
        # Clear out the textbox screen
        textBox.delete(1.0, END)

        # Closes any open files before reading another one
        if file is not None: file.close()

        file = open(filename, 'r+')

        # Read the file and also save the number of lines
        linenums = read_file(file)
        linenumbers.set(linenums)

def read_file(file):
    """ Inserts line by line while counting the number of lines"""
    if file is not None:
        linenumstring = ''
        for num, line in enumerate(file, start=1):
            # print('inside loop')
            linenumstring += '{}\n'.format(num)
            # linenumbers.set(linenumstring)
            textBox.insert(INSERT, line)
        return linenumstring
    else:
        print('is none')
        return ''

def save_file():
    global file

    if not file.closed:
        " Get the text from the textbox"
        contents = textBox.get("1.0",END)
        print("contents are {}".format(contents))

        file.seek(0)
        file.truncate()
        file.write(contents)
        file.flush()
        print("File was saved")
    else:
        print('No file is curently opened')

def save_as():
    global file
    path = filedialog.asksaveasfile( defaultextension=".txt")
    if path:
        print(path.name)
        print(os.path.isfile(path.name))
        " Get the text from the textbox"
        contents = textBox.get("1.0", END)
        file = open(path.name, 'r+')
        file.seek(0)
        file.truncate()
        file.write(contents)
        file.flush()
        print("File was saved")

def close_file():
    global file
    if file is None:
        print('No file to close')
    else:
        file.close()
        textBox.delete(1.0, END)

def show_linenums():
    global content
    if not has_linenums.get():
        linenumbar.pack_forget()
        linenum_label.pack_forget()
    else:

        textBox.pack_forget()
        linenumbar.pack(expand=NO, fill=Y, side=LEFT)
        linenum_label.pack(fill=Y)

        textBox.pack(expand=YES, fill=BOTH)

def cut(): textBox.event_generate("<<Cut>>")
def copy(): textBox.event_generate("<<Copy>>")
def paste(): textBox.event_generate("<<Paste>>")
def undo(): textBox.event_generate("<<Undo>>")
def redo(): textBox.event_generate("<<Redo>>")
def select_all(): textBox.tag_add('sel', '1.0', 'end')

def getimg(img_path):
    im = Image.open(img_path)
    photo = ImageTk.PhotoImage(im)
    im.close()
    return photo

def draw_info_dialog():
    info_dialog = Toplevel(root, bg="#E4E4E4")
    info_dialog.title="About"
    info_dialog.transient(root)

    # get screen width and height
    ws = info_dialog.winfo_screenwidth()  # width of the screen
    # print(info_dialog.winfo_screenwidth())
    hs = info_dialog.winfo_screenheight()  # height of the screen

    # calculate x and y coordinates for the Tk root window
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)

    # set the dimensions of the screen and where it is placed
    info_dialog.geometry('%dx%d+%d+%d' % (300, 80, x+120, y+100))

    version_label = Label(info_dialog, bg="#E4E4E4",
                          text = "Version: OTE Version 0.1 Copyright 2018")
    author_label = Label(info_dialog, bg="#E4E4E4",
                         text = "Author: Orlando R.")
    version_label.pack()
    author_label.pack()

################################# MAIN ########################################
root = Tk()
root.title("Orr's Text Editor")
w = 600
h = 650
root.tk_setPalette(background='#C6C6C6')

# get screen width and height
ws = root.winfo_screenwidth() # width of the screen
hs = root.winfo_screenheight() # height of the screen

# calculate x and y coordinates for the Tk root window
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)

# set the dimensions of the screen 
# and where it is placed
root.geometry('%dx%d+%d+%d' % (w, h, x, y))

########################## ICONS ##############################################

disk_icon = getimg('res/disk-black.png')
open_icon = getimg('res/folder-horizontal-open.png')
copy_icon = getimg('res/blue-document-copy.png')
paste_icon = getimg('res/clipboard-paste-document-text.png')
undo_icon = getimg('res/arrow-curve-180-left.png')
redo_icon = getimg('res/arrow-curve.png')
cut_icon = getimg('res/scissors-blue.png')
search_icon = getimg('res/magnifier-zoom.png')
info_icon = getimg('res/information.png')

############################# MENUBAR #########################################
menubar = Menu(root)
root.config(menu=menubar)

############################# FILE MENU #######################################
file_menu = Menu (menubar)
menubar.add_cascade(label='File', menu=file_menu)

file_menu.add_command(label="Open", command=open_file, compound=LEFT,
                      image=open_icon, accelerator="Ctrl-O", underline=0)
file_menu.add_command(label="Save", command=save_file, compound=LEFT,
                      image=disk_icon, accelerator="Ctrl-S")

file_menu.add_command(label="Save as", command=save_as, compound=LEFT,
                      image=disk_icon, accelerator="Ctrl-S")
file_menu.add_command(label="Close", command=close_file, compound=LEFT,
                      accelerator="Ctrl-w")
file_menu.add_command(label='Exit', command=sys.exit, accelerator="Ctrl-Q")

############################# EDIT MENU #######################################
edit_menu = Menu(menubar)
menubar.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Undo", accelerator="Ctrl-Z", compound=LEFT,
                      image=undo_icon, command=undo)
edit_menu.add_command(label="Redo", accelerator="Ctrl-Y", compound=LEFT,
                      image=redo_icon, command=redo)
edit_menu.add_separator()
edit_menu.add_command(label="Cut", accelerator="Ctrl-X", compound=LEFT,
                      image=cut_icon, command=cut)
edit_menu.add_command(label="Copy", accelerator="Ctrl-C", compound=LEFT,
                      image=copy_icon, command=copy)
edit_menu.add_command(label="Paste", accelerator="Ctrl-V", compound=LEFT,
                      image=paste_icon, command=paste)
edit_menu.add_separator()
edit_menu.add_command(label="Select all", accelerator="Ctrl-A",
                      command=select_all)

########################### VIEW/HELP MENU ####################################
view_menu = Menu(menubar)
menubar.add_cascade(label="View", menu=view_menu)
has_linenums = BooleanVar(value=True)
view_menu.add_checkbutton(label="Show line numbers", variable=has_linenums,
                          command=show_linenums)
help_menu = Menu(menubar)
menubar.add_cascade(label="Help", menu=view_menu)

###############################################################################
toolbar = Frame(root,  height=55, bg='#c6c6c6')
toolbar.pack(expand=NO, fill=X)

content = Frame(root, bg='blue')
content.pack(expand=YES, fill=BOTH)

statusbar = Frame(root, height=20, bg='#c6c6c6')
statusbar.pack(fill=X)

linenumbar = Frame(content, width=10, borderwidth=1, relief='flat',
                   bg='#F9F9F9')
linenumbar.pack(expand=NO, fill=Y, side=LEFT)

linenumbers = StringVar()
linenum_label = Label(linenumbar, width=2, textvariable=linenumbers,
                      bg='#F9F9F9', justify='right')
linenum_label.pack(fill=Y)
linenum_label.config(font=('Consolas',13))

button1 = Button(toolbar, text="Open file", bg='#c6c6c6', image=open_icon,
                 padx=2,pady=2, command=open_file)
button2 = Button(toolbar, text="Save file", bg='#c6c6c6', image=disk_icon,
                 padx=2,pady=2, command=save_file)
button3 = Button(toolbar, text="Cut", bg='#c6c6c6', image=cut_icon, padx=2,
                 pady=2, command=cut)
button4 = Button(toolbar, text="Copy", bg='#c6c6c6', image=copy_icon, padx=2,
                 pady=2, command=copy)
button5 = Button(toolbar, text="Paste", bg='#c6c6c6', image=paste_icon, padx=2,
                 pady=2, command=paste)
button6 = Button(toolbar, text="Undo", bg='#c6c6c6', image=undo_icon, padx=2,
                 pady=2, command=undo)
button7 = Button(toolbar, text="Redo", bg='#c6c6c6', image=redo_icon, padx=2,
                 pady=2, command=redo)
button8 = Button(toolbar, text="Info", bg='#c6c6c6', image=info_icon,
                  padx=2,pady=2, command=draw_info_dialog)

for i in range(1,9):
  eval("button{}".format(i)).pack(side=LEFT)

############################## TEXT AREA ######################################
textBox = Text(content)
textBox.config(highlightthickness=0,bg='white',pady=4, undo=True)
textBox.pack(expand=YES, fill=BOTH)

scroll=Scrollbar(textBox)
textBox.configure(yscrollcommand=scroll.set)
scroll.config(command=textBox.yview)
scroll.pack(side=RIGHT, fill=Y)

############################ GLOBAL BINDINGS ##################################
root.focus_set()
root.bind_all('<Control-KeyPress-q>', sys.exit)
root.bind_all('<Command-KeyPress-o>', open_file)


###############################################################################
# Hack to keep window focus
subprocess.call(['/usr/bin/osascript', '-e', 'tell app "Finder" to set'
                ' frontmost of process "Python" to true'])
root.mainloop()
