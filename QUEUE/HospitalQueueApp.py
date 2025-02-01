import tkinter as tk
from tkinter import messagebox
import heapq  # To implement priority queue efficiently

# Priority Queue class to manage the patients
class PriorityQueue:
    def __init__(self):
        self._queue = []
        self._index = 0  # To handle equal priority cases

    def insert(self, patient_name, priority):
        # The patient name is stored with the priority and index for stable sorting
        heapq.heappush(self._queue, (-priority, self._index, patient_name))
        self._index += 1

    def pop(self):
        if self._queue:
            return heapq.heappop(self._queue)[-1]
        return None

    def peek(self):
        if self._queue:
            return self._queue[0][-1]
        return None

    def size(self):
        return len(self._queue)

    def display_queue(self):
        return [patient[-1] for patient in self._queue]

    def clear(self):
        self._queue.clear()

    def remove_by_name(self, name):
        # Remove a patient by name
        for i, patient in enumerate(self._queue):
            if patient[-1] == name:
                del self._queue[i]
                heapq.heapify(self._queue)
                return True
        return False

    def update_priority(self, name, new_priority):
        # Update the priority of a patient by name
        for i, patient in enumerate(self._queue):
            if patient[-1] == name:
                self._queue[i] = (-new_priority, self._index, name)
                heapq.heapify(self._queue)
                self._index += 1
                return True
        return False

    def is_empty(self):
        return len(self._queue) == 0

# Application class to manage the GUI
class HospitalQueueApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hospital Priority Queue")
        self.root.geometry("500x600")  
        
        # Initialize the Priority Queue
        self.queue = PriorityQueue()

        # Define UI elements 
        self.patient_name_label = tk.Label(root, text="Patient Name:", font=("Arial", 16))
        self.patient_name_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.patient_name_entry = tk.Entry(root, font=("Arial", 16))
        self.patient_name_entry.grid(row=0, column=1, padx=10, pady=10)

        self.priority_label = tk.Label(root, text="Priority (1-10):", font=("Arial", 16))
        self.priority_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.priority_entry = tk.Entry(root, font=("Arial", 16))
        self.priority_entry.grid(row=1, column=1, padx=10, pady=10)

        self.add_button = tk.Button(root, text="Add to Queue", command=self.add_patient, font=("Arial", 16))
        self.add_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        self.remove_button = tk.Button(root, text="Remove by Name", command=self.remove_patient, font=("Arial", 16))
        self.remove_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        self.update_button = tk.Button(root, text="Update Priority", command=self.update_priority, font=("Arial", 16))
        self.update_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        self.view_button = tk.Button(root, text="View Queue", command=self.view_queue, font=("Arial", 16))
        self.view_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

        self.pop_button = tk.Button(root, text="Serve Next", command=self.serve_patient, font=("Arial", 16))
        self.pop_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

        self.clear_button = tk.Button(root, text="Clear Queue", command=self.clear_queue, font=("Arial", 16))
        self.clear_button.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

        self.peek_button = tk.Button(root, text="Check Next Patient", command=self.check_next_patient, font=("Arial", 16))
        self.peek_button.grid(row=8, column=0, columnspan=2, padx=10, pady=10)

        self.queue_listbox = tk.Listbox(root, height=10, width=40, font=("Arial", 16))
        self.queue_listbox.grid(row=9, column=0, columnspan=2, padx=10, pady=10)

        self.status_label = tk.Label(root, text="Queue Size: 0", font=("Arial", 16))
        self.status_label.grid(row=10, column=0, columnspan=2, padx=10, pady=10)

        # Centering the UI elements in the window
        self.center_ui_elements()

    def center_ui_elements(self):
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

    def add_patient(self):
        name = self.patient_name_entry.get()
        priority = self.priority_entry.get()

        if not name or not priority:
            messagebox.showerror("Input Error", "Please provide both patient name and priority.")
            return

        try:
            priority = int(priority)
            if priority < 1 or priority > 10:
                messagebox.showerror("Priority Error", "Priority must be between 1 and 10.")
                return
        except ValueError:
            messagebox.showerror("Priority Error", "Priority must be an integer.")
            return

        self.queue.insert(name, priority)
        messagebox.showinfo("Success", f"Patient '{name}' added with priority {priority}.")
        self.patient_name_entry.delete(0, tk.END)
        self.priority_entry.delete(0, tk.END)
        self.update_queue_info()

    def remove_patient(self):
        name = self.patient_name_entry.get()
        if not name:
            messagebox.showerror("Input Error", "Please provide a patient name to remove.")
            return

        if self.queue.remove_by_name(name):
            messagebox.showinfo("Success", f"Patient '{name}' removed from the queue.")
        else:
            messagebox.showerror("Error", f"Patient '{name}' not found in the queue.")
        self.update_queue_info()

    def update_priority(self):
        name = self.patient_name_entry.get()
        priority = self.priority_entry.get()

        if not name or not priority:
            messagebox.showerror("Input Error", "Please provide both patient name and new priority.")
            return

        try:
            priority = int(priority)
            if priority < 1 or priority > 10:
                messagebox.showerror("Priority Error", "Priority must be between 1 and 10.")
                return
        except ValueError:
            messagebox.showerror("Priority Error", "Priority must be an integer.")
            return

        if self.queue.update_priority(name, priority):
            messagebox.showinfo("Success", f"Patient '{name}' priority updated to {priority}.")
        else:
            messagebox.showerror("Error", f"Patient '{name}' not found in the queue.")
        self.update_queue_info()

    def view_queue(self):
        self.queue_listbox.delete(0, tk.END)
        queue_display = self.queue.display_queue()
        if not queue_display:
            self.queue_listbox.insert(tk.END, "No patients in the queue.")
        else:
            for patient in queue_display:
                self.queue_listbox.insert(tk.END, patient)

    def serve_patient(self):
        patient = self.queue.pop()
        if patient:
            messagebox.showinfo("Next Patient", f"Serving next patient: {patient}.")
        else:
            messagebox.showinfo("Queue Empty", "No patients in the queue.")
        self.update_queue_info()

    def clear_queue(self):
        self.queue.clear()
        messagebox.showinfo("Success", "All patients have been removed from the queue.")
        self.update_queue_info()

    def check_next_patient(self):
        patient = self.queue.peek()
        if patient:
            messagebox.showinfo("Next Patient", f"Next patient: {patient}.")
        else:
            messagebox.showinfo("Queue Empty", "No patients in the queue.")

    def update_queue_info(self):
        self.status_label.config(text=f"Queue Size: {self.queue.size()}")

# Create the Tkinter root window
root = tk.Tk()
app = HospitalQueueApp(root)
root.mainloop()
