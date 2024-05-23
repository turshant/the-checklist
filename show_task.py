import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import mysql.connector

class ShowTasksForm:
    def __init__(self, master):
        self.master = master
        self.master.title("Show Tasks")
        self.master.geometry("2036x1264")

        self.canvas = tk.Canvas(self.master, width=2036, height=1264)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.background_image = Image.open('C:/Users/HP/Documents/task app/task manager.jpg')
        self.background_image = self.background_image.resize((2036, 1264), Image.Resampling.LANCZOS)
        self.background_photo = ImageTk.PhotoImage(self.background_image)

        self.canvas.create_image(0, 0, image=self.background_photo, anchor=tk.NW)

        self.tree = ttk.Treeview(self.master, columns=('ID', 'assigned_date','deadline', 'task', 'remarks', 're_email', 'send_pending_mail_flag','completed',), show='headings')
        self.tree.heading('ID', text='ID')
        self.tree.heading('assigned_date', text='assigned_date')
        self.tree.heading('deadline', text='deadline')
        self.tree.heading('task', text='Task')
        self.tree.heading('remarks', text='Remarks')
        self.tree.heading('re_email', text='Re Email')
        self.tree.heading('send_pending_mail_flag', text='Send Pending Mail Flag')
        self.tree.heading('completed', text='completed')
        self.tree.column('ID', width=50)
        self.tree.column('assigned_date',width=150 )
        self.tree.column('deadline',width=150 )
        self.tree.column('task', width=300)
        self.tree.column('remarks', width=150)
        self.tree.column('re_email', width=250)
        self.tree.column('send_pending_mail_flag', width=150)
        self.tree.column('completed', width=50)


        self.tree_window = self.canvas.create_window(50, 50, anchor=tk.NW, window=self.tree, width=1436, height=736)

        self.populate_tasks()

    def populate_tasks(self):
        tasks = self.fetch_tasks_from_database()

        if tasks:
            for task in tasks:
                self.tree.insert('', tk.END, values=task)
        else:
            messagebox.showinfo("No Tasks", "No tasks found.")

    def fetch_tasks_from_database(self):
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="python",
            auth_plugin="mysql_native_password",
        )

        mycursor = mydb.cursor()

        mycursor.execute("SELECT * FROM lists")
        tasks = mycursor.fetchall()
        return tasks

