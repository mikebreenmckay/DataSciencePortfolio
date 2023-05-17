import tkinter as tk
from tkcalendar import DateEntry, Calendar
import sqlite3
from datetime import date

# Connect to / create database
conn = sqlite3.connect('data/todo.db')
cursor = conn.cursor()
command1 = """CREATE TABLE IF NOT EXISTS todos(due_date DATE, todo VARCHAR(100) PRIMARY KEY, notes VARCHAR(100))"""
cursor.execute(command1)

# initialize app
root = tk.Tk()
root.title("ToDo List")

# constants
bg_color = '#3d6466'
btn_bg = '#28393a'
btn_bg_clk = '#badee2'

# functions


def clear_widgets():
	# select all frame widgets and delete them
    for frame in [view_frame, new_frame, mod_frame, search_frame]:
            for widget in frame.winfo_children():
                widget.destroy()

def load_view_frame():
    clear_widgets()
    view_frame.pack_propagate(False)
    #todo_frame = tk.Frame(view_frame, bg="white")
    view_cursor = conn.execute("SELECT * FROM todos")
    i = 0
    for todo in view_cursor:
        print(todo)
        todo_date = tk.Label(view_frame, width=10, fg='blue', text=todo[0],
                             relief='ridge', anchor='w')
        todo_todo = tk.Label(view_frame, width=40, fg='blue', text=todo[1],
                             relief='ridge', anchor='nw')
        todo_date.grid(row=i, column=0)
        todo_todo.grid(row=i, column=1)
        i+=1
    view_frame.pack(expand=True, fill='both')

    #todo_frame.pack(expand=True, fill='both')

# Load the frame that allows you to add new tasks
def load_new_frame():
    # function that saves the form and clears
    def savetodb():
        command2 = 'INSERT INTO todos VALUES (?,?,?)'
        values = date_picker.get_date(), add_box.get(), notes_box.get()
        cursor.execute(command2, values)
        conn.commit()
        add_box.delete('0','end')
        notes_box.delete('0','end')
        date_picker.set_date(date.today())
    clear_widgets()
    new_frame.pack_propagate(False)
    entry_label = tk.Label(
        new_frame,
        text="Enter a ToDo:",
        bg=bg_color,
        fg='white',
        font=("Impact", 20)
    )
    add_box = tk.Entry(new_frame, bg='white', justify='center', width=75)
    date_label = tk.Label(
        new_frame,
        text="Enter Due Date:",
        bg=bg_color,
        fg='white',
        font=("Impact", 20)
    )
    date_picker = DateEntry(new_frame,selectmode='day')
    notes_label = tk.Label(
        new_frame,
        text="Notes:",
        bg=bg_color,
        fg='white',
        font=("Impact", 20)
    )
    notes_box = tk.Entry(new_frame, bg='white', justify='center', width=75, )
    addBt = tk.Button(
        new_frame,
        text="Add ToDo",
        font=('TkMenuFont', 14),
        bg='#28393a',
        fg='white',
        cursor="hand2",
        activebackground='#badee2',
        activeforeground='black',
        command=savetodb
    )
    entry_label.pack(pady=20)
    add_box.pack()
    date_label.pack(pady=20)
    date_picker.pack()
    notes_label.pack(pady=20)
    notes_box.pack()
    addBt.pack(pady=20)
    new_frame.pack(expand=True, fill='both')


def load_mod_frame():
    clear_widgets()
def load_search_frame():
    clear_widgets()

# Place the window
x = int(root.winfo_screenwidth() * 0.3)
y = int(root.winfo_screenheight() * 0.07)
root.geometry('500x600+' + str(x) + '+' + str(y))

view_frame = tk.Frame(root, bg=bg_color)
new_frame = tk.Frame(root, bg=bg_color)
mod_frame = tk.Frame(root, bg=bg_color)
search_frame = tk.Frame(root, bg=bg_color)


# common widgets
title_widget = tk.Label(
    root,
    text="ToDo",
    bg=bg_color,
    fg='white',
    font=("Impact", 24)
)

button_frame = tk.Frame(root, bg=bg_color)

viewBt = tk.Button(
    button_frame,
    text="ToDos",
    font=('TkMenuFont', 14),
    bg='#28393a',
    fg='white',
    cursor="hand2",
    activebackground='#badee2',
    activeforeground='black',
    command=lambda:load_view_frame()
)

newBt = tk.Button(
    button_frame,
    text="Add/Delete",
    font=('TkMenuFont', 14),
    bg='#28393a',
    fg='white',
    cursor="hand2",
    activebackground='#badee2',
    activeforeground='black',
    command=lambda:load_new_frame()
)

modBt = tk.Button(
    button_frame,
    text="Modify",
    font=('TkMenuFont', 14),
    bg='#28393a',
    fg='white',
    cursor="hand2",
    activebackground='#badee2',
    activeforeground='black',
    command=lambda:load_mod_frame()
)

searchBt = tk.Button(
            button_frame,
            text="Search",
            font=('TkMenuFont', 14),
            bg='#28393a',
            fg='white',
            cursor="hand2",
            activebackground='#badee2',
            activeforeground='black',
            command=lambda:load_search_frame()
        )



# pack layout
title_widget.pack(side='top', fill='both')
viewBt.pack(side='left', fill='both', expand=True)
newBt.pack(side='left', fill='both', expand=True)
modBt.pack(side='left', fill='both', expand=True)
searchBt.pack(side='left', fill='both', expand=True)
button_frame.pack(fill='x', ipadx=25)




# menu
menu = tk.Menu(root)

# sub menu
file_menu = tk.Menu(menu)
menu.add_cascade(label='File', menu=file_menu)

root.configure(menu=menu)

# load first frame
load_view_frame()




# run app
root.mainloop()

