from tkinter import *

# Create the main window
window = Tk()
window.geometry("570x690+400+0")
window.resizable(False, False)
window.title("SAS To-Do List")
window.config(bg="#c99dd9")
bt1=Button(window,text="hiiii")
bt1.place(x=10,y=100)

# Load the image
image_lbl = PhotoImage(file=r"background4.png")  # Ensure the image path is correct
var_enter_task=StringVar()
image_add = PhotoImage(file=r"")
# Create a label to display the image and place it in the main window
lbl = Label(window, image=image_lbl)
lbl.place(x=0, y=0, relwidth=1, relheight=1)  # Make the label fill the window
ent_task=Entry(window,highlightthickness=3,highlightbackground="white",bd=0,relief="flat",highlightcolor="white",font=("arial"),textvariable=var_enter_task)
ent_task.place(x=100,y=317,width=165)
placeholder_lbl=Label(window,text="Enter a Task",highlightthickness=3,highlightbackground="white",bg="white",bd=0,relief="flat",highlightcolor="white",fg="grey")
placeholder_lbl.place(x=95,y=313,width=90)
add_bt=Button(window,image=)

# Start the Tkinter main loop
window.mainloop()