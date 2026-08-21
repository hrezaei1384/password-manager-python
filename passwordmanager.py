import json
import os
class Crypto:
    def __init__(self, key):
        self.key = key
    def encrypt_decrypt(self, text):
        result = ""
        for i in range(len(text)):
            char_code = ord(text[i]) ^ ord(self.key[i % len(self.key)])
            result += chr(char_code)
        return result
class PasswordManager:
    def __init__(self, key, filename="passwords.json"):
        self.key = key
        self.cipher = Crypto(key)
        self.encrypto = key + "_enc"
        self.decrypto = key + "_dec"
        self.filename = filename
        self.passwords = {}
        self.load_from_file()
    def load_from_file(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    self.passwords = json.load(f)
                print(f" Data loaded from {self.filename}")
            except Exception as e:
                print(f"Error loading file: {e}")
                self.passwords = {}
        else:
            print("No existing database found. Creating a new one.")
            self.passwords = {}
    def save_to_file(self):
        try:
            with open(self.filename, 'w') as f:
                json.dump(self.passwords, f, indent=4)
            print("[*] Changes saved successfully!")
        except Exception as e:
            print(f"[!] Error saving file: {e}")

    def add_password(self, website, username, password, email):
        encrypted_pw = self.cipher.encrypt_decrypt(password)
        self.passwords[website] = {"username": username, "email": email, "password": encrypted_pw}
        print(f"Saved password for {website}!")
        self.save_to_file()  
    def get_password(self, website):
        if website in self.passwords:
            encrypted_pw = self.passwords[website]["password"]
            decrypted_pw = self.cipher.encrypt_decrypt(encrypted_pw)
            username = self.passwords[website]["username"]
            print(f"\n Results ")
            print(f"Website: {website}\nUsername: {username}\nPassword: {decrypted_pw}")
        else:
            print("Error: Website not found!")
    def list_all(self):
        if not self.passwords:
            print("Your password list is empty. Enter a password: ")
        else:
            print("\n Saved Websites ")
            for website in self.passwords:
                print(f" {website}")
    def delete_password(self, website, username):
        if website in self.passwords:
           if self.passwords[website]["username"] == username:
            del self.passwords[website]
            print(f"Deleted password for {website}")
            self.save_to_file()  
           else:
               print("[-] Error: Incorrect username for this website!")
        else:
            print("[-] Error: Website not found!")
manager = PasswordManager("mykey")
while True:
    print("\n1. Add password")
    print("2. Get password")
    print("3. List websites")
    print("4. Delete password")
    print("5. Exit of website")
    choice = input("Choose an option: ")
    if choice == '1':
        site = input("Enter website name: ")
        username = input("Enter username: ")
        password = input("Enter password: ")
        email = input("Enter your email")
        manager.add_password(site, username, password, email)
    elif choice == '2':
        site = input("Enter website name: ")
        manager.get_password(site)
    elif choice == '3':
        manager.list_all()
    elif choice == '4':
        site = input("Enter website name")
        username = input("Enter a username")
        manager.delete_password(site, username)
    elif choice == '5':
        print("Goodbye!")
        break
    else:
        print("Invalid option! Try again.")




  























        

