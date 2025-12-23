import csv
import datetime
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