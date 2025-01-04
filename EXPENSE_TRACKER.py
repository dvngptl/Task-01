import sqlite3
from tkinter import *
from tkinter import messagebox

# Initialize SQLite database
conn = sqlite3.connect("expenses.db")
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    description TEXT,
                    amount REAL,
                    category TEXT,
                    date TEXT)''')
conn.commit()

# Functions to handle database operations
def add_expense():
    description = entry_description.get()
    amount = entry_amount.get()
    category = combo_category.get()
    date = entry_date.get()

    if description and amount and category and date:
        cursor.execute("INSERT INTO expenses (description, amount, category, date) VALUES (?, ?, ?, ?)", 
                       (description, amount, category, date))
        conn.commit()
        messagebox.showinfo("Success", "Expense Added Successfully!")
        clear_fields()
        display_expenses()
    else:
        messagebox.showerror("Error", "Please fill all fields!")

def display_expenses():
    for row in tree.get_children():
        tree.delete(row)
        
    cursor.execute("SELECT * FROM expenses")
    rows = cursor.fetchall()
    
    for row in rows:
        tree.insert("", "end", values=row)

def clear_fields():
    entry_description.delete(0, END)
    entry_amount.delete(0, END)
    entry_date.delete(0, END)
    combo_category.set("")

# Create main window
root = Tk()
root.title("Expense Tracker")
root.geometry("800x600")

# Labels and Entries
Label(root, text="Description:").grid(row=0, column=0, pady=10, padx=10)
entry_description = Entry(root, width=30)
entry_description.grid(row=0, column=1, pady=10)

Label(root, text="Amount:").grid(row=1, column=0, pady=10, padx=10)
entry_amount = Entry(root, width=30)
entry_amount.grid(row=1, column=1, pady=10)

Label(root, text="Category:").grid(row=2, column=0, pady=10, padx=10)
categories = ["Food", "Transport", "Utilities", "Entertainment", "Other"]
combo_category = ttk.Combobox(root, values=categories, width=28)
combo_category.grid(row=2, column=1, pady=10)

Label(root, text="Date (YYYY-MM-DD):").grid(row=3, column=0, pady=10, padx=10)
entry_date = Entry(root, width=30)
entry_date.grid(row=3, column=1, pady=10)

# Add Expense Button
button_add = Button(root, text="Add Expense", command=add_expense)
button_add.grid(row=4, column=0, columnspan=2, pady=20)

# Expense Display (Treeview)
tree = ttk.Treeview(root, columns=("ID", "Description", "Amount", "Category", "Date"), show="headings")
tree.grid(row=5, column=0, columnspan=2, pady=20)

tree.heading("ID", text="ID")
tree.heading("Description", text="Description")
tree.heading("Amount", text="Amount")
tree.heading("Category", text="Category")
tree.heading("Date", text="Date")

# Display expenses initially
display_expenses()

# Start the main loop
root.mainloop()

# Close the connection when the app is closed
conn.close()
