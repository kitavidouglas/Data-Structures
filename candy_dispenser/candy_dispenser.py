import tkinter as tk
from tkinter import PhotoImage
import random

class CandyDispenser:
    def __init__(self, root):
        self.stack = []  # Stack to hold candies
        self.max_size = 10  # Maximum stack size
        self.candy_height = 50  # Height of each candy
        self.container_height = 550  # Height of the container
        self.container_width = 300  # Width of the container
        self.spring_tags = []  # Tags for spring elements
        self.spring_bottom = self.container_height  # Bottom position of the spring
        self.spring_left = 60  # Left boundary of the spring
        self.spring_right = self.container_width - 60  # Right boundary of the spring

        # List of candy image file paths
        self.candy_images = [
            "assets/candy1.png", 
            "assets/candy2.png", 
            "assets/candy3.png", 
            "assets/candy4.png", 
        ]
        self.images = [self.load_image(image) for image in self.candy_images]  # Load and scale images

        # GUI Setup
        self.root = root
        self.root.title("Candy Dispenser")

        # Canvas for drawing
        self.canvas = tk.Canvas(
            root, width=self.container_width, height=self.container_height, bg="white", highlightthickness=0
        )
        self.canvas.pack(pady=20)

        # Draw container
        self.container = self.canvas.create_rectangle(
            40, 10, self.container_width - 40, self.container_height, outline="pink", width=5
        )

        # Status label
        self.status_label = tk.Label(root, text="", font=("Arial", 14))
        self.status_label.pack(pady=10)

        # Button frame
        button_frame = tk.Frame(root)
        button_frame.pack()

        tk.Button(button_frame, text="Push", command=self.push_candy, width=10).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(button_frame, text="Pop", command=self.pop_candy, width=10).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(button_frame, text="Is Empty?", command=self.check_is_empty, width=10).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(button_frame, text="Length", command=self.check_length, width=10).grid(row=1, column=1, padx=5, pady=5)
        tk.Button(button_frame, text="Top", command=self.check_top, width=10).grid(row=2, column=0, padx=5, pady=5)

        # Initial refresh
        self.refresh_spring()

    def load_image(self, image_path):
        """Loading image and resizing it"""
        image = PhotoImage(file=image_path)
        # Resizing the image to match the candy height
        width = int(image.width() * self.candy_height / image.height())
        image = image.subsample(int(image.width() / width), int(image.height() / self.candy_height))
        return image

    def refresh_spring(self):
        """Refreshing the spring."""
        y_init = self.spring_bottom
        squeeze = 40 - (len(self.stack) * 4.2)  # Adjust compression based on stack size

        # Clear previous spring visuals
        for tag in self.spring_tags:
            self.canvas.delete(tag)
        self.spring_tags.clear()

        # Draw the spring's zigzag lines
        for i in range(6):
            if i % 2 == 0:
                self.spring_tags.append(self.canvas.create_line(
                    self.spring_left, y_init, self.spring_right, y_init - squeeze, fill="black", width=3
                ))
            else:
                self.spring_tags.append(self.canvas.create_line(
                    self.spring_right, y_init, self.spring_left, y_init - squeeze, fill="black", width=3
                ))
            y_init -= squeeze

        # Draw the top line of the spring
        self.spring_tags.append(self.canvas.create_line(
            self.spring_left, y_init, self.spring_right, y_init, fill="black", width=3
        ))

    def render_stack(self):
        """Render the stack of candies on the canvas."""
        self.canvas.delete("candy")  # Clear existing candies

        # Calculate the topmost position based on spring compression
        y_top_of_spring = self.spring_bottom - (40 - len(self.stack) * 4.2) * 6
        for index, value in enumerate(self.stack):
            image = random.choice(self.images)  # Choose a random image for each candy
            x1, y1 = 60, y_top_of_spring - (index + 1) * self.candy_height
            x2, y2 = self.container_width - 60, y_top_of_spring - index * self.candy_height

            # Place the image on the canvas
            self.canvas.create_image(
                (x1 + x2) // 2, (y1 + y2) // 2, image=image, tags="candy"
            )

            self.canvas.create_text(
                (x1 + x2) // 2, (y1 + y2) // 2, text=str(value), font=("Arial", 14), fill="white", tags="candy"
            )

    def push_candy(self):
        """Push a candy onto the stack."""
        if len(self.stack) < self.max_size:
            value = len(self.stack) + 1
            self.stack.append(value)
            self.refresh_spring()
            self.render_stack()
            self.update_status(f"Pushed: {value}")
        else:
            self.update_status("Stack is full!")

    def pop_candy(self):
        """Pop a candy from the stack with animation."""
        if self.stack:
            value = self.stack.pop()
            self.refresh_spring()
            self.animate_pop(value)
        else:
            self.update_status("Stack is empty!")

    def animate_pop(self, value):
        """Animating the popping of a candy."""
        top_candy = self.canvas.find_withtag("candy")[-1]
        for _ in range(10):
            self.canvas.move(top_candy, 0, -5)  # Move the candy upwards
            self.root.update()
            self.root.after(20)
        self.canvas.delete(top_candy)
        self.render_stack()
        self.update_status(f"Popped: {value}")

    def check_is_empty(self):
        """Check if the stack is empty."""
        self.update_status(f"Is Empty: {'Yes' if not self.stack else 'No'}")

    def check_length(self):
        """Check the length of the stack."""
        self.update_status(f"Length: {len(self.stack)}")

    def check_top(self):
        """Check the top element of the stack."""
        if self.stack:
            self.update_status(f"Top: {self.stack[-1]}")
        else:
            self.update_status("Top: None")

    def update_status(self, message):
        """Update the status label."""
        self.status_label.config(text=message)


# Main program
if __name__ == "__main__":
    root = tk.Tk()
    app = CandyDispenser(root)
    root.mainloop()
