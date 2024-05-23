import tkinter as tk
import datetime
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox, ttk
from tkcalendar import Calendar
import mysql.connector
from datetime import date
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar
import mysql.connector
from PIL import Image, ImageTk
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart



class Thechecklist():
    

    def __init__(self, master):
        self.master = master
       
        self.master.title("The checklist conquer")
        self.master.geometry("2036x1264")

        
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()

        background_image = Image.open('C:/Users/HP/Documents/task app/the check list.jpg')
        background_image = background_image.resize((screen_width, screen_height))
        background_photo = ImageTk.PhotoImage(background_image)

        self.label_background = tk.Label(master, image=background_photo)
        self.label_background.image = background_photo
        self.label_background.place(x=0, y=0, relwidth=1, relheight=1)

        self.calendar_frame = tk.Frame(self.master)
        self.calendar_frame.grid(row=0, column=0, padx=10, pady=10)

        self.add_form_frame = tk.Frame(self.master)
        self.add_form_frame.grid(row=0, column=1, padx=10, pady=10)

        self.todo_frame = tk.Frame(self.master)
        self.todo_frame.grid(row=1, columnspan=2, padx=10, pady=10)

        self.calendar_label = tk.Label(self.calendar_frame, text="Select date:")
        self.calendar_label.pack(pady=10)
        self.calendar = Calendar(self.calendar_frame, selectmode='day', date_pattern='yyyy-MM-dd')
        self.calendar.pack(padx=10, pady=10)
        self.calendar.bind("<<CalendarSelected>>", self.display_todos)

        self.task_label = tk.Label(self.add_form_frame, text="Task:")
        self.task_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.task_entry = tk.Entry(self.add_form_frame)
        self.task_entry.grid(row=0, column=1, padx=5, pady=5)

        self.remarks_label = tk.Label(self.add_form_frame, text="Remarks:")
        self.remarks_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.remarks_entry = tk.Entry(self.add_form_frame)
        self.remarks_entry.grid(row=1, column=1, padx=5, pady=5)
        
        intialvalu="no"
        self.completed = tk.Label(self.add_form_frame, text="completed")
        self.completed.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.completed_entry = tk.Entry(self.add_form_frame)
        self.completed_entry.insert(0, intialvalu)
        self.completed_entry.configure(state='readonly', disabledbackground='white', disabledforeground='gray')
        self.completed_entry.grid(row=2, column=1, padx=5, pady=5)

        self.re_email = tk.Label(self.add_form_frame, text="re_email:")
        self.re_email.grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.re_email_entry = tk.Entry(self.add_form_frame)
        self.re_email_entry.grid(row=3, column=1, padx=5, pady=5)
        

        self.add_button = tk.Button(self.add_form_frame, text="Add Task", command=self.add_todo)
        self.add_button.grid(row=4, columnspan=2, padx=5, pady=5)

        self.todo_table = ttk.Treeview(self.todo_frame, columns=("ID", "SLNO", "Task", "Remarks","re_email","completed"), show="headings")
        self.todo_table.heading("ID", text="ID", anchor='w')
        self.todo_table.heading("SLNO", text="SL NO")
        self.todo_table.heading("Task", text="Task")
        self.todo_table.heading("Remarks", text="Remarks")
        self.todo_table.heading("re_email", text="re_email")
        self.todo_table.heading("completed", text="completed")
        self.todo_table.column("ID", width=0, stretch=tk.NO)  # Hide the ID column
        self.todo_table.pack(pady=10)
        self.todo_table.bind("<Button-3>", self.on_right_click)
        self.todo_table.bind("<ButtonRelease-1>", self.display_selected_todo)

        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="python",
            auth_plugin='mysql_native_password'
        )
        self.cursor = self.db.cursor()

        # Email configuration
        self.email_sender = 'turshantkalia88@gmail.com'
        self.email_password = 'otvn fvrz qphb ghkx'

    def add_todo(self):
        selected_date = self.calendar.get_date()
        task = self.task_entry.get()
        remarks = self.remarks_entry.get()
        re_email = self.re_email_entry.get()
        completed=self.completed_entry.get()
        assigned_date = date.today()
        if task:
            sql = "INSERT INTO lists (deadline, task, remarks, re_email,completed, assigned_date) VALUES (%s, %s, %s,%s,%s,%s)"
            values = (selected_date, task, remarks, re_email,completed, assigned_date)
            self.cursor.execute(sql, values)
            self.db.commit()
            self.task_entry.delete(0, tk.END)
            self.remarks_entry.delete(0, tk.END)
            self.send_email_notification(task, selected_date)
            self.display_todos(event=None) 
            messagebox.showinfo("task Added", f"Todo '{task}' added on {selected_date}")

        else:
            messagebox.showwarning("Incomplete Todo", "Please enter task.")

    def send_email_notification(self, task, selected_date):
        receiver_email =self.re_email_entry.get()
        subject = 'New Task Added'
        body = f"New task '{task}' has been added on {selected_date}."
        message = MIMEMultipart()
        message['From'] = self.email_sender
        message['To'] = receiver_email
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))
        

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(self.email_sender, self.email_password)
            text = message.as_string()
            server.sendmail(self.email_sender, receiver_email, text)
            server.quit()
        except Exception as e:
            messagebox.showerror("Email Error", f"An error occurred while sending email: {str(e)}")
            

    def display_todos(self, event):
        selected_date = self.calendar.get_date()
        sql = "SELECT id, task, remarks,re_email,completed FROM lists WHERE deadline = %s"
        values = (selected_date,)
        self.cursor.execute(sql, values,)
        todos = self.cursor.fetchall()

        self.todo_table.delete(*self.todo_table.get_children())

        if todos:
            for i, todo in enumerate(todos, start=1):
                self.todo_table.insert("", "end", values=(todo[0], i,) + todo[1:])

    def on_right_click(self, event):
        item = self.todo_table.identify_row(event.y)
        if item:
            self.todo_table.focus(item)
            self.todo_table.selection_set(item)
            self.todo_table.bind("<ButtonRelease-3>", self.delete_todo)

    def delete_todo(self, event):
        item = self.todo_table.selection()
        if item:
            confirmation = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this task?")
            if confirmation:
                todo_id = self.todo_table.item(item, "values")[0]  
                sql = "DELETE FROM lists WHERE id = %s"
                values = (todo_id,)
                self.cursor.execute(sql, values)
                self.db.commit()
                messagebox.showinfo("Task Deleted", "Task deleted successfully")
                self.display_todos(event=None) 

    def display_selected_todo(self, event):
        if event.num == 3: 
            item = self.todo_table.selection()
            if item:
                selected_date, task, remarks = self.todo_table.item(item, "values")[2:]
                self.display_task_value.config(text=task)
                self.display_remarks_value.config(text=remarks)
                
    










