import tkinter as tk
from tkinter import ttk, messagebox, font
from database import Database


class OscarDatabaseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Oscars Application")
        self.root.geometry("800x600")  # Larger window size

        # colors here
        self.bg_color = "#0A1929"  # navy blue background
        self.box_color = "#333333"  # dark grey for boxes
        self.text_color = "#FFFFFF"  # white for text
        self.button_bg = "#555555"  # light grey for buttons

        self.root.configure(bg=self.bg_color)

        # fonts
        self.title_font = font.Font(family="Helvetica", size=18, weight="bold")
        self.header_font = font.Font(family="Helvetica", size=14, weight="bold")
        self.normal_font = font.Font(family="Helvetica", size=12)
        self.button_font = font.Font(family="Helvetica", size=12)

        self.connection = None
        self.current_username = None
        self.db = None

        self.connect_to_db()

        self.create_login_frame()  # create the login frame

    def connect_to_db(self):  # forms connection with database
        self.db = Database()
        self.connection = self.db.connection

        if not self.connection or not self.connection.is_connected():
            messagebox.showerror(
                "Connection Error", "Failed to connect to the database"
            )
            self.root.destroy()

    def create_login_frame(self):  # funct that will create the login box/frame
        self.login_frame = tk.Frame(
            self.root, bg=self.box_color, bd=2, relief=tk.GROOVE
        )
        self.login_frame.place(
            relx=0.5, rely=0.5, anchor=tk.CENTER, width=400, height=300
        )

        tk.Label(
            self.login_frame,
            text="Oscars Application",
            font=self.title_font,
            bg=self.box_color,
            fg=self.text_color,
        ).pack(pady=20)

        tk.Label(
            self.login_frame,
            text="Username:",
            font=self.normal_font,
            bg=self.box_color,
            fg=self.text_color,
        ).pack(pady=5)
        self.username_entry = tk.Entry(
            self.login_frame,
            width=30,
            font=self.normal_font,
            bg="#555555",
            fg=self.text_color,
            insertbackground=self.text_color,
        )
        self.username_entry.pack(pady=5)

        button_frame = tk.Frame(self.login_frame, bg=self.box_color)
        button_frame.pack(pady=20)

        # login button
        self.login_button = tk.Button(
            button_frame,
            text="Login",
            command=self.login,
            font=self.button_font,
            bg="#FFFFFF",
            fg="#000000",
            width=15,
            height=1,
            activebackground="#45a049",
            activeforeground="#000000",
        )
        self.login_button.grid(row=0, column=0, padx=10)

        # register button
        self.register_button = tk.Button(
            button_frame,
            text="Register",
            command=self.register_user,
            font=self.button_font,
            bg="#FFFFFF",
            fg="#000000",
            width=15,
            height=1,
            activebackground="#45a049",
            activeforeground="#000000",
        )
        self.register_button.grid(row=0, column=1, padx=10)

    def login(self):  # function to handle login for user
        username = self.username_entry.get()

        if not username:
            messagebox.showerror("Error", "Please enter a username")
            return

        user = self.db.get_user(username)

        if user:
            messagebox.showinfo("Login Successful", f"Welcome, {username}!")
            self.show_main_menu(username)
        else:
            messagebox.showerror(
                "Login Failed", "User not found. Please register or try again."
            )

    def register_user(self):  # function to register a new user
        register_window = tk.Toplevel(self.root)
        register_window.title("Register New User")
        register_window.geometry("500x400")
        register_window.configure(bg=self.bg_color)

        register_frame = tk.Frame(
            register_window, bg=self.box_color, bd=2, relief=tk.GROOVE
        )
        register_frame.place(
            relx=0.5, rely=0.5, anchor=tk.CENTER, width=450, height=350
        )

        tk.Label(
            register_frame,
            text="Register New User",
            font=self.header_font,
            bg=self.box_color,
            fg=self.text_color,
        ).pack(pady=10)

        form_frame = tk.Frame(register_frame, bg=self.box_color)
        form_frame.pack(pady=10, padx=20, fill="both")

        tk.Label(
            form_frame,
            text="Email:",
            font=self.normal_font,
            bg=self.box_color,
            fg=self.text_color,
        ).grid(row=0, column=0, sticky="w", pady=8)
        email_entry = tk.Entry(
            form_frame,
            width=30,
            font=self.normal_font,
            bg="#555555",
            fg=self.text_color,
            insertbackground=self.text_color,
        )
        email_entry.grid(row=0, column=1, pady=8, padx=10)

        tk.Label(
            form_frame,
            text="Username:",
            font=self.normal_font,
            bg=self.box_color,
            fg=self.text_color,
        ).grid(row=1, column=0, sticky="w", pady=8)
        username_entry = tk.Entry(
            form_frame,
            width=30,
            font=self.normal_font,
            bg="#555555",
            fg=self.text_color,
            insertbackground=self.text_color,
        )
        username_entry.grid(row=1, column=1, pady=8, padx=10)

        tk.Label(
            form_frame,
            text="Birth Date (YYYY-MM-DD):",
            font=self.normal_font,
            bg=self.box_color,
            fg=self.text_color,
        ).grid(row=2, column=0, sticky="w", pady=8)
        birthdate_entry = tk.Entry(
            form_frame,
            width=30,
            font=self.normal_font,
            bg="#555555",
            fg=self.text_color,
            insertbackground=self.text_color,
        )
        birthdate_entry.grid(row=2, column=1, pady=8, padx=10)

        tk.Label(
            form_frame,
            text="Gender (M/F):",
            font=self.normal_font,
            bg=self.box_color,
            fg=self.text_color,
        ).grid(row=3, column=0, sticky="w", pady=8)
        gender_entry = tk.Entry(
            form_frame,
            width=30,
            font=self.normal_font,
            bg="#555555",
            fg=self.text_color,
            insertbackground=self.text_color,
        )
        gender_entry.grid(row=3, column=1, pady=8, padx=10)

        tk.Label(
            form_frame,
            text="Country:",
            font=self.normal_font,
            bg=self.box_color,
            fg=self.text_color,
        ).grid(row=4, column=0, sticky="w", pady=8)
        country_entry = tk.Entry(
            form_frame,
            width=30,
            font=self.normal_font,
            bg="#555555",
            fg=self.text_color,
            insertbackground=self.text_color,
        )
        country_entry.grid(row=4, column=1, pady=8, padx=10)

        def save_user():  # function that saves the user information in the database
            email = email_entry.get()
            username = username_entry.get()
            birthdate = birthdate_entry.get()
            gender = gender_entry.get()
            country = country_entry.get()

            if not email or not username or not birthdate or not gender or not country:
                messagebox.showerror(
                    "Error", "All fields are required", parent=register_window
                )
                return

            if gender.upper() not in ["M", "F"]:
                messagebox.showerror(
                    "Error", "Gender must be 'M' or 'F'", parent=register_window
                )
                return

            if self.db.add_user(email, username, birthdate, gender.upper(), country):
                messagebox.showinfo(
                    "Success", "User registered successfully!", parent=register_window
                )
                register_window.destroy()
            else:
                messagebox.showerror(
                    "Error",
                    "Failed to register user. Please try again.",
                    parent=register_window,
                )

        register_button = tk.Button(
            form_frame,
            text="Register",
            command=save_user,
            font=self.button_font,
            bg="#FFFFFF",
            fg="#000000",
            width=15,
            height=1,
            activebackground="#666666",
            activeforeground="#000000",
        )
        register_button.grid(row=5, column=0, columnspan=2, pady=20)

    def show_main_menu(self, username):  # main home page
        self.login_frame.place_forget()
        self.current_username = username

        self.main_menu_frame = tk.Frame(self.root, bg=self.bg_color)
        self.main_menu_frame.pack(pady=20, padx=20, fill="both", expand=True)

        title_frame = tk.Frame(self.main_menu_frame, bg=self.bg_color)
        title_frame.pack(fill="x", pady=10)

        tk.Label(
            title_frame,
            text="Main Dashboard",
            font=self.title_font,
            bg=self.bg_color,
            fg=self.text_color,
        ).pack(side=tk.TOP)

        tk.Label(
            title_frame,
            text=f"Welcome, {username}!",
            font=self.normal_font,
            bg=self.bg_color,
            fg=self.text_color,
        ).pack(side=tk.TOP, pady=5)

        button_frame = tk.Frame(self.main_menu_frame, bg=self.bg_color)
        button_frame.pack(fill="both", expand=True, pady=10)

        for i in range(3):
            button_frame.columnconfigure(i, weight=1)
        for i in range(3):
            button_frame.rowconfigure(i, weight=1)

        # functions for the different queries
        functions = [
            ("Add New Nomination", self.add_nomination),
            ("View My Nominations", self.view_my_nominations),
            ("Top User Nominated Movies", self.top_nominated_movies),
            ("Staff Member Stats", self.staff_member_stats),
            ("Top Birth Countries", self.top_birth_countries),
            ("Nominated Staff by Country", self.nominated_staff_by_country),
            ("Dream Team", self.dream_team),
            ("Top Production Companies", self.top_production_companies),
            ("Non-English Oscar Winners", self.non_english_winners),
        ]

        for i in range(3):
            button_frame.columnconfigure(i, weight=1)
        for i in range(3):
            button_frame.rowconfigure(i, weight=1)

        for i, (text, command) in enumerate(functions):
            row = i // 3
            col = i % 3

            button = tk.Button(
                button_frame,
                text=text,
                command=command,
                font=self.button_font,
                bg=self.button_bg,
                fg="#000000",
                activebackground="#666666",
                activeforeground="#000000",
            )
            button.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)

        bottom_frame = tk.Frame(self.main_menu_frame, bg=self.bg_color)
        bottom_frame.pack(fill="x", pady=10)

        logout_button = tk.Button(
            bottom_frame,
            text="Logout",
            command=self.logout,
            font=self.button_font,
            bg="#FFFFFF",
            fg="#000000",
            width=15,
            height=1,
            activebackground="#e53935",
            activeforeground="#000000",
        )
        logout_button.pack(pady=10)

        self.root.resizable(True, True)

    def logout(self):
        self.main_menu_frame.destroy()
        self.create_login_frame()
        self.current_username = None
        messagebox.showinfo("Logout", "You have been logged out!")

    def view_my_nominations(self):  # view my nomination
        user = self.db.get_user(self.current_username)
        if not user:
            messagebox.showerror("Error", "User information could not be retrieved.")
            return

        user_email = user["email"]

        nominations = self.db.get_user_nominations(
            user_email
        )  # call function to execute query

        nominations_window = tk.Toplevel(self.root)
        nominations_window.title("My Nominations")
        nominations_window.geometry("800x500")
        nominations_window.configure(bg=self.bg_color)

        content_frame = tk.Frame(
            nominations_window, bg=self.box_color, bd=2, relief=tk.GROOVE
        )
        content_frame.pack(padx=20, pady=20, fill="both", expand=True)

        tk.Label(
            content_frame,
            text="My Nominations",
            font=self.header_font,
            bg=self.box_color,
            fg=self.text_color,
        ).pack(pady=10)

        if not nominations:
            tk.Label(
                content_frame,
                text="No Nominations, Please Add a Nomination.",
                font=self.normal_font,
                bg=self.box_color,
                fg=self.text_color,
            ).pack(pady=20)
        else:
            table_frame = tk.Frame(content_frame, bg=self.box_color)
            table_frame.pack(padx=10, pady=10, fill="both", expand=True)

            headers = ["Movie Title", "Release Year", "Person", "Category", "Iteration"]

            for col, header in enumerate(headers):
                tk.Label(
                    table_frame,
                    text=header,
                    font=self.normal_font,
                    bg=self.box_color,
                    fg=self.text_color,
                    borderwidth=1,
                    relief="solid",
                    width=15,
                    padx=5,
                    pady=5,
                ).grid(row=0, column=col, sticky="nsew", padx=1, pady=1)

            for i in range(len(headers)):
                table_frame.columnconfigure(i, weight=1)

            for row_idx, nomination in enumerate(nominations, start=1):
                person_name = f"{nomination['firstName']} {nomination['lastName']}"

                data = [
                    nomination["movieTitle"],
                    nomination["releaseYear"],
                    person_name,
                    nomination["categoryName"],
                    nomination["iteration"],
                ]

                for col_idx, value in enumerate(data):
                    tk.Label(
                        table_frame,
                        text=str(value),
                        font=self.normal_font,
                        bg="#444444",
                        fg=self.text_color,
                        borderwidth=1,
                        relief="solid",
                        padx=5,
                        pady=5,
                    ).grid(row=row_idx, column=col_idx, sticky="nsew", padx=1, pady=1)

            for row_idx in range(1, len(nominations) + 1):
                bg_color = "#3A3A3A" if row_idx % 2 == 0 else "#444444"
                for col_idx in range(len(headers)):
                    table_frame.grid_slaves(row=row_idx, column=col_idx)[0].configure(
                        bg=bg_color
                    )

        close_button = tk.Button(
            content_frame,
            text="Close",
            command=nominations_window.destroy,
            font=self.button_font,
            bg=self.button_bg,
            fg="#000000",
            activebackground="#1e88e5",
            activeforeground="#000000",
            width=15,
        )
        close_button.pack(pady=15)

    def add_nomination(self):
        user = self.db.get_user(self.current_username)
        if not user:
            messagebox.showerror("Error", "User information could not be retrieved.")
            return

        user_email = user["email"]

        nomination_window = tk.Toplevel(self.root)
        nomination_window.title("Add New Nomination")
        nomination_window.geometry("600x500")
        nomination_window.configure(bg=self.bg_color)

        content_frame = tk.Frame(
            nomination_window, bg=self.box_color, bd=2, relief=tk.GROOVE
        )
        content_frame.pack(padx=20, pady=20, fill="both", expand=True)

        tk.Label(
            content_frame,
            text="Add New Nomination",
            font=self.header_font,
            bg=self.box_color,
            fg=self.text_color,
        ).pack(pady=10)

        form_frame = tk.Frame(content_frame, bg=self.box_color)
        form_frame.pack(padx=20, pady=10, fill="both")

        tk.Label(
            form_frame,
            text="Movie Title:",
            font=self.normal_font,
            bg=self.box_color,
            fg=self.text_color,
        ).grid(row=0, column=0, sticky="w", pady=8)
        movie_title_entry = tk.Entry(
            form_frame,
            width=30,
            font=self.normal_font,
            bg="#555555",
            fg=self.text_color,
            insertbackground=self.text_color,
        )
        movie_title_entry.grid(row=0, column=1, pady=8, padx=10)

        tk.Label(
            form_frame,
            text="Release Year:",
            font=self.normal_font,
            bg=self.box_color,
            fg=self.text_color,
        ).grid(row=1, column=0, sticky="w", pady=8)
        release_year_entry = tk.Entry(
            form_frame,
            width=30,
            font=self.normal_font,
            bg="#555555",
            fg=self.text_color,
            insertbackground=self.text_color,
        )
        release_year_entry.grid(row=1, column=1, pady=8, padx=10)

        tk.Label(
            form_frame,
            text="Person First Name:",
            font=self.normal_font,
            bg=self.box_color,
            fg=self.text_color,
        ).grid(row=2, column=0, sticky="w", pady=8)
        first_name_entry = tk.Entry(
            form_frame,
            width=30,
            font=self.normal_font,
            bg="#555555",
            fg=self.text_color,
            insertbackground=self.text_color,
        )
        first_name_entry.grid(row=2, column=1, pady=8, padx=10)

        tk.Label(
            form_frame,
            text="Person Last Name:",
            font=self.normal_font,
            bg=self.box_color,
            fg=self.text_color,
        ).grid(row=3, column=0, sticky="w", pady=8)
        last_name_entry = tk.Entry(
            form_frame,
            width=30,
            font=self.normal_font,
            bg="#555555",
            fg=self.text_color,
            insertbackground=self.text_color,
        )
        last_name_entry.grid(row=3, column=1, pady=8, padx=10)

        tk.Label(
            form_frame,
            text="Category Name:",
            font=self.normal_font,
            bg=self.box_color,
            fg=self.text_color,
        ).grid(row=4, column=0, sticky="w", pady=8)
        category_entry = tk.Entry(
            form_frame,
            width=30,
            font=self.normal_font,
            bg="#555555",
            fg=self.text_color,
            insertbackground=self.text_color,
        )
        category_entry.grid(row=4, column=1, pady=8, padx=10)

        tk.Label(
            form_frame,
            text="Iteration (e.g., 95th):",
            font=self.normal_font,
            bg=self.box_color,
            fg=self.text_color,
        ).grid(row=5, column=0, sticky="w", pady=8)
        iteration_entry = tk.Entry(
            form_frame,
            width=30,
            font=self.normal_font,
            bg="#555555",
            fg=self.text_color,
            insertbackground=self.text_color,
        )
        iteration_entry.grid(row=5, column=1, pady=8, padx=10)

        error_label = tk.Label(
            form_frame,
            text="",
            font=self.normal_font,
            bg=self.box_color,
            fg="#FF6B6B",
            wraplength=400,
        )
        error_label.grid(row=6, column=0, columnspan=2, pady=10)

        def validate_and_submit():  # ensures that all the fields are filled in correctly
            error_label.config(text="")

            movie_title = movie_title_entry.get().strip()
            release_year = release_year_entry.get().strip()
            first_name = first_name_entry.get().strip()
            last_name = last_name_entry.get().strip()
            category = category_entry.get().strip()
            iteration = iteration_entry.get().strip()

            if not (
                movie_title
                and release_year
                and first_name
                and last_name
                and category
                and iteration
            ):
                error_label.config(text="All fields are required.")
                return

            try:
                year_value = int(release_year)
                if (
                    year_value < 1900 or year_value > 2030
                ):  # due to constraint of year datatype
                    error_label.config(
                        text="Release year must be between 1900 and 2030."
                    )
                    return
            except ValueError:
                error_label.config(text="Release year must be a valid number.")
                return

            if not (
                iteration.endswith("th")
                or iteration.endswith("st")  # ensures iteration is correctly formatted
                or iteration.endswith("nd")
                or iteration.endswith("rd")
            ):
                error_label.config(
                    text="Iteration should end with 'th', 'st', 'nd', or 'rd' (e.g., '95th')."
                )
                return

            movie_exists = self.db.check_movie_exists(movie_title, release_year)
            if not movie_exists:
                error_label.config(
                    text="Movie not found in database. Please check the title and release year."
                )
                return

            person_exists = self.db.check_person_exists(first_name, last_name)
            if not person_exists:
                error_label.config(
                    text="Person not found in database. Please check the first and last name."
                )
                return

            try:
                success = self.db.add_nomination(  # function call to execute query to insert data in the user
                    movie_title,
                    release_year,
                    first_name,
                    last_name,
                    user_email,
                    category,
                    iteration,
                )

                if success:
                    messagebox.showinfo(
                        "Success",
                        "Nomination added successfully!",
                        parent=nomination_window,
                    )
                    nomination_window.destroy()
                else:
                    error_label.config(
                        text="Failed to add nomination. Please check your inputs."
                    )
            except Exception as e:
                error_label.config(text=f"Error: {str(e)}")

        buttons_frame = tk.Frame(content_frame, bg=self.box_color)
        buttons_frame.pack(pady=15)

        submit_button = tk.Button(
            buttons_frame,
            text="Submit",
            command=validate_and_submit,
            font=self.button_font,
            bg="#FFFFFF",
            fg="#000000",
            activebackground="#1e88e5",
            activeforeground="#000000",
            width=15,
        )
        submit_button.grid(row=0, column=0, padx=10)

        cancel_button = tk.Button(
            buttons_frame,
            text="Cancel",
            command=nomination_window.destroy,
            font=self.button_font,
            bg="#FFFFFF",
            fg="#000000",
            activebackground="#1e88e5",
            activeforeground="#000000",
            width=15,
        )

        cancel_button.grid(row=0, column=1, padx=10)

    def top_nominated_movies(
        self,
    ):  # function that retrieves the top nominated movies amongst the users
        top_movies = (
            self.db.get_top_nominated_movies_by_category_iteration()
        )  # execute query to fetch top nominated movie data

        if not top_movies:
            messagebox.showinfo("Info", "No nominations have been made by users yet.")
            return

        top_movies_window = tk.Toplevel(self.root)
        top_movies_window.title("Top User Nominated Movies")
        top_movies_window.geometry("800x600")
        top_movies_window.configure(bg=self.bg_color)

        content_frame = tk.Frame(
            top_movies_window, bg=self.box_color, bd=2, relief=tk.GROOVE
        )
        content_frame.pack(padx=20, pady=20, fill="both", expand=True)

        tk.Label(
            content_frame,
            text="Top Nominated Movies by Category & Iteration",
            font=self.header_font,
            bg=self.box_color,
            fg=self.text_color,
        ).pack(pady=10)

        table_frame = tk.Frame(content_frame, bg=self.box_color)
        table_frame.pack(padx=10, pady=10, fill="both", expand=True)

        headers = ["Movie Title", "Category", "Iteration", "Nomination Count"]

        for col, header in enumerate(headers):
            tk.Label(
                table_frame,
                text=header,
                font=self.normal_font,
                bg=self.box_color,
                fg=self.text_color,
                borderwidth=1,
                relief="solid",
                padx=5,
                pady=5,
            ).grid(row=0, column=col, sticky="nsew", padx=1, pady=1)

        for i in range(len(headers)):
            table_frame.columnconfigure(i, weight=1)

        for row_idx, movie in enumerate(top_movies, start=1):
            data = [
                movie["movieTitle"],
                movie["categoryName"],
                movie["iteration"],
                movie["nomination_count"],
            ]

            for col_idx, value in enumerate(data):
                tk.Label(
                    table_frame,
                    text=str(value),
                    font=self.normal_font,
                    bg="#444444",
                    fg=self.text_color,
                    borderwidth=1,
                    relief="solid",
                    padx=5,
                    pady=5,
                ).grid(row=row_idx, column=col_idx, sticky="nsew", padx=1, pady=1)

        for row_idx in range(1, len(top_movies) + 1):
            bg_color = "#3A3A3A" if row_idx % 2 == 0 else "#444444"
            for col_idx in range(len(headers)):
                table_frame.grid_slaves(row=row_idx, column=col_idx)[0].configure(
                    bg=bg_color
                )

        close_button = tk.Button(
            content_frame,
            text="Close",
            command=top_movies_window.destroy,
            font=self.button_font,
            bg=self.button_bg,
            fg="#000000",
            activebackground="#666666",
            activeforeground="#000000",
            width=15,
        )
        close_button.pack(pady=15)

    def staff_member_stats(self):
        stats_window = tk.Toplevel(self.root)
        stats_window.title("Staff Member Stats")
        stats_window.geometry("600x500")
        stats_window.configure(bg=self.bg_color)

        content_frame = tk.Frame(
            stats_window, bg=self.box_color, bd=2, relief=tk.GROOVE
        )
        content_frame.pack(padx=20, pady=20, fill="both", expand=True)

        tk.Label(
            content_frame,
            text="Staff Member Statistics",
            font=self.header_font,
            bg=self.box_color,
            fg=self.text_color,
        ).pack(pady=10)

        tk.Label(
            content_frame,
            text="(Singer, Composer, Director, Actor, Actress roles only)",
            font=self.normal_font,
            bg=self.box_color,
            fg=self.text_color,
        ).pack(pady=5)

        input_frame = tk.Frame(content_frame, bg=self.box_color)
        input_frame.pack(pady=10, fill="x")

        tk.Label(
            input_frame,
            text="First Name:",
            font=self.normal_font,
            bg=self.box_color,
            fg=self.text_color,
        ).grid(row=0, column=0, padx=5, pady=5, sticky="e")
        first_name_entry = tk.Entry(
            input_frame, font=self.normal_font, bg="#555555", fg=self.text_color
        )
        first_name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        tk.Label(
            input_frame,
            text="Last Name:",
            font=self.normal_font,
            bg=self.box_color,
            fg=self.text_color,
        ).grid(row=1, column=0, padx=5, pady=5, sticky="e")
        last_name_entry = tk.Entry(
            input_frame, font=self.normal_font, bg="#555555", fg=self.text_color
        )
        last_name_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        results_frame = tk.Frame(content_frame, bg=self.box_color)
        results_frame.pack(pady=10, fill="both", expand=True)

        def fetch_stats():
            for widget in results_frame.winfo_children():
                widget.destroy()

            first_name = first_name_entry.get().strip()
            last_name = last_name_entry.get().strip()

            if not first_name or not last_name:
                messagebox.showerror(
                    "Error", "Please enter both first name and last name."
                )
                return

            person_exists = self.db.check_person_exists(
                first_name, last_name
            )  # first call function to validate if person exists in database
            if not person_exists:
                tk.Label(
                    results_frame,
                    text=f"No person found with name {first_name} {last_name}.",
                    font=self.normal_font,
                    bg=self.box_color,
                    fg="#FF6B6B",
                ).pack(pady=10)
                return

            stats = self.db.get_staff_member_stats(
                first_name, last_name
            )  # call function to execute query

            if not stats:
                tk.Label(
                    results_frame,
                    text=f"{first_name} {last_name} has no roles as Singer, Composer, Director, Actor, or Actress.",
                    font=self.normal_font,
                    bg=self.box_color,
                    fg=self.text_color,
                ).pack(pady=10)
            else:
                table_frame = tk.Frame(results_frame, bg=self.box_color)
                table_frame.pack(padx=10, pady=10, fill="both", expand=True)

                headers = ["Role", "Total Nominations", "Total Oscars"]
                for col, header in enumerate(headers):
                    tk.Label(
                        table_frame,
                        text=header,
                        font=self.normal_font,
                        bg=self.box_color,
                        fg=self.text_color,
                        borderwidth=1,
                        relief="solid",
                        padx=5,
                        pady=5,
                    ).grid(row=0, column=col, sticky="nsew", padx=1, pady=1)

                for row, stat in enumerate(stats, start=1):
                    role_type = stat["roleType"]
                    nominations = stat["total_nominations"]
                    oscars = stat["total_oscars"]

                    tk.Label(
                        table_frame,
                        text=role_type,
                        font=self.normal_font,
                        bg="#444444",
                        fg=self.text_color,
                        borderwidth=1,
                        relief="solid",
                        padx=5,
                        pady=5,
                    ).grid(row=row, column=0, sticky="nsew", padx=1, pady=1)
                    tk.Label(
                        table_frame,
                        text=str(nominations),
                        font=self.normal_font,
                        bg="#444444",
                        fg=self.text_color,
                        borderwidth=1,
                        relief="solid",
                        padx=5,
                        pady=5,
                    ).grid(row=row, column=1, sticky="nsew", padx=1, pady=1)
                    tk.Label(
                        table_frame,
                        text=str(oscars),
                        font=self.normal_font,
                        bg="#444444",
                        fg=self.text_color,
                        borderwidth=1,
                        relief="solid",
                        padx=5,
                        pady=5,
                    ).grid(row=row, column=2, sticky="nsew", padx=1, pady=1)

                for row_idx in range(1, len(stats) + 1):
                    bg_color = "#3A3A3A" if row_idx % 2 == 0 else "#444444"
                    for col_idx in range(len(headers)):
                        table_frame.grid_slaves(row=row_idx, column=col_idx)[
                            0
                        ].configure(bg=bg_color)

                # total_nominations = sum(stat['total_nominations'] for stat in stats)
                # total_oscars = sum(stat['total_oscars'] for stat in stats)

        fetch_button = tk.Button(
            content_frame,
            text="Fetch Stats",
            command=fetch_stats,
            font=self.button_font,
            bg="#FFFFFF",
            fg="#000000",
            activebackground="#666666",
            activeforeground="#000000",
        )
        fetch_button.pack(pady=10)

        close_button = tk.Button(
            content_frame,
            text="Close",
            command=stats_window.destroy,
            font=self.button_font,
            bg=self.button_bg,
            fg="#000000",
            activebackground="#666666",
            activeforeground="#000000",
        )
        close_button.pack(pady=10)

    def top_birth_countries(self):
        top_countries = (
            self.db.get_top_birth_countries_for_best_actor()
        )  # execute query to get top birth countries for best actor winners

        if not top_countries:
            messagebox.showinfo("Information", "No data found for Best Actor winners.")
            return

        countries_window = tk.Toplevel(self.root)
        countries_window.title("Top Birth Countries - Best Actor Winners")
        countries_window.geometry("600x500")
        countries_window.configure(bg=self.bg_color)

        content_frame = tk.Frame(
            countries_window, bg=self.box_color, bd=2, relief=tk.GROOVE
        )
        content_frame.pack(padx=20, pady=20, fill="both", expand=True)

        tk.Label(
            content_frame,
            text="Top 5 Birth Countries for Best Actor Winners",
            font=self.header_font,
            bg=self.box_color,
            fg=self.text_color,
        ).pack(pady=10)

        table_frame = tk.Frame(content_frame, bg=self.box_color)
        table_frame.pack(padx=10, pady=10, fill="both", expand=True)

        headers = ["Country", "Number of Winners"]

        for i in range(len(headers)):
            table_frame.columnconfigure(i, weight=1)

        for row_idx, country in enumerate(top_countries, start=1):
            tk.Label(
                table_frame,
                text=country["birthCountry"] or "Unknown",
                font=self.normal_font,
                bg="#444444",
                fg=self.text_color,
                borderwidth=1,
                relief="solid",
                padx=5,
                pady=5,
            ).grid(row=row_idx, column=0, sticky="nsew", padx=1, pady=1)

            tk.Label(
                table_frame,
                text=str(country["winner_count"]),
                font=self.normal_font,
                bg="#444444",
                fg=self.text_color,
                borderwidth=1,
                relief="solid",
                padx=5,
                pady=5,
            ).grid(row=row_idx, column=1, sticky="nsew", padx=1, pady=1)

        close_button = tk.Button(
            content_frame,
            text="Close",
            command=countries_window.destroy,
            font=self.button_font,
            bg=self.button_bg,
            fg="#000000",
            activebackground="#666666",
            activeforeground="#000000",
            width=15,
        )
        close_button.pack(pady=0)

    def nominated_staff_by_country(self):
        country_window = tk.Toplevel(self.root)
        country_window.title("Nominated Staff by Country")
        country_window.geometry("900x600")
        country_window.configure(bg=self.bg_color)

        content_frame = tk.Frame(
            country_window, bg=self.box_color, bd=2, relief=tk.GROOVE
        )
        content_frame.pack(padx=20, pady=20, fill="both", expand=True)

        tk.Label(
            content_frame,
            text="Nominated Staff Members by Country",
            font=self.header_font,
            bg=self.box_color,
            fg=self.text_color,
        ).pack(pady=10)

        input_frame = tk.Frame(content_frame, bg=self.box_color)
        input_frame.pack(pady=10, fill="x")

        tk.Label(
            input_frame,
            text="Enter Country:",
            font=self.normal_font,
            bg=self.box_color,
            fg=self.text_color,
        ).pack(side=tk.LEFT, padx=10)
        country_entry = tk.Entry(
            input_frame,
            font=self.normal_font,
            bg="#555555",
            fg=self.text_color,
            width=30,
        )
        country_entry.pack(side=tk.LEFT, padx=10)

        results_container = tk.Frame(content_frame, bg=self.box_color)
        results_container.pack(pady=10, fill="both", expand=True)

        canvas = tk.Canvas(results_container, bg=self.box_color, highlightthickness=0)
        scrollbar = tk.Scrollbar(
            results_container, orient="vertical", command=canvas.yview
        )
        results_frame = tk.Frame(canvas, bg=self.box_color)

        results_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=results_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        def fetch_staff():
            for widget in results_frame.winfo_children():
                widget.destroy()

            country = country_entry.get().strip()

            if not country:
                messagebox.showerror("Error", "Please enter a country name.")
                return

            staff_members = self.db.get_nominated_staff_by_country(
                country
            )  # execute query to get nominated staff members by country

            if not staff_members:  # handle possible error
                tk.Label(
                    results_frame,
                    text=f"No nominated staff members found from {country}.",
                    font=self.normal_font,
                    bg=self.box_color,
                    fg=self.text_color,
                ).pack(pady=10)
                return

            headers = ["Name", "Categories", "Nominations", "Oscars"]
            header_frame = tk.Frame(results_frame, bg=self.box_color)
            header_frame.pack(fill="x", pady=5)

            col_widths = [200, 600, 100, 100]

            for col, header in enumerate(headers):
                tk.Label(
                    header_frame,
                    text=header,
                    font=self.normal_font,
                    bg=self.box_color,
                    fg=self.text_color,
                    borderwidth=1,
                    relief="solid",
                    width=col_widths[col] // 10,
                    padx=5,
                    pady=5,
                ).grid(row=0, column=col, sticky="nsew", padx=1, pady=1)

            for row_idx, staff in enumerate(staff_members, start=1):
                row_frame = tk.Frame(
                    results_frame, bg="#444444" if row_idx % 2 == 0 else "#3A3A3A"
                )
                row_frame.pack(fill="x", pady=1)

                name = f"{staff['firstName']} {staff['lastName']}"
                name_label = tk.Label(
                    row_frame,
                    text=name,
                    font=self.normal_font,
                    bg=row_frame["bg"],
                    fg=self.text_color,
                    borderwidth=1,
                    relief="solid",
                    anchor="w",
                    width=col_widths[0] // 10,
                    padx=5,
                    pady=5,
                )
                name_label.grid(row=0, column=0, sticky="nsew", padx=1)

                categories_text = staff["categories"]
                categories_label = tk.Label(
                    row_frame,
                    text=categories_text,
                    font=self.normal_font,
                    bg=row_frame["bg"],
                    fg=self.text_color,
                    borderwidth=1,
                    relief="solid",
                    anchor="w",
                    width=col_widths[1] // 10,
                    padx=5,
                    pady=5,
                    wraplength=380,
                )
                categories_label.grid(row=0, column=1, sticky="nsew", padx=1)

                nominations_label = tk.Label(
                    row_frame,
                    text=str(staff["nomination_count"]),
                    font=self.normal_font,
                    bg=row_frame["bg"],
                    fg=self.text_color,
                    borderwidth=1,
                    relief="solid",
                    width=col_widths[2] // 10,
                    padx=5,
                    pady=5,
                )
                nominations_label.grid(row=0, column=2, sticky="nsew", padx=1)

                oscars_label = tk.Label(
                    row_frame,
                    text=str(staff["oscar_count"]),
                    font=self.normal_font,
                    bg=row_frame["bg"],
                    fg=self.text_color,
                    borderwidth=1,
                    relief="solid",
                    width=col_widths[3] // 10,
                    padx=5,
                    pady=5,
                )
                oscars_label.grid(row=0, column=3, sticky="nsew", padx=1)

        fetch_button = tk.Button(
            input_frame,
            text="Search",
            command=fetch_staff,
            font=self.button_font,
            bg="#FFFFFF",
            fg="#000000",
            activebackground="#666666",
            activeforeground="#000000",
        )
        fetch_button.pack(side=tk.LEFT, padx=10)

        close_button = tk.Button(
            content_frame,
            text="Close",
            command=country_window.destroy,
            font=self.button_font,
            bg=self.button_bg,
            fg="#000000",
            activebackground="#666666",
            activeforeground="#000000",
            width=15,
        )
        close_button.pack(pady=15)

    def top_production_companies(self):
        top_companies = (
            self.db.get_top_production_companies()
        )  # executes query to retrieve production companies info

        if not top_companies:
            messagebox.showinfo(
                "Information", "No data found for production companies with Oscar wins."
            )
            return

        companies_window = tk.Toplevel(self.root)
        companies_window.title("Top 5 Production Companies by Oscar Wins")
        companies_window.geometry("600x400")
        companies_window.configure(bg=self.bg_color)

        content_frame = tk.Frame(
            companies_window, bg=self.box_color, bd=2, relief=tk.GROOVE
        )
        content_frame.pack(padx=20, pady=20, fill="both", expand=True)

        tk.Label(
            content_frame,
            text="Top 5 Production Companies by Oscar Wins",
            font=self.header_font,
            bg=self.box_color,
            fg=self.text_color,
        ).pack(pady=10)

        table_frame = tk.Frame(content_frame, bg=self.box_color)
        table_frame.pack(padx=10, pady=10, fill="both", expand=True)

        headers = ["Rank", "Company Name", "Oscar Wins"]

        for col, header in enumerate(headers):
            tk.Label(
                table_frame,
                text=header,
                font=self.normal_font,
                bg=self.box_color,
                fg=self.text_color,
                borderwidth=1,
                relief="solid",
                padx=5,
                pady=5,
            ).grid(row=0, column=col, sticky="nsew", padx=1, pady=1)

        for i in range(len(headers)):
            table_frame.columnconfigure(i, weight=1)

        for rank, company in enumerate(top_companies, start=1):
            tk.Label(
                table_frame,
                text=str(rank),
                font=self.normal_font,
                bg="#444444",
                fg=self.text_color,
                borderwidth=1,
                relief="solid",
                padx=5,
                pady=5,
            ).grid(row=rank, column=0, sticky="nsew", padx=1, pady=1)

            tk.Label(
                table_frame,
                text=company["companyName"],
                font=self.normal_font,
                bg="#444444",
                fg=self.text_color,
                borderwidth=1,
                relief="solid",
                padx=5,
                pady=5,
            ).grid(row=rank, column=1, sticky="nsew", padx=1, pady=1)

            tk.Label(
                table_frame,
                text=str(company["oscar_count"]),
                font=self.normal_font,
                bg="#444444",
                fg=self.text_color,
                borderwidth=1,
                relief="solid",
                padx=5,
                pady=5,
            ).grid(row=rank, column=2, sticky="nsew", padx=1, pady=1)

        close_button = tk.Button(
            content_frame,
            text="Close",
            command=companies_window.destroy,
            font=self.button_font,
            bg=self.button_bg,
            fg="#000000",
            activebackground="#666666",
            activeforeground="#000000",
            width=15,
        )
        close_button.pack(pady=15)

    def non_english_winners(self):
        non_english_movies = (
            self.db.get_non_english_oscar_winners()
        )  # executes query to retrieve info on non english oscar winners

        if not non_english_movies:
            messagebox.showinfo(
                "Information", "No non-English movies with Oscar wins found."
            )
            return

        movies_window = tk.Toplevel(self.root)
        movies_window.title("Non-English Oscar-Winning Movies")
        movies_window.geometry("700x500")
        movies_window.configure(bg=self.bg_color)

        content_frame = tk.Frame(
            movies_window, bg=self.box_color, bd=2, relief=tk.GROOVE
        )
        content_frame.pack(padx=20, pady=20, fill="both", expand=True)

        tk.Label(
            content_frame,
            text="Non-English Movies That Won Oscars",
            font=self.header_font,
            bg=self.box_color,
            fg=self.text_color,
        ).pack(pady=10)

        list_container = tk.Frame(content_frame, bg=self.box_color)
        list_container.pack(padx=10, pady=10, fill="both", expand=True)

        canvas = tk.Canvas(list_container, bg=self.box_color, highlightthickness=0)
        scrollbar = tk.Scrollbar(
            list_container, orient="vertical", command=canvas.yview
        )
        scrollable_frame = tk.Frame(canvas, bg=self.box_color)

        scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        headers_frame = tk.Frame(scrollable_frame, bg=self.box_color)
        headers_frame.pack(fill="x", pady=5)

        headers = ["Movie Title", "Release Year", "Language"]
        col_widths = [350, 100, 150]

        for col, header in enumerate(headers):
            tk.Label(
                headers_frame,
                text=header,
                font=self.normal_font,
                bg=self.box_color,
                fg=self.text_color,
                borderwidth=1,
                relief="solid",
                width=col_widths[col] // 10,
                padx=5,
                pady=5,
            ).grid(row=0, column=col, sticky="nsew", padx=1, pady=1)

        for row_idx, movie in enumerate(non_english_movies, start=1):
            row_frame = tk.Frame(
                scrollable_frame, bg="#444444" if row_idx % 2 == 0 else "#3A3A3A"
            )
            row_frame.pack(fill="x", pady=1)

            tk.Label(
                row_frame,
                text=movie["movieTitle"],
                font=self.normal_font,
                bg=row_frame["bg"],
                fg=self.text_color,
                borderwidth=1,
                relief="solid",
                width=col_widths[0] // 10,
                padx=5,
                pady=5,
                anchor="w",
            ).grid(row=0, column=0, sticky="nsew", padx=1)

            tk.Label(
                row_frame,
                text=str(movie["releaseYear"]),
                font=self.normal_font,
                bg=row_frame["bg"],
                fg=self.text_color,
                borderwidth=1,
                relief="solid",
                width=col_widths[1] // 10,
                padx=5,
                pady=5,
            ).grid(row=0, column=1, sticky="nsew", padx=1)

            tk.Label(
                row_frame,
                text=movie["language"],
                font=self.normal_font,
                bg=row_frame["bg"],
                fg=self.text_color,
                borderwidth=1,
                relief="solid",
                width=col_widths[2] // 10,
                padx=5,
                pady=5,
            ).grid(row=0, column=2, sticky="nsew", padx=1)

        language_counts = {}
        for movie in non_english_movies:
            language = movie["language"]
            language_counts[language] = language_counts.get(language, 0) + 1

        close_button = tk.Button(
            content_frame,
            text="Close",
            command=movies_window.destroy,
            font=self.button_font,
            bg=self.button_bg,
            fg="#000000",
            activebackground="#666666",
            activeforeground="#000000",
            width=15,
        )
        close_button.pack(pady=15)

    def dream_team(self):
        dream_team = self.db.get_dream_team()  # execute dream team query

        if not dream_team:
            messagebox.showinfo("Information", "Could not retrieve Dream Team data.")
            return

        dream_team_window = tk.Toplevel(self.root)
        dream_team_window.title("Oscar Dream Team")
        dream_team_window.geometry("700x600")
        dream_team_window.configure(bg=self.bg_color)

        content_frame = tk.Frame(
            dream_team_window, bg=self.box_color, bd=2, relief=tk.GROOVE
        )
        content_frame.pack(padx=20, pady=20, fill="both", expand=True)

        tk.Label(
            content_frame,
            text="The Oscar Dream Team",
            font=self.title_font,
            bg=self.box_color,
            fg=self.text_color,
        ).pack(pady=10)

        tk.Label(
            content_frame,
            text="The living cast members that can create the best movie ever",
            font=self.normal_font,
            bg=self.box_color,
            fg=self.text_color,
        ).pack(pady=5)

        team_frame = tk.Frame(content_frame, bg=self.box_color)
        team_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # roles that make up the dream team
        roles = [
            "Director",
            "Leading Actor",
            "Leading Actress",
            "Supporting Actor",
            "Supporting Actress",
            "Producer",
            "Composer",
        ]

        headers = ["Role", "Name", "Oscar Wins"]
        for col, header in enumerate(headers):
            tk.Label(
                team_frame,
                text=header,
                font=self.normal_font,
                bg=self.box_color,
                fg=self.text_color,
                borderwidth=1,
                relief="solid",
                padx=5,
                pady=5,
            ).grid(row=0, column=col, sticky="nsew", padx=1, pady=1)

        for i in range(len(headers)):
            team_frame.columnconfigure(i, weight=1)

        row_idx = 1
        for role in roles:
            if role in dream_team:
                member = dream_team[role]
                name = f"{member['firstName']} {member['lastName']}"

                tk.Label(
                    team_frame,
                    text=role,
                    font=self.normal_font,
                    bg="#444444",
                    fg=self.text_color,
                    borderwidth=1,
                    relief="solid",
                    padx=5,
                    pady=5,
                ).grid(row=row_idx, column=0, sticky="nsew", padx=1, pady=1)

                tk.Label(
                    team_frame,
                    text=name,
                    font=self.normal_font,
                    bg="#444444",
                    fg=self.text_color,
                    borderwidth=1,
                    relief="solid",
                    padx=5,
                    pady=5,
                ).grid(row=row_idx, column=1, sticky="nsew", padx=1, pady=1)

                tk.Label(
                    team_frame,
                    text=str(member["oscar_count"]),
                    font=self.normal_font,
                    bg="#444444",
                    fg=self.text_color,
                    borderwidth=1,
                    relief="solid",
                    padx=5,
                    pady=5,
                ).grid(row=row_idx, column=2, sticky="nsew", padx=1, pady=1)

                row_idx += 1

        for row_idx in range(1, len(dream_team) + 1):
            bg_color = "#3A3A3A" if row_idx % 2 == 0 else "#444444"
            for col_idx in range(len(headers)):
                team_frame.grid_slaves(row=row_idx, column=col_idx)[0].configure(
                    bg=bg_color
                )

        description_frame = tk.Frame(content_frame, bg=self.box_color)
        description_frame.pack(padx=10, pady=10, fill="x")

        close_button = tk.Button(
            content_frame,
            text="Close",
            command=dream_team_window.destroy,
            font=self.button_font,
            bg=self.button_bg,
            fg="#000000",
            activebackground="#666666",
            activeforeground="#000000",
            width=15,
        )
        close_button.pack(pady=15)
