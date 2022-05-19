### pgma_v01.py ###

import string
from pathlib import Path
from enum import Enum
from random import randint, shuffle, choice
from tkinter import *
from tkinter import messagebox
import random
import hashlib
import pyperclip
from datetime import datetime
import yaml


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


NAVY = '#0A043C'
WHITE = '#FFFFFF'
BLACK = '#000000'
GREEN = '#00FF00'

class PasswordError(Exception):
    __module__ = Exception.__module__


# Types of characters possible
class PasswordGenerator(Enum):
    CAP = 'CAP'  # Capital
    SMA = 'SMA'  # Small
    DIG = 'DIG'  # Digits
    SPE = 'SPE'  # Special


# Characters for each type of possible characters
type_chars = {
    PasswordGenerator.CAP: string.ascii_uppercase,
    PasswordGenerator.SMA: string.ascii_lowercase,
    PasswordGenerator.DIG: string.digits,
    PasswordGenerator.SPE: '!()-.?[]_`~;:@#$%^&*='
}

class PasswordGeneratorUI():
    def __init__(self, email="Team9_email@gmail.com", site=""):
        self.email = email
        self.site = site
        self.window = Tk()
        self.window.title("Password Generator & App Management (Team 9)")
        icon = PhotoImage(file='logo.png')
        self.window.iconphoto(True, icon)
        self.window.config(padx=50, pady=50, bg=NAVY)

# ---------------------------- PASSWORD GENERATOR ------------------------------- #

    def PasswordGenerator(self):
        letters = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        numbers = list('0123456789')
        symbols = list('!@#$%^&*()_+')
        letters_lower = list(map(str.lower, letters))
        letters.extend(letters_lower)

        length = self.scale_bar.get()

        # Return a number between a and b (both included):

        num_letters = random.randint(1, int(length/2))  # num_letters=5 -> 8 characters; else num_letters=13 -> 16 characters; BUT INCONSISTENT
        num_numbers = random.randint(1, length-num_letters-2)
        num_symbols = length - num_letters - num_numbers

        # Creating password and concat to a list
        rand_letters = [random.choice(letters) for i in range(num_letters)]
        rand_numbers = [random.choice(numbers) for i in range(num_numbers)]
        rand_symbols = [random.choice(symbols) for i in range(num_symbols)]

        created_password = rand_letters + rand_numbers + rand_symbols

        # Shuffle the positions and join to create str
        random.shuffle(created_password)
        created_password = ''.join(created_password)

        # Insert into password_entry label upon clicking "Generate password"
        self.password_entry.delete(0, END)
        self.password_entry.insert(0, created_password)

        # Copy created password to clipboard
        pyperclip.copy(created_password)


# ---------------------------- Password Management ------------------------------- #

    def PasswordManagement(self):
        # GETTING THE USER INPUTS
        user_website    = self.website_entry.get()
        user_email      = self.email_entry.get()
        user_password   = self.password_entry.get()


        user_password = user_password.encode()
        #user_password = user_password.decode()

        new_data = {
            user_website: {
                'email': user_email,
                'password': user_password
            }
        }
        if len(user_website) != 0 and len(user_password) != 0:

            try:
                with open('data.yaml', 'r') as data_file:
                    data = yaml.safe_load(data_file)
                    data.update(new_data)
            except FileNotFoundError:
                with open('data.yaml', 'w') as data_file:
                    yaml.safe_dump(new_data, data_file, indent=4)
            else:
                is_correct = messagebox.askyesno(
                    title=f"{user_website}",
                    message=f"\n'email': {user_email}\n'password': {user_password}\n\nPlease confirm before saving!")
                if is_correct:
                    with open('data.yaml', 'w') as data_file:
                        yaml.safe_dump(data, data_file, indent=4)
                        self.website_entry.delete(0, END)
                        self.password_entry.delete(0, END)
        else:
            # IF WEBSITE OR EMAIL ENTRY IS BLANK
            messagebox.showwarning(
                title='Oops',
                message="Please don't leave any fields empty!"
            )

    # ---------------------------- UI SETUP ------------------------------- #

    def main_menu(self):
        from main import MainMenu
        self.destroy()
        MainMenu().render()

    def render(self):
        # ROW 0
        canvas = Canvas(height=200, width=200, bg=NAVY, highlightthickness=0)
        img = PhotoImage(file='icon_logo.png')
        canvas.create_image(100, 100, image=img)
        canvas.grid(row=0, column=1)

        # ROW 1
        website_label = Label(text='Website:', bg=NAVY, fg=GREEN)
        website_label.grid(row=1, column=0, sticky="W")

        self.website_entry = Entry(font=('Times New Roman', 15))
        self.website_entry.grid(row=1, column=1, columnspan=2, sticky="EW")
        self.website_entry.insert(0, self.site)
        self.website_entry.focus()

        # ROW 2
        email_label = Label(text='Email/Username:', bg=NAVY, fg=GREEN)
        email_label.grid(row=2, column=0, sticky="W")

        self.email_entry = Entry(font=('Times New Roman', 15))
        self.email_entry.grid(row=2, column=1, columnspan=2, sticky="EW")
        self.email_entry.insert(0, self.email)

        # ROW 3
        scale_label = Label(self.window, text="Length", bg=NAVY, fg=GREEN)
        scale_label.grid(row=3, column=0, sticky="W")

        self.scale_bar = Scale(self.window, font=('Times New Roman', 15, 'bold'), from_=8, to=16, orient=HORIZONTAL, resolution=4,
                        bg=BLACK, fg=WHITE, troughcolor=NAVY)
        self.scale_bar.grid(row=3, column=1, sticky='EW')

        # ROW 4
        password_label = Label(text='Password:', bg=NAVY, fg=GREEN)
        password_label.grid(row=4, column=0, sticky="W")

        self.password_entry = Entry(font=('Times New Roman', 15))
        self.password_entry.grid(row=4, column=1, sticky="EW")

        password_button = Button(text='Generate Password', bg=BLACK, fg=GREEN, command=self.PasswordGenerator)
        password_button.grid(row=4, column=2, sticky="EW")

        # ROW 5
        button = Button(text='Add', bg=BLACK, fg=GREEN, command=self.PasswordManagement)
        button.grid(row=5, column=1, columnspan=2, sticky="EW")
        button.config(pady=2)

        menu_image = PhotoImage(file=relative_to_assets("menu_button.png"))
        menu_button = Button(
            image=menu_image,
            borderwidth=0,
            highlightthickness=0,
            command=self.main_menu,
            relief="flat"
        )
        menu_button.place( x=170.0, y=370.0, width=155.0, height=30.0 )


        self.window.mainloop()


    def destroy(self):
        self.window.destroy()


if __name__ == '__main__':
    PasswordGeneratorUI().render()
