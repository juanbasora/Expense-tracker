from tkinter.ttk import Entry, Button, Checkbutton, OptionMenu, Scrollbar
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import Tk, Frame, Canvas, StringVar, IntVar
from matplotlib.figure import Figure
from tkcalendar import Calendar
from tkinter import messagebox
from ttkwidgets import Table
from backend import Database


class ExpenseTracker:

    def __init__(self):
        self.database = Database()
        self.master = Tk()
        self.master.title("Expense Tracker")
        self.master = Frame(self.master)
        self.master.pack()
        self.Gui = Canvas(self.master, width=840, height=520, highlightthickness=0, bg='whitesmoke')
        self.Gui.pack()

        # Variables
        self.drop_choice = StringVar()
        self.entries_dict = {}

        # Calendar
        self.cal = Calendar(self.Gui)
        self.Gui.create_window(140, 110, window=self.cal)

        # labels and input boxes
        self.Gui.create_text(370, 90, font="Times 16", text="Amount")
        self.amount_entry = Entry(self.Gui, width=30)
        self.Gui.create_window(380, 120, window=self.amount_entry)

        self.Gui.create_text(370, 30, font="Times 16", text="Category")
        self.categories = ["Select", "Food", "Shopping", "Health", "Bills", "Transport", "Travel"]
        self.drop_menu = OptionMenu(self.Gui, self.drop_choice, *self.categories)
        self.Gui.create_window(380, 60, window=self.drop_menu)

        self.Gui.create_text(370, 160, font="Times 16", text="Notes")
        self.notes_entry = Entry(self.Gui, width=30)
        self.Gui.create_window(380, 190, window=self.notes_entry)

        # Buttons
        self.delete_button = Button(self.Gui, text="Delete", command=self.delete, width=12)
        self.Gui.create_window(130, 280, window=self.delete_button)

        self.show_by_date = Button(self.Gui, text="Search Date", command=self.search_by_date, width=12)
        self.Gui.create_window(80, 240, window=self.show_by_date)

        self.show_by_month = Button(self.Gui, text="Show Month", command=self.get_month, width=12)
        self.Gui.create_window(190, 240, window=self.show_by_month)

        self.submit = Button(self.Gui, text="Submit", command=self.submit, width=12)
        self.Gui.create_window(380, 240, window=self.submit)

        # Checkbox
        self.check_button = IntVar()
        self.dollar_value = Checkbutton(self.Gui, text="Dollar Value", variable=self.check_button, onvalue=1,
                                        offvalue=0, command=self.get_pie_info)
        self.Gui.create_window(650, 280, window=self.dollar_value)

        # Table with its own frame so we can attach a scrollbar.
        self.table_frame = Frame(self.master, borderwidth=6)
        self.table_frame.pack()

        titles = ["ID", "Date", "Amount", "Category", "Notes"]
        self.Etable = Table(self.table_frame, columns=titles, height=9)

        # Configuring the table.
        for header in titles:
            self.Etable.heading(header, text=header)
            self.Etable.column(header, width=160, stretch=False)
            self.Etable.config(drag_cols=False)
            self.Etable.config(drag_rows=False)

        # Attaching scrollbar to the table.
        self.scrollbar = Scrollbar(self.table_frame, orient='vertical', command=self.Etable.yview)
        self.Etable.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side='right', fill='y')

        # Setting colunmns "ID" and "Amount" as int for better sorting.
        self.Etable.column("ID", type=int)
        self.Etable.column("Amount", type=int)
        self.Etable.pack()
        self.Gui.create_window(420, 405, window=self.table_frame)

        # Get entries for the month.
        self.get_month()

    def get_pie_info(self):
        self.entries_dict.clear()  # reset the dictionary to be emtpy

        for items in self.Etable.get_children():
            row = self.Etable.item(items)
            category = row['values'][3]
            amount = row['values'][2]
            if category in self.entries_dict:
                self.entries_dict[category] += float(amount)
            else:
                self.entries_dict[category] = float(amount)

        self.pie_chart_config(self.entries_dict)

    def edit_pie_chart(self, category, amount, deduct=False):
        if deduct:
            if category in self.entries_dict:
                self.entries_dict[category] -= float(amount)
                if self.entries_dict[category] == 0:
                    self.entries_dict.pop(category)
                    if len(self.entries_dict) == 0:
                        self.empty_pie_chart()
                    else:
                        self.pie_chart_config(self.entries_dict)
        elif category in self.entries_dict:
            self.entries_dict[category] += float(amount)
        else:
            self.entries_dict[category] = float(amount)

        self.pie_chart_config(self.entries_dict)

    def pie_chart_config(self, entries):
        label = []
        values = []

        for item, amount in entries.items():
            label.append(item)
            values.append(amount)

        if self.check_button.get() == 1:
            number_display = lambda p: f'${p * sum(values) / 100 :.2f}'
        else:
            number_display = '%1.0f%%'

        fig = Figure(figsize=(3.4, 2.5))
        fig.patch.set_facecolor('whitesmoke')
        ax = fig.add_subplot(111)
        ax.pie(values, radius=1.2, labels=label, autopct=number_display, shadow=True)
        self.add_pie_chart_to_window(fig, 660, 135, 'enabled')

    def empty_pie_chart(self):
        fig = Figure(figsize=(3.4, 2.5))
        fig.patch.set_facecolor('whitesmoke')
        ax = fig.add_subplot(111)
        ax.pie([100], radius=1.2, labels=['No data'], labeldistance=0, colors='green', shadow=False)
        self.add_pie_chart_to_window(fig, 660, 135, 'disabled')

    def add_pie_chart_to_window(self, fig, arg1, arg2, state):
        pie = FigureCanvasTkAgg(fig, self.master)
        self.Gui.create_window(arg1, arg2, window=pie.get_tk_widget())
        self.dollar_value.config(state=state)

    def search_by_date(self):
        # Clear the table and insert entries that match the search date.
        for items in self.Etable.get_children():
            self.Etable.delete(items)
        for rows in self.database.search_date(self.cal.get_date()):
            self.Etable.insert('', 'end', values=rows)

    def get_month(self):
        # Clear table and insert entries that match the month displayed.
        for items in self.Etable.get_children():
            self.Etable.delete(items)

        for entries in self.database.view_all():
            date = entries[1]
            if date.split('/')[0] == str(self.cal.get_displayed_month()[0]):
                self.Etable.insert('', 'end', values=entries)

        if len(self.Etable.get_children()) == 0:
            self.empty_pie_chart()
        else:
            self.get_pie_info()

    def submit(self):
        if self.drop_choice.get() != "Select":
            try:
                self.add_to_db()
            except ValueError:
                messagebox.showinfo("Error", "Please enter a valid dollar amount")
        else:
            messagebox.showinfo("Error", "Please choose a category")

    def add_to_db(self):
        # float(self.amount_entry.get())
        self.database.add_entry(self.cal.get_date(), self.amount_entry.get(), self.drop_choice.get(),
                                self.notes_entry.get())

        values = [self.database.last_edit()[0], self.cal.get_date(), self.amount_entry.get(), self.drop_choice.get(),
                  self.notes_entry.get()]
        self.Etable.insert('', 'end', values=values)

        self.edit_pie_chart(self.drop_choice.get(), self.amount_entry.get())
        self.amount_entry.delete(0, 'end')
        self.notes_entry.delete(0, 'end')

    def delete(self):
        # Getting the values from the selected item.
        for entrie in self.Etable.selection():
            row = self.Etable.item(entrie)
            # Deleting from database using the ID.
            self.database.delete(row['values'][0])
            # Deletgin from table
            self.Etable.delete(entrie)
            # Delete from pie chart
            self.edit_pie_chart(row['values'][3], row['values'][2], True)

    def start(self):
        self.master.mainloop()


if __name__ == "__main__":
    ExpenseTracker().start()
