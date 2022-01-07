from tkinter import *
from tkinter.ttk import *
from backend import Database
from tkcalendar import Calendar


class expense_tracker:

    def __init__(self, master):
        self.databse = Database()
        master.title("Expense Tracker")
        self.master = Frame(master)
        self.master.pack()
        #self.master.title("Expense Tracker")
        self.Gui = Canvas(self.master, width=840, height=500, highlightthickness=0)
        self.Gui.pack()

        # Variables
        #self.amount = StringVar()
        self.drop_choice = StringVar()
        self.notes = StringVar()


        # Calendar
        self.cal = Calendar(self.Gui)
        self.Gui.create_window(140, 110, window=self.cal)

        # Input labels and boxes
        self.Gui.create_text(370, 90, font="Times 16", text="Ammount")
        self.amount_entry = Entry(self.Gui, width=30)
        self.Gui.create_window(380, 120, window=self.amount_entry)


        self.category = ["Select","Food", "Bills", "shopping", "travel"]
        self.Gui.create_text(370, 30, font="Times 16", text="Category")
        
        self.drop_menu = OptionMenu(self.Gui, self.drop_choice, *self.category)
        self.Gui.create_window(380, 60, window=self.drop_menu)

        self.Gui.create_text(370, 160, font="Times 16", text="Notes")
        self.notes_entry = Entry(self.Gui, width=30, textvariable=self.notes)
        self.Gui.create_window(380, 190, window=self.notes_entry)


        # Buttons
        self.show_by_date = Button(self.Gui, text="Search Date", command=self.search_by_date, width=12)
        self.Gui.create_window(80, 240, window=self.show_by_date)

        self.show_all_button = Button(self.Gui, text="Show all", command=self.fill_tables, width=12)
        self.Gui.create_window(200, 240, window=self.show_all_button)

        self.submit = Button(self.Gui, text="Submit", command=self.submit, width=12)
        self.Gui.create_window(380, 240, window=self.submit)


        # Table to show info.
        self.frame = Frame(self.Gui, borderwidth=6)
        self.frame.pack()

        self.scrollbar = Scrollbar(self.frame, orient='vertical')

        Elist = ["Date", "Amount", "Category", "Notes"]
        self.Etable=Treeview(self.frame,column=Elist,show='headings',height=9, yscrollcommand=self.scrollbar.set)
        for column in Elist:
            self.Etable.heading(column, text=column.title())

        self.scrollbar.config(command=self.Etable.yview)
        self.scrollbar.pack(side='right', fill='y')

        self.Etable.pack()
        self.Gui.create_window(420, 380, window=self.frame)

        self.fill_tables()


    def fill_tables(self):
        for items in self.Etable.get_children():
            self.Etable.delete(items)
        for row in self.databse.view_all():
            self.Etable.insert('', 'end', values=row)

    def search_by_date(self):
        for items in self.Etable.get_children():
            self.Etable.delete(items)
        for rows in self.databse.search_date(self.cal.get_date()):
            self.Etable.insert('', 'end', values=rows)

    def get_date(self):
        print(self.cal.get_date())

    def submit(self):
        values = [self.cal.get_date(), self.amount_entry.get(), self.drop_choice.get(), self.notes_entry.get()]
        self.databse.add_entry(self.cal.get_date(), self.amount_entry.get(), self.drop_choice.get(), self.notes_entry.get())

        self.Etable.insert('', 'end', values=values)

        print(values)


if __name__ == "__main__":
    window = Tk()
    expense_tracker(window)
    window.mainloop()



# different borders
#https://stackoverflow.com/questions/39416021/border-for-tkinter-label/39416145
