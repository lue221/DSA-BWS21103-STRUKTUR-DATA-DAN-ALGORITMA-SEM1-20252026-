class Patient:
    def __init__(self, p_id, name, age,gender, allergies):
        self.p_id = p_id
        self.name = name
        self.age = age
        self.gender = gender
        self.allergies = allergies
        self.time_completed = "Pending"
class Node:
    def __init__(self, patient):
        self.patient = patient
        self.next = None