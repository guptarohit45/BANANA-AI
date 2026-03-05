import tkinter as tk
from tkinter import messagebox
import random
import time

# ----------------- MAIN APP -----------------
root = tk.Tk()
root.geometry("950x600")
root.title("☕ Café Management System")

# ----------------- VARIABLES -----------------
menu_items = {
    "Espresso": 60,
    "Cappuccino": 80,
    "Latte": 90,
    "Tea": 40,
    "Sandwich": 120,
    "Burger": 150,
    "Pastry": 70,
    "Muffin": 60,
}

quantities = {}
for item in menu_items:
    quantities[item] = tk.IntVar()

total_var = tk.StringVar()
tax_var = tk.StringVar()
final_var = tk.StringVar()   
receipt_text = tk.StringVar()


# ----------------- FUNCTIONS -----------------
def calculate_total():
    subtotal = 0
    for item, price in menu_items.items():
        subtotal += quantities[item].get() * price

    tax = round(subtotal * 0.05, 2)  # 5% GST
    total = round(subtotal + tax, 2)

    total_var.set(f"₹ {subtotal}")
    tax_var.set(f"₹ {tax}")
    final_var.set(f"₹ {total}")

    return subtotal, tax, total


def generate_receipt():
    subtotal, tax, total = calculate_total()
    receipt = "===== Café Receipt =====\n"
    receipt += f"Bill No: {random.randint(1000, 9999)}\n"
    receipt += f"Date: {time.strftime('%d/%m/%Y')}\n\n"
    for item, qty in quantities.items():
        if qty.get() > 0:
            receipt += f"{item} x {qty.get()} = ₹ {qty.get() * menu_items[item]}\n"
    receipt += "\n----------------------\n"
    receipt += f"Subtotal: {total_var.get()}\n"
    receipt += f"Tax (5%): {tax_var.get()}\n"
    receipt += f"Total: {final_var.get()}\n"
    receipt += "=======================\n"
    receipt_text.set(receipt)


def reset_order():
    for qty in quantities.values():
        qty.set(0)
    total_var.set("")
    tax_var.set("")
    final_var.set("")
    receipt_text.set("")
    receipt_box.delete(1.0, "end")


def exit_app():
    if messagebox.askyesno("Exit", "Do you really want to exit?"):
        root.destroy()


# ----------------- UI LAYOUT -----------------
title = tk.Label(root, text="☕ Café Management System", font=("Arial", 24, "bold"), bg="brown", fg="white")
title.pack(fill="x")

frame_menu = tk.Frame(root, bd=8, relief="ridge", bg="beige")
frame_menu.place(x=20, y=60, width=450, height=400)

frame_bill = tk.Frame(root, bd=8, relief="ridge", bg="beige")
frame_bill.place(x=500, y=60, width=420, height=400)

frame_buttons = tk.Frame(root, bd=8, relief="ridge", bg="lightgrey")
frame_buttons.place(x=20, y=480, width=900, height=100)

# Menu section
tk.Label(frame_menu, text="Menu", font=("Arial", 20, "bold"), bg="beige").grid(row=0, column=0, columnspan=2)

row = 1
for item, price in menu_items.items():
    tk.Label(frame_menu, text=f"{item} (₹{price})", font=("Arial", 14), bg="beige").grid(row=row, column=0, sticky="w",
                                                                                         pady=5)
    tk.Entry(frame_menu, textvariable=quantities[item], font=("Arial", 14), width=5).grid(row=row, column=1, pady=5)
    row += 1

# Bill details
tk.Label(frame_bill, text="Bill Summary", font=("Arial", 20, "bold"), bg="beige").pack()

# Receipt text box
receipt_box = tk.Text(frame_bill, font=("Courier New", 12), width=45, height=10)
receipt_box.pack(pady=5)

# Show Subtotal, Tax and Total under receipt
tk.Label(frame_bill, text="Subtotal:", font=("Arial", 12, "bold"), bg="beige").pack(anchor="w")
tk.Label(frame_bill, textvariable=total_var, font=("Arial", 12), bg="beige").pack(anchor="w")

tk.Label(frame_bill, text="Tax (5%):", font=("Arial", 12, "bold"), bg="beige").pack(anchor="w")
tk.Label(frame_bill, textvariable=tax_var, font=("Arial", 12), bg="beige").pack(anchor="w")

tk.Label(frame_bill, text="Total:", font=("Arial", 12, "bold"), bg="beige").pack(anchor="w")
tk.Label(frame_bill, textvariable=final_var, font=("Arial", 12), bg="beige").pack(anchor="w")

# Buttons
btn_total = tk.Button(frame_buttons, text="Calculate Total", font=("Arial", 14, "bold"), bg="green", fg="white",
                      width=15, command=calculate_total)
btn_total.grid(row=0, column=0, padx=10)

btn_receipt = tk.Button(frame_buttons, text="Generate Receipt", font=("Arial", 14, "bold"), bg="blue", fg="white",
                        width=18,
                        command=lambda: [generate_receipt(), receipt_box.delete(1.0, "end"),
                                         receipt_box.insert("end", receipt_text.get())])
btn_receipt.grid(row=0, column=1, padx=10)

btn_reset = tk.Button(frame_buttons, text="Reset", font=("Arial", 14, "bold"), bg="orange", fg="white", width=10,
                      command=reset_order)
btn_reset.grid(row=0, column=2, padx=10)

btn_exit = tk.Button(frame_buttons, text="Exit", font=("Arial", 14, "bold"), bg="red", fg="white", width=10,
                     command=exit_app)
btn_exit.grid(row=0, column=3, padx=10)

# ----------------- START -----------------
root.mainloop()