import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import mysql.connector

class DeleteTaskForm:
    def __init__(self, master):
        self.master = master
        self.master.title("Delete Tasks")
        self.master.geometry("2036x1264")

        self.canvas = tk.Canvas(self.master, width=2036, height=1264)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.background_image = Image.open('C:/Users/HP/Documents/task app/task manager.jpg')
        self.background_image = self.background_image.resize((2036, 1264), Image.Resampling.LANCZOS)
        self.background_photo = ImageTk.PhotoImage(self.background_image)

        self.canvas.create_image(0, 0, image=self.background_photo, anchor=tk.NW)

        self.tree = ttk.Treeview(self.master, columns=('ID', 'assigned_date','deadline', 'task', 'remarks', 're_email', 'send_pending_mail_flag'), show='headings', selectmode='extended')
        self.tree.heading('ID', text='ID')
        self.tree.heading('assigned_date', text='assigned_date')
        self.tree.heading('deadline', text='deadline')
        self.tree.heading('task', text='Task')
        self.tree.heading('remarks', text='Remarks')
        self.tree.heading('re_email', text='Re_Email')
        self.tree.heading('send_pending_mail_flag', text='Send Pending Mail Flag')
        self.tree.column('ID', width=50)
        self.tree.column('assigned_date',width=150 )
        self.tree.column('deadline',width=150 )
        self.tree.column('task', width=150)
        self.tree.column('remarks', width=100)
        self.tree.column('re_email', width=150)
        self.tree.column('send_pending_mail_flag', width=150)

        self.tree_window = self.canvas.create_window(50, 50, anchor=tk.NW, window=self.tree, width=1434, height=736)
        self.scrollbar = ttk.Scrollbar(self.master, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.place(x=1484, y=50, height=736)

        self.populate_delete_tasks()

        self.context_menu = tk.Menu(self.master, tearoff=0)
        self.context_menu.add_command(label="Delete Task(s)", command=self.on_delete_task)

        self.tree.bind('<Button-3>', self.show_context_menu)

    def populate_delete_tasks(self):
        delete_tasks = self.fetch_delete_tasks_from_database()

        if delete_tasks:
            for task in delete_tasks:
                self.tree.insert('', tk.END, values=task)
        else:
            messagebox.showinfo("No delete Tasks", "No delete tasks found.")

    def fetch_delete_tasks_from_database(self):
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="python",
            auth_plugin="mysql_native_password",
        )

        mycursor = mydb.cursor()

        mycursor.execute("SELECT * FROM lists")
        delete_tasks = mycursor.fetchall()
        return delete_tasks

    def show_context_menu(self, event):
        selected_items = self.tree.selection()
        if selected_items:
            self.context_menu.post(event.x_root, event.y_root)

    def on_delete_task(self):
        selected_items = self.tree.selection()
        if not selected_items:
            return

        task_ids = [self.tree.item(item, "values")[0] for item in selected_items]
        if messagebox.askyesno("Delete Task", "Are you sure you want to delete the selected task(s)?"):
            self.delete_tasks(task_ids)
            self.refresh_task_list()

    def delete_tasks(self, task_ids):
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="python",
            auth_plugin="mysql_native_password",
        )

        mycursor = mydb.cursor()

        for task_id in task_ids:
            mycursor.execute("DELETE FROM lists WHERE id=%s", (task_id,))
        
        mydb.commit()
        mycursor.close()
        mydb.close()

    def refresh_task_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.populate_delete_tasks()
