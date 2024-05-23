import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
import mysql.connector
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class TaskReminder():
    def __init__(self, email_sender, email_password):
        self.email_sender = email_sender
        self.email_password = email_password
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="python",
            auth_plugin="mysql_native_password",
        )

    def check_date(self):
        today = datetime.now().date()
        tomorrow = today + timedelta(days=1)
        print("Today's Date:", today) 
        print("Tomorrow's Date:", tomorrow) 
        
        cursor = self.db.cursor()
        sql = "SELECT task, assigned_date, deadline, re_email, id FROM lists WHERE deadline IN (%s, %s) AND (send_pending_mail_flag IS NULL OR send_pending_mail_flag = 0)"
        values = (today, tomorrow)
        cursor.execute(sql, values)
        lists = cursor.fetchall()

        if lists:
            messagebox.showinfo("Pending Tasks", f"You have pending tasks for today or tomorrow:")
            for task in lists:
                messagebox.showinfo("Task Details", f"Task: {task[0]}\nAssign Date: {task[1]}\nDue Date: {task[2]}")
                re_email = task[3]
                result = self.send_email_notification(task[0], task[1], task[2], re_email)
                if result == "Email Sent Successfully":
                    messagebox.showinfo("Success", "Email sent successfully!")
                else:
                    messagebox.showerror("Error", "Failed to send email.")
                sql = "UPDATE lists SET send_pending_mail_flag = 1 WHERE id = %s"
                values = (task[4],)
                cursor.execute(sql, values)
                self.db.commit()
        else:
            messagebox.showinfo("No Tasks", "No pending tasks for today or tomorrow.")

    def send_email_notification(self, task_name, assign_date, due_date, re_email):
        receiver_email = re_email
        subject = "Pending Task reminder"
        body = f"You have a pending task: {task_name}\nAssigned Date: {assign_date}\nDue Date: {due_date}"
        message = MIMEMultipart()
        message["From"] = self.email_sender
        message["To"] = receiver_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(self.email_sender, self.email_password)
            text = message.as_string()
            server.sendmail(self.email_sender, receiver_email, text)
            server.quit()
            return "Email Sent Successfully"
        except Exception as e:
            print("Email Error:", f"An error occurred while sending email: {str(e)}")
            return "Email Sending Failed"

if __name__ == "__main__":
    email_sender = 'turshantkalia88@gmail.com'
    email_password = 'fpwc vect lgxl wtnt'
    task_reminder = TaskReminder(email_sender, email_password)
    task_reminder.check_date()
