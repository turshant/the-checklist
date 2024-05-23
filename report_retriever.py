import tkinter as tk
from tkinter import messagebox, Toplevel, ttk
import mysql.connector
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ReportRetriever(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

    def retrieve_reportss(self):
        email_window = Toplevel(self.master)
        email_window.title("Enter User Email")
        email_window.geometry("400x150")

        email_label = tk.Label(email_window, text="Enter User Email:")
        email_label.pack(pady=10)
        email_entry = tk.Entry(email_window)
        email_entry.pack(pady=5)

        submit_button = tk.Button(email_window, text="Submit", command=lambda: self.retrieve_reports_for_email(email_entry.get()))
        submit_button.pack(pady=5)

    def retrieve_reports_for_email(self, email):
        tasks = self.get_completed_tasks_for_user(email)

        if tasks:
            total_tasks = len(tasks)
            completed_tasks_count = sum(1 for task in tasks if task['completed'] == 'yes')
            pending_tasks_count = total_tasks - completed_tasks_count

            report_window = Toplevel(self.master)
            report_window.title(f"Task Reports for {email}")
            report_window.geometry("800x600")

            report_frame = tk.Frame(report_window)
            report_frame.pack(fill=tk.BOTH, expand=True)

            summary_label = tk.Label(report_window, text="", justify=tk.LEFT, anchor="nw")
            summary_label.pack(fill=tk.BOTH, expand=True)

            summary_text = f"User: {email}\nTotal Tasks: {total_tasks}\nCompleted Tasks: {completed_tasks_count}\nPending Tasks: {pending_tasks_count}"
            summary_label.config(text=summary_text)

            self.plot_tasks_bar_chart(total_tasks, completed_tasks_count, pending_tasks_count, report_frame)
        else:
            messagebox.showerror("Error", f"No tasks found for the provided email: {email}")

    def get_completed_tasks_for_user(self, email):
        try:
            
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="python",
                auth_plugin="mysql_native_password"
            )
            mycursor = mydb.cursor()

           
            query = "SELECT task, completed FROM lists WHERE re_email = %s"
            mycursor.execute(query, (email,))
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

        plt.close(fig)  

    def show_frame(self):
        self.pack(fill=tk.BOTH, expand=True)

    def hide_frame(self):
        self.pack_forget()

if __name__ == "__main__":
    root = tk.Tk()
    report_retriever = ReportRetriever(root)
    report_retriever.pack(fill=tk.BOTH, expand=True)
    report_retriever.retrieve_reports()
    root.mainloop()
