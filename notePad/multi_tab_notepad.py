import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class MultiTabNotepad(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Multi-Tab Notepad")
        self.geometry("800x500")

        # Tab Control
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)

        # Menu Bar
        self.create_menu()

        # Start with one tab
        self.new_tab()

    def create_menu(self):
        menu_bar = tk.Menu(self)

        # File menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="New Tab", command=self.new_tab)
        file_menu.add_command(label="Open File", command=self.open_file)
        file_menu.add_command(label="Save File", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

        # Edit menu
        edit_menu = tk.Menu(menu_bar, tearoff=0)
        edit_menu.add_command(label="Cut", command=lambda: self.get_current_text().event_generate("<<Cut>>"))
        edit_menu.add_command(label="Copy", command=lambda: self.get_current_text().event_generate("<<Copy>>"))
        edit_menu.add_command(label="Paste", command=lambda: self.get_current_text().event_generate("<<Paste>>"))
        menu_bar.add_cascade(label="Edit", menu=edit_menu)

        self.config(menu=menu_bar)

    def new_tab(self):
        frame = ttk.Frame(self.notebook)
        text_area = tk.Text(frame, wrap="word", font=("Consolas", 12))
        text_area.pack(fill="both", expand=True)
        self.notebook.add(frame, text=f"Untitled {len(self.notebook.tabs())+1}")
        self.notebook.select(frame)

    def get_current_text(self):
        current_tab = self.notebook.select()
        current_frame = self.nametowidget(current_tab)
        return current_frame.winfo_children()[0]

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()
                self.new_tab()
                text_area = self.get_current_text()
                text_area.delete(1.0, tk.END)
                text_area.insert(tk.END, content)
                self.notebook.tab(self.notebook.select(), text=file_path.split("/")[-1])
            except Exception as e:
                messagebox.showerror("Error", f"Could not open file: {e}")

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            try:
                content = self.get_current_text().get(1.0, tk.END)
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(content)
                self.notebook.tab(self.notebook.select(), text=file_path.split("/")[-1])
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file: {e}")

if __name__ == "__main__":
    app = MultiTabNotepad()
    app.mainloop()
