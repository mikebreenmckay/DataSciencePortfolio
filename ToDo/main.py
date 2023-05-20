import tkinter as tk
from tkcalendar import DateEntry, Calendar
import sqlite3
from datetime import date

# Connect to / create database
conn = sqlite3.connect('data/todo.db')
cursor = conn.cursor()
command1 = """CREATE TABLE IF NOT EXISTS todos(due_date DATE, todo VARCHAR(100) PRIMARY KEY, notes VARCHAR(100))"""
cursor.execute(command1)

# constants
bg_color = '#3d6466'
btn_bg = '#28393a'
btn_bg_clk = '#badee2'

# Main app class
class TODOapp(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        # Place the window
        x = int(self.winfo_screenwidth() * 0.1)
        y = int(self.winfo_screenheight() * 0.07)
        self.geometry('1000x600+' + str(x) + '+' + str(y))

        # Build menu frame
        menuFrame = tk.Frame(self, bg=bg_color)
        # menu widgets
        title_widget = tk.Label(
            menuFrame,
            text="ToDo",
            bg=bg_color,
            fg='white',
            font=("Impact", 24)
        )

        button_frame = tk.Frame(menuFrame, bg=bg_color)

        viewBt = tk.Button(
            button_frame,
            text="ToDos",
            font=('TkMenuFont', 14),
            bg='#28393a',
            fg='white',
            cursor="hand2",
            activebackground='#badee2',
            activeforeground='black',
            command=lambda: self.show_frame(ViewPage)
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
            command=lambda: self.show_frame(NewPage)
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
            command=lambda: self.show_frame(ModPage)
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
            command=lambda: self.show_frame(SearchPage)
        )
        viewBt.pack(side='left', fill='both', expand=True)
        newBt.pack(side='left', fill='both', expand=True)
        modBt.pack(side='left', fill='both', expand=True)
        searchBt.pack(side='left', fill='both', expand=True)
        title_widget.pack(expand=True, fill='x', padx=10)
        button_frame.pack(expand=True, fill='x', padx=10)


        menuFrame.pack()

        # Build main frame
        mainFrame = tk.Frame(self, bg=bg_color)

        self.frames = {}

        for F in (ViewPage, NewPage, ModPage, SearchPage):
            currFrame = F(mainFrame, self)
            self.frames[F] = currFrame
            currFrame.grid(row=0, column=0, sticky='nsew')

        self.show_frame(ViewPage)
        mainFrame.pack()

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class ViewPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self['bg']=bg_color
        view_cursor = conn.execute("SELECT * FROM todos")
        i = 0
        for todo in view_cursor:
            # print(todo)
            todo_date = tk.Label(self, width=10, fg='blue', text=todo[0],
                                 relief='ridge', anchor='w')
            todo_todo = tk.Label(self, width=40, fg='blue', text=todo[1],
                                 relief='ridge', anchor='w')
            todo_note = tk.Label(self, width=80, fg='blue', text=todo[2],
                                 relief='ridge', anchor='w')
            todo_date.grid(row=i, column=0)
            todo_todo.grid(row=i, column=1)
            todo_note.grid(row=i, column=2)
            i += 1
        # self.pack(expand=True, fill='both')

class NewPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #### new_frame
        #new_frame = tk.Frame(root, bg=bg_color)
        #new_frame.pack_propagate(False)
        self['bg']=bg_color
        entry_label = tk.Label(
            self,
            text="Enter a ToDo:",
            bg=bg_color,
            fg='white',
            font=("Impact", 20)
        )
        self.add_box = tk.Entry(self, bg='white', justify='center', width=75)
        date_label = tk.Label(
            self,
            text="Enter Due Date:",
            bg=bg_color,
            fg='white',
            font=("Impact", 20)
        )
        self.date_picker = DateEntry(self, selectmode='day')
        notes_label = tk.Label(
            self,
            text="Notes:",
            bg=bg_color,
            fg='white',
            font=("Impact", 20)
        )
        self.notes_box = tk.Entry(self, bg='white', justify='center', width=75, )
        addBt = tk.Button(
            self,
            text="Add ToDo",
            font=('TkMenuFont', 14),
            bg='#28393a',
            fg='white',
            cursor="hand2",
            activebackground='#badee2',
            activeforeground='black',
            command=lambda: self.savetodb()
        )
        entry_label.pack(pady=20)
        self.add_box.pack()
        date_label.pack(pady=20)
        self.date_picker.pack()
        notes_label.pack(pady=20)
        self.notes_box.pack()
        addBt.pack(pady=20)
        # self.pack(expand=True, fill='both')

        # functions

    def savetodb(self):
        comm = "INSERT INTO todos VALUES (?,?,?)"
        values = self.date_picker.get_date(), self.add_box.get(), self.notes_box.get()
        cursor.execute(comm, values)
        conn.commit()
        self.add_box.delete('0', 'end')
        self.notes_box.delete('0', 'end')
        self.date_picker.set_date(date.today())

class ModPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self['bg']=bg_color
        self.pack_propagate(False)
        view_cursor = conn.execute("SELECT * FROM todos")
        i = 0
        self.var = dict()
        for todo in view_cursor:
            self.var[todo[1]] = tk.IntVar()
            c = tk.Checkbutton(self, variable=self.var[todo[1]], command=lambda key=todo[1]: self.Readstatus(key))
            todo_date = tk.Label(self, width=10, fg='blue', text=todo[0],
                                 relief='ridge', anchor='n')
            todo_todo = tk.Label(self, width=40, fg='blue', text=todo[1],
                                 relief='ridge', anchor='n')
            c.grid(row=i, column=0)
            todo_date.grid(row=i, column=1)
            todo_todo.grid(row=i, column=2)
            i += 1

        delBt = tk.Button(
            self,
            text="Delete ToDos",
            font=('TkMenuFont', 14),
            bg='#28393a',
            fg='white',
            cursor="hand2",
            activebackground='#badee2',
            activeforeground='black',
            command=lambda: self.delete_from_db()
        )
        delBt.grid(row=i+1,column=0)

    def Readstatus(self, key):
        var_obj = self.var.get(key)
        return (var_obj.get())

    def delete_from_db(self):
        try:
            view_cursor = conn.execute("SELECT * FROM todos")
            comm = "DELETE FROM todos WHERE todo=?"
            for todo in view_cursor:
                to_delete = todo[1]
                print(type(todo[1]))
                if self.Readstatus(to_delete) == 1:
                    cursor.execute(comm, (to_delete,))
                    conn.commit()
                    print('Deleted ' + to_delete)

            pass
        except sqlite3.Error as error:
            print('Failed to delete record from sqlite table', error)


class SearchPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
















# def load_view_frame():
#     view_frame.tkraise()


    #todo_frame.pack(expand=True, fill='both')

# Load the frame that allows you to add new tasks
# def load_new_frame():
#     # function that saves the form and clears
#
#
#
#
# def load_mod_frame():
#     clear_widgets()
# def load_search_frame():
#     clear_widgets()








#### view_frame
#view_frame = tk.Frame(root, bg=bg_color)
#view_frame.pack_propagate(False)




#### mod_frame
# mod_frame = tk.Frame(root, bg=bg_color)

#### search_frame
# search_frame = tk.Frame(root, bg=bg_color)


if __name__ == '__main__':

    # initialize app
    root = TODOapp()
    root.title("ToDo List")

    # menu
    menu = tk.Menu(root)

    # sub menu
    file_menu = tk.Menu(menu)
    menu.add_cascade(label='File', menu=file_menu)

    root.configure(menu=menu)

    # run app
    root.mainloop()

