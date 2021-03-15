# Note: This software has only developed and tested on GNU/Linux (linux mint 19.3) and Microsoft Windows 10!
# This programm won't fully work on Mac OS.
import csv
import os
import sys
import tkinter
#import hashlib
from glob import glob
from tkinter import messagebox

from PIL import Image, ImageTk
from pyautogui import prompt

VERSION = "Alpha 1.2"
NAME = "DriveNavigator"
TITLE = f"{NAME} - {VERSION}"
TITLE_ERROR = "Oops! An error. :("
CREATOR = "Creator: Erik Petersen"
SIZE = "1200x800"
RESIZABLE = False
IMAGES = []
#STARTUP = """Created by Erik Petersen
#Github: https://github.com/Code-web0"""
linux_fm = "nemo"
linux_iv = "xviewer"
win_fm = "explorer"
win_iv = "explorer" # Apparently calling explorer [file] opens the file with the default application
image_loc = ""
db = None
exc_loc = None

def find_images():
    id = "K0juDIH1pKsWasuYIC7BYib5lsiKIUXb4ogKWWC0kiDhzM7pS6RHvLOKMveu0chrzmIy3S33Pz3D8N63G4rRfg6RlJzfk6g2N2KzPR2yDo0zcEHe0CljbbXu06Hy7r8iF9AKMHvZvgaVwyjL5Uz6tp59DXit9CL2DcbGzcuFJy8HAOo7rBUPuU3wsZXZtc4YhmEiHV4buqFaNYcvirjySMSc5rQ1S59BEsbRSGl8qeugttvEQ8cisv5hfWL3eUE1Z8GCcJhPDdnWk8uAtXXzafz8I4yOplyx1oKEs1dReeeZpLG5y0gO7ktl5RmEUNmlwaTOdYeO0W5sYO5gjgQDrqnkG8KYCuAb0diNB07sLb98yQpJbpGz1yYE4agnQRvI7URyfSglsE3gPwu6JVO0DRhhNPfwicdc60VCsLKMFm5FLCENbzz7JhR24fyJaHwIaEy60Bys3TvNwHAZ4Z2oBSli052QyobIxB78nJIASwDr8bPcXdptjiAfrwGduVw1"
    loc = ""
    dir_path = os.path.dirname(os.path.realpath(__file__)) 
    
    for root, dirs, files in os.walk(dir_path): 
        for file in files:
            if file == "loc":
                #print(root + '/'  +str(file)) 
                with open(root + os.sep + file) as file:
                    content = file.read()
                    file.close()
                if content == id:
                    loc = root
                    break

    if loc == "":
        dir_path = "/home/erik"
        
        for root, dirs, files in os.walk(dir_path): 
            for file in files:
                if file == "loc":
                    with open(root + os.sep + file) as file:
                        content = file.read()
                        file.close()
                    if content == id:
                        loc = root
                        break
 

    return loc

def getImages():
    images = []
    for i in range(len(db)):
        images.append(db[i].split(",")[0])

    return images

def load_loc():
    for i in range(len(db)):
        org_path = os.path.split(db[i].split(",")[0])[0]
        db[i] = db[i].replace(org_path,image_loc)

def save_db():
    with open('database.csv', mode='w') as db_file:
        db_writer = csv.writer(db_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for entry in db:
            data = entry.split(",")
            if not len(data) <= 1:
                db_writer.writerow(data)

def create_thumbnail(image,maxWidth=200,maxHeight=200):
    img = Image.open(image)

    width, height = img.size

    new_width  = maxWidth
    new_height = new_width * height / width

    if new_height > maxHeight:
        new_height = maxHeight
        new_width  = new_height * width / height

    size = (int(new_width), int(new_height))

    img = img.resize(size, Image.ANTIALIAS)
    
    return img

def restart_program():
    """Restarts the current program.
    Note: this function does not return. Any cleanup action (like
    saving data) must be done before calling this function."""
    python = sys.executable
    os.execl(python, python, exc_loc)

def show_warning():
    win = tkinter.Tk()
    win.withdraw()
    messagebox.showwarning("Warning!",f"Version {VERSION} is not stable so it might contain major bugs.")
    win.destroy()

def search():
    try:
        userInput = prompt(text="Enter key words for describing the image(s) you're looking for.\nNote: Loading images might take some time!", title=TITLE, default="anime,jojo,gpio,vesi,meri,codes,meme,windows,flower")
    except:
        sys.exit()
    
    results = []

    for e in db:
        entry = e.split(',')
        index = entry[0]
        eTAGS = entry
        eTAGS.remove(index)
        output = [index]
            

        for tag in list(userInput.split(",")):
            if tag in eTAGS:
                output.append(tag)

        check = list(output)
        check.remove(output[0])

        if check != []:
            results.append(output)
    
    if results == []:
        root = tkinter.Tk()
        root.withdraw()
        messagebox.showerror(TITLE_ERROR,f"No results for {userInput}! Please try again!")
        root.destroy()
        search()

    return results

def main(images):
    startup = True
    main = tkinter.Tk()
    main.geometry(SIZE)
    main.title(TITLE)
    main.resizable(width=RESIZABLE, height=RESIZABLE)
    try:
        main.iconphoto("Icon", tkinter.PhotoImage(file='ES-icon.png'))
    except:
        pass

    index = 0
    page_index = index
    index_max = len(images) - 1
    page_index_max = int(index_max/6)
    img_panel = [None]*int(index_max+1)
    img_cache = [None]*int(index_max+1)
    text_table = ["View","Edit","Open in\nfolder","PLACE\nHOLDER","Previous\n<==","Next\n==>","Search"]

    page = None

    # anime,jojo,gpio,vesi,meri,codes,meme,windows,flower

    def draw_image():
        try:
            blanker = [None,None]
            IMAGE = os.path.split(os.path.abspath(exc_loc))[0] + os.sep + "blank.png"
            img = Image.open(IMAGE)
            img = ImageTk.PhotoImage(img)
            blanker[0] = tkinter.Label(main, image=img)
            blanker[0].image = img
            blanker[0].place(x=0, y=0, width=1200, height=300)

            blanker[1] = tkinter.Label(main, image=img)
            blanker[1].image = img
            blanker[1].place(x=0, y=392, width=1200, height=300)
        except Exception as EXC:
            print(EXC)
            messagebox.showerror(TITLE_ERROR,EXC)

        index_pos = index*6
        yp = 0
        for n in range(2):
            for i in range(3):
                xp = 398*i

                if i > 0:
                    xp += 2
                
                if index_pos > index_max:
                    break

                #if img_panel[index_pos] != None:
                #    img_panel[index_pos].destroy()

                try:
                    if img_cache[index_pos] != None:
                        img = img_cache[index_pos]
                    else:
                        IMAGE = images[index_pos][0]
                        img = create_thumbnail(IMAGE,maxWidth=398,maxHeight=299)
                        img_cache[index_pos] = img

                    img = ImageTk.PhotoImage(img)
                    img_panel[index_pos] = tkinter.Label(main, image=img)
                    img_panel[index_pos].image = img
                    img_panel[index_pos].place(x=0+xp, y=0+yp)
                except Exception as EXC:
                    print(EXC)
                    messagebox.showerror(TITLE_ERROR,EXC)

                index_pos += 1
                
            yp = 392
            xp = 0
        
        try:
            img.destroy()
        except:
            pass

    def draw_text():
        nonlocal page
        page = tkinter.Label(main, text=f"Page {page_index+1}/{int(index_max/6)+1}", font=("Ubuntu Mono", 12))
        page.place(x=0, y=760+20)

    def view(num): # NotFullyImplemented/not finished
        if os.name == "nt":
            #img = Image.open(images[index*6+num][0])
            #img.show()
            os.system(f"{win_iv} {images[index*6+num][0]}")
        elif os.name == "posix":
            os.system(f"{linux_iv} {images[index*6+num][0]}")
        else:
            messagebox.showerror(TITLE_ERROR,f"Feature is not available on {sys.platform}.")
            
    def edit(num): # NotFullyImplemented/not finished
        db_index = 0
        tags = []
        target = images[index*6+num][0]
        for entry in db:
            if entry.split(",")[0] == target:
                #print(entry)
                tags = entry.split(",")

                break
            db_index += 1
        tags.remove(tags[0])
        text = ""
        for i in range(len(tags)):
            if i < len(tags)-1:
                text += tags[i] + ","
            else:
                text += tags[i]
        new_tags = prompt(default=text)
        new_entry = target + "," + new_tags
        #if new_tags != text:
            #db_edited = True
        db[db_index] = new_entry

        #print(db[db_index])
        #print(new_entry)

    def open_in_folder(num): # NotFullyImplemented/not finished
        #print("Warning: NotFullyImplemented")
        file = images[index*6+num][0]
        #print(page_index*6+num)
        if os.name == "posix":
            os.system(f"{linux_fm} {file}")
        elif os.name == "nt":
            os.system(f"{win_fm} {file}")
        else:
            messagebox.showerror(TITLE_ERROR,f"Feature is not available on {sys.platform}.")

    def update_button_state():
        #print(f"{page_index} {page_index_max}")
        if page_index >= page_index_max:
            next_button["state"] = tkinter.DISABLED
        elif page_index < page_index_max:
            next_button["state"] = tkinter.NORMAL

        
        if page_index <= 0:
            previous_button["state"] = tkinter.DISABLED
        elif page_index > 0:
            previous_button["state"] = tkinter.NORMAL

    def next():
        nonlocal page_index, index
        if page_index < page_index_max:
            page_index += 1
            index += 1
            draw_text()
            draw_image()
            update_button_state()

    def previous():
        nonlocal page_index, index
        if page_index_max > 0:
            page_index -= 1
            index -= 1
            draw_text()
            draw_image()
            update_button_state()

    previous_button = tkinter.Button(main, text = text_table[4], command = previous)
    next_button = tkinter.Button(main, text = text_table[5], command = next)

    def new_search():
        restart_program()

    def create_buttons():
        images_visable = int((index_max+1)/(index+1))
        button0 = tkinter.Button(main, text = text_table[0], command = lambda: view(0))
        button1 = tkinter.Button(main, text = text_table[1], command = lambda: edit(0))#,state=tkinter.DISABLED)
        button2 = tkinter.Button(main, text = text_table[2], command = lambda: open_in_folder(0))#,state=tkinter.DISABLED)
        #button3 = tkinter.Button(main, text = text_table[3], command = lambda: None,state=tkinter.DISABLED)

        button4 = tkinter.Button(main, text = text_table[0], command = lambda: view(1))
        button5 = tkinter.Button(main, text = text_table[1], command = lambda: edit(1))#,state=tkinter.DISABLED)
        button6 = tkinter.Button(main, text = text_table[2], command = lambda: open_in_folder(1))#,state=tkinter.DISABLED)
        #button7 = tkinter.Button(main, text = text_table[3], command = lambda: None,state=tkinter.DISABLED)

        button8 = tkinter.Button(main, text = text_table[0], command = lambda: view(2))
        button9 = tkinter.Button(main, text = text_table[1], command = lambda: edit(2))#,state=tkinter.DISABLED)
        button10 = tkinter.Button(main, text = text_table[2], command = lambda: open_in_folder(2))#,state=tkinter.DISABLED)
        #button11 = tkinter.Button(main, text = text_table[3], command = lambda: None,state=tkinter.DISABLED)


        button12 = tkinter.Button(main, text = text_table[0], command = lambda: view(3))
        button13 = tkinter.Button(main, text = text_table[1], command = lambda: edit(3))#,state=tkinter.DISABLED)
        button14 = tkinter.Button(main, text = text_table[2], command = lambda: open_in_folder(3))#,state=tkinter.DISABLED)
        #button15 = tkinter.Button(main, text = text_table[3], command = lambda: None,state=tkinter.DISABLED)

        button16 = tkinter.Button(main, text = text_table[0], command = lambda: view(4))
        button17 = tkinter.Button(main, text = text_table[1], command = lambda: edit(4))#,state=tkinter.DISABLED)
        button18 = tkinter.Button(main, text = text_table[2], command = lambda: open_in_folder(4))#,state=tkinter.DISABLED)
        #button19 = tkinter.Button(main, text = text_table[3], command = lambda: None,state=tkinter.DISABLED)

        button20 = tkinter.Button(main, text = text_table[0], command = lambda: view(5))
        button21 = tkinter.Button(main, text = text_table[1], command = lambda: edit(5))#,state=tkinter.DISABLED)
        button22 = tkinter.Button(main, text = text_table[2], command = lambda: open_in_folder(5))#,state=tkinter.DISABLED)
        #button23 = tkinter.Button(main, text = text_table[3], command = lambda: None,state=tkinter.DISABLED)

        next_button.place(x=600, y=745, height=55, width=100)
        previous_button.place(x=490, y=745, height=55, width=100)

        search = tkinter.Button(main, text = text_table[6], command = new_search)
        search.place(x=1100, y=745, height=55, width=100)
        #button27 = tkinter.Button(main, text = "Button0", command = lambda: action())

        dist = 101
        height = 35
        width = 80
        y1 = 300
        y2 = 692

        if images_visable-index*6 > 0:
            button0.place(x=0, y=y1, height=height, width=width)
            button1.place(x=dist, y=y1, height=height, width=width)
            button2.place(x=dist*2, y=y1, height=height, width=width)
            #button3.place(x=dist*3, y=y1, height=height, width=width)

        if images_visable-index*6 > 1:
            button4.place(x=dist*4, y=y1, height=height, width=width)
            button5.place(x=dist*5, y=y1, height=height, width=width)
            button6.place(x=dist*6, y=y1, height=height, width=width)
            #button7.place(x=dist*7, y=y1, height=height, width=width)

        if images_visable-index*6 > 2:
            button8.place(x=dist*8, y=y1, height=height, width=width)
            button9.place(x=dist*9, y=y1, height=height, width=width)
            button10.place(x=dist*10, y=y1, height=height, width=width)
            #button11.place(x=dist*11, y=y1, height=height, width=width)

        if images_visable-index*6 > 3:
            button12.place(x=0, y=y2, height=height, width=width)
            button13.place(x=dist, y=y2, height=height, width=width)
            button14.place(x=dist*2, y=y2, height=height, width=width)
            #button15.place(x=dist*3, y=y2, height=height, width=width)

        if images_visable-index*6 > 4:
            button16.place(x=dist*4, y=y2, height=height, width=width)
            button17.place(x=dist*5, y=y2, height=height, width=width)
            button18.place(x=dist*6, y=y2, height=height, width=width)
            #button19.place(x=dist*7, y=y2, height=height, width=width)

        if images_visable-index*6 > 5:
            button20.place(x=dist*8, y=y2, height=height, width=width)
            button21.place(x=dist*9, y=y2, height=height, width=width)
            button22.place(x=dist*10, y=y2, height=height, width=width)
            #button23.place(x=dist*11, y=y2, height=height, width=width)
    
        
        #button26.place(x=dist*, y=y1, height=height, width=width)
        #button27.place(x=dist*, y=y1, height=height, width=width)


    if startup:
        for _index in range(index_max+1):
            img_cache[_index] = create_thumbnail(images[_index][0],maxWidth=398,maxHeight=299)
        draw_text()
        draw_image()
        create_buttons()
        update_button_state()
        startup = False

    main.mainloop()

if __name__ == "__main__":
    exc_loc = os.path.abspath(__file__)
    image_loc = find_images()
    os.chdir(image_loc)

    with open("database.csv","r") as file:
        content = file.read()
        file.close()
    
    db = content.split("\n")
    IMAGES = getImages() # Replace with loading from database! - Done!

    main(search())
    save_db()
