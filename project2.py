from tkinter import *
from tkinter import ttk


class Task:
    PRIORITY_MAP = {"High": 3, "Medium": 2, "Low": 1}

    def __init__(self, description, priority):
        self.description = description
        self.priority = priority

    def get_priority_value(self):
        return Task.PRIORITY_MAP[self.priority]


class TreeNode:
    def __init__(self, task):
        self.task = task
        self.left = None
        self.right = None


class TaskManager:
    def __init__(self):
        self.root = None

    def insert(self, task):
        if not self.root:
            self.root = TreeNode(task)
        else:
            self._insert(self.root, task)

    def _insert(self, node, task):
        if task.get_priority_value() > node.task.get_priority_value():
            if node.left:
                self._insert(node.left, task)
            else:
                node.left = TreeNode(task)
        else:
            if node.right:
                self._insert(node.right, task)
            else:
                node.right = TreeNode(task)

    def delete(self, description):
        self.root = self._delete(self.root, description.lower())

    def _delete(self, node, description):
        if not node:
            return None
        node_description = node.task.description.lower()
        if description < node_description:
            node.left = self._delete(node.left, description)
        elif description > node_description:
            node.right = self._delete(node.right, description)
        else:
            if not node.left:
                return node.right
            elif not node.right:
                return node.left
            successor = self._find_min(node.right)
            node.task = successor.task
            node.right = self._delete(node.right, successor.task.description.lower())
        return node

    def _find_min(self, node):
        while node.left:
            node = node.left
        return node


class Node:
    def __init__(self, description, priority, state):
        self.description = description
        self.priority = priority
        self.state = state
        self.next = None

    def __repr__(self):
        return f"{self.description}, {self.priority}, {self.state}"


class HashTable:
    def __init__(self, size=10):
        self.size = size
        self.n_items = 0
        self.items = [None] * self.size
        self.base = 37

    def hash(self, description):
        index = 0
        description = description.strip().lower().replace(" ", "")
        for i, k in enumerate(description):
            index += ord(k) * self.base ** i
        return index % self.size

    def insert(self, description, priority, state):
        # Assign default values if the user didn't select priority/state
        if not priority or priority == "Select Priority":
            priority = "Low"
        if not state or state == "Select State":
            state = "Uncompleted"

        i = self.hash(description)
        new_node = Node(description, priority, state)

        if not self.items[i]:  # If the slot is empty, insert the new task
            self.items[i] = new_node
            return (f"Added successfully!\n"
                    f"Task: {description}\n"
                    f"Priority: {priority}\n"
                    f"State: {state}"), None, None
        else:
            curr = self.items[i]
            while curr:
                if curr.description.lower() == description.lower():
                    # Check if the task already exists with the same priority and state
                    if curr.priority == priority and curr.state == state:
                        return "The task already exists!", None, None

                    # If the priority or state is different, update the task
                    old_priority = curr.priority
                    old_state = curr.state
                    curr.priority = priority
                    curr.state = state
                    return (f"The task was successfully edited!\n"
                            f"Task: {description}\n"
                            f"New Priority: {priority}\n"
                            f"New State: {state}"), old_priority, old_state
                if not curr.next:
                    break
                curr = curr.next

            # If not found in the list, add the new task
            curr.next = new_node
            return (f"Added successfully!\n"
                    f"Task: {description}\n"
                    f"Priority: {priority}\n"
                    f"State: {state}"), None, None

    def delete(self, description):
        i = self.hash(description)
        curr = self.items[i]

        # Check if the first node is the one to delete
        if curr and curr.description.lower() == description.lower():
            self.items[i] = curr.next  # Remove the first node
            return

        # Traverse the list to find the node to delete
        while curr and curr.next:
            if curr.next.description.lower() == description.lower():
                curr.next = curr.next.next  # Correctly update the link to skip the deleted node
                return
            curr = curr.next

    def get(self, description):
        i = self.hash(description)
        curr = self.items[i]
        while curr:
            if curr.description.lower() == description.lower():
                return curr  # Return the Node object
            curr = curr.next
        return "Task not found!"  # Return a string when task doesn't exist

    def rehashing(self):
        old_list = self.items
        self.items = [None for _ in range(self.size * self.resize_factor)]  # Create a new list with increased size
        old_size = self.size  # Store the old size
        self.size *= self.resize_factor  # Update the size based on resize factor
        self.n_items = 0  # Reset item count

        for i in old_list:
            cur_node = i
            while cur_node is not None:
                des = cur_node.description  # Correct attribute name
                priority = cur_node.priority  # Correct attribute name
                state = cur_node.state
                self.insert(des, priority, state)  # Reinsert items
                cur_node = cur_node.next
class App(Tk):
    def __init__(self):
        super().__init__()
        self.geometry("570x690+400+0")
        self.resizable(False, False)
        self.title("SAS To-Do List")

        # Initialize the hash table and BST
        self.task_table = HashTable()
        self.task_tree = TaskManager()

        # Dummy images and variable initialization
        self.image_lbl = PhotoImage(file=r"background.png")
        self.var_enter_task = StringVar()
        self.image_add = PhotoImage(file=r"Add_button.png")
        self.image_search = PhotoImage(file=r"search_button~2.png")
        self.image_delete = PhotoImage(file=r"Delete_button.png")
        self.image_priority = PhotoImage(file=r"priority_button.png")
        self.image_show = PhotoImage(file=r"show_bt.png")

        # Create a label to display the image and place it in the main window
        lbl = Label(self, image=self.image_lbl)
        lbl.place(x=0, y=0, relwidth=1, relheight=1)

        # Create the entry widget
        self.ent_task = Entry(self, highlightthickness=3, highlightbackground="white", bd=0, relief="flat",
                              highlightcolor="white", font=("arial"), textvariable=self.var_enter_task)
        self.ent_task.place(x=100, y=317, width=165)

        # Create a placeholder label
        self.placeholder_lbl = Label(self, text="Enter a Task", bg="white", fg="grey", font=("arial"))
        self.placeholder_lbl.place(x=95, y=317, width=90)

        # Bind events to manage the placeholder
        self.ent_task.bind("<FocusIn>", self.hide_placeholder)
        self.ent_task.bind("<FocusOut>", self.show_placeholder)
        self.ent_task.bind("<KeyRelease>", self.check_placeholder)

        # Priority ComboBox with placeholder
        self.priority_var = StringVar()
        self.priority_combobox = ttk.Combobox(self, textvariable=self.priority_var, state="readonly")
        self.priority_combobox['values'] = ('High', 'Medium', 'Low')
        self.priority_combobox.place(x=100, y=350, width=165)
        self.priority_combobox.set("Select Priority")  # Placeholder text

        # State ComboBox with placeholder
        self.state_var = StringVar()
        self.state_combobox = ttk.Combobox(self, textvariable=self.state_var, state="readonly")
        self.state_combobox['values'] = ('Completed', 'Uncompleted')
        self.state_combobox.place(x=100, y=385, width=165)
        self.state_combobox.set("Select State")  # Placeholder text

        # Style the ComboBoxes
        self.style_combobox(self.priority_combobox)
        self.style_combobox(self.state_combobox)

        # Add button
        self.add_bt = Button(self, image=self.image_add, relief="flat", highlightthickness=3,
                             highlightbackground="white", bd=0, highlightcolor="white", command=self.add_task)
        self.add_bt.place(x=382, y=235, width=110, height=40)

        # Search button
        self.search_bt = Button(self, image=self.image_search, relief="flat", highlightthickness=3,
                                highlightbackground="white", bd=0, highlightcolor="white", command=self.search_task)
        self.search_bt.place(x=382, y=290, width=110, height=40)

        # Delete button
        self.delete_bt = Button(self, image=self.image_delete, relief="flat", highlightthickness=3,
                                highlightbackground="white", bd=0, highlightcolor="white", command=self.delete_task)
        self.delete_bt.place(x=382, y=345, width=110, height=40)

        # Priority button
        self.priority_bt = Button(self, image=self.image_priority, relief="flat", highlightthickness=3,
                                  highlightbackground="white", bd=0, highlightcolor="white",
                                  command=self.show_tasks_by_priority)
        self.priority_bt.place(x=382, y=520, width=110, height=40)
        # show button
        self.show_bt = Button(self, image=self.image_show, relief="flat", highlightthickness=3,
                                  highlightbackground="white", bd=0, highlightcolor="white",)
        self.show_bt.place(x=382, y=575, width=110, height=40)

    def hide_placeholder(self, event):
        self.placeholder_lbl.place_forget()

    def show_placeholder(self, event):
        if self.ent_task.get() == "":
            self.placeholder_lbl.place(x=95, y=317, width=90)

    def check_placeholder(self, event):
        if self.ent_task.get() == "":
            self.show_placeholder(event)

    def clear_placeholder(self, combobox, placeholder):
        if combobox.get() == placeholder:
            combobox.set('')

    def set_placeholder(self, combobox, placeholder):
        if not combobox.get():
            combobox.set(placeholder)

    def style_combobox(self, combobox):
        style = ttk.Style()
        style.configure('TCombobox',
                        bordercolor='blue',
                        borderwidth=2,
                        relief='solid',  # Solid border for better appearance
                        font=("Arial", 10))

    def add_task(self):
        task_description = self.ent_task.get()
        priority = self.priority_var.get() or "Low" # Get the selected priority
        state = self.state_var.get() or "Uncompleted"  # Default to Uncompleted if not selected

        # Ensure priority is valid, default to "Low" if not selected
        if priority == "Select Priority":
            priority = "Low"
        if task_description:
            # Add to HashTable
            message, old_priority, old_state = self.task_table.insert(task_description, priority, state)
            # Add to BST
            task = Task(task_description, priority)
            self.task_tree.insert(task)
            self.show_message(message)
            self.ent_task.delete(0, END)  # Clear the entry after adding
            self.show_placeholder(None)  # Reset placeholder visibility
            self.priority_combobox.set("Select Priority")  # Reset ComboBox
            self.state_combobox.set("Select State")  # Reset ComboBox
        else:
            self.show_message("Please enter a task.")

    def search_task(self):
        task_description = self.ent_task.get()
        if task_description:
            result = self.task_table.get(task_description)
            if isinstance(result, Node):  # If result is a Node, format the message
                message = (f"The searching result:\n"
                           f"Task: {result.description}\n"
                           f"Priority: {result.priority}\n"
                           f"State: {result.state}")
            else:  # If result is a string, it's "Task not found!"
                message = result
            self.show_message(message)
        else:
            self.show_message("Please enter a task to search.")

    def delete_task(self):
        task_description = self.ent_task.get()
        if task_description:
            # Delete from HashTable
            self.task_table.delete(task_description)
            # Delete from BST
            self.task_tree.delete(task_description)
            self.show_message(f"Task '{task_description}' deleted successfully!")
            self.ent_task.delete(0, END)  # Clear the entry after deleting
            self.show_placeholder(None)  # Reset placeholder visibility
            self.priority_combobox.set("Select Priority")  # Reset ComboBox
        else:
            self.show_message("Please enter a task to delete.")

    def show_tasks_by_priority(self):
        """Display tasks sorted by priority."""
        sorted_tasks = self._inorder_traversal(self.task_tree.root)
        if sorted_tasks:
            message = "Tasks sorted by priority (High to Low):\n"
            for task in sorted_tasks:
                message += f"Task: {task.description}, Priority: {task.priority}\n"
        else:
            message = "No tasks found!"
        self.show_message(message)

    def _inorder_traversal(self, node):
        """Helper method to perform inorder traversal of the BST."""
        tasks = []
        if node:
            tasks = self._inorder_traversal(node.left)
            tasks.append(node.task)
            tasks += self._inorder_traversal(node.right)
        return tasks

    def show_message(self, message):
        """Show a simple message box with a light blue background."""
        message_window = Toplevel(self)
        message_window.geometry("300x150")  # Set a fixed size for the message window
        message_window.title("Message")

        # Create a Text widget for multiline results
        text_area = Text(message_window, wrap=WORD, bg="#ADD8E6", fg="#40799f", font=("Arial", 14), bd=0)
        text_area.insert(END, message)  # Insert the message
        text_area.config(state=DISABLED)  # Disable editing
        text_area.pack(expand=True, fill=BOTH, padx=10, pady=(10, 0))  # Fill the window with padding

        # Add a button to close the message window
        button = Button(message_window, text="OK", command=message_window.destroy,
                        bg="#4CAF50", fg="white", font=("Arial", 10), relief="flat",
                        padx=10, pady=5)
        button.pack(pady=(10, 0))  # Pack the button with padding

        # Center the message window on the main window
        x = self.winfo_x() + (self.winfo_width() // 2) - (300 // 2)
        y = self.winfo_y() + (self.winfo_height() // 2) - (150 // 2)
        message_window.geometry(f"+{x}+{y}")  # Position the window


# Start the Tkinter main loop
my_app = App()
my_app.mainloop()