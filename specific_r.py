import tkinter as tk
from tkinter import simpledialog, messagebox
from datetime import datetime
import mysql.connector
import matplotlib.pyplot as plt
from tkcalendar import DateEntry  
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg# Import DateEntry widget
from PIL import Image, ImageTk

class ReportGenerator3(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

    def generate_report_for_date(self):
        # Create a Toplevel window for the date picker
        date_picker_window = tk.Toplevel(self.master)
        date_picker_window.title("Select Date")
        
        # Create a DateEntry widget for selecting the date
        date_entry = DateEntry(date_picker_window, date_pattern="yyyy-mm-dd", width=12, height=16)
        date_entry.pack(pady=10)
        
        # Function to handle generating report based on selected date
        def generate_report():
            report_date = date_entry.get_date()

            completed_tasks = self.get_completed_tasks_for_date(report_date)

            total_tasks = self.count_total_tasks_for_date(report_date)
            completed_tasks_count = len(completed_tasks)

            if completed_tasks:
                report_text = f"Report for {report_date}:\n"
                for task in completed_tasks:
                    report_text += f"- {task}\n"
                messagebox.showinfo("Task Report", report_text)
            else:
                messagebox.showinfo("No Tasks", f"No tasks completed on {report_date}.")

            # Create a frame to embed the graph
            graph_frame = tk.Frame(date_picker_window)
            graph_frame.pack(pady=10)

            self.plot_tasks_bar_chart(graph_frame, total_tasks, completed_tasks_count)
            
        # Create a button to generate the report
        generate_button = tk.Button(date_picker_window, text="Generate Report", command=generate_report)
        generate_button.pack()



    def get_completed_tasks_for_date(self, date):
        try:
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="python",
                auth_plugin="mysql_native_password"
            )
            mycursor = mydb.cursor()

            query = "SELECT task FROM lists WHERE deadline = %s AND completed = 'yes'"
            mycursor.execute(query, (date,))
            completed_tasks = [task[0] for task in mycursor.fetchall()]

            mycursor.close()
            mydb.close()

            return completed_tasks
        except mysql.connector.Error as err:
            print("Error:", err)
            return []

    def count_total_tasks_for_date(self, date):
        try:
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="python",
                auth_plugin="mysql_native_password"
            )

            mycursor = mydb.cursor()

            query = "SELECT COUNT(*) FROM lists WHERE deadline = %s"
            mycursor.execute(query, (date,))
            total_tasks = mycursor.fetchone()[0]

            mycursor.close()
            mydb.close()

            return total_tasks

        except mysql.connector.Error as err:
            print("Error:", err)
            return 0

    def plot_tasks_bar_chart(self, frame, total_tasks, completed_tasks_count):
        categories = ['Total Tasks', 'Completed Tasks']
        values = [total_tasks, completed_tasks_count]

        fig, ax = plt.subplots(figsize=(8, 6))
        ax.bar(categories, values, color=['blue', 'green'])
        ax.set_title('Task Report for Specific Date')
        ax.set_xlabel('Tasks')
        ax.set_ylabel('Count')

        # Embedding the graph in the frame
        canvas = FigureCanvasTkAgg(fig, master=frame)  
        canvas.draw()
        canvas.get_tk_widget().pack()

        plt.close(fig)  

    def show_frame(self):
        self.pack(fill=tk.BOTH, expand=True)

    def hide_frame(self):
        self.pack_forget()
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Report Generator")

    # Load background image
    img = Image.open("C:/Users/HP/Documents/task app/images.jpg")
    img = img.resize((root.winfo_screenwidth(), root.winfo_screenheight()), Image.Resampling.LANCZOS)
    background_image = ImageTk.PhotoImage(img)

    # Create a label with the background image
    background_label = tk.Label(root, image=background_image)
    background_label.place(relwidth=1, relheight=1)

    # Create report generator frame
    app = ReportGenerator3(root)
    app.show_frame()

    # Maximize window to full screen
    root.attributes('-fullscreen', True)  

    root.mainloop()