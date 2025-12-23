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