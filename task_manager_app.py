import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import csv
import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk
import tkinter.font as tkFont
import tkinter as tk
from tkinter import messagebox, ttk
import csv
from PIL import Image, ImageTk
import re
from PIL import Image, ImageTk
from tkinter import messagebox
from tkcalendar import Calendar
import mysql.connector
import matplotlib.pyplot as plt
from datetime import datetime
from tkinter import simpledialog
from mail_sending import TaskReminder# type:ignore
from report_retriever import ReportRetriever # type:ignore
from show_task import ShowTasksForm# type:ignore
from complete_task import CompletedTaskForm# type:ignore
from delete_task import DeleteTaskForm  # type:ignore
from pending_task import PendingTaskForm # type:ignore
from today_r import ReportGenerator2 # type:ignore
from alltime_r import ReportGenerator# type:ignore
from thechecklist import Thechecklist# type:ignore
import tkinter.font as tkFont
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk, messagebox
import mysql.connector
from specific_r import ReportGenerator3# type:ignore

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import csv
import re
import os

class SignUp:
    def __init__(self, master):
        self.master = master
        self.master.title("Sign Up")
        self.master.attributes('-fullscreen', True)  # Enable fullscreen mode

        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()

        # Load the background image
        try:
            background_image = Image.open('C:/Users/HP/Documents/task app/signnn.png')
            background_image = background_image.resize((screen_width, screen_height))
            background_photo = ImageTk.PhotoImage(background_image)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load background image: {e}")
            return

        # Create a label to display the background image
        self.label_background = tk.Label(self.master, image=background_photo)
        self.label_background.image = background_photo
        self.label_background.place(x=0, y=0, relwidth=1, relheight=1)

        # Create a frame to contain the sign-up elements
        try:
            self.bg_image_signup = Image.open('C:/Users/HP/Documents/task app/signnn.png')
            self.bg_image_signup = self.bg_image_signup.resize((600, 400), Image.LANCZOS)
            self.bg_photo_signup = ImageTk.PhotoImage(self.bg_image_signup)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load sign-up image: {e}")
            return

        # Create the signup frame
        self.signup_frame = tk.Frame(self.master, borderwidth=4, relief="groove", width=600, height=400)
        self.signup_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Create a label to hold the background image
        self.bg_label_signup = tk.Label(self.signup_frame, image=self.bg_photo_signup)
        self.bg_label_signup.image = self.bg_photo_signup  # Keep a reference to the image to prevent garbage collection
        self.bg_label_signup.place(relwidth=1, relheight=1)

        # Welcome message
        self.label_welcome_signup = tk.Label(self.signup_frame, text="Sign Up", font=("Helvetica", 16, "bold"), fg="black", bg=self.signup_frame.cget("bg"))
        self.label_welcome_signup.place(relx=0.5, rely=0.1, anchor="center")

        # Sign-up Form inside the frame
        self.label_username = tk.Label(self.signup_frame, text="Username:", bg=self.signup_frame.cget("bg"))
        self.label_username.place(relx=0.3, rely=0.3, anchor="e")

        self.entry_username = tk.Entry(self.signup_frame)
        self.entry_username.place(relx=0.4, rely=0.3, anchor="w")

        self.label_email = tk.Label(self.signup_frame, text="Email:", bg=self.signup_frame.cget("bg"))
        self.label_email.place(relx=0.26, rely=0.4, anchor="e")

        self.entry_email = tk.Entry(self.signup_frame)
        self.entry_email.place(relx=0.4, rely=0.4, anchor="w")

        self.label_password = tk.Label(self.signup_frame, text="Password:", bg=self.signup_frame.cget("bg"))
        self.label_password.place(relx=0.29, rely=0.5, anchor="e")

        self.entry_password = tk.Entry(self.signup_frame, show="*")
        self.entry_password.place(relx=0.4, rely=0.5, anchor="w")

        self.label_phone = tk.Label(self.signup_frame, text="Phone Number:", bg=self.signup_frame.cget("bg"))
        self.label_phone.place(relx=0.34, rely=0.6, anchor="e")

        self.entry_phone = tk.Entry(self.signup_frame)
        self.entry_phone.place(relx=0.4, rely=0.6, anchor="w")

        self.button_signup = tk.Button(self.signup_frame, text="Sign Up", command=self.signup)
        self.button_signup.place(relx=0.5, rely=0.8, anchor="center")

        self.button_login = tk.Button(self.signup_frame, text="Already have an account? Login", command=self.open_login_window)
        self.button_login.place(relx=0.5, rely=0.9, anchor="center")

    def signup(self):
        username = self.entry_username.get()
        email = self.entry_email.get()
        password = self.entry_password.get()
        phone = self.entry_phone.get()

        # Validate email and phone number
        if not self.validate_email(email):
            messagebox.showerror("Error", "Invalid email format")
            return

        if not self.validate_phone(phone):
            messagebox.showerror("Error", "Invalid phone number format")
            return

        # Store user information in a CSV file
        try:
            with open('C:/Users/HP/Documents/task app/checkist.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([username, email, password, phone])
        except PermissionError:
            messagebox.showerror("Error", "Permission denied: unable to write to file")
            return
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            return

        messagebox.showinfo("Success", "Sign up successful!")
        self.open_login_window()

    def validate_email(self, email):
        # Regular expression for email validation
        pattern = r"^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$"
        return re.match(pattern, email)

    def validate_phone(self, phone):
        # Regular expression for phone number validation
        pattern = r"^[0-9]{10}$"
        return re.match(pattern, phone)

    def open_login_window(self):
        self.clear_widgets()
        SignupPage(self.master)

    def clear_widgets(self):
        for widget in self.master.winfo_children():
            widget.destroy()

# The SignupPage class would be similarly updated with appropriate error handling and path corrections.

class SignupPage:
    def __init__(self, master):
        self.master = master
        self.master.title("Login")
        self.master.attributes('-fullscreen', True)  # Enable fullscreen mode

        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()

        # Load the background image
        background_image = Image.open('C:/Users/HP/Documents/task app/signnn.png')
        background_image = background_image.resize((screen_width, screen_height))
        background_photo = ImageTk.PhotoImage(background_image)

        # Create a label to display the background image
        self.label_background = tk.Label(self.master, image=background_photo)
        self.label_background.image = background_photo
        self.label_background.place(x=0, y=0, relwidth=1, relheight=1)

        # Create a label for the login window
        self.label_login_window = tk.Label(self.master, text="Welcome To Login", font=("Helvetica", 22, "bold"), fg="black", bg="cyan")
        self.label_login_window.place(relx=0.5, rely=0.1, anchor="center")

        self.bg_image = Image.open("C:/Users/HP/Documents/task app/signnn.png")
        self.bg_image = self.bg_image.resize((900, 300), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        # Create a frame to contain the login elements
        self.login_frame = tk.Frame(self.master, borderwidth=9, relief="groove", width=600, height=300, highlightbackground="black")
        self.login_frame.place(relx=0.5, rely=0.4, anchor="center")

        # Create a label to hold the background image
        self.bg_label = tk.Label(self.login_frame, image=self.bg_photo)
        self.bg_label.place(relwidth=1, relheight=1)

        # Welcome message
        self.label_welcome = tk.Label(self.login_frame, text="Welcome to the Checklist", font=("Helvetica", 16, "bold"), fg="black", bg=self.login_frame.cget("bg"))
        self.label_welcome.place(relx=0.5, rely=0.1, anchor="center")

        # Login form inside the frame
        self.label_login_email_phone = tk.Label(self.login_frame, text="Email/Phone:", fg="black", bg=self.login_frame.cget("bg"))
        self.label_login_email_phone.place(relx=0.3, rely=0.3, anchor="e")

        self.entry_login_email_phone = tk.Entry(self.login_frame)
        self.entry_login_email_phone.place(relx=0.4, rely=0.3, anchor="w")
        self.entry_login_email_phone.bind("<FocusOut>", self.fill_password)

        self.label_login_password = tk.Label(self.login_frame, text="Password:", fg="black", bg=self.login_frame.cget("bg"))
        self.label_login_password.place(relx=0.27, rely=0.5, anchor="e")

        self.entry_login_password = tk.Entry(self.login_frame, show="*")
        self.entry_login_password.place(relx=0.4, rely=0.5, anchor="w")

        self.show_password = tk.BooleanVar()
        self.show_password.set(False)
        self.eye_button = tk.Button(self.login_frame, text="👁️", command=self.toggle_password_visibility)
        self.eye_button.place(relx=0.7, rely=0.5, anchor="w")

        self.btn_login = tk.Button(self.login_frame, text="Login", command=self.login)
        self.btn_login.place(relx=0.5, rely=0.8, anchor="center")
        self.master.bind('<Return>', lambda event: self.login())

        # Label for non-registered users
        self.label_not_registered = tk.Label(self.master, text="Not a user? Register here.", fg="blue", cursor="hand2")
        self.label_not_registered.place(relx=0.5, rely=0.7, anchor="center")
        self.label_not_registered.bind("<Button-1>", self.open_signup_window)

        self.task_manager_window = None  # Initialize task manager window reference

        # Load saved login details if available
        self.saved_login_details = self.load_saved_login_details()

    def open_signup_window(self, event):
        self.clear_widgets()
        SignUp(self.master)
    
    def clear_widgets(self):
        for widget in self.master.winfo_children():
            widget.destroy()

    def login(self):
     email_phone = self.entry_login_email_phone.get().strip()
     password = self.entry_login_password.get().strip()

     self.entry_login_email_phone.delete(0, tk.END)
     self.entry_login_password.delete(0, tk.END)

    # Admin login condition
     if email_phone == "turshantkalia88@gmail.com" and password == "8876":
        messagebox.showinfo("Success", "Welcome turshant")
     elif email_phone == "turshantkalia5@gmail.com" and password == "8876":
        messagebox.showinfo("Success", "Welcome my lord")   
        self.master.destroy()
        root = tk.Tk()
        TaskManagerApp(root, role="admin")
        return

    # Check user credentials from CSV
     try:
        with open('C:/Users/HP/Documents/task app/checkist.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) != 4:
                    messagebox.showerror("Error", "Invalid format in CSV file.")
                    return

                username, email, user_password, phone = row

                if (email_phone == email or email_phone == phone) and password == user_password:
                    messagebox.showinfo("Success", "User login successful!")
                    if email_phone not in self.saved_login_details:
                        self.save_login_details_prompt(email_phone, password)
                    self.master.destroy()
                    root = tk.Tk()
                    TaskManagerApp(root, role="user")
                    return
        messagebox.showerror("Error", "Invalid email or password")
     except FileNotFoundError:
        messagebox.showerror("Error", "CSV file not found.")
     except Exception as e:
         messagebox.showerror("Error", f"Failed to read user data: {e}")


    def save_login_details_prompt(self, email, password):
        if email not in self.saved_login_details:
            if messagebox.askyesno("Save Login Details", "Do you want to save your login details?"):
                self.saved_login_details[email] = password
                self.save_login_details()

    def save_login_details(self):
        with open('C:/Users/HP/Documents/task app/checkist.csv', 'w', newline='') as file:
            fieldnames = ['email', 'password']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for email, password in self.saved_login_details.items():
                writer.writerow({'email': email, 'password': password})

    def toggle_password_visibility(self):
        if self.show_password.get():
            self.entry_login_password.config(show="")
        else:
            self.entry_login_password.config(show="*")
        self.show_password.set(not self.show_password.get())

    def load_saved_login_details(self):
        saved_login_details = {}
        try:
            with open('saved_login_details.csv', 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    saved_login_details[row['email']] = row['password']
        except FileNotFoundError:
            pass
        return saved_login_details

    def fill_password(self, event):
        email = self.entry_login_email_phone.get().strip()
        if email in self.saved_login_details:
            password = self.saved_login_details[email]
            self.entry_login_password.delete(0, tk.END)
            self.entry_login_password.insert(0, password)


class TaskManagerApp:
    def __init__(self, master, role):
        self.master = master
        self.master.title("Task Manager")
        self.master.geometry("2036x1264")  
        self.role = role  
        self.task_tree = None
        self.displayed_tasks = None  
        self.alltime_r = ReportGenerator(master)
        self.today_r = ReportGenerator2(master) 
        self.specific_r = ReportGenerator3(master)
        self.report_retriever=ReportRetriever(master)

        background_image = Image.open('C:/Users/HP/Documents/task app/task manager.jpg')
        background_image = background_image.resize((master.winfo_screenwidth(), master.winfo_screenheight()))
        background_photo = ImageTk.PhotoImage(background_image)

        self.label_background = tk.Label(master, image=background_photo)
        self.label_background.image = background_photo
        self.label_background.place(x=0, y=0, relwidth=1, relheight=1)

        self.menu_bar = tk.Menu(self.master)
        self.menu_bar.add_command(label="Home", command=self.show_main_interface)
        self.menu_bar.add_command(label="Your Reports", command=self.retrieve_reportss)
        if self.role == "admin":
         self.menu_bar.add_command(label="Task Reminder", command=self.send_task_reminder_email)

        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        if self.role == "admin":
            self.file_menu.add_command(label="New Task", command=self.thechecklist)
            self.file_menu.add_separator()
            self.file_menu.add_command(label="Exit", command=self.master.quit)
            self.menu_bar.add_cascade(label="Task", menu=self.file_menu)

        self.dropdown_menu = tk.Menu(self.menu_bar, tearoff=0)
        if self.role == "admin":
            self.dropdown_menu.add_command(label="Pending Task", command=self.pending_tasks)
            self.dropdown_menu.add_command(label="Delete Task", command=self.delete_tasks)
            self.dropdown_menu.add_command(label="Complete Task", command=self.complete_task)
        self.dropdown_menu.add_command(label="Show Tasks", command=self.show_tasks)
        self.menu_bar.add_cascade(label="Task Actions", menu=self.dropdown_menu)

        self.dropdown_menu2 = tk.Menu(self.menu_bar, tearoff=0)
        if self.role == "admin":
         self.dropdown_menu2.add_command(label="All time Report", command=self.generate_report)
         self.dropdown_menu2.add_command(label="Pie Chart", command=self.show_today_tasks_pie_chart)
         self.dropdown_menu2.add_command(label="Report on Specific Date", command=self.generate_report_for_date)
         self.dropdown_menu2.add_command(label="Today's Report", command=self.today_report)
         self.menu_bar.add_cascade(label="Reports", menu=self.dropdown_menu2)
        self.menu_bar.add_command(label="Exit", command=self.exit_program)

        self.master.config(menu=self.menu_bar)

        self.create_dashboard()
       
        self.update_dashboard()

        self.show_today_tasks_pie_chart()

        button_font = tkFont.Font(size=15)
        self.footer_frame = tk.Frame(self.master, bg="black", bd=1, relief=tk.SUNKEN, height=150)
        self.footer_frame.pack(side=tk.BOTTOM, fill=tk.X)

        tk.Label(self.footer_frame, text="Project: The checklist", font=button_font).pack(side=tk.LEFT, padx=10)
        tk.Label(self.footer_frame, text="Contact: +91 765780548", font=button_font).pack(side=tk.LEFT, padx=10)
        tk.Label(self.footer_frame, text="© The checklist", font=button_font).pack(side=tk.RIGHT, padx=10)

        help_label = tk.Label(self.footer_frame, text="Help: www.taskmanager.com/help", fg="blue", cursor="hand2", font=button_font)
        help_label.pack(side=tk.RIGHT, padx=10)
        help_label.bind("<Button-1>", self.show_help)

        self.btn_hamburger = tk.Button(master, text="☰", command=self.show_additional_menu)
        self.btn_hamburger.pack(anchor="ne", padx=10, pady=10)


    def create_dashboard(self):
        # Create the dashboard frame
        self.dashboard_frame = tk.Frame(self.master, bg="white", bd=2, relief=tk.RAISED)
        self.dashboard_frame.pack(fill=tk.X, side=tk.TOP)

        self.welcome_message = tk.Label(self.dashboard_frame, text="WELCOME TO THE CHECKLIST", font=("Arial", 24), bg="white")
        self.welcome_message.pack(pady=10)
        
        checklist_text = """
        Stay organized stay on track."""
     
        # Display additional text for the checklist project
        tk.Label(self.dashboard_frame, text=checklist_text, font=("Arial", 16), bg="sky blue", justify=tk.LEFT).pack(pady=10)        
        total_tasks_label = tk.Label(self.dashboard_frame, text="Total Tasks:", font=("Arial", 14), bg="white")
        total_tasks_label.pack(side=tk.LEFT, padx=10)
        self.total_tasks_count_label = tk.Label(self.dashboard_frame, text="0", font=("Arial", 14, "bold"), bg="white")
        self.total_tasks_count_label.pack(side=tk.LEFT)

        # Display completed tasks count
        completed_tasks_label = tk.Label(self.dashboard_frame, text="Completed Tasks:", font=("Arial", 14), bg="white")
        completed_tasks_label.pack(side=tk.LEFT, padx=10)
        self.completed_tasks_count_label = tk.Label(self.dashboard_frame, text="0", font=("Arial", 14, "bold"), bg="white")
        self.completed_tasks_count_label.pack(side=tk.LEFT)

        # Display pending tasks count
        pending_tasks_label = tk.Label(self.dashboard_frame, text="Pending Tasks:", font=("Arial", 14), bg="white")
        pending_tasks_label.pack(side=tk.LEFT, padx=10)
        self.pending_tasks_count_label = tk.Label(self.dashboard_frame, text="0", font=("Arial", 14, "bold"), bg="white")
        self.pending_tasks_count_label.pack(side=tk.LEFT)

    def update_dashboard(self):
        # Connect to MySQL database
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="python",
            auth_plugin="mysql_native_password",
        )
        mycursor = mydb.cursor()

        # Retrieve total tasks count
        mycursor.execute("SELECT COUNT(*) FROM lists")
        total_tasks = mycursor.fetchone()[0]

        # Retrieve completed tasks count
        mycursor.execute("SELECT COUNT(*) FROM lists WHERE completed = 'yes'")
        completed_tasks = mycursor.fetchone()[0]

        # Calculate pending tasks count
        pending_tasks = total_tasks - completed_tasks

        # Update labels with retrieved data
        self.total_tasks_count_label.config(text=str(total_tasks))
        self.completed_tasks_count_label.config(text=str(completed_tasks))
        self.pending_tasks_count_label.config(text=str(pending_tasks))

        # Close database connection
        mycursor.close()
        mydb.close()

 

    def show_additional_menu(self):
        # Create the additional menu
        additional_menu = tk.Menu(self.master, tearoff=0)
        additional_menu.add_command(label="About Us", command=self.about_us)
        additional_menu.add_command(label="Log Out", command=self.log_out)
        additional_menu.add_command(label="Profile", command=self.profile)
        additional_menu.add_command(label="Help", command=self.help)

        # Calculate the x and y coordinates for the dropdown menu
        x = self.master.winfo_screenwidth() - self.btn_hamburger.winfo_width() - 100
        y = self.btn_hamburger.winfo_rooty() + self.btn_hamburger.winfo_height()

        # Show the dropdown menu
        additional_menu.post(x, y)
  
 
    def send_task_reminder_email(self):
        email_sender = 'turshantkalia88@gmail.com'
        email_password = 'fpwc vect lgxl wtnt'
        task_reminder = TaskReminder(email_sender, email_password)
        result = task_reminder.check_date()

        if result == "success":
            messagebox.showinfo("Success", "Task reminder email sent successfully!")
        elif result == "no_tasks":
            messagebox.showinfo("No Tasks", "No pending tasks for today or tomorrow.")
        elif result == "error":
            messagebox.showerror("Error", "An error occurred while sending email.")


    
    def retrieve_reportss(self):
        self.report_retriever.retrieve_reportss()
    

    def show_main_interface(self):
        if self.pie_chart_canvas:
            self.pie_chart_canvas.get_tk_widget().destroy()

         
        self.dashboard_frame.pack(fill=tk.X, side=tk.TOP)
        self.footer_frame.pack(side=tk.BOTTOM, fill=tk.X)
        self.btn_hamburger.pack(anchor="ne", padx=10, pady=10)

   
    def show_tasks(self):
        show_tasks = tk.Toplevel(self.master)
        ShowTasksForm(show_tasks)
    
    def complete_task(self):
        complete_task = tk.Toplevel(self.master)
        CompletedTaskForm(complete_task)

    def pending_tasks(self):
        pending_tasks = tk.Toplevel(self.master)
        PendingTaskForm(pending_tasks)   

    def delete_tasks(self):
        delete_task = tk.Toplevel(self.master)
        DeleteTaskForm(delete_task)      
   
    def generate_report(self):
     self.alltime_r.generate_report()
     self.alltime_r.show_frame()

    def mail(self):
     self.alltime_r.generate_report() 


    def today_report(self):
        self.today_r.today_report()
        self.today_r.show_frame()
        


    def generate_report_for_date(self):
     self.specific_r.generate_report_for_date()

        
    def logout(self):
        if messagebox.askokcancel("Exit", "Are you sure you want to logout?"):
            self.master.quit()  

    def about_us(self):
        print("About Us")

    def log_out(self):
        if messagebox.askokcancel("Exit", "Are you sure you want to logout?"):
            self.master.quit()   
    def profile(self):
        print("Profile")

    def help(self):
        print("Help")

    def exit_program(self):
        if messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
            self.master.quit()    

    def thechecklist(self):
        thechecklist = tk.Toplevel(self.master)
        Thechecklist(thechecklist)    
    
    def show_today_tasks_pie_chart(self):

        # Connect to MySQL database
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="python",
            auth_plugin="mysql_native_password",
        )

        mycursor = mydb.cursor()

        mycursor.execute("SELECT COUNT(*) FROM lists")
        count = mycursor.fetchone()[0]

        labels = ['Scheduled Tasks', 'Total Tasks']
        sizes = [count, 100 - count]  

       
        fig, ax = plt.subplots(figsize=(8,6))
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
        ax.axis('equal')  
        ax.set_title("Tasks ")

        
        self.pie_chart_canvas = FigureCanvasTkAgg(fig, master=self.master)
        self.pie_chart_canvas.draw()
        self.pie_chart_canvas.get_tk_widget().pack()


        

    def show_help(self, event):
        help_message = (
            "To add a task:\n"
            "1. Click on the 'New Task' button in the menu.\n"
            "2. Fill in the details of the task and click 'Save'.\n\n"
            "To view completed tasks:\n"
            "1. Click on the 'Show Tasks' button in the menu.\n"
            "2. Select the 'Completed Tasks' tab.\n\n"
            "To view pending tasks:\n"
            "1. Click on the 'Show Tasks' button in the menu.\n"
            "2. Select the 'Pending Tasks' tab."
        )
        messagebox.showinfo("Help", help_message)

    def logout(self):
        self.master.destroy()

def main():
    root = tk.Tk()
    app = SignupPage(root)
    root.mainloop()

if __name__ == "__main__":
    main()
