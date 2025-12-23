# TOP OF MAIN.PY

# 1. Import Queue from queue.py
from queue import ClinicQueue 

# 2. Import LinkedList from the renamed file (linked_list.py)
# You might need to open linked_list.py to check if the class is named 
from linked_list import LinkedListrecords, Patient 

import os
from your_module_name import Patient, ClinicQueue, LinkedListrecords 
# NOTE: Replace 'your_module_name' with the name of the file where your friends' code is saved!

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    queue_system = ClinicQueue()
    history_system = LinkedListrecords()
    
    # Load previous history if it exists
    try:
        history_system.load_from_csv()
    except FileNotFoundError:
        print("No previous history found. Starting fresh.")

    while True:
        clear_screen()
        print("====================================")
        print("   CLINIC MANAGEMENT SYSTEM v1.0    ")
        print("====================================")
        print("1. Register New Patient (Enqueue)")
        print("2. Call Next Patient (Dequeue)")
        print("3. View Current Queue")
        print("4. View Patient History")
        print("5. Exit")
        print("====================================")
        
        choice = input("Enter option (1-5): ")

        if choice == '1':
            print("\n--- NEW PATIENT REGISTRATION ---")
            p_id = input("ID: ")
            name = input("Name: ")
            age = input("Age: ")
            gender = input("Gender: ")
            reason = input("Reason for Visit: ")
            
            # Create object and add to queue
            new_p = Patient(p_id, name, age, gender, reason)
            queue_system.enqueue(new_p)
            print("Patient added to queue successfully!")
            input("\nPress Enter to continue...")

        elif choice == '2':
            print("\n--- CALLING NEXT PATIENT ---")
            served_patient = queue_system.dequeue()
            
            if served_patient:
                print(f"Now serving: {served_patient.name} ({served_patient.p_id})")
                print("Consultation completed.")
                
                # Move to history
                history_system.new_history(served_patient)
                print("Record saved to history.")
            else:
                print("Queue is empty! No patients to serve.")
            input("\nPress Enter to continue...")

        elif choice == '3':
            print("\n--- CURRENT WAITING ROOM ---")
            current_queue = queue_system.get_queue_as_list()
            if not current_queue:
                print("The waiting room is empty.")
            else:
                print(f"{'No.':<5} {'Name':<20} {'Reason':<20}")
                print("-" * 45)
                for pos, patient in current_queue:
                    print(f"{pos:<5} {patient.name:<20} {patient.reason_of_visit:<20}")
            input("\nPress Enter to continue...")

        elif choice == '4':
            # Note: You might need to add a 'display' function to LinkedListrecords 
            # for this to work perfectly, or just open the CSV file here.
            print("\n--- PATIENT HISTORY (Saved in CSV) ---")
            print(f"History saved to {history_system.filename}")
            input("\nPress Enter to continue...")

        elif choice == '5':
            print("Exiting system. Goodbye!")
            break
        
        else:
            print("Invalid selection. Please try again.")
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
