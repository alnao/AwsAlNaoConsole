import tkinter as tk
from tkinter import Toplevel
from tkinter import Menu

#see https://www.pythontutorial.net/tkinter/tkinter-menu/
if __name__ == '__main__':
    print("file not runnable")


def create_menu(root,lista_profili_aws,load_profile_function):
    # create a menubar
    menubar = Menu(root)
    root.config(menu=menubar)

    # create the file_menu
    file_menu = Menu(
        menubar,
        tearoff=0
    )

    # add menu items to the File menu
    file_menu.add_command(label='None')
    #file_menu.add_command(label='Open...')
    #file_menu.add_command(label='Close')
    file_menu.add_separator()

    # add Exit menu item
    file_menu.add_command(
        label='Exit',
        command=root.destroy
    )

    # add the File menu to the menubar
    menubar.add_cascade(
        label="File",
        menu=file_menu
    )


    # profili bar
    profili_menu = Menu(menubar,tearoff=0)
    for profilo in lista_profili_aws:
        profili_menu.add_command(label=profilo, command=lambda:load_profile_function(root,profilo) )
    menubar.add_cascade(
        label="Profili",
        menu=profili_menu
    )

    # create the Help menu
    help_menu = Menu(
        menubar,
        tearoff=0
    )
    #help_menu.add_command(label='Welcome')
    help_menu.add_command(label='About...', command=lambda:open_about(root) )
    # add the Help menu to the menubar
    menubar.add_cascade(
        label="Help",
        menu=help_menu
    )

#see https://www.plus2net.com/python/tkinter-Toplevel.php
def open_about(root):
    my_w_child=Toplevel(root) # Child window 
    #x=root.winfo_screenwidth() // 6
    #y=int(root.winfo_screenheight() * 0.1)
    my_w_child.geometry("300x300")#+ str(x) + "+" + str(y))  # Size of the window 
    my_w_child.title("Aws Py Console - About")

    my_str1 = tk.StringVar()
    l1 = tk.Label(my_w_child,  textvariable=my_str1 )
    l1.grid(row=1,column=2) 
    my_str1.set("Aws Py Console - see www.alnao.it")