
import sys
from tkinter import Tk
from ui.app_ui import AppUI

def main():
    root = Tk()  # Create the Tkinter root window
    window = AppUI(root)  # Pass the root window as the 'master' argument
    root.mainloop()  # Start the Tkinter event loop

if __name__ == "__main__":
    main()