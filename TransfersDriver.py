from Item import *
from TransfersList import *
from StudioEnums import *
from WomenItem import *
from StockParser import *
import tkinter.filedialog as tkFileDialog
from tkinter import *
from PIL import ImageTk, Image
import os
import platform
import subprocess
from functools import partial


def main(pathOfStock, desired_stock_rishpon, desired_stock_tachana):
    warnings_file = openWarningFile()
    Item.update_desired_values(int(desired_stock_rishpon), int(desired_stock_tachana))
    TransferFromTo.updateToFromDirections()
    parser = StockParser(pathOfStock)
    while (not parser.isEOF()):
        item = parser.getNextItem()
        if item is None:
            break
        item.transfer(warnings_file)
    outputSucceeded = TransferList.exportTransfers()
    parser.closeParser()
    warnings_file.close()
    if not outputSucceeded:
        return False
    return True

def gui():
    """make the GUI version of this command that is run if no options are
    provided on the command line"""

    def button_go_callback():
        """ what to do when the "Go" button is pressed """
        input_file = entry.get()
        num_rishpon = entry_rishpon.get()
        num_tachana = entry_tachana.get()
        if input_file.rsplit(".")[-1] != "csv":
            statusText.set("Filename must end in `.csv'")
            message4.configure(fg="red")
            return
        else:
            outputSucceeded = main(input_file, num_rishpon, num_tachana)
            if not outputSucceeded:
                statusText.set("Error has occurred. Please try again!")
                message4.configure(fg="red")
                return
            statusText.set("Transfers are ready for you!'")
            message4.configure(fg="blue")
            # Opens the output directory at the end of the execution.
            desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
            path = os.path.join(desktop, "Transfers")
            if platform.system() == "Windows":
                subprocess.Popen("explorer " + path)
            elif platform.system() == "Darwin":
                subprocess.Popen(["open", path])
            else:
                subprocess.Popen(["xdg-open", path])
            return

    def button_browse_callback():
        """ What to do when the Browse button is pressed """
        filename = tkFileDialog.askopenfilename()
        entry.delete(0, END)
        entry.insert(0, filename)

    root = Tk()
    root.title("Studio-Noa Transfers")
    root.configure(background="white")
    root.minsize(400,500)
    frame = Frame(root)
    frame.pack()
    statusText = StringVar(root)

    if getattr(sys, 'frozen', False):   # Opens the script's address.
    # frozen
        script_dir = os.path.dirname(sys.executable)
    else:
    # unfrozen
        path = __file__ if platform.system() == 'Windows' else '__file__'
        script_dir = os.path.dirname(os.path.realpath(path))
    image_path = os.path.join(script_dir, "logo.jpg")
    img = ImageTk.PhotoImage(Image.open(image_path))
    logo = Label(root, image = img)
    logo.config(bg='white')
    logo.pack()

    label = Label(root, text=":של המלאי CSV טען את קובץ ה")
    label.config(bg='white')
    entry = Entry(root, width=40)
    button_browse = Button(root, text="ייבא קובץ", command=button_browse_callback)
    label.pack()
    entry.pack()
    button_browse.pack()

    desired_rishpon = Label(root, text=":כמות המלאי הרצויה ברשפון")
    desired_rishpon.config(bg='white')
    desired_rishpon.pack()
    entry_rishpon = Entry(root, width=5)
    entry_rishpon.pack()

    desired_tachana = Label(root, text=":כמות המלאי הרצויה בתחנה")
    desired_tachana.config(bg='white')
    desired_tachana.pack()
    entry_tachana = Entry(root, width=5)
    entry_tachana.pack()

    separator = Frame(root, height=2, bd=1, relief=SUNKEN)
    separator.pack(fill=X, padx=5, pady=5)

    button_go = Button(root, text="התחל", command=button_go_callback)
    button_exit = Button(root, text="צא", command=exitAll)
    button_go.pack()
    button_exit.pack()

    separator = Frame(root, height=2, bd=1, relief=SUNKEN)
    separator.pack(fill=X, padx=5, pady=5)

    statusText1 = StringVar(root)
    statusText2 = StringVar(root)
    statusText3 = StringVar(root)
    statusText1.set("1) חפש את קובץ המלאי בעזרת החיפוש.")
    statusText2.set("2) קבע את כמות המלאי הרצויה בכל אחת מהחנויות.")
    statusText3.set("3) לחץ על כפתור ההתחלה וקדימה להעברות :) ")
    message1 = Label(root, textvariable=statusText1)
    message1.config(bg='white')
    message1.pack()
    message2 = Label(root, textvariable=statusText2)
    message2.config(bg='white')
    message2.pack()
    message3 = Label(root, textvariable=statusText3)
    message3.config(bg='white')
    message3.pack()
    message4 = Label(root, textvariable=statusText)
    message4.config(bg='white')
    message4.pack()

    mainloop()

def exitAll():
    os._exit(1)
    exit()
    quit()
    raise SystemExit

def openWarningFile():
    desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
    new_dir = desktop + "/Transfers"
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)
    warnings_file = open(new_dir + '/Warnings.html', 'wb')

    warnings_file.write("<html> <body dir='rtl'>\n".encode("utf8"))
    warnings_file.write("<?php header('Content-Type: text/html; charset=utf-8'); ?>\n".encode("utf8"))
    warnings_file.write("<meta http-equiv='Content-Type' content='text/html; charset=utf-8' />\n".encode("utf8"))
    return warnings_file

if __name__ == "__main__":
    # execute only if run as a script
    gui()
