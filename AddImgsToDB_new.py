import csv
import os
import tkinter
from glob import glob
from tkinter import filedialog, messagebox

from PIL import Image, ImageTk

SIZE = "1200x800"
RESIZABLE = False
VERSION = "N/A"
NAME = "DriveNavigator"
TITLE = NAME
CREATOR = "Creator: Erik Petersen"
FILE_EXTENSIONS = ['.jpeg', '.jpg', '.png', '.gif', '.bmp', '.JPEG', '.JPG', '.PNG', '.GIF', '.BMP']#, '.tiff', '.tif']
IMAGES = []
LOC_SELF = os.path.split(os.path.abspath(__file__))[0]
SAMPLE_IMAGES = LOC_SELF + os.sep + "Test" + os.sep + "images"
LOC = [SAMPLE_IMAGES, "/home/erik/Documents/.tor-download", "/home/erik/Pictures"]
LOC_INDEX = 2

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

def getImages():
    root = tkinter.Tk()
    root.withdraw()
    loc = "/home/erik/Documents/Code/ImgEplorer/images"#LOC[LOC_INDEX]#filedialog.askdirectory()
    
    #print(loc)
    
    #if loc == "":
    #    loc += filedialog.askdirectory()
    
    #loc = filedialog.askdirectory()

    files = []
    for f in FILE_EXTENSIONS:
        found_files = glob(loc + os.sep + '*' + f)
        files.append(found_files)
    
    try:
        files.remove([])
    except:
        pass

    output = []

    for i in files:
        for n in i:
            output.append(os.path.split(n)[1])

    os.chdir(loc)

    root.destroy()

    return sorted(output)

def load_db():
    with open("database.csv","r") as file:
        content = file.read()
        file.close()
    output = content.split("\n")
    if [] in output:
        output.remove([])    
    return output

def main():
    startup = True
    main = tkinter.Tk()
    main.geometry(SIZE)
    main.title(TITLE)
    main.resizable(width=RESIZABLE, height=RESIZABLE)
    try:
        main.iconphoto("Icon", tkinter.PhotoImage(file='ES-icon.png'))
    except:
        pass

    db = [""] * len(IMAGES)
    index = 0
    img_panel = None
    index_max = len(IMAGES) - 1
    img_cache = [None] * len(IMAGES)

    page = None
    img_path = None

    #status = tkinter.Label(main, text="", font=("Ubuntu Mono", 12))
    
    text_box = tkinter.Text(main, height = 2, width = 85)
    text_box.place(x=250,y=705)

    def getInput():
        try:
            inp = text_box.get(1.0, "end-1c")
        except Exception as EXC:
            inp = None
            print(EXC)
            messagebox.showerror(TITLE,EXC)

        return inp

    def update_textbox():
        text_box.delete("1.0", tkinter.END)
        text_box.insert('1.0', db[index])

    def draw_image():
        nonlocal img_panel
        if img_panel != None:
            img_panel.destroy()
        try:
            if img_cache[index] != None:
                img = img_cache[index]
            else:
                IMAGE = IMAGES[index]
                img = create_thumbnail(IMAGE,maxWidth=1198,maxHeight=700)
                img_cache[index] = img

            img = ImageTk.PhotoImage(img)
            img_panel = tkinter.Label(main, image=img)
            img_panel.image = img
            img_panel.place(x=0, y=0)
        except Exception as EXC: 
            print(EXC)
            messagebox.showerror(TITLE,EXC)

    def draw_text():
        nonlocal page, img_path
        if page != None:
            page.destroy()
        if img_path != None:
            img_path.destroy()

        img_path = tkinter.Label(main, text=IMAGES[index], font=("Ubuntu Mono", 12))
        img_path.place(x=0, y=780)
        page = tkinter.Label(main, text=f"Image {index+1}/{index_max+1}", font=("Ubuntu Mono", 12))
        page.place(x=0, y=760)

    def update_cache():
        db[index] = getInput()
        #print(f"{index} {db} {db[index]}")

    def save_changes():
        update_cache()
        with open('database.csv', mode='w') as db_file:
            db_writer = csv.writer(db_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            index_local = 0
            for img in db:
                data = [os.path.split(IMAGES[index_local])[1]]
                for i in img.split(","):
                    data.append(i)
                print(data)
                db_writer.writerow(data)
                index_local += 1

    def update_button_state():
        if index >= index_max:
            next_button["state"] = tkinter.DISABLED
        elif index < index_max:
            next_button["state"] = tkinter.NORMAL

        
        if index <= 0:
            previous_button["state"] = tkinter.DISABLED
        elif index > 0:
            previous_button["state"] = tkinter.NORMAL
            
    def next():
        nonlocal index
        if index < index_max:
            update_cache()
            index += 1
            update_button_state()
            update_textbox()
            draw_image()
            draw_text()

    def previous():
        nonlocal index
        if index > 0:
            update_cache()
            index -= 1
            update_button_state()
            update_textbox()
            draw_image()
            draw_text()
    
    save_changes_button = tkinter.Button(main, text = "Save changes", bg = "gray", command = save_changes)
    next_button = tkinter.Button(main, text = "Next\n==>", bg = "gray", command = next)
    previous_button = tkinter.Button(main, text = "Previous\n<==", bg = "gray", command = previous)
    #load_db_button = tkinter.Button(main, text = "Edit Database", bg = "gray", command = None)

    save_changes_button.place(x=1079, y=715, height=85, width=120)
    next_button.place(x=600, y=745, height=55, width=100)
    previous_button.place(x=490, y=745, height=55, width=100)
    #load_db_button.place(x=974, y=745, height=55, width=100)

    #tkinter.Label(main, text="Version: " + VERSION, font=("Ubuntu Mono", 9)).place(x=0, y=0)
    #tkinter.Label(main, text=CREATOR, font=("Ubuntu Mono", 9)).place(x=0, y=0)
    
    if startup:
        with open("database.csv","r") as file:
            content = file.read()
            file.close()

        _db = content.split("\n")
        
        for _index in range(len(IMAGES)):
            image = IMAGES[_index]
            for entry in _db:
                _entry = entry.split(',')
                if _entry[0] == image:
                    for __index in range(len(_entry)):
                        if __index != 0:
                            db[_index] += _entry[__index]
                            if __index < len(_entry)-1:
                                db[_index] += ","       
        
        draw_image()
        draw_text()
        update_button_state()
        update_textbox()
        startup = False

    main.mainloop()

if __name__ == "__main__":
    #os.chdir(LOC_SELF)
    IMAGES = getImages()
    main()
