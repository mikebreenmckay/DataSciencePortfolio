import tkinter as tk
from tkcalendar import DateEntry, Calendar
import sqlite3
from datetime import date, datetime, timedelta

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
"""
ToDo haha.. 
-Add more menu items.
-Fix bg color issues
-Update frames when database is changed
"""
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
            text="Add ToDo",
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

# Frame that allows you to view existing todos
"""
ToDo:
-Add scroll bar window
"""
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

# Frame where you can add new todos
"""
Todo:
-Change button to only say Add
-Possible make notes entry bigger
-Check to make sure a values is entered in Note and that it does not match existing values
"""
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

# Page where you can delete existing todos and modify their values
"""
Todos:
-Might want to add a simple search to this
-Add a select all button for the deletion checkboxes  
"""
class ModPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self['bg']=bg_color
        self.pack_propagate(False)

        self.var = dict()
        self.build_frame()

        self.curr_record = ""

    def send_to_update(self,record):
        command = "SELECT * FROM todos WHERE todo=?"
        update_cursor = conn.execute(command, (record,))
        old_todo=""
        old_note=""
        old_date=date.today()
        for row in update_cursor:
            old_todo = row[1]
            old_date = datetime.strptime(row[0], '%Y-%m-%d').date()
            old_note = row[2]
        global curr_record
        self.curr_record = old_todo
        self.add_box.delete('0',tk.END)
        self.add_box.insert(tk.END,old_todo)
        self.date_picker.set_date(old_date)
        self.notes_box.delete('1.0',tk.END)
        self.notes_box.insert(tk.END,old_note)

    def add_entry(self):
        if len(self.add_box.get()) == 0:
            print('Nothing to add')
        else:
            comm = "INSERT INTO todos VALUES (?,?,?)"
            values = self.date_picker.get_date(), self.add_box.get(), self.notes_box.get("1.0",tk.END)[:-1]
            cursor.execute(comm, values)
            conn.commit()
            self.curr_record = ""
            for widget in self.winfo_children():
                widget.destroy()
            self.build_frame()

    def update_entry(self):
        new_todo = self.add_box.get()
        new_date = self.date_picker.get_date()
        new_notes = self.notes_box.get("1.0",tk.END)[:-1]
        if len(self.curr_record) == 0:
            print("Nothing Selected")
        else:
            command="UPDATE todos SET due_date=?, todo=?, notes=? WHERE todo=?"
            val = (new_date, new_todo, new_notes, self.curr_record)
            cursor.execute(command, val)
            conn.commit()
            self.curr_record = ""
            for widget in self.winfo_children():
                widget.destroy()
            self.build_frame()

    def clear_entry(self):
        self.add_box.delete('0', tk.END)
        self.date_picker.set_date(date.today())
        self.notes_box.delete('1.0', tk.END)
        self.curr_record = ""

    def build_frame(self, scommand="SELECT * FROM todos", svar=()):
        self.leftframe = leftframe = tk.Frame(self, bg=bg_color)
        self.rightframe = rightframe = tk.Frame(self, bg=bg_color)
        self.leftframe_upper = leftframe_upper = tk.Frame(leftframe, bg=bg_color)
        self.leftframe_lower = leftframe_lower = tk.Frame(leftframe, bg=bg_color)
        self.rightframe_upper = rightframe_upper = tk.Frame(rightframe, bg=bg_color)
        self.rightframe_lower = rightframe_lower = tk.Frame(rightframe, bg=bg_color)
        self.canvas = canvas = tk.Canvas(rightframe_upper)
        canvas.pack(side='left', fill='both', expand=True)
        rightframe_upper.pack(side='top', fill='both', expand=True)
        rightframe_lower.pack(side='bottom', fill='y', expand=True)

        scrollbar = tk.Scrollbar(rightframe_upper, orient='vertical', command=canvas.yview)
        scrollbar.pack(side='right', fill='y')

        canvas.configure(yscrollcommand=scrollbar.set)

        inner_frame = tk.Frame(canvas)
        canvas.create_window((0,0), window=inner_frame, anchor='nw')

        view_cursor = conn.execute(scommand, svar)
        i = 0
        header_date = tk.Label(inner_frame, width=10, fg='white', text='Date', anchor='n', bg=bg_color)
        header_todo = tk.Label(inner_frame, width=40, fg='white', text='ToDo', anchor='n', bg=bg_color)
        header_date.grid(row=i, column=1, sticky='w')
        header_todo.grid(row=i, column=2, sticky='w')
        i += 1
        for todo in view_cursor:
            self.var[todo[1]] = tk.IntVar()
            if i % 2 == 0:
                alt_bg = '#61acb0'
            else:
                alt_bg = '#1d5457'
            c = tk.Checkbutton(inner_frame, bg=alt_bg, variable=self.var[todo[1]], command=lambda key=todo[1]: self.Readstatus(key))
            todo_date = tk.Label(inner_frame, width=10, fg='white', text=todo[0],
                                 relief='flat', anchor='n', bg=alt_bg)
            todo_todo = tk.Label(inner_frame, width=40, fg='white', text=todo[1],
                                 relief='flat', anchor='n', bg=alt_bg)
            edit_btn = tk.Button(
                inner_frame,
                text="View/Edit",
                font=('TkMenuFont', 8),
                bg='#28393a',
                fg='white',
                cursor="hand2",
                activebackground='#badee2',
                activeforeground='black',
                command=lambda key=todo[1]: self.send_to_update(key)
            )
            c.grid(row=i, column=0, sticky='w')
            todo_date.grid(row=i, column=1, sticky='w')
            todo_todo.grid(row=i, column=2, sticky='w')
            edit_btn.grid(row=i, column=3, sticky='w')
            i += 1

        i+=1
        self.select_all_var = tk.IntVar()
        select_all_cb = tk.Checkbutton(rightframe_lower, bg=bg_color, text="Select All", variable=self.select_all_var,
                           command=lambda: self.select_all())

        entry_label = tk.Label(
            leftframe_upper,
            text="ToDo:",
            bg=bg_color,
            fg='white',
            font=("Impact", 10)
        )
        self.add_box = tk.Entry(leftframe_upper, bg='white', justify='left', width=60)
        date_label = tk.Label(
            leftframe_upper,
            text="Edit Date:",
            bg=bg_color,
            fg='white',
            font=("Impact", 10)
        )
        self.date_picker = DateEntry(leftframe_upper, selectmode='day')
        notes_label = tk.Label(
            leftframe_upper,
            text="Edit Notes:",
            bg=bg_color,
            fg='white',
            font=("Impact", 10)
        )
        self.notes_box = tk.Text(leftframe_upper, bg='white', height=7, width=45)
        addBt = tk.Button(
            leftframe_upper,
            text="Add",
            font=('TkMenuFont', 10),
            bg='#28393a',
            fg='white',
            cursor="hand2",
            activebackground='#badee2',
            activeforeground='black',
            command=lambda: self.add_entry()
        )
        updateBt = tk.Button(
            leftframe_upper,
            text="Update",
            font=('TkMenuFont', 10),
            bg='#28393a',
            fg='white',
            cursor="hand2",
            activebackground='#badee2',
            activeforeground='black',
            command=lambda: self.update_entry()
        )

        clearBt = tk.Button(
            leftframe_upper,
            text="Clear",
            font=('TkMenuFont', 10),
            bg='#28393a',
            fg='white',
            cursor="hand2",
            activebackground='#badee2',
            activeforeground='black',
            command=lambda: self.clear_entry()
        )
        select_all_cb.pack(anchor='sw')
        entry_label.grid(row=0,column=0,columnspan=1, sticky='e', ipady=10)
        self.add_box.grid(row=0,column=1,columnspan=2, sticky='w')
        date_label.grid(row=1,column=0,columnspan=1, sticky='e', ipady=10)
        self.date_picker.grid(row=1,column=1,columnspan=1, sticky='w')
        notes_label.grid(row=2,column=0,columnspan=1, sticky='ne', ipady=10)
        self.notes_box.grid(row=2,column=1,columnspan=3, sticky='w')
        addBt.grid(row=3,column=2, pady=10, sticky='w')
        updateBt.grid(row=3,column=2, pady=10)
        clearBt.grid(row=3,column=2,pady=10, sticky='e')

        canvas.configure(scrollregion=canvas.bbox("all"))

        search_label = tk.Label(
            leftframe_lower,
            text="Search:",
            bg=bg_color,
            fg='white',
            font=("Impact", 10)
        )
        self.search_box = tk.Entry(leftframe_lower, bg='white', justify='left', width=60)
        date_search_label = tk.Label(
            leftframe_lower,
            text="Between:",
            bg=bg_color,
            fg='white',
            font=("Impact", 10)
        )
        self.lower_date_picker = DateEntry(leftframe_lower, selectmode='day')
        self.higher_date_picker = DateEntry(leftframe_lower, selectmode='day')
        self.higher_date_picker.set_date(date.today()+timedelta(days=100))

        searchBt = tk.Button(
            leftframe_lower,
            text="Search",
            font=('TkMenuFont', 10),
            bg='#28393a',
            fg='white',
            cursor="hand2",
            activebackground='#badee2',
            activeforeground='black',
            command=lambda: self.search()
        )

        clearBt = tk.Button(
            leftframe_lower,
            text="See All",
            font=('TkMenuFont', 10),
            bg='#28393a',
            fg='white',
            cursor="hand2",
            activebackground='#badee2',
            activeforeground='black',
            command=lambda: self.reload_frame()
        )

        search_label.grid(row=0,column=0,columnspan=1, sticky='e', ipady=10)
        self.search_box.grid(row=0,column=1,columnspan=2,sticky='w')
        date_search_label.grid(row=1,column=0,columnspan=1,sticky='e',ipady=10)
        self.lower_date_picker.grid(row=1,column=1,columnspan=1,sticky='w')
        self.higher_date_picker.grid(row=1, column=1, columnspan=1, sticky='e')
        searchBt.grid(row=2, column=2, pady=10)
        clearBt.grid(row=2, column=2, pady=10, sticky='e')


        delBt = tk.Button(
            rightframe_lower,
            text="Delete ToDos",
            font=('TkMenuFont', 10),
            bg='#28393a',
            fg='white',
            cursor="hand2",
            activebackground='#badee2',
            activeforeground='black',
            command=lambda: self.delete_from_db()
        )
        delBt.pack(anchor="se")

        leftframe_upper.pack(expand=True, fill='both')
        leftframe_lower.pack(expand=True, fill='both')
        leftframe.pack(expand=False, fill='both', side='left', padx=10)
        rightframe.pack(expand=True, fill='both', side='left')



    # Function to select all check boxes if select all is chosen
    def select_all(self):
        if self.select_all_var.get() == 1:
            for key in self.var.keys():
                self.var.get(key).set(1)
    def Readstatus(self, key):
        var_obj = self.var.get(key)
        return (var_obj.get())

    def reload_frame(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.build_frame()

    def search(self):
        term = self.search_box.get()
        term = '%' + term + '%'
        date_low = self.lower_date_picker.get_date()
        date_high = self.higher_date_picker.get_date()
        command = "SELECT * FROM todos WHERE (due_date >= ? AND due_date <= ?) AND (todo LIKE ?)"
        variables = (date_low, date_high, term)
        print(variables)
        for widget in self.winfo_children():
            widget.destroy()
        self.build_frame(command, variables)

    def delete_from_db(self):
        try:
            view_cursor = conn.execute("SELECT * FROM todos")
            comm = "DELETE FROM todos WHERE todo=?"
            for todo in view_cursor:
                to_delete = todo[1]
                if self.Readstatus(to_delete) == 1:
                    cursor.execute(comm, (to_delete,))
                    conn.commit()
                    print('Deleted ' + to_delete)
            self.reload_frame()


            pass
        except sqlite3.Error as error:
            print('Failed to delete record from sqlite table', error)






class SearchPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self['bg'] = bg_color
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

    # def refresh():
    #     root.after(1000, refresh)
    # root.title("ToDo List")
    #
    # refresh()

    # menu
    menu = tk.Menu(root)

    # sub menu
    file_menu = tk.Menu(menu)
    menu.add_cascade(label='File', menu=file_menu)

    root.configure(menu=menu)

    # run app
    root.mainloop()

