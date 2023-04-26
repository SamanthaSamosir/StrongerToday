import re
import requests
import tkinter as tk
import mysql.connector
from tkinter.font import Font
from trycourier import Courier
from tkinter import messagebox

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="strongtoday"
)

def start_now():

    label1.destroy()
    label2.destroy()
    button.destroy()
    sign_in_button.place(x=180, y=300, anchor=tk.CENTER)
    sign_up_button.place(x=180, y=350, anchor=tk.CENTER)

def sign_up():
    def submit_signup(name, email, password, subscribe):
        name = name_input.get()
        email = email_input.get()
        password = password_input.get()
        subscribe = subscribe_var.get()

        # check if all fields are filled
        if not name or not email or not password:
            messagebox.showwarning("Warning", "Please fill in all the required fields!")
            return

        # validate name
        if not re.match("^[a-zA-Z ]+$", name):
            messagebox.showwarning("Warning", "Please enter a valid name!")
            return

        # validate email
        if not re.match("^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
            messagebox.showwarning("Warning", "Please enter a valid email address!")
            return

        # connect to the database
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="strongtoday"
        )

        # create a cursor object
        mycursor = mydb.cursor()

        # check if email is already present in the database
        query = "SELECT * FROM users WHERE email = %s"
        value = (email,)
        mycursor.execute(query, value)

        if mycursor.fetchone():
            messagebox.showwarning("Warning", "This email is already registered!")
            return

        # prepare the SQL query
        sql = "INSERT INTO users (name, email, password, subscribe) VALUES (%s, %s, %s, %s)"
        values = (name, email, password, subscribe)

        # execute the query
        mycursor.execute(sql, values)

        # commit the changes
        mydb.commit()

        # close the cursor and database connections
        mycursor.close()
        mydb.close()

        # reset the input fields and show a confirmation message
        name_input.delete(0, tk.END)
        email_input.delete(0, tk.END)
        password_input.delete(0, tk.END)
        subscribe_var.set(0)
        messagebox.showinfo("Success", "Thank you for signing up!")

        # send notification via Courier API
        # prod token: pk_prod_JYRK4ZZ2F2MJM3NS1DFFCBQTFTRP
        # test token: pk_test_ES1QJ92R2K4W5FPEVGS7GY3XMJA3
        if subscribe:
            client = Courier(auth_token="pk_prod_JYRK4ZZ2F2MJM3NS1DFFCBQTFTRP")

            resp = client.send_message(
                message={
                    "to": {
                        "email": email,
                    },
                    "template": "60335EDJW8MG4APSCE3JNQ2P6M2T",
                    "data": {
                        "recipientName": name,
                    },
                }
            )
            print(resp['requestId'])

        # create a new window with the same size as the previous window and close the old window
        root2 = tk.Tk()
        root2.title("StrongerToday")
        root2.geometry("{}x{}".format(root.winfo_width(), root.winfo_height()))
        root.resizable(False, False)

        # create a canvas widget
        canvas2 = tk.Canvas(root2, width=360, height=640)
        canvas2.pack()

        # draw a gradient background on the canvas
        canvas2.create_rectangle(0, 0, 360, 640, fill="", outline="")
        for i in range(640):
            color = "#%02x%02x%02x" % (
                int((1 - i / 640) * int(start_color[1:3], 16) + i / 640 * int(end_color[1:3], 16)),
                int((1 - i / 640) * int(start_color[3:5], 16) + i / 640 * int(end_color[3:5], 16)),
                int((1 - i / 640) * int(start_color[5:], 16) + i / 640 * int(end_color[5:], 16))
            )
            canvas2.create_line(0, i, 360, i, fill=color)

        # make a request to the Forismatic API to get a random quote
        response = requests.get("http://api.forismatic.com/api/1.0/?method=getQuote&format=json&lang=en")

        # parse the JSON response to get the quote and author
        data = response.json()
        quote = data["quoteText"]
        author = data["quoteAuthor"] if data["quoteAuthor"] else "Unknown"

        # display the quote and author on the canvas
        author_text = canvas2.create_text(180, 180, text="" + author, fill="#7f2982", font=("Montserrat", 12),
                                          width=300, anchor=tk.CENTER)
        quote_text = canvas2.create_text(180, 270, text=quote, fill="#7f2982", font=("Montserrat", 14), width=300,
                                         anchor=tk.CENTER)

        # create a button to get a new quote
        def get_new_quote():
            try:
                response = requests.get("http://api.forismatic.com/api/1.0/?method=getQuote&format=json&lang=en")
                data = response.json()
                quote = data["quoteText"]
                author = data["quoteAuthor"] if data["quoteAuthor"] else "Unknown"
                canvas2.itemconfigure(quote_text, text=quote)
                canvas2.itemconfigure(author_text, text="" + author)

            except Exception as e:
                error_label = tk.Label(root2, text="Failed to get a new quote. Please try again later.", fg="red", bg='#16001e')
                error_label.place(x=180, y=420, anchor=tk.CENTER)
                root2.after(3000, error_label.destroy)

        new_quote_button = tk.Button(root2, text="New Quote", font=("Montserrat", 12), command=get_new_quote, bg='#16001e', fg="#ffffff", bd=0, highlightthickness=0,padx=20, pady=10, activebackground='#f7b2b7', activeforeground='#ffffff')
        new_quote_button.place(x=180, y=380, anchor=tk.CENTER)

        def send_email():

            # send the email using the Courier API
            client = Courier(auth_token="pk_prod_JYRK4ZZ2F2MJM3NS1DFFCBQTFTRP")

            resp = client.send_message(
                message={
                    "to": {
                        "email": email,
                    },
                    "template": "1Q6YKFYQY0MDTYNFJ4ZKA20HWQN4",
                    "data": {
                        "recipientName": name,
                        "body": [quote]
                    },
                }
            )
            print(resp['requestId'])

        emailme_button = tk.Button(root2, text="Email Me!", command=send_email, font=("Montserrat", 12), bg='#16001e',fg="#ffffff", bd=0, highlightthickness=0,padx=23, pady=10, activebackground='#f7b2b7', activeforeground='#ffffff')
        emailme_button.place(x=180, y=435, anchor=tk.CENTER)

        root.destroy()
        root2.mainloop()

    sign_in_button.destroy()
    sign_up_button.destroy()

    # Add label and input for name
    name_label = tk.Label(root, text="Name:", font=catchphrase_font, fg='#ffffff', bg='#16001e', padx=30, pady=15)
    name_label.place(x=123, y=230, anchor='e')
    name_input = tk.Entry(root, width=30)
    name_input.place(x=name_label.winfo_width() + 130, y=220)

    # Add label and input for password
    password_label = tk.Label(root, text="Password:", font=catchphrase_font, fg='#ffffff', bg='#16001e', padx=16,
                              pady=15)
    password_label.place(x=123, y=350, anchor='e')
    password_input = tk.Entry(root, show='*', width=30)
    password_input.place(x=password_label.winfo_width() + 130, y=340)

    # Add label and input for email
    email_label = tk.Label(root, text="Email:", font=catchphrase_font, fg='#ffffff', bg='#16001e', padx=31, pady=15)
    email_label.place(x=123, y=290, anchor='e')
    email_input = tk.Entry(root, width=30)
    email_input.place(x=email_label.winfo_width() + 130, y=280)

    # Add checkbox for daily motivation
    subscribe_var = tk.IntVar()
    subscribe_checkbox = tk.Checkbutton(root, text="Subscribe for daily dose of motivation!", font=normal_font,
                                        fg='#ffffff', bg='#16001e', variable=subscribe_var)
    subscribe_checkbox.place(x=75, y=390)
    subscribe_checkbox.configure(activeforeground='#7f2982', selectcolor='#7f2982')

    # Add submit button
    submit_button = tk.Button(root, text="Submit", font=catchphrase_font, fg='#ffffff', bg='#7f2982', padx=20, pady=5,
                              command=lambda: submit_signup(name_input.get(), email_input.get(), password_input.get(), subscribe_var.get()))
    submit_button.place(x=130, y=420)

def sign_in():
    def submit_signin():
        # Get user input
        email = email_input.get()
        password = password_input.get()


        # check if all fields are filled
        if not email or not password:
            messagebox.showwarning("Warning", "Please fill in all the required fields!")
            return

        # Connect to database
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="strongtoday"
        )
        cursor = db.cursor()

        # Check if email and password match a user in the database
        query = "SELECT * FROM users WHERE email = %s AND password = %s"
        cursor.execute(query, (email, password))
        result = cursor.fetchone()

        # If a user is found, sign them in and destroy the signin page
        if result:
            # Perform sign-in actions
            messagebox.showinfo("Success", "You have successfully signed in.")
            # create a new window with the same size as the previous window and close the old window
            root3 = tk.Tk()
            root3.title("StrongerToday")
            root3.geometry("{}x{}".format(root.winfo_width(), root.winfo_height()))
            root3.resizable(False, False)

            # create a canvas widget
            canvas3 = tk.Canvas(root3, width=360, height=640)
            canvas3.pack()

            # draw a gradient background on the canvas
            canvas3.create_rectangle(0, 0, 360, 640, fill="", outline="")
            for i in range(640):
                color = "#%02x%02x%02x" % (
                    int((1 - i / 640) * int(start_color[1:3], 16) + i / 640 * int(end_color[1:3], 16)),
                    int((1 - i / 640) * int(start_color[3:5], 16) + i / 640 * int(end_color[3:5], 16)),
                    int((1 - i / 640) * int(start_color[5:], 16) + i / 640 * int(end_color[5:], 16))
                )
                canvas3.create_line(0, i, 360, i, fill=color)

            # make a request to the Forismatic API to get a random quote
            response = requests.get("http://api.forismatic.com/api/1.0/?method=getQuote&format=json&lang=en")

            # parse the JSON response to get the quote and author
            data = response.json()
            quote = data["quoteText"]
            author = data["quoteAuthor"] if data["quoteAuthor"] else "Unknown"

            # display the quote and author on the canvas
            author_text = canvas3.create_text(180, 180, text="" + author, fill="#7f2982", font=("Montserrat", 12),
                                              width=300, anchor=tk.CENTER)
            quote_text = canvas3.create_text(180, 270, text=quote, fill="#7f2982", font=("Montserrat", 14), width=300,
                                             anchor=tk.CENTER)

            # create a button to get a new quote
            def get_new_quote():
                try:
                    response = requests.get("http://api.forismatic.com/api/1.0/?method=getQuote&format=json&lang=en")
                    data = response.json()
                    quote = data["quoteText"]
                    author = data["quoteAuthor"] if data["quoteAuthor"] else "Unknown"
                    canvas3.itemconfigure(quote_text, text=quote)
                    canvas3.itemconfigure(author_text, text="" + author)

                except Exception as e:
                    error_label = tk.Label(root3, text="Failed to get a new quote. Please try again later.", fg="red",
                                           bg='#16001e')
                    error_label.place(x=180, y=420, anchor=tk.CENTER)
                    root3.after(3000, error_label.destroy)

            new_quote_button = tk.Button(root3, text="New Quote", font=("Montserrat", 12), command=get_new_quote,
                                         bg='#16001e', fg="#ffffff", bd=0, highlightthickness=0, padx=20, pady=10,
                                         activebackground='#f7b2b7', activeforeground='#ffffff')
            new_quote_button.place(x=180, y=380, anchor=tk.CENTER)

            def send_email():

                # send the email using the Courier API
                client = Courier(auth_token="pk_prod_JYRK4ZZ2F2MJM3NS1DFFCBQTFTRP") #You can use your own API Key

                resp = client.send_message(
                    message={
                        "to": {
                            "email": email,
                        },
                        "template": "43T1ARP3AWMNJHQ84Y0RCVVCDDFV",
                        "data": {
                            "body": [quote]
                        },
                    }
                )
                print(resp['requestId'])

            emailme_button = tk.Button(root3, text="Email Me!", command=send_email, font=("Montserrat", 12),
                                       bg='#16001e', fg="#ffffff", bd=0, highlightthickness=0, padx=23, pady=10,
                                       activebackground='#f7b2b7', activeforeground='#ffffff')
            emailme_button.place(x=180, y=435, anchor=tk.CENTER)

            root.destroy()
            root3.mainloop()
        else:
            # Display error message
            messagebox.showwarning("Error", "Incorrect email or password. Please try again or sign up if you haven't created an account.")

        # Close database connection
        cursor.close()
        db.close()

    sign_in_button.destroy()
    sign_up_button.destroy()

    # Add label and input for email
    email_label = tk.Label(root, text="Email:", font=catchphrase_font, fg='#ffffff', bg='#16001e', padx=31, pady=15)
    email_label.place(x=123, y=230, anchor='e')
    email_input = tk.Entry(root, width=30)
    email_input.place(x=email_label.winfo_width() + 130, y=220)

    # Add label and input for password
    password_label = tk.Label(root, text="Password:", font=catchphrase_font, fg='#ffffff', bg='#16001e', padx=16,
                              pady=15)
    password_label.place(x=123, y=290, anchor='e')
    password_input = tk.Entry(root, show='*', width=30)
    password_input.place(x=password_label.winfo_width() + 130, y=280)

    # Add submit button
    submit_button = tk.Button(root, text="Submit", font=catchphrase_font, fg='#ffffff', bg='#7f2982', padx=20, pady=5,
                              command=submit_signin)
    submit_button.place(x=130, y=340)

# declare global variables for the start and end colors of the gradient
start_color = "#ffffff"
end_color = "#f7b2b7"

# create the main window
root = tk.Tk()
root.title("StrongerToday")
root.geometry("360x640")
root.resizable(False, False)

# create a canvas widget
canvas = tk.Canvas(root, width=360, height=640)
canvas.pack()

# create font object
title_font = Font(family='Montserrat', size=28)
catchphrase_font = Font(family='Montserrat', size=12)
normal_font = Font(family='Montserrat', size=8)

# create a signin button
sign_in_button = tk.Button(root, text="Sign In", command=sign_in, font=catchphrase_font, fg='#ffffff', bg='#16001e', bd=0, highlightthickness=0, padx=20, pady=10, activebackground='#f7b2b7', activeforeground='#ffffff')
sign_in_button.config(width=10, height=1, borderwidth=0, relief="solid", highlightbackground="#16001e")

# create a signup button
sign_up_button = tk.Button(root, text="Sign Up", command=sign_up, font=catchphrase_font, fg='#ffffff', bg='#16001e', bd=0, highlightthickness=0, padx=20, pady=10, activebackground='#f7b2b7', activeforeground='#ffffff')
sign_up_button.config(width=10, height=1, borderwidth=0, relief="solid", highlightbackground="#16001e")

# place the buttons at the center of the app
sign_in_button.place(x=180, y=400, anchor=tk.CENTER)
sign_up_button.place(x=180, y=450, anchor=tk.CENTER)

# place the buttons at the center of the app
sign_in_button.place_forget()
sign_up_button.place_forget()

# add a label for the title
label1 = tk.Label(root, text="Stronger Today", font=title_font, fg='#ffffff', bg='#16001e', padx=35, pady=15)
label1.place(x=180, y=276, anchor=tk.CENTER)

# add a label for the catchphrase
label2 = tk.Label(root, text="Believe in yourself, and anything is possible!", font=catchphrase_font, fg='#de639a', bg='#16001e', padx=10, pady=10)
label2.place(x=180, y=317, anchor=tk.CENTER)

# draw a gradient background on the canvas
canvas.create_rectangle(0, 0, 360, 640, fill="", outline="")
for i in range(640):
    color = "#%02x%02x%02x" % (
        int((1-i/640)*int(start_color[1:3], 16) + i/640*int(end_color[1:3], 16)),
        int((1-i/640)*int(start_color[3:5], 16) + i/640*int(end_color[3:5], 16)),
        int((1-i/640)*int(start_color[5:], 16) + i/640*int(end_color[5:], 16))
    )
    canvas.create_line(0, i, 360, i, fill=color)

# create a button widget
button = tk.Button(root, text="Start Now", font=catchphrase_font, fg='#ffffff', bg='#16001e', bd=0, highlightthickness=0, command=start_now, padx=20, pady=10, activebackground='#f7b2b7', activeforeground='#ffffff')
button.config(width=10, height=1, borderwidth=0, relief="solid", highlightbackground="#16001e")
button.place(x=180, y=400, anchor=tk.CENTER)

# start the main event loop
root.mainloop()
