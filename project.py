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
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            else:
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


class LinkedList:
    def __init__(self):
        self.head = None

    def insert(self, description, priority, state):
        new_node = Node(description, priority, state)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

    def delete(self, description):
        current = self.head
        prev = None
        while current:
            if current.description.lower() == description.lower():
                if prev:
                    prev.next = current.next
                else:
                    self.head = current.next
                return
            prev = current
            current = current.next

    def get_all_tasks(self):
        tasks = []
        current = self.head
        while current:
            tasks.append(current)
            current = current.next
        return tasks


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
        if not priority or priority == "Select Priority":
            priority = "Low"
        if not state or state == "Select State":
            state = "Uncompleted"

        i = self.hash(description)
        new_node = Node(description, priority, state)

        if not self.items[i]:
            self.items[i] = new_node
            return (f"Added successfully!\n"
                    f"Task: {description}\n"
                    f"Priority: {priority}\n"
                    f"State: {state}"), None, None
        else:
            curr = self.items[i]
            while curr:
                if curr.description.lower() == description.lower():
                    if curr.priority == priority and curr.state == state:
                        return "The task already exists!", None, None
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

            curr.next = new_node
            return (f"Added successfully!\n"
                    f"Task: {description}\n"
                    f"Priority: {priority}\n"
                    f"State: {state}"), None, None

    def delete(self, description):
        i = self.hash(description)
        curr = self.items[i]

        if curr and curr.description.lower() == description.lower():
            self.items[i] = curr.next
            return

        while curr and curr.next:
            if curr.next.description.lower() == description.lower():
                curr.next = curr.next.next
                return
            curr = curr.next

    def get(self, description):
        i = self.hash(description)
        curr = self.items[i]
        while curr:
            if curr.description.lower() == description.lower():
                return curr
            curr = curr.next
        return "Task not found!"


class App(Tk):
    def __init__(self):
        super().__init__()
        self.geometry("570x690+400+0")
        self.resizable(False, False)
        self.title("SAS To-Do List")

        self.task_table = HashTable()
        self.task_tree = TaskManager()
        self.linked_list = LinkedList()

        self.image_lbl = PhotoImage(file=r"background.png")
        self.var_enter_task = StringVar()
        self.image_add = PhotoImage(file=r"Add_button.png")
        self.image_search = PhotoImage(file=r"search_button~2.png")
        self.image_delete = PhotoImage(file=r"Delete_button.png")
        self.image_priority = PhotoImage(file=r"priority_button.png")
        self.image_show = PhotoImage(file=r"show_bt.png")

        lbl = Label(self, image=self.image_lbl)
        lbl.place(x=0, y=0, relwidth=1, relheight=1)

        label_task = Label(self, text="Enter your task:", font=("Arial", 12), bg="white")
        label_task.place(x=100, y=340)

        self.ent_task = Entry(self, highlightthickness=3, highlightbackground="white", bd=0, relief="flat",
                              highlightcolor="white", font=("arial"), textvariable=self.var_enter_task)
        self.ent_task.place(x=100, y=374, width=163)

        self.priority_var = StringVar()
        self.priority_combobox = ttk.Combobox(self, textvariable=self.priority_var, state="readonly")
        self.priority_combobox['values'] = ('High', 'Medium', 'Low')
        self.priority_combobox.place(x=100, y=420, width=165)
        self.priority_combobox.set("Select Priority")

        self.state_var = StringVar()
        self.state_combobox = ttk.Combobox(self, textvariable=self.state_var, state="readonly")
        self.state_combobox['values'] = ('Completed', 'Uncompleted')
        self.state_combobox.place(x=100, y=460, width=165)
        self.state_combobox.set("Select State")

        self.style_combobox(self.priority_combobox)
        self.style_combobox(self.state_combobox)

        self.add_bt = Button(self, image=self.image_add, relief="flat", highlightthickness=3,
                             highlightbackground="white", bd=0, highlightcolor="white", command=self.add_task)
        self.add_bt.place(x=382, y=235, width=110, height=40)

        self.search_bt = Button(self, image=self.image_search, relief="flat", highlightthickness=3,
                                highlightbackground="white", bd=0, highlightcolor="white", command=self.search_task)
        self.search_bt.place(x=382, y=290, width=110, height=40)

        self.delete_bt = Button(self, image=self.image_delete, relief="flat", highlightthickness=3,
                                highlightbackground="white", bd=0, highlightcolor="white", command=self.delete_task)
        self.delete_bt.place(x=382, y=345, width=110, height=40)

        self.priority_bt = Button(self, image=self.image_priority, relief="flat", highlightthickness=3,
                                  highlightbackground="white", bd=0, highlightcolor="white",
                                  command=self.show_tasks_by_priority)
        self.priority_bt.place(x=382, y=520, width=110, height=40)

        self.show_bt = Button(self, image=self.image_show, relief="flat", highlightthickness=3,
                              highlightbackground="white", bd=0, highlightcolor="white", command=self.show_tasks)
        self.show_bt.place(x=382, y=575, width=110, height=40)

    def style_combobox(self, combobox):
        style = ttk.Style()
        style.configure('TCombobox',
                        bordercolor='blue',
                        borderwidth=2,
                        relief='solid',
                        font=("Arial", 10))

    def add_task(self):
        task_description = self.ent_task.get()
        priority = self.priority_var.get() or "Low"
        state = self.state_var.get() or "Uncompleted"

        if priority == "Select Priority":
            priority = "Low"

        if task_description:
            existing_task_node = self.task_table.get(task_description)

            if isinstance(existing_task_node, Node):

                existing_task_node.priority = priority
                existing_task_node.state = state

                curr = self.task_table.items[self.task_table.hash(task_description)]
                while curr:
                    if curr.description.lower() == task_description.lower():
                        curr.priority = priority
                        curr.state = state
                        break
                    curr = curr.next

                message = (f"The task was successfully edited!\n"
                           f"Task: {task_description}\n"
                           f"New Priority: {priority}\n"
                           f"New State: {state}")
            else:
                # Add new task
                message, old_priority, old_state = self.task_table.insert(task_description, priority, state)
                self.task_tree.insert(Task(task_description, priority))
                self.linked_list.insert(task_description, priority, state)  # Default to "Uncompleted"

            self.show_message(message)
            self.ent_task.delete(0, END)
            self.priority_combobox.set("Select Priority")
            self.state_combobox.set("Select State")
        else:
            self.show_message("Please enter a task.")

    def search_task(self):
        task_description = self.ent_task.get()
        if task_description:
            result = self.task_table.get(task_description)
            if isinstance(result, Node):
                message = (f"The searching result:\n"
                           f"Task: {result.description}\n"
                           f"Priority: {result.priority}\n"
                           f"State: {result.state}")
            else:
                message = result
            self.show_message(message)
        else:
            self.show_message("Please enter a task to search.")

    def delete_task(self):
        task_description = self.ent_task.get()
        if task_description:
            task_node = self.task_table.get(task_description)
            if isinstance(task_node, Node):
                self.task_table.delete(task_description)
                self.task_tree.delete(task_description)
                self.linked_list.delete(task_description)
                self.show_message(f"Task '{task_description}' deleted successfully!")
            else:
                self.show_message(f"Task '{task_description}' not found!")
            self.ent_task.delete(0, END)
            self.priority_combobox.set("Select Priority")
        else:
            self.show_message("Please enter a task to delete.")

    def show_tasks(self):
        tasks = self.linked_list.get_all_tasks()
        if tasks:
            tasks_message = "Tasks:\n"
            for task in tasks:
                tasks_message += f"Task: {task.description}\n"
            self.show_message1(tasks_message)
        else:
            self.show_message1("No tasks found!")

    def show_tasks_by_priority(self):
        sorted_tasks = self._inorder_traversal(self.task_tree.root)
        if sorted_tasks:
            message = "Tasks sorted by priority (High to Low):\n"
            for task in sorted_tasks:
                task_node = self.task_table.get(task.description)
                if isinstance(task_node, Node):
                    message += f"Task: {task.description}, Priority: {task.priority}\n"
            if message == "Tasks sorted by priority (High to Low):\n":
                message = "No tasks found!"
        else:
            message = "No tasks found!"
        self.show_message1(message)

    def _inorder_traversal(self, node):
        tasks = []
        if node:
            tasks = self._inorder_traversal(node.left)
            tasks.append(node.task)
            tasks += self._inorder_traversal(node.right)
        return tasks

    def show_message(self, message):
        message_window = Toplevel(self)
        message_window.geometry("300x220")
        message_window.title("Message")
        message_window.resizable(False, False)

        text_area = Text(message_window, wrap=WORD, bg="#ADD8E6", fg="#40799f", font=("Arial", 14), bd=0, height=9,
                         width=25)
        text_area.insert(END, message)
        text_area.config(state=DISABLED)
        text_area.place(x=10, y=9)

        button = Button(message_window, text="OK", command=message_window.destroy,
                        bg="#4CAF50", fg="white", font=("Arial", 10), relief="flat",
                        padx=10, pady=5)
        button.place(x=125, y=160)

        x = self.winfo_x() + (self.winfo_width() // 2) - (300 // 2)
        y = self.winfo_y() + (self.winfo_height() // 2) - (150 // 2)
        message_window.geometry(f"+{x}+{y}")

    def show_message1(self, message):

        message_window = Toplevel(self)
        message_window.geometry("300x220")
        message_window.title("Message")
        message_window.resizable(False, False)
        message_window.iconbitmap('photo_icon/todo.ico')

        text_area = Text(message_window, wrap=WORD, bg="#ADD8E6", fg="#40799f", font=("Arial", 14), bd=0, height=9,
                         width=25)
        text_area.insert(END, message)
        scrollbar = Scrollbar(message_window, command=text_area.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        text_area.config(state=DISABLED, yscrollcommand=scrollbar.set)
        text_area.place(x=10, y=9)

        x = self.winfo_x() + (self.winfo_width() // 2) - (300 // 2)
        y = self.winfo_y() + (self.winfo_height() // 2) - (150 // 2)
        message_window.geometry(f"+{x}+{y}")


my_app = App()
my_app.mainloop()