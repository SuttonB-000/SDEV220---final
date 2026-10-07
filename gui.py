import tkinter as tk

root = tk.Tk()

root.title('Coffee Manager')
root.configure(background='yellow')
root.minsize(400,200)
root.geometry('300x300+50+50') #size and shape

header = tk.Label(root, text='Coffee Manager')

header.pack()
image = tk.PhotoImage(file='redbull.png')
tk.Label(root, image=image).pack()
root.mainloop()
