import tkinter as tk
from ui import OscarDatabaseApp

# main function that calls the application
if __name__ == "__main__":
    root = tk.Tk()
    app = OscarDatabaseApp(root)
    root.mainloop()