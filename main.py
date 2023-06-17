import tkinter as tk
from tkinter import filedialog as fd
from PIL import ImageTk, Image
import os
from tensorflow_model import main as model_tf
from model import main2 as model_nasz
from tkinter import messagebox as mb

IMAGE_WIDTH, IMAGE_HEIGHT = 400, 300
REF_MODEL_GIF, OUR_MODEL_GIF = 'gif_tf.gif', 'gif.gif'
REF_MODEL_FRAMES, OUR_MODEL_FRAMES = 100, 41


class App:
    def __init__(self, root):
        self.root = root
        self.root.title('Style transfer')
        self.root.geometry('1024x720')

        self.content = None
        self.style = None

        self.frame = tk.Frame(self.root)
        self.frame.pack()

        self.b1 = tk.Button(root, text="Wybierz styl", command=self.select_style)
        self.b2 = tk.Button(root, text='Wybierz obraz', command=self.select_content)
        self.b3 = tk.Button(root, text='Nasz model', command=lambda: self.model('nasz'))
        self.b4 = tk.Button(root, text='Model referencyjny', command=lambda: self.model('ref'))

        self.imagebox = tk.Label(root)
        self.imagebox.pack()

        self.b1.pack()
        self.b2.pack()
        self.b3.pack()
        self.b4.pack()

    def select_style(self):
        self.style = self.select_file()
        self.display_image(self.style, x=0, y=0)

    def select_content(self):
        self.content = self.select_file()
        self.display_image(self.content, x=600, y=0)

    def select_file(self):
        filename = fd.askopenfilename(title='Wybierz plik', initialdir='/')
        return os.path.abspath(filename)

    def display_image(self, filepath, x, y):
        image = Image.open(filepath)
        image = image.resize((IMAGE_WIDTH, IMAGE_HEIGHT))
        test = ImageTk.PhotoImage(image)
        label = tk.Label(image=test)
        label.image = test
        label.pack()
        label.place(x=x, y=y)

    def model(self, type):
        path = REF_MODEL_GIF if type == 'ref' else OUR_MODEL_GIF
        frames = REF_MODEL_FRAMES if type == 'ref' else OUR_MODEL_FRAMES
        model = model_tf if type == 'ref' else model_nasz
        if os.path.exists(path) is False:
            if self.content is not None and self.style is not None:
                model(self.style, self.content)
                self.show_gif(path, frames)
            else:
                mb.showinfo(title='Błąd', message='Nie wybrano plików!')
        else:
            self.show_gif(path, frames)

    def show_gif(self, path, cnt):
        def update(ind):
            frame = frames[ind]
            ind += 1
            print(ind)
            if ind > cnt - 1:
                ind = 0
            label_gif.configure(image=frame)
            self.root.after(100, update, ind)

        frames = [tk.PhotoImage(file=path, format='gif -index %i' % i) for i in range(cnt)]
        label_gif = tk.Label(self.root)
        label_gif.pack_forget()
        label_gif.pack()
        label_gif.place(x=530, y=310)
        self.root.after(0, update, 0)


root = tk.Tk()
app = App(root)
root.mainloop()
