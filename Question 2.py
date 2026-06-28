import tkinter as tk
from tkinter import messagebox
import time


# ==================================================
# 📦 TRANSACTION CLASS
# ==================================================
class Transaction:
    def __init__(self, transactionID, customerName, productName, amount, transactionDate):
        self.transactionID = int(transactionID)
        self.customerName = customerName
        self.productName = productName
        self.amount = float(amount)
        self.transactionDate = transactionDate

    def __str__(self):
        return f"ID:{self.transactionID} | {self.customerName} | {self.productName} | RM{self.amount} | {self.transactionDate}"



#DATASET
transactions = [
    Transaction(105, "Ali", "Shoes", 120.5, "2025-01-10"),
    Transaction(101, "Aisyah", "Bag", 80.0, "2025-03-11"),
    Transaction(110, "John", "Watch", 250.0, "2025-02-20"),
    Transaction(103, "Lina", "Phone Case", 15.0, "2025-05-02"),
    Transaction(108, "Raj", "Laptop", 1500.0, "2025-06-01"),
    Transaction(102, "Sarah", "Headphones", 200.0, "2025-04-15"),
    Transaction(109, "Mike", "Keyboard", 90.0, "2025-03-25"),
    Transaction(104, "Nora", "Mouse", 40.0, "2025-02-05"),
    Transaction(107, "David", "Monitor", 300.0, "2025-01-28"),
    Transaction(106, "Emma", "Tablet", 600.0, "2025-06-10")
]

sorted_transactions = None
merge_calls = 0
is_sorted = False



# DISPLAY
def display(arr):
    output_box.delete("1.0", tk.END)
    for t in arr:
        output_box.insert(tk.END, str(t) + "\n")



# MERGE SORT (BY ATTRIBUTE)
def merge_sort(arr, key):
    global merge_calls
    merge_calls += 1

    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid], key)
    right = merge_sort(arr[mid:], key)

    return merge(left, right, key)

def merge(left, right, key):
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if getattr(left[i], key) <= getattr(right[j], key):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result



# BINARY SEARCH
def binary_search(arr, target, low, high):
    if low > high:
        return -1

    mid = (low + high) // 2

    if arr[mid].transactionID == target:
        return mid
    elif arr[mid].transactionID > target:
        return binary_search(arr, target, low, mid - 1)
    else:
        return binary_search(arr, target, mid + 1, high)



#LINEAR SEARCH
def linear_search(arr, target):
    for i in range(len(arr)):
        if arr[i].transactionID == target:
            return i
    return -1


#ADD TRANSACTION
def add_transaction():
    global is_sorted
    try:
        # Ensure no empty fields (placeholders will be empty strings if not touched)
        if not all([entry_id.get(), entry_name.get(), entry_product.get(), entry_amount.get(), entry_date.get()]):
            raise ValueError("All fields are required.")

        t = Transaction(
            entry_id.get(),
            entry_name.get(),
            entry_product.get(),
            entry_amount.get(),
            entry_date.get()
        )
        transactions.append(t)

        # Invalidate the sorted cache since we added a new item
        is_sorted = False

        display(transactions)
        messagebox.showinfo("Success", "Transaction Added")
    except ValueError as e:
        messagebox.showerror("Error", f"Invalid input: {str(e)}")
    except Exception:
        messagebox.showerror("Error", "An unexpected error occurred.")



#SORT FUNCTION
def sort_data():
    global sorted_transactions, merge_calls, is_sorted

    merge_calls = 0
    key = sort_option.get()

    # 1. Capture the unsorted state
    before_text = "--- BEFORE SORTING ---\n" + "\n".join(str(t) for t in transactions) + "\n\n"

    start = time.perf_counter_ns()
    sorted_transactions = merge_sort(transactions.copy(), key)
    end = time.perf_counter_ns()

    is_sorted = True

    # 2. Capture the sorted state
    after_text = "--- AFTER SORTING ---\n" + "\n".join(str(t) for t in sorted_transactions) + "\n"

    # 3. Display BOTH in the output box
    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, before_text + after_text)

    messagebox.showinfo(
        "Merge Sort",
        f"Sorted by: {key}\nTime: {end - start} ns\nRecursive Calls: {merge_calls}"
    )

#  SEARCH FUNCTIONS
def binary_search_gui():
    try:
        target = int(entry_search.get())
    except ValueError:
        messagebox.showerror("Error", "Invalid ID. Please enter an integer.")
        return

    # FIX: Binary search strictly requires the array to be sorted by the search key (transactionID).
    # We only use the cached sorted_transactions if it was actually sorted by transactionID.
    if is_sorted and sort_option.get() == "transactionID":
        data = sorted_transactions
    else:
        # Otherwise, we must sort a copy by transactionID first
        data = merge_sort(transactions.copy(), "transactionID")

    start = time.perf_counter_ns()
    index = binary_search(data, target, 0, len(data) - 1)
    end = time.perf_counter_ns()

    # Combined into a single message box for better UX
    if index != -1:
        messagebox.showinfo("Binary Search Result", f"Found:\n{data[index]}\n\nTime: {end - start} ns")
    else:
        messagebox.showinfo("Binary Search Result", f"ID {target} Not Found.\n\nTime: {end - start} ns")


def linear_search_gui():
    try:
        target = int(entry_search.get())
    except ValueError:
        messagebox.showerror("Error", "Invalid ID. Please enter an integer.")
        return

    start = time.perf_counter_ns()
    index = linear_search(transactions, target)
    end = time.perf_counter_ns()

    if index != -1:
        messagebox.showinfo("Linear Search Result", f"Found:\n{transactions[index]}\n\nTime: {end - start} ns")
    else:
        messagebox.showinfo("Linear Search Result", f"ID {target} Not Found.\n\nTime: {end - start} ns")



#
# GUI SETUP
root = tk.Tk()
root.title("Advanced Transaction System")
root.geometry("1000x650")


# Helper function to create auto-clearing placeholder text
def setup_placeholder(entry, placeholder):
    entry.insert(0, placeholder)
    entry.config(fg='grey')

    def on_focus_in(event):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.config(fg='black')

    def on_focus_out(event):
        if not entry.get():
            entry.insert(0, placeholder)
            entry.config(fg='grey')

    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)


# ---------------- SORT OPTIONS ----------------
sort_option = tk.StringVar(value="transactionID")


# Invalidate cache if the user changes the dropdown without clicking "Merge Sort"
def on_sort_change(*args):
    global is_sorted
    is_sorted = False


sort_option.trace_add("write", on_sort_change)

tk.Label(root, text="Sort By:", font=("Arial", 10, "bold")).pack(pady=(10, 0))
tk.OptionMenu(root, sort_option, "transactionID", "amount", "transactionDate").pack()

# ---------------- ADD TRANSACTION ----------------
frame_add = tk.Frame(root)
frame_add.pack(pady=15)

entry_id = tk.Entry(frame_add, width=10)
entry_name = tk.Entry(frame_add, width=15)
entry_product = tk.Entry(frame_add, width=15)
entry_amount = tk.Entry(frame_add, width=10)
entry_date = tk.Entry(frame_add, width=12)

setup_placeholder(entry_id, "ID")
setup_placeholder(entry_name, "Name")
setup_placeholder(entry_product, "Product")
setup_placeholder(entry_amount, "Amount")
setup_placeholder(entry_date, "YYYY-MM-DD")

entry_id.grid(row=0, column=0, padx=5)
entry_name.grid(row=0, column=1, padx=5)
entry_product.grid(row=0, column=2, padx=5)
entry_amount.grid(row=0, column=3, padx=5)
entry_date.grid(row=0, column=4, padx=5)

tk.Button(frame_add, text="Add", command=add_transaction, bg="#4CAF50", fg="white").grid(row=0, column=5, padx=5)

# ---------------- SEARCH ----------------
frame_search = tk.Frame(root)
frame_search.pack(pady=10)

entry_search = tk.Entry(frame_search, width=20)
entry_search.pack(padx=10, pady=5)
setup_placeholder(entry_search, "Enter Transaction ID")

# ---------------- BUTTONS ----------------
frame_btn = tk.Frame(root)
frame_btn.pack(pady=10)

tk.Button(frame_btn, text="Show All", command=lambda: display(transactions), width=12).grid(row=0, column=0, padx=5)
tk.Button(frame_btn, text="Merge Sort", command=sort_data, width=12).grid(row=0, column=1, padx=5)
tk.Button(frame_btn, text="Binary Search", command=binary_search_gui, width=12).grid(row=0, column=2, padx=5)
tk.Button(frame_btn, text="Linear Search", command=linear_search_gui, width=12).grid(row=0, column=3, padx=5)

# ---------------- OUTPUT ----------------
output_box = tk.Text(root, height=50, width=110, font=("Consolas", 10))
output_box.pack(padx=20, pady=10)

# Initial display
display(transactions)

root.mainloop()