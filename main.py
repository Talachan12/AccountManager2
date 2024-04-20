import customtkinter
import mysql.connector

class Window():
    def __init__(self):


        customtkinter.set_appearance_mode("light")
        customtkinter.set_default_color_theme("green")

        self.root = customtkinter.CTk()
        self.root.geometry("500x350")

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


        # Store Management
        # Store button
        self.create_store_button = customtkinter.CTkButton(master=self.frame, text="Create a store")
        self.manage_saved_store = customtkinter.CTkButton(master=self.frame, text="Manage saved store")
        # Store entry
        self.create_store_entry = customtkinter.CTkEntry(master=self.frame, placeholder_text="Store name")
        # Store label
        self.store_label = customtkinter.CTkLabel(master=self.frame, text="Please provide a name of the store")



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

            cursor.execute("SELECT password FROM users_info WHERE username = %s", (username,))
            result = cursor.fetchone()

            # Sprawdź czy użytkownik istnieje i czy hasło się zgadza
            if result and result[0] == password:
                print("Login successful!")
                self.label.configure(text="Logged Successfully!")
                self.entry1.pack_forget()
                self.entry2.pack_forget()
                self.checkbox.pack_forget()
                self.login_button.pack_forget()
                self.register_button.pack_forget()
                self.create_store_button.pack(pady=12, padx=10)
                self.manage_saved_store.pack(pady=12, padx=10)
                self.back_button = customtkinter.CTkButton(master=self.frame, text="Back", command=self.back_to_main_menu)
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
        self.manage_saved_store.pack_forget()
        self.create_store_button.pack_forget()


    def register(self):
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

            sql = "INSERT INTO users_info (username, password) VALUES (%s, %s)"
            cursor.execute(sql, (username, password))
            conn.commit()
            self.label.configure(text="Registered successfully")
            print("Registered")

        except mysql.connector.Error as e:
            print(f"Error: {e}")

    def create_store(self):
        self.label.configure(text="Please provide a name of the store")

    def add_product(self):
        self.label.configure(text="Please provide a name and quantity of a product")




if __name__ == "__main__":
    window = Window()
    window.root.mainloop()
