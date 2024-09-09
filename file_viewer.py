import customtkinter as ctk
from CTkListbox import *
from tkinter import filedialog
import os

class FileViewerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("dark")

        self.title("File Viewer")
        self.geometry("1200x500")

        # Specify the default parent folder path here
        self.parent_folder_path = "C:/Users/Admin/Desktop/Mock_EPR_File/"  # Replace with your desired path
        self.current_folder_path = self.parent_folder_path

        # Create frames for the folder list, file list, and content display
        self.folder_list_frame = ctk.CTkFrame(self)
        self.folder_list_frame.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=10, pady=10)
        self.folder_list_frame.grid_rowconfigure(0, weight=1)
        #self.folder_list_frame.grid_columnconfigure(0, weight=1)

        self.file_list_frame = ctk.CTkFrame(self)
        self.file_list_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.file_list_frame.grid_rowconfigure(0, weight=1)
        self.file_list_frame.grid_columnconfigure(0, weight=1)

        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)

        # Create the folder listbox
        self.folder_listbox = CTkListbox(self.folder_list_frame, command=self.populate_file_listbox)
        self.folder_listbox.grid(row=0, columnspan=2, column=0, sticky="nsew")

        # Create a button to go up a directory
        self.home_button = ctk.CTkButton(master=self.folder_list_frame, text="Home", command=self.go_home_directory)
        self.home_button.grid(row=1, column=0, sticky="ws", padx=10, pady=5)

        # Create a button to go up a directory
        self.up_button = ctk.CTkButton(master=self.folder_list_frame, text="Up", command=self.go_up_directory)
        self.up_button.grid(row=1, column=1, sticky="es", padx=10, pady=5)

        # Create the file listbox
        self.file_listbox = CTkListbox(self.file_list_frame, command=self.display_file_content)
        self.file_listbox.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=10, pady=5)

        # Create a text widget to display the file content
        self.content_text = ctk.CTkTextbox(self.content_frame)
        self.content_text.grid(row=0, column=0, sticky="nsew")

        self.select_button = ctk.CTkButton(master=self, text="Select Directory", command=self.select_home_directory)
        self.select_button.grid(row=1, column=1, sticky="es", padx=10, pady=10)

        # Configure grid weights for resizing
        self.grid_rowconfigure((0, 1), weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Populate the folder listbox with folders from the default parent folder
        self.populate_folder_listbox()        

    def populate_folder_listbox(self):
        """Populates the folder listbox with folders from the current parent folder."""
        if self.folder_listbox.size() > 0:
            self.folder_listbox.delete("all")  # Clear existing folders

        if self.file_listbox.size() > 0:
            self.file_listbox.delete("all")  # Clear existing folders
        
        ix = 0
        for foldername in os.listdir(self.current_folder_path):
            folder_path = os.path.join(self.current_folder_path, foldername)
            if os.path.isdir(folder_path):  # Check if it's a directory
                self.folder_listbox.insert(ix, foldername)
                ix += 1

    def select_home_directory(self):
        """Allows the user to select a new home directory."""
        selected_directory = filedialog.askdirectory(initialdir=self.current_folder_path)
        if selected_directory:  # If a directory was selected
            self.parent_folder_path = selected_directory
            self.current_folder_path = selected_directory
            self.populate_folder_listbox()

    def go_home_directory(self):
        self.current_folder_path = self.parent_folder_path
        self.populate_folder_listbox()

    def go_up_directory(self):
        """Goes up to the parent directory."""
        target_path = os.path.dirname(self.current_folder_path)
        if os.path.normpath(os.path.commonpath([target_path, self.parent_folder_path])) == os.path.normpath(self.parent_folder_path):
            self.current_folder_path = target_path
            print(self.current_folder_path)
            self.populate_folder_listbox()

    def populate_file_listbox(self, selection):
        """Populates the file listbox with files from the selected folder."""
        selected_folder = selection
        self.current_folder_path = os.path.join(self.current_folder_path, selected_folder)
        self.populate_folder_listbox()

        if self.file_listbox.size() > 0:
            self.file_listbox.delete("all")  # Clear existing folders

        ix = 0        
        for filename in os.listdir(self.current_folder_path):
            if filename.endswith((".docx", ".txt", ".pdf")):
                self.file_listbox.insert(ix, filename)
                ix += 1

        if ix == 0:
            self.file_listbox.insert(0, "No files found...")  # Message for no valid files

    def display_file_content(self, selection):
        """Displays the content of the selected file in the text widget."""
        
        if selection:
            file_path = os.path.join(self.current_folder_path, selection)

            try:
                if selection.endswith(".pdf"):
                    self.content_text.configure(state="normal")
                    self.content_text.delete("0.0", "end")  # delete all text
                    self.content_text.configure(state="disabled")
                    os.startfile(file_path)
                    return
                elif selection.endswith(".docx"):
                    import docx
                    doc = docx.Document(file_path)
                    content = "\n".join([paragraph.text for paragraph in doc.paragraphs])
                elif selection.endswith(".txt"):
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                self.content_text.configure(state="normal")
                self.content_text.delete("0.0", "end")  # delete all text
                self.content_text.insert("0.0", content)
                self.content_text.configure(state="disabled")
            except Exception as e:
                self.content_text.configure(state="normal")
                self.content_text.delete("0.0", "end")
                self.content_text.insert("0.0", f"Error: {e}")
                self.content_text.configure(state="disabled")

if __name__ == "__main__":
    app = FileViewerApp()
    app.mainloop()