import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import csv

class Patient:
    def __init__(self, p_id, name, age, gender, reason_of_visit):
        self.p_id = p_id
        self.name = name
        self.age = age
        self.gender = gender
        self.reason_of_visit = reason_of_visit
        self.time_completed = "Pending"


class Node:
    def __init__(self, patient):
        self.patient = patient
        self.next = None


class ClinicQueue:
    def __init__(self):
        self.front = None
        self.rear = None

    def enqueue(self, patient):
        new_node = Node(patient)
        if self.rear is None:
            self.front = self.rear = new_node
        else:
            self.rear.next = new_node
            self.rear = new_node

    def dequeue(self):
        if self.front is None: return None
        temp = self.front
        self.front = temp.next
        if self.front is None: self.rear = None
        return temp.patient

    def get_queue_as_list(self):
        data = []
        current = self.front
        pos = 1
        while current:
            data.append((pos, current.patient))
            current = current.next
            pos += 1
        return data


class LinkedListrecords:
    def __init__(self):
        self.head = None
        self.filename = "clinic_patient_history.csv"

    def new_history(self,patient):
        patient.time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        new_patient_node=Node(patient)
        if self.head is None:
            self.head=new_patient_node
        else:
            current=self.head
            while current.next:
                current= current.next
            current.next=new_patient_node
        self.save_record_csv()

    def save_record_csv(self):
        with open(self.filename, mode='w',newline='') as record:
            writer = csv.writer(record)
            writer.writerow(["ID", "Name", "Age",'Gender', "Reason_Of_Visit", "Time Completed"])
            current=self.head
            while current:
                p = current.patient
                writer.writerow([p.p_id,p.name,p.age,p.gender,p.reason_of_visit,p.time])
                current=current.next

    def load_from_csv(self):
        with open(self.filename, mode='r') as record:
            reader = csv.reader(record)
            next(reader, None)
            for row in reader:
                if row:
                    p = Patient(row[0], row[1], row[2], row[3],row[4])
                    p.time_completed = row[5]
                    new_node = Node(p)
                    if not self.head:
                        self.head = new_node
                    else:
                        current = self.head
                        while current.next: current = current.next
                        current.next = new_node



class ClinicApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Clinic System with Edit Function")
        self.root.geometry("1000x650")  # Made slightly wider to fit extra column

        self.queue = ClinicQueue()
        self.history = LinkedListrecords()

        register_frame = tk.LabelFrame(root, text="New Patient Registration", font=("Arial", 10, "bold"))
        register_frame.pack(fill="x", padx=10, pady=5)

        # ID
        tk.Label(register_frame, text="ID:").grid(row=0, column=0)
        self.ent_id = tk.Entry(register_frame, width=10)
        self.ent_id.grid(row=0, column=1)

        # Name
        tk.Label(register_frame, text="Name:").grid(row=0, column=2)
        self.ent_name = tk.Entry(register_frame, width=20)
        self.ent_name.grid(row=0, column=3)

        # Age
        tk.Label(register_frame, text="Age:").grid(row=0, column=4)
        self.ent_age = tk.Entry(register_frame, width=5)
        self.ent_age.grid(row=0, column=5)

        # Gender (Fixed: Unique Variable and Grid Position)
        tk.Label(register_frame, text="Gender:").grid(row=0, column=6)
        self.ent_gender = tk.Entry(register_frame, width=10)
        self.ent_gender.grid(row=0, column=7)

        tk.Label(register_frame, text="Reason_of_Visit:").grid(row=0, column=8)
        self.ent_all = tk.Entry(register_frame, width=15)
        self.ent_all.grid(row=0, column=9)

        btn_add = tk.Button(register_frame, text="Add to Queue", bg="#2196f3", fg="white", command=self.add_to_queue)
        btn_add.grid(row=0, column=10, padx=10)

        tk.Label(root, text="Current Waiting Queue", font=("Arial", 12, "bold"), fg="red").pack(pady=(10, 0))

        cols_q = ("Pos", "ID", "Name", "Age", "Gender", "RoV")

        self.tree_q = ttk.Treeview(root, columns=cols_q, show="headings", height=6)

        self.tree_q.heading("Pos", text="#")
        self.tree_q.heading("ID", text="ID")
        self.tree_q.heading("Name", text="Name")
        self.tree_q.heading("Age", text="Age")
        self.tree_q.heading("Gender", text="Gender")
        self.tree_q.heading("RoV", text="Reason_Of_Visit")

        self.tree_q.column("Pos", width=40)
        self.tree_q.column("ID", width=80)
        self.tree_q.column("Gender", width=80)

        self.tree_q.pack(fill="x", padx=10)

        q_btn_frame = tk.Frame(root)
        q_btn_frame.pack(pady=5)

        btn_call = tk.Button(q_btn_frame, text="Next Patient", bg="green", fg="white", width=20,
                             command=self.next_patient)
        btn_call.pack(side=tk.LEFT, padx=10)

    def add_to_queue(self):
        if not self.ent_name.get() or not self.ent_id.get():
            messagebox.showerror("Error", "ID and Name required")
            return

        p = Patient(
            self.ent_id.get(),
            self.ent_name.get(),
            self.ent_age.get(),
            self.ent_gender.get(),
            self.ent_all.get()
        )

        self.queue.enqueue(p)
        self.refresh_tables()

        self.ent_id.delete(0, tk.END)
        self.ent_name.delete(0, tk.END)
        self.ent_age.delete(0, tk.END)
        self.ent_gender.delete(0, tk.END)
        self.ent_all.delete(0, tk.END)

    def next_patient(self):
        popped = self.queue.dequeue()
        if popped:
            self.history.new_history(popped)
            messagebox.showinfo("Processed", f"Called {popped.name}. Moved to History.")
            self.refresh_tables()
        else:
            messagebox.showwarning("Empty", "Queue is empty.")

    def refresh_tables(self):
        for i in self.tree_q.get_children():
            self.tree_q.delete(i)

        for pos, p in self.queue.get_queue_as_list():
            self.tree_q.insert("", "end", values=(pos, p.p_id, p.name, p.age, p.gender, p.reason_of_visit))


if __name__ == "__main__":
    root = tk.Tk()
    app = ClinicApp(root)
    root.mainloop()



