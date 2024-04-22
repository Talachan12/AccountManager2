import customtkinter
import mysql.connector

class Window():
    def __init__(self):

        # Logged user id container

        self.logged_user_id = None

        # Appearance settings
        customtkinter.set_appearance_mode("light")
        customtkinter.set_default_color_theme("green")

        # Window settings
        self.root = customtkinter.CTk()
        self.root.geometry("500x350")
        self.root.title("Login System 1.0")
        self.frame = customtkinter.CTkFrame(master=self.root)
        self.frame.pack(pady=20, padx=60, fill="both", expand=True)

        # Main label
        self.label = customtkinter.CTkLabel(master=self.frame, text="Login System")
        self.label.pack(pady=12, padx=10)

        # Username entry
        self.entry1 = customtkinter.CTkEntry(master=self.frame, placeholder_text="Username")
        self.entry1.pack(pady=12, padx=10)

        # Password entry
        self.entry2 = customtkinter.CTkEntry(master=self.frame, placeholder_text="Password", show="*")
        self.entry2.pack(pady=12, padx=10)

        # Login button
        self.login_button = customtkinter.CTkButton(master=self.frame, text="Login", command=self.login)
        self.login_button.pack(pady=12, padx=10)

        # Register button
        self.register_button = customtkinter.CTkButton(master=self.frame, text="Register", command=self.register)
        self.register_button.pack(pady=12, padx=10)

        # Checkbox
        self.checkbox = customtkinter.CTkCheckBox(master=self.frame, text="Remember me")
        self.checkbox.pack(pady=12, padx=10)

        # Back Button
        self.back_button = customtkinter.CTkButton(master=self.frame, text="Back", command=self.back_to_main_menu)


        # Store Management
        # Store buttons
        self.create_store_button = customtkinter.CTkButton(master=self.frame, text="Create a store", command=self.create_store)
        self.manage_store_button = customtkinter.CTkButton(master=self.frame, text="Manage saved store", command=self.manage_store_button)
        self.add_store_database = customtkinter.CTkButton(master=self.frame, text="Confirm", command=self.store_database_add)

        # Store entries
        self.store_name_entry = customtkinter.CTkEntry(master=self.frame, placeholder_text="Store name")






    def login(self):
        # Pobierz nazwę użytkownika i hasło wprowadzone przez użytkownika
        username = self.entry1.get()
        password = self.entry2.get()

        # Połącz się z bazą danych
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="misiek123",
                database="users",
            )

            cursor = conn.cursor()

            cursor.execute("SELECT user_id FROM users_info WHERE username = %s AND password = %s", (username, password))
            result = cursor.fetchone()

            # Sprawdź czy użytkownik istnieje i czy hasło się zgadza
            if result:
                self.logged_user_id = result[0]
                print(f"Logged as user_id: {self.logged_user_id} ")
                self.label.configure(text=f"Logged successfully as {username}!")
                self.entry1.pack_forget()
                self.entry2.pack_forget()
                self.checkbox.pack_forget()
                self.login_button.pack_forget()
                self.register_button.pack_forget()
                self.create_store_button.pack(pady=12, padx=10)
                self.manage_store_button.pack(pady=12, padx=10)
                self.back_button.pack(pady=12, padx=10)

            else:
                print("Invalid username or password")
                self.label.configure(text="Invalid username or password")

        except mysql.connector.Error as e:
            print(f"Error connecting to MySQL: {e}")


    def back_to_main_menu(self):
        self.label.configure(text="Login System")
        self.back_button.pack_forget()
        self.entry1.delete(0, 'end')
        self.entry2.delete(0,'end')
        self.entry1.pack(pady=12, padx=10)
        self.entry2.pack(pady=12, padx=10)
        self.login_button.pack(pady=12, padx=10)
        self.register_button.pack(pady=12, padx=10)
        self.checkbox.pack(pady=12, padx=10)
        self.manage_store_button.pack_forget()
        self.create_store_button.pack_forget()

    def back_to_logged_panel(self):
        self.label.configure(text=f"Logged as {self.entry1.get()}")
        self.store_name_entry.pack_forget()
        self.add_store_database.pack_forget()
        self.back_button.pack_forget()
        self.entry1.pack_forget()
        self.entry2.pack_forget()
        self.checkbox.pack_forget()
        self.login_button.pack_forget()
        self.register_button.pack_forget()
        self.create_store_button.pack(pady=12, padx=10)
        self.manage_store_button.pack(pady=12, padx=10)
        self.back_button.configure(text="Back", command=self.back_to_main_menu)
        self.back_button.pack(pady=12, padx=10)


    def register(self):
        # Collecting username and password
        username = self.entry1.get()
        password = self.entry2.get()

        # Connecting to the database
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="misiek123",
                database="users",
            )
            cursor = conn.cursor()

            sql = "INSERT INTO users_info (username, password) VALUES (%s, %s)"
            cursor.execute(sql, (username, password))
            conn.commit()
            self.label.configure(text="Registered successfully")
            print("Registered")

        except mysql.connector.Error as e:
            print(f"Error: {e}")

        finally:
            cursor.close()
            conn.close()
            print("Connection closed")

    # Create store config
    def create_store(self):
        # Create store GUI
        self.label.configure(text="Please provide a name of the store")
        self.store_name_entry.pack()
        self.back_button.pack_forget()
        self.add_store_database.pack(pady=12, padx=10)
        self.back_button.configure(text="Back to logged panel", command=self.back_to_logged_panel)
        self.back_button.pack()
        self.create_store_button.pack_forget()
        self.manage_store_button.pack_forget()


    def store_database_add(self):
        # Adding store name to the database

        store_name = self.store_name_entry.get()

        if self.logged_user_id is not None:
            # If user is logged, store can be created on his account
            try:
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="misiek123",
                    database="users",
                )
                cursor = conn.cursor()

                cursor.execute("INSERT INTO store_info (store_name, user_info_id) VALUES (%s, %s)",
                               (store_name, self.logged_user_id))
                conn.commit()
                print(f"Created store: {store_name}")
                self.label.configure(text="Store created successfully!")
                self.store_name_entry.pack_forget()
                self.add_store_database.pack_forget()

            except mysql.connector.Error as e:
                print(f"Error: {e}")

        else:
            print("User is not logged in")


    # Manage store config

    def manage_store_button(self):
        self.label.configure(text="Work in progress")



if __name__ == "__main__":
    window = Window()
    window.root.mainloop()
