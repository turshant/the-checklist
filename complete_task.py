import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import mysql.connector

class CompletedTaskForm:
    def __init__(self, master):
        self.master = master
        self.master.title("Completed Tasks")
        self.master.geometry("2036x1264")

        self.canvas = tk.Canvas(self.master, width=2036, height=1264)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.background_image = Image.open('C:/Users/HP/Documents/task app/task manager.jpg')
        self.background_image = self.background_image.resize((2036, 1264), Image.Resampling.LANCZOS)
        self.background_photo = ImageTk.PhotoImage(self.background_image)

        self.canvas.create_image(0, 0, image=self.background_photo, anchor=tk.NW)

        self.tree = ttk.Treeview(self.master, columns=('ID', 'assigned_date','deadline', 'task', 'remarks', 're_email', 'send_pending_mail_flag',), show='headings')
        self.tree.heading('ID', text='ID')
        self.tree.heading('assigned_date', text='assigned_date')
        self.tree.heading('deadline', text='deadline')
        self.tree.heading('task', text='Task')
        self.tree.heading('remarks', text='Remarks')
        self.tree.heading('re_email', text='Re_Email')
        self.tree.heading('send_pending_mail_flag', text='Send Pending Mail Flag')
        self.tree.column('ID',width=50) 
        self.tree.column('assigned_date',width=150 )
        self.tree.column('deadline',width=150 )
        self.tree.column('task', width=250)
        self.tree.column('remarks',width=150 )
        self.tree.column('re_email',width=150 )
        self.tree.column('send_pending_mail_flag', width=150)

        self.tree_window = self.canvas.create_window(50, 50, anchor=tk.NW, window=self.tree, width=1434, height=736)
        self.scrollbar = ttk.Scrollbar(self.master, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        self.context_menu = tk.Menu(self.master, tearoff=0)
        self.context_menu.add_command(label="Mark as Completed", command=self.mark_as_completed)

        self.tree.bind("<Button-3>", self.open_context_menu)

        self.populate_completed_tasks()

    def open_context_menu(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item) 
            self.context_menu.post(event.x_root, event.y_root)  

    def mark_as_completed(self):
        selected_item = self.tree.selection()
        if selected_item:
            task_id = self.tree.item(selected_item, 'values')[0]
            self.update_task_as_completed(task_id)
        else:
            messagebox.showwarning("No Task Selected", "Please select a task to mark as completed.")

    def update_task_as_completed(self, task_id):
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="python",
            auth_plugin="mysql_native_password",
        )

        mycursor = mydb.cursor()

        mycursor.execute("UPDATE lists SET completed='yes' WHERE id=%s", (task_id,))
        mydb.commit()
        messagebox.showinfo("Task Completed", "Task marked as completed successfully.")

    def populate_completed_tasks(self):
        completed_tasks = self.fetch_completed_tasks_from_database()

        if completed_tasks:
            for task in completed_tasks:
                self.tree.insert('', tk.END, values=task)
        else:
            messagebox.showinfo("No Completed Tasks", "No completed tasks found.")

    def fetch_completed_tasks_from_database(self):
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="python",
            auth_plugin="mysql_native_password",
        )

        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM lists")
        completed_tasks = mycursor.fetchall()
        return completed_tasks


if __name__=="__main__":
    root=tk.Tk()
    app=CompletedTaskForm(root)
    root.mainloop()
