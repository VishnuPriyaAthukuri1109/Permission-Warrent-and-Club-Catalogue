import sqlite3
from tkinter import*
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime
# student_database = {
#     "556":"123",
#     "509":"123",
#     "560":"123",
#     "530":"123"
# }
# faculty_database={
#     "abc":"123"
# 
conn = sqlite3.connect('student_login.db')
cursor = conn.cursor()

# Create student login table if not exists
cursor.execute('''
    CREATE TABLE IF NOT EXISTS student_login (
        roll_number TEXT PRIMARY KEY,
        password TEXT
    )
''')

# Insert sample student login data
student_credentials = [
    ("556", "123"),
    ("509", "123"),
    ("560", "123"),
    ("530", "123")
]

# cursor.executemany('''
#     INSERT INTO student_login (roll_number, password)
#     VALUES (?, ?)
# ''', student_credentials)

# Commit the changes
conn.commit()
conn = sqlite3.connect('faculty_login.db')
cursor = conn.cursor()

# Create faculty login table if not exists
cursor.execute('''
    CREATE TABLE IF NOT EXISTS faculty_login (
        username TEXT PRIMARY KEY,
        password TEXT
    )
''')

# Insert sample faculty login data
faculty_credentials = [
    ("ramu", "123"),("ravi","123"),("anil","123"),("radha","123")
]

# cursor.executemany('''
#     INSERT INTO faculty_login (username, password)
#     VALUES (?, ?)
# ''', faculty_credentials)

# Commit the changes
conn.commit()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_name TEXT NOT NULL,
        venue TEXT NOT NULL,
        event_date TEXT NOT NULL
    )
''')

# Commit the changes
conn.commit()


# Close cursor and connection
cursor.close()
conn.close()

requests_database={}
root=Tk()
class Home:
    def __init__(self,root):
        self.root=root
        self.root.title("Permission catalog")
        self.heading_label=Label(root,text="welcome to application",font=("Times New Roman",30,"bold"))
        self.heading_label.pack(pady=(10,0),fill='x')
        self.btn_student=Button(root,text="Student",fg="blue",width=15,height=2,font=("Times New Roman",15),command = lambda user_type="student":self.open_login(user_type))
        self.btn_student.place(x=200,y=150)
        self.btn_faculty=Button(root,text="Faculty",fg="blue",width=15,height=2,font=("Times New Roman",15),command= lambda user_type="faculty":self.open_login(user_type))
        self.btn_faculty.place(x=200,y=250)
        self.message_label = Label(root, text="", font=("courier new", 14, "bold"), fg="red")
        self.message_label.pack()

    def open_login(self,user_type):
        self.heading_label.destroy()
        self.btn_student.destroy()
        self.btn_faculty.destroy()
        # self.request_label.destroy()
        self.root.title("LOGIN CREDENTIALS")
        self.login_ID=Label(root,text=f"{user_type}-ID",font=("courier new",14,"bold"))
        self.login_ID.place(x=80,y=90)
        self.password=Label(root,text="Password",font=("courier new",14,"bold"))
        self.password.place(x=100,y=160)
        self.entry_id=Entry(root)
        self.entry_id.place(x=200,y=80,width=250,height=50)
        self.entry_passwd=Entry(root,show='*')
        self.entry_passwd.place(x=200,y=150,width=250,height=50)
        self.submit=Button(root,text="Submit",font=("bold"),command=lambda user_type=user_type:self.login(user_type))
        self.submit.place(x=380,y=280)
        self.back=Button(root,text="Back1",font=("bold"),command=self.select_back)
        self.back.place(x=200,y=280)

    def select_back(self):
        self.heading_label.destroy()
        self.btn_student.destroy()
        self.btn_faculty.destroy()
        self.message_label.destroy()
        self.entry_id.destroy()
        self.entry_passwd.destroy()
        self.login_ID.destroy()
        self.password.destroy()
        self.submit.destroy()
        
        # Destroy the "Back" button if it exists
        if hasattr(self, 'back'):
            self.back.destroy()

        # Recreate the Home instance
        home = Home(root)

    
    def login(self, user_type):
        username = self.entry_id.get().lower()
        password = self.entry_passwd.get()

        if user_type == "student":
            conn = sqlite3.connect('student_login.db')
        elif user_type == "faculty":
            conn = sqlite3.connect('faculty_login.db')

        cursor = conn.cursor()

        # Query the database for login credentials
        if user_type=="faculty":
            cursor.execute("SELECT * FROM {} WHERE username = ? AND password = ?".format(user_type+"_login"), (username, password))
        else:
            cursor.execute("SELECT * FROM {} WHERE roll_number = ? AND password = ?".format(user_type+"_login"), (username, password))
        result = cursor.fetchone()

        # Close cursor and connection
        cursor.close()
        conn.close()

        if result:
            self.message_label.config(text=f"{user_type.capitalize()} login successful", fg="green")
            self.entry_id.delete(0, END)
            self.entry_passwd.delete(0, END)
            self.show_next_form(user_type)
        else:
            self.message_label.config(text="Invalid Login Credentials", fg="red")
            self.entry_id.delete(0, END)
            self.entry_passwd.delete(0, END)

        
    def show_next_form(self,user_type):
        self.login_ID.destroy()
        self.password.destroy()
        self.submit.destroy()
        self.back.destroy()
        self.back1=Button(root,text="Back2",font=("bold"),command=self.select_back1)
        self.back1.place(x=80,y=350)
        self.entry_id.destroy()
        self.entry_passwd.destroy()
        self.message_label.config(text="")
        if hasattr(self, 'request_display'):
            self.request_display.destroy()
        if hasattr(self, 'status_display'):
            self.status_display.destroy()
        if hasattr(self, 'after_request_back'):
            self.after_request_back.destroy()
        if user_type=="student":
            self.heading_label=Label(root,text="Student Forum",font=("Times New Roman",20,"bold"))
            self.heading_label.place(x=210,y=30)
            self.request_label=Button(root,text="Request",fg="blue",width=15,height=2,font=("courier new",16,"bold"),
                                      command=lambda user_type=user_type: self.permissions(user_type))
            self.request_label.place(x=200,y=90)
            self.todays_event=Button(root,text="Today's events",fg="blue",width=15,height=2,font=("courier new",16,"bold"),command=lambda user_type=user_type:self.show_today_events())
            self.todays_event.place(x=200,y=180)
            self.back_from_student=Button(root,text="Back3",font=("bold"),command=self.select_back_from_student)
            self.back_from_student.place(x=80,y=350)
        elif user_type=="faculty":
            self.heading_label=Label(root,text="Faculty Forum",font=("Times New Roman",20,"bold"))
            self.heading_label.place(x=210,y=30)
            self.label1=Button(root,text="Students Requests",fg="blue",width=18,height=2,font=("courier new",16,"bold"))
            self.label1.place(x=200,y=90)
            self.addevent_label=Button(root,text="Add Events",fg="blue",width=15,height=2,font=("courier new",16,"bold"),command=lambda user_type=user_type:self.add_event())
            self.addevent_label.place(x=200,y=270)
            self.todays_event=Button(root,text="Today's events",fg="blue",width=15,height=2,font=("courier new",16,"bold"),command=lambda user_type=user_type:self.show_today_events())
            self.todays_event.place(x=200,y=180)
            self.back_from_faculty=Button(root,text="Back4",font=("bold"),command=self.select_back1)
            self.back_from_faculty.place(x=80,y=350)
    
    def permissions(self, user_type):
        self.heading_label.destroy()
        self.request_label.destroy()
        self.todays_event.destroy()
        self.back.destroy()
        self.back_from_student.destroy()
        self.back1.destroy()

        self.heading_label1 = Label(root, text="PERMISSIONS", font=("Times New Roman", 30, "bold"))
        self.heading_label1.pack(pady=(10, 0), fill='x')

        self.requests_label = Label(root, text="Request", font=("courier new", 14, "bold"))
        self.requests_label.place(x=100, y=160)

        self.permission_entry = Entry(root)
        self.permission_entry.place(x=200, y=150, width=250, height=50)

        self.status_label = Label(root, text="Status", font=("courier new", 14, "bold"))
        self.status_label.place(x=100, y=250)

        self.submit = Button(root, text="Submit", font=("bold"), command=lambda user_type=user_type: self.submit_permissions(user_type))
        self.submit.place(x=380, y=280)

        self.back2 = Button(root, text="Back", font=("bold"),command=self.select_back2)
        self.back2.place(x=80, y=350)

    def submit_permissions(self, user_type):
        request = self.permission_entry.get()

        if not request:
            self.message_label.config(text="Please enter the name of event", fg="red")
        else:
            requests_database[user_type] = {"request": request, "status": "Pending"}

            self.message_label.config(text="Request submitted successfully", fg="green")
            self.permission_entry.delete(0, END)
            self.show_request_status(user_type)
    
    def show_request_status(self, user_type):
        self.requests_label.destroy()
        self.status_label.destroy()
        self.permission_entry.destroy()
        self.submit.destroy()
        self.back1.destroy()
        self.back2.destroy()

        self.requests_label = Label(root, text="Request", font=("courier new", 14, "bold"))
        self.requests_label.place(x=100, y=160)

        request_text = requests_database[user_type]["request"]
        self.request_display = Label(root, text=request_text, font=("courier new", 12))
        self.request_display.place(x=200, y=150)

        self.status_label = Label(root, text="Status", font=("courier new", 14, "bold"))
        self.status_label.place(x=100, y=250)
        status_text = requests_database[user_type]["status"]
        self.status_display = Label(root, text=status_text, font=("courier new", 12))
        self.status_display.place(x=200, y=250)
        self.after_request_back = Button(root, text="Back", font=("bold"), command=self.select_after_request_back)
        self.after_request_back.place(x=80, y=350)
    
    def show_today_events(self):
        # Fetch today's date
        today_date = datetime.now().strftime("%d-%m-%Y")

        # Connect to the database
        conn = sqlite3.connect('faculty_login.db')
        cursor = conn.cursor()

        # Retrieve today's events from the database
        cursor.execute("SELECT * FROM events WHERE event_date = ?", (today_date,))
        today_events = cursor.fetchall()

        # Close cursor and connection
        cursor.close()
        conn.close()

        # Display today's events
        if today_events:
            messagebox.showinfo("Today's Events", "\n".join([f"{event[1]} at {event[2]}" for event in today_events]))
        else:
            messagebox.showinfo("Today's Events", "No events scheduled for today")


    def select_back2(self):
        self.back1.destroy()
        self.heading_label.destroy()
        self.todays_event.destroy()
        self.request_label.destroy()
        self.entry_id.destroy()
        self.entry_passwd.destroy()
        self.login_ID.destroy()
        self.password.destroy()
        self.submit.destroy()
        self.back.destroy()
        self.requests_label.destroy()
        self.status_label.destroy()
        self.message_label.config(text="")
        self.heading_label1.destroy()
        self.permission_entry.destroy()
        self.back2.destroy()
        

        self.show_next_form("student")

    def add_event(self):
        self.heading_label.destroy()
        self.todays_event.destroy()
        self.addevent_label.destroy()
        self.label1.destroy()
        self.back.destroy()
        self.back1.destroy()
        self.back_from_faculty.destroy()
        self.root.title("Adding the events")
        self.event_label=Label(root,text=f"Event name",font=("courier new",14,"bold"))
        self.event_label.place(x=80,y=90)
        self.venue_label=Label(root,text="venue",font=("courier new",14,"bold"))
        self.venue_label.place(x=100,y=160)
        self.entry_event=Entry(root)
        self.entry_event.place(x=200,y=80,width=250,height=50)
        self.entry_venue=Entry(root)
        self.entry_venue.place(x=200,y=150,width=250,height=50)
        current_date = datetime.now().strftime("%d-%m-%Y ")
        self.date_label = Label(root, text="Event date", font=("courier new", 14,"bold"))
        self.date_label.place(x=80, y=220)
        self.entry_date=Entry(root)
        self.entry_date.place(x=200,y=210,width=250,height=50)
        venue_info=self.entry_venue.get()
        event_info=self.entry_event.get()
        date_info=self.entry_date.get()
        self.submit_add_event=Button(root,text="Submit",font=("bold"),command=self.submit_add_event_to_database)
        self.submit_add_event.place(x=300,y=280)
        self.back_addevent=Button(root,text="Back5",font=("bold"),command=self.select_back_addevent)
        self.back_addevent.place(x=80,y=350)

    def submit_add_event_to_database(self):
        event_name = self.entry_event.get()
        venue = self.entry_venue.get()
        event_date = self.entry_date.get()

        if not event_name or not venue or not event_date:
            messagebox.showerror("Error", "Please fill in all the fields")
        else:
            conn = sqlite3.connect('faculty_login.db')
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO events (event_name, venue, event_date) VALUES (?, ?, ?)", (event_name, venue, event_date))
                conn.commit()
                messagebox.showinfo("Success", "Event added successfully")
                self.entry_event.delete(0, END)
                self.entry_venue.delete(0, END)
                self.entry_date.delete(0, END)
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"Error adding event: {e}")
            # finally:
            #     cursor.close()
            #     conn.close()
   
    def select_back1(self):
    # Destroy widgets related to the current page
        self.todays_event.destroy()
        self.entry_id.destroy()
        self.entry_passwd.destroy()
        self.login_ID.destroy()
        self.password.destroy()
        self.submit.destroy()
        # self.message_label.config(text="")
        self.addevent_label.destroy()
        self.label1.destroy()
        self.back.destroy()
        self.back1.destroy()

        # Destroy the "Back" button if it exists
        if hasattr(self, 'back_from_faculty'):
            self.back_from_faculty.destroy()
        self.open_login("faculty")
        
        

    def select_back_addevent(self):
        # Destroy widgets related to the "Add Event" form
        self.event_label.destroy()
        self.venue_label.destroy()
        self.date_label.destroy()
        self.entry_event.destroy()
        self.entry_venue.destroy()
        self.entry_date.destroy()
        self.submit_add_event.destroy()
        self.back_addevent.destroy()
        self.message_label.config(text="")
        self.back1.destroy()

        # Destroy the "Back" button if it exists
        if hasattr(self, 'back_from_faculty'):
            self.back_from_faculty.destroy()
        if hasattr(self,'back'):
            self.back.destroy()
        if hasattr(self,'back_addevent'):
            self.back_addevent.destroy()

        # Recreate the previous form
        self.show_next_form("faculty")

    def select_back_from_student(self):
        # Destroy widgets related to the current page
        self.heading_label.destroy()
        self.request_label.destroy()
        self.todays_event.destroy()
        self.back_from_student.destroy()
        self.back1.destroy()

        # Recreate the previous form
        self.open_login("student")

    def select_after_request_back(self):
        self.heading_label1.destroy()
        self.requests_label.destroy()
        self.status_label.destroy()
        self.status_display.destroy()
        self.message_label.config(text="")
        self.back.destroy()
        self.permission_entry.destroy()
        self.submit.destroy()
        self.back1.destroy()
        self.heading_label.destroy()
        self.request_label.destroy()
        self.todays_event.destroy()
        self.back.destroy()
        self.after_request_back.destroy()
        

        self.show_next_form("student")





home=Home(root)
root.geometry('600x400')
root.mainloop()