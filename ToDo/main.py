import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
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
class TodoApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # Place the window
        x = int(self.winfo_screenwidth() * 0.1)
        y = int(self.winfo_screenheight() * 0.07)
        self.geometry('1000x600+' + str(x) + '+' + str(y))

        # Build title frame
        title_frame = tk.Frame(self, bg=bg_color)
        # title widget
        title_widget = tk.Label(
            title_frame,
            text="ToDo",
            bg=bg_color,
            fg='white',
            font=("Impact", 24)
        )
        # Pack title
        title_widget.pack(expand=True, fill='x', padx=10)
        title_frame.pack(fill='x')

        # Build main frame
        main_frame = tk.Frame(self, bg=bg_color)
        # Insert ModPage where all the main widgets live.
        curr_frame = ModPage(main_frame)

        curr_frame.pack(expand=True, fill='both')
        main_frame.pack(expand=True, fill='both')


# The main frame that displays, updates, and searches
class ModPage(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.higher_date_picker = None
        self.lower_date_picker = None
        self.search_box = None
        self.notes_box = None
        self.date_picker = None
        self.select_all_var = None
        self.canvas = None
        self.rightFrame_lower = None
        self.rightFrame_upper = None
        self.leftFrame_lower = None
        self.leftFrame_upper = None
        self.rightFrame = None
        self.leftFrame = None
        self.add_box = None
        self['bg'] = bg_color
        self.pack_propagate(False)
        self.var = dict()
        self.build_frame()
        self.curr_record = ""

    # Updates record in view/edit frame in database
    def send_to_update(self, record):
        command = "SELECT * FROM todos WHERE todo=?"
        update_cursor = conn.execute(command, (record,))
        old_todo = ""
        old_note = ""
        old_date = date.today()
        for row in update_cursor:
            old_todo = row[1]
            old_date = datetime.strptime(row[0], '%Y-%m-%d').date()
            old_note = row[2]
        self.curr_record = old_todo
        self.add_box.delete('0', tk.END)
        self.add_box.insert(tk.END, old_todo)
        self.date_picker.set_date(old_date)
        self.notes_box.delete('1.0', tk.END)
        self.notes_box.insert(tk.END, old_note)

    # adds record in view/edit frame to database
    def add_entry(self):
        if len(self.add_box.get()) == 0:
            messagebox.showerror('Error', 'ToDo box cannot be left blank')
        else:
            try:
                comm = "INSERT INTO todos VALUES (?,?,?)"
                values = self.date_picker.get_date(), self.add_box.get(), self.notes_box.get("1.0", tk.END)[:-1]
                cursor.execute(comm, values)
                conn.commit()
                self.curr_record = ""
                for widget in self.winfo_children():
                    widget.destroy()
                self.build_frame()
            except sqlite3.Error as error:
                messagebox.showerror('SQL Error', 'Failed to add record to table ' + str(error))

    # Displays selected record in the view/edit frame
    def view_entry(self):
        new_todo = self.add_box.get()
        new_date = self.date_picker.get_date()
        new_notes = self.notes_box.get("1.0", tk.END)[:-1]
        if len(self.curr_record) == 0:
            messagebox.showerror('Error', 'Nothing selected ')
        else:
            try:
                command = "UPDATE todos SET due_date=?, todo=?, notes=? WHERE todo=?"
                val = (new_date, new_todo, new_notes, self.curr_record)
                cursor.execute(command, val)
                conn.commit()
                self.curr_record = ""
                for widget in self.winfo_children():
                    widget.destroy()
                self.build_frame()
            except sqlite3.Error as error:
                messagebox.showerror('SQL Error', 'Failed to update record ' + str(error))

    # Clears the values in the view/edit frame
    def clear_entry(self):
        self.add_box.delete('0', tk.END)
        self.date_picker.set_date(date.today())
        self.notes_box.delete('1.0', tk.END)
        self.curr_record = ""

    """
    This function builds the entire frame.  This is what allows for a 'refresh'
    when new data is added to the database. 
    """
    def build_frame(self, command="SELECT * FROM todos ORDER BY due_date ASC", svar=()):
        self.pack_propagate(False)

        # Divide the frame up into 2 sub frames side to side
        self.leftFrame = leftFrame = tk.Frame(self, bg=bg_color)
        self.rightFrame = rightFrame = tk.Frame(self, bg=bg_color)

        # Divide each subframe into two sub frames top to bottom
        self.leftFrame_upper = leftFrame_upper = tk.Frame(leftFrame, bg=bg_color)
        self.leftFrame_lower = leftFrame_lower = tk.Frame(leftFrame, bg=bg_color)
        self.rightFrame_upper = rightFrame_upper = tk.Frame(rightFrame, bg=bg_color)
        self.rightFrame_lower = rightFrame_lower = tk.Frame(rightFrame, bg=bg_color)

        # Implement a canvas to allow for a scrollbar
        self.canvas = canvas = tk.Canvas(rightFrame_upper, bg=bg_color)
        canvas.pack(side='left', fill='both', expand=True)
        rightFrame_upper.pack(side='top', fill='both', expand=True)
        rightFrame_lower.pack(side='bottom', fill='y', expand=True)

        # Scrollbar
        scrollbar = tk.Scrollbar(rightFrame_upper, orient='vertical', command=canvas.yview)
        scrollbar.pack(side='right', fill='y')
        canvas.configure(yscrollcommand=scrollbar.set)

        # Place inner_frame in canvas to hold widgets
        inner_frame = tk.Frame(canvas, bg=bg_color)
        inner_frame.pack(expand=True, fill='x')
        inner_frame.pack_propagate(False)
        canvas.create_window((0, 0), window=inner_frame, anchor='nw')

        # Pull the data from the database, add a header, and iterate through the rows.
        # Adds a checkbox at the front and view/edit button at the end of each row
        view_cursor = conn.execute(command, svar)
        i = 0
        header_date = tk.Label(inner_frame, width=10, fg='white', text='Date', anchor='n', bg=bg_color)
        header_todo = tk.Label(inner_frame, width=60, fg='white', text='ToDo', anchor='n', bg=bg_color)
        header_date.grid(row=i, column=1, sticky='ew')
        header_todo.grid(row=i, column=2, columnspan=2, sticky='ew')
        i += 1
        for todo in view_cursor:
            # Dynamically creates checkbox variable in a dictionary for each row
            self.var[todo[1]] = tk.IntVar()
            # Changes the colors from line to line
            if i % 2 == 0:
                alt_bg = '#61acb0'
            else:
                alt_bg = '#1d5457'
            c = tk.Checkbutton(inner_frame, bg=alt_bg, variable=self.var[todo[1]],
                               command=lambda key=todo[1]: self.read_status(key))
            todo_date = tk.Label(inner_frame, width=10, fg='white', text=todo[0],
                                 relief='flat', anchor='n', bg=alt_bg)
            todo_todo = tk.Label(inner_frame, width=50, fg='white', text=todo[1],
                                 relief='flat', anchor='w', bg=alt_bg)

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
            c.grid(row=i, column=0, sticky='nsew')
            todo_date.grid(row=i, column=1, sticky='nsew')
            todo_todo.grid(row=i, column=2, sticky='nsew')
            edit_btn.grid(row=i, column=3, sticky='nsew')
            i += 1

        i += 1
        self.select_all_var = tk.IntVar()
        select_all_cb = tk.Checkbutton(rightFrame_lower, bg=bg_color, text="Select All", variable=self.select_all_var,
                                       command=lambda: self.select_all())

        entry_label = tk.Label(
            leftFrame_upper,
            text="ToDo:",
            bg=bg_color,
            fg='white',
            font=("Impact", 10)
        )
        self.add_box = tk.Entry(leftFrame_upper, bg='white', justify='left', width=60)
        date_label = tk.Label(
            leftFrame_upper,
            text="Date:",
            bg=bg_color,
            fg='white',
            font=("Impact", 10)
        )
        self.date_picker = DateEntry(leftFrame_upper, selectmode='day')
        notes_label = tk.Label(
            leftFrame_upper,
            text="Notes:",
            bg=bg_color,
            fg='white',
            font=("Impact", 10)
        )
        self.notes_box = tk.Text(leftFrame_upper, bg='white', height=7, width=45)
        add_bt = tk.Button(
            leftFrame_upper,
            text="Add",
            font=('TkMenuFont', 10),
            bg='#28393a',
            fg='white',
            cursor="hand2",
            activebackground='#badee2',
            activeforeground='black',
            command=lambda: self.add_entry()
        )
        update_bt = tk.Button(
            leftFrame_upper,
            text="Update",
            font=('TkMenuFont', 10),
            bg='#28393a',
            fg='white',
            cursor="hand2",
            activebackground='#badee2',
            activeforeground='black',
            command=lambda: self.view_entry()
        )

        clear_button = tk.Button(
            leftFrame_upper,
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
        entry_label.grid(row=0, column=0, columnspan=1, sticky='e', ipady=10)
        self.add_box.grid(row=0, column=1, columnspan=6, sticky='w')
        date_label.grid(row=1, column=0, columnspan=1, sticky='e', ipady=10)
        self.date_picker.grid(row=1, column=1, columnspan=2, sticky='w')
        notes_label.grid(row=2, column=0, columnspan=1, sticky='ne', ipady=10)
        self.notes_box.grid(row=2, column=1, columnspan=6, sticky='w')
        add_bt.grid(row=3, column=1, pady=10, sticky='e')
        update_bt.grid(row=3, column=2, pady=10, padx=5)
        clear_button.grid(row=3, column=3, pady=10, sticky='w')

        canvas.configure(scrollregion=canvas.bbox("all"))

        search_label = tk.Label(
            leftFrame_lower,
            text="Search:",
            bg=bg_color,
            fg='white',
            font=("Impact", 10)
        )
        self.search_box = tk.Entry(leftFrame_lower, bg='white', justify='left', width=60)
        date_search_label = tk.Label(
            leftFrame_lower,
            text="Between:",
            bg=bg_color,
            fg='white',
            font=("Impact", 10)
        )
        self.lower_date_picker = DateEntry(leftFrame_lower, selectmode='day')
        self.higher_date_picker = DateEntry(leftFrame_lower, selectmode='day')
        self.higher_date_picker.set_date(date.today() + timedelta(days=100))

        search_bt = tk.Button(
            leftFrame_lower,
            text="Search",
            font=('TkMenuFont', 10),
            bg='#28393a',
            fg='white',
            cursor="hand2",
            activebackground='#badee2',
            activeforeground='black',
            command=lambda: self.search()
        )

        reset_search_bt = tk.Button(
            leftFrame_lower,
            text="See All",
            font=('TkMenuFont', 10),
            bg='#28393a',
            fg='white',
            cursor="hand2",
            activebackground='#badee2',
            activeforeground='black',
            command=lambda: self.reload_frame()
        )

        search_label.grid(row=0, column=0, columnspan=1, sticky='e', ipady=10)
        self.search_box.grid(row=0, column=1, columnspan=6, sticky='w')
        date_search_label.grid(row=1, column=0, columnspan=1, sticky='e', ipady=10)
        self.lower_date_picker.grid(row=1, column=1, columnspan=1, sticky='w')
        self.higher_date_picker.grid(row=1, column=2, columnspan=1, sticky='e')
        search_bt.grid(row=2, column=1, pady=10, padx=5, sticky='e')
        reset_search_bt.grid(row=2, column=2, pady=10, sticky='w')

        delete_bt = tk.Button(
            rightFrame_lower,
            text="Delete ToDos",
            font=('TkMenuFont', 10),
            bg='#28393a',
            fg='white',
            cursor="hand2",
            activebackground='#badee2',
            activeforeground='black',
            command=lambda: self.delete_from_db()
        )
        delete_bt.pack(anchor="se")

        leftFrame_upper.pack(expand=True, fill='both')
        leftFrame_lower.pack(expand=True, fill='both')
        leftFrame.pack(expand=False, fill='both', side='left', padx=10)
        rightFrame.pack(expand=True, fill='both', side='left')

    # Function to select all check boxes if select all is chosen
    def select_all(self):
        if self.select_all_var.get() == 1:
            for key in self.var.keys():
                self.var.get(key).set(1)

    def read_status(self, key):
        var_obj = self.var.get(key)
        return var_obj.get()

    def reload_frame(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.build_frame()

    def search(self):
        term = self.search_box.get()
        term = '%' + term + '%'
        date_low = self.lower_date_picker.get_date()
        date_high = self.higher_date_picker.get_date()
        command = "SELECT * FROM todos WHERE (due_date >= ? AND due_date <= ?) AND (todo LIKE ?) ORDER BY due_date ASC"
        variables = (date_low, date_high, term)
        for widget in self.winfo_children():
            widget.destroy()
        self.build_frame(command, variables)

    def delete_from_db(self):
        try:
            view_cursor = conn.execute("SELECT * FROM todos")
            comm = "DELETE FROM todos WHERE todo=?"
            for todo in view_cursor:
                to_delete = todo[1]
                if self.read_status(to_delete) == 1:
                    cursor.execute(comm, (to_delete,))
                    conn.commit()
            self.reload_frame()
            pass
        except sqlite3.Error as error:
            messagebox.showerror('SQL Error', 'Failed to delete record from table ' + str(error))


if __name__ == '__main__':
    # initialize app
    root = TodoApp()
    root.title("ToDo List")

    # run app
    root.mainloop()
