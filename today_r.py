import tkinter as tk
from tkinter import Toplevel, ttk
from datetime import datetime
import mysql.connector
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ReportGenerator2(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

    def today_report(self):
        today_date = datetime.now().date()

        usernames = self.get_usernames_for_date(today_date)

        # Create a new window to display the reports
        report_window = Toplevel(self.master)
        report_window.title("Today's Task Reports")
        report_window.geometry("2036x1264")

        # Create a dropdown menu (combobox) to select the user
        user_label = tk.Label(report_window, text="Select User:")
        user_label.pack(pady=10)
        user_combobox = ttk.Combobox(report_window, values=usernames, state="readonly")
        user_combobox.pack(pady=10)

        user_combobox.bind("<<ComboboxSelected>>", lambda event: self.update_graph(today_date, user_combobox.get(), report_frame))

        report_frame = tk.Frame(report_window)
        report_frame.pack(fill=tk.BOTH, expand=True)

        if usernames:
            self.update_graph(today_date, usernames[0], report_frame)

    def get_usernames_for_date(self, date):
        try:
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="python",
                auth_plugin="mysql_native_password"
            )
            mycursor = mydb.cursor()

            query = "SELECT DISTINCT re_email FROM lists WHERE deadline = %s"
            mycursor.execute(query, (date,))
            usernames = [row[0] for row in mycursor.fetchall()]

            mycursor.close()
            mydb.close()

            return usernames
        except mysql.connector.Error as err:
            print("Error:", err)
            return []

    def update_graph(self, date, username, parent):
        tasks = self.get_completed_tasks_for_user(date, username)

        total_tasks = len(tasks)
        completed_tasks_count = sum(1 for task in tasks if task['completed'] == 'yes')
        pending_tasks_count = total_tasks - completed_tasks_count

        for widget in parent.winfo_children():
            widget.destroy()

        self.plot_tasks_bar_chart(total_tasks, completed_tasks_count, pending_tasks_count, parent)

    def get_completed_tasks_for_user(self, date, username):
        try:
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="python",
                auth_plugin="mysql_native_password"
            )
            mycursor = mydb.cursor()

            query = "SELECT task, completed FROM lists WHERE deadline = %s AND re_email = %s"
            mycursor.execute(query, (date, username))
            tasks = [{'task': row[0], 'completed': row[1]} for row in mycursor.fetchall()]

            mycursor.close()
            mydb.close()

            return tasks
        except mysql.connector.Error as err:
            print("Error:", err)
            return []

    def plot_tasks_bar_chart(self, total_tasks, completed_tasks_count, pending_tasks_count, parent):
        categories = ['Total Tasks', 'Completed Tasks', 'Pending Tasks']
        values = [total_tasks, completed_tasks_count, pending_tasks_count]

        fig, ax = plt.subplots(figsize=(8, 6))
        ax.bar(categories, values, color=['blue', 'green', 'red'])
        ax.set_title('Task Report')
        ax.set_xlabel('Tasks')
        ax.set_ylabel('Count')

        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


    def show_frame(self):
        self.pack(fill=tk.BOTH, expand=True)

    def hide_frame(self):
        self.pack_forget()