import csv
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry  # type: ignore # Import DateEntry for calendar dropdown
from datetime import datetime

class Expense:
    def __init__(self, date, description, amount):  # Fixed __init__ method
        self.date = date
        self.description = description
        self.amount = amount

class ExpenseTracker:
    def __init__(self, filename="expenses.csv"):  # Fixed __init__ method
        self.expenses = []
        self.filename = filename
        self.load_expenses()

    def add_expense(self, expense):
        self.expenses.append(expense)
        self.save_expenses()

    def remove_expense(self, index):
        if 0 <= index < len(self.expenses):
            self.expenses.pop(index)
            self.save_expenses()

    def total_expenses(self):
        return sum(expense.amount for expense in self.expenses)

    def save_expenses(self):
        with open(self.filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Description", "Amount"])
            for expense in self.expenses:
                writer.writerow([expense.date, expense.description, expense.amount])

    def load_expenses(self):
        try:
            with open(self.filename, "r") as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    if len(row) == 3:
                        date, description, amount = row
                        self.expenses.append(Expense(date, description, float(amount)))
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"Error loading expenses: {e}")

class ExpenseTrackerApp:
    def __init__(self, root):  # Fixed __init__ method
        self.tracker = ExpenseTracker()
        self.root = root
        self.root.title("Expense Tracker")
        self.root.configure(bg="#f0f0f0")  # Light grey background

        # Dropdown menu
        self.menu_label = tk.Label(root, text="Select an Action:", font=("Arial", 12), bg="#f0f0f0")
        self.menu_label.pack(pady=5)

        self.actions = ["Add Expense", "Remove Expense", "View Expenses", "Total Expenses"]
        self.action_var = tk.StringVar()
        self.dropdown = ttk.Combobox(root, textvariable=self.action_var, values=self.actions, state="readonly")
        self.dropdown.pack(pady=5)
        self.dropdown.bind("<<ComboboxSelected>>", self.handle_dropdown)

        # Input fields
        self.date_label = tk.Label(root, text="Select Date:", bg="#f0f0f0")
        self.date_entry = DateEntry(root, date_pattern="yyyy-MM-dd")  # Calendar dropdown
        self.description_label = tk.Label(root, text="Description:", bg="#f0f0f0")
        self.description_entry = tk.Entry(root)
        self.amount_label = tk.Label(root, text="Amount:", bg="#f0f0f0")
        self.amount_entry = tk.Entry(root)

        # Buttons with colors
        self.add_button = tk.Button(root, text="Add Expense", command=self.add_expense, bg="#4CAF50", fg="white")
        self.remove_button = tk.Button(root, text="Remove Selected Expense", command=self.remove_expense, bg="#f44336", fg="white")
        self.view_button = tk.Button(root, text="View Expenses", command=self.view_expenses, bg="#008CBA", fg="white")
        self.total_button = tk.Button(root, text="Show Total Expenses", command=self.show_total_expenses, bg="#ff9800", fg="white")

        # Expense listbox
        self.expense_list = tk.Listbox(root, width=50, height=10, bg="#ffffff", fg="#333333")
        self.update_expense_list()

    def handle_dropdown(self, event):
        action = self.action_var.get()
        self.clear_widgets()

        if action == "Add Expense":
            self.show_add_expense()
        elif action == "Remove Expense":
            self.show_remove_expense()
        elif action == "View Expenses":
            self.show_view_expenses()
        elif action == "Total Expenses":
            self.show_total_expenses()

    def show_add_expense(self):
        self.date_label.pack()
        self.date_entry.pack()
        self.description_label.pack()
        self.description_entry.pack()
        self.amount_label.pack()
        self.amount_entry.pack()
        self.add_button.pack(pady=5)

    def show_remove_expense(self):
        self.show_view_expenses()
        self.remove_button.pack(pady=5)

    def show_view_expenses(self):
        self.expense_list.pack(pady=5)
        self.view_button.pack(pady=5)

    def show_total_expenses(self):
        total = self.tracker.total_expenses()
        messagebox.showinfo("Total Expenses", f"Total Expenses: ${total:.2f}")

    def add_expense(self):
        date = self.date_entry.get_date().strftime("%Y-%m-%d")
        description = self.description_entry.get().strip()
        amount = self.amount_entry.get().strip()

        if not date or not description or not amount:
            messagebox.showerror("Error", "All fields are required!")
            return

        try:
            amount = float(amount)
            if amount < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Invalid amount format.")
            return

        self.tracker.add_expense(Expense(date, description, amount))
        messagebox.showinfo("Success", "Expense added successfully!")
        self.update_expense_list()

    def remove_expense(self):
        selected_index = self.expense_list.curselection()
        if not selected_index:
            messagebox.showerror("Error", "Please select an expense to remove.")
            return

        index = selected_index[0]
        self.tracker.remove_expense(index)
        messagebox.showinfo("Success", "Expense removed successfully!")
        self.update_expense_list()

    def view_expenses(self):
        self.update_expense_list()

    def update_expense_list(self):
        self.expense_list.delete(0, tk.END)
        for i, expense in enumerate(self.tracker.expenses, start=1):
            self.expense_list.insert(tk.END, f"{i}. {expense.date} | {expense.description} | ${expense.amount:.2f}")

    def clear_widgets(self):
        self.date_label.pack_forget()
        self.date_entry.pack_forget()
        self.description_label.pack_forget()
        self.description_entry.pack_forget()
        self.amount_label.pack_forget()
        self.amount_entry.pack_forget()
        self.add_button.pack_forget()
        self.remove_button.pack_forget()
        self.view_button.pack_forget()
        self.total_button.pack_forget()
        self.expense_list.pack_forget()

if __name__ == "__main__":  # Fixed __name__ check
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()