import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import os

# ----------------- File Setup -----------------
FILE_NAME = "Patients.xlsx"

# If file does not exist, create a new one with headers
if not os.path.exists(FILE_NAME):
    df = pd.DataFrame(columns=["Patient ID", "Name", "Age", "Gender", "Appointment Date", "Doctor"])
    df.to_excel(FILE_NAME, index=False)


# ----------------- Functions -----------------
def load_data():
    """Load Excel data into the Treeview"""

    tree.delete(*tree.get_children())  # clear old data
    df = pd.read_excel(FILE_NAME)
    for _, row in df.iterrows():
        tree.insert("", tk.END, values=list(row))


def add_patient():
    """Add a new patient record"""
    try:
        patient_id = entry_id.get()
        name = entry_name.get()
        age = int(entry_age.get())
        gender = combo_gender.get()
        appointment_date = entry_date.get()
        doctor = entry_doctor.get()

        if not (patient_id and name and gender and appointment_date and doctor):
            messagebox.showwarning("Input Error", "All fields are required!")
            return

        df = pd.read_excel(FILE_NAME)
        new_data = pd.DataFrame([[patient_id, name, age, gender, appointment_date, doctor]],
                                columns=df.columns)
        df = pd.concat([df, new_data], ignore_index=True)
        df.to_excel(FILE_NAME, index=False)
        load_data()
        clear_entries()
        messagebox.showinfo("Success", "Patient added successfully!")

    except ValueError:
        messagebox.showerror("Error", "Age must be a number!")


def delete_patient():
    """Delete selected patient record"""
    try:
        selected_item = tree.selection()[0]
        values = tree.item(selected_item, "values")
        patient_id = values[0]

        df = pd.read_excel(FILE_NAME)
        df = df[df["Patient ID"] != patient_id]
        df.to_excel(FILE_NAME, index=False)
        load_data()
        messagebox.showinfo("Deleted", "Patient record deleted successfully!")
    except IndexError:
        messagebox.showwarning("Error", "Please select a patient to delete.")


def delete_patient():
    selected_items = tree.selection()
    if not selected_items:
        messagebox.showwarning("Error", "Please select a patient to delete.")
        return

    selected_item = selected_items[0]
    values = tree.item(selected_item, "values")
    patient_id = values[0]

    # Confirm before deleting
    confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete Patient ID {patient_id}?")
    if not confirm:
        return

    try:
        # Read Excel and delete the row safely
        df = pd.read_excel(FILE_NAME)
        df = df[df["Patient ID"].astype(str) != str(patient_id)]
        df.to_excel(FILE_NAME, index=False)

        # Refresh Treeview
        load_data()
        messagebox.showinfo("Deleted", "Patient record deleted successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


def search_patient():
    """Search patient by name"""
    query = entry_search.get().lower()
    tree.delete(*tree.get_children())
    df = pd.read_excel(FILE_NAME)

    for _, row in df.iterrows():
        if query in str(row["Name"]).lower():
            tree.insert("", tk.END, values=list(row))


def clear_entries():
    """Clear all input fields"""
    entry_id.delete(0, tk.END)
    entry_name.delete(0, tk.END)
    entry_age.delete(0, tk.END)
    combo_gender.set("")
    entry_date.delete(0, tk.END)
    entry_doctor.delete(0, tk.END)


# ----------------- GUI Setup -----------------
root = tk.Tk()
root.title("🏥 Patient Appointment Tracker")
root.geometry("900x600")
root.configure(bg="#f4f6f7")

frame_form = tk.Frame(root, bg="#d6eaf8", padx=10, pady=10, relief=tk.RIDGE, bd=3)
frame_form.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

tk.Label(frame_form, text="Patient ID:", bg="#d6eaf8").grid(row=0, column=0, sticky="w")
entry_id = tk.Entry(frame_form)
entry_id.grid(row=0, column=1)

tk.Label(frame_form, text="Name:", bg="#d6eaf8").grid(row=1, column=0, sticky="w")
entry_name = tk.Entry(frame_form)
entry_name.grid(row=1, column=1)

tk.Label(frame_form, text="Age:", bg="#d6eaf8").grid(row=2, column=0, sticky="w")
entry_age = tk.Entry(frame_form)
entry_age.grid(row=2, column=1)

tk.Label(frame_form, text="Gender:", bg="#d6eaf8").grid(row=0, column=2, sticky="w")
combo_gender = ttk.Combobox(frame_form, values=["Male", "Female", "Other"])
combo_gender.grid(row=0, column=3)

tk.Label(frame_form, text="Appointment Date (YYYY-MM-DD):", bg="#d6eaf8").grid(row=1, column=2, sticky="w")
entry_date = tk.Entry(frame_form)
entry_date.grid(row=1, column=3)

tk.Label(frame_form, text="Doctor:", bg="#d6eaf8").grid(row=2, column=2, sticky="w")
entry_doctor = tk.Entry(frame_form)
entry_doctor.grid(row=2, column=3)

btn_add = tk.Button(frame_form, text="➕ Add Patient", command=add_patient, bg="#27ae60", fg="white", width=15)
btn_add.grid(row=3, column=0, pady=5)

btn_delete = tk.Button(frame_form, text="🗑 Delete Patient", command=delete_patient, bg="#c0392b", fg="white", width=15)
btn_delete.grid(row=3, column=1, pady=5)

btn_clear = tk.Button(frame_form, text="❌ Clear", command=clear_entries, bg="#7f8c8d", fg="white", width=15)
btn_clear.grid(row=3, column=2, pady=5)

btn_load = tk.Button(frame_form, text="🔄 Refresh", command=load_data, bg="#2980b9", fg="white", width=15)
btn_load.grid(row=3, column=3, pady=5)

# ----------------- Search Section -----------------
frame_search = tk.Frame(root, bg="#f9e79f", padx=10, pady=10, relief=tk.RIDGE, bd=3)
frame_search.pack(fill=tk.X, padx=10, pady=5)

tk.Label(frame_search, text="🔍 Search by Name:", bg="#f9e79f").pack(side=tk.LEFT)
entry_search = tk.Entry(frame_search)
entry_search.pack(side=tk.LEFT, padx=5)
btn_search = tk.Button(frame_search, text="Search", command=search_patient, bg="#8e44ad", fg="white")
btn_search.pack(side=tk.LEFT, padx=5)

# ----------------- Patient Table -----------------
frame_table = tk.Frame(root, bg="white")
frame_table.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

columns = ("Patient ID", "Name", "Age", "Gender", "Appointment Date", "Doctor")
tree = ttk.Treeview(frame_table, columns=columns, show="headings", height=15)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center")

tree.pack(fill=tk.BOTH, expand=True)

# ----------------- Run App -----------------
load_data()
root.mainloop()

# pip install customtkinter