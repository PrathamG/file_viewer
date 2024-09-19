import customtkinter as ctk
import tkinter as tk
import os

class FileViewerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("dark")

        self.title("File Viewer")
        self.geometry("1200x500")

        # Specify the default parent folder path here
        self.parent_folder_path = "C:/Users/Admin/Desktop/Mock_EPS_File/"  # Replace with your desired path
        self.path_tree = []

        # Create frames for the folder list, file list, and content display
        self.folder_list_frame = ctk.CTkFrame(self, fg_color="#212121")
        self.folder_list_frame.grid(row=0, column=0, rowspan=3, sticky="nsew", padx=10, pady= 10)
        self.folder_list_frame.grid_rowconfigure(0, weight=1)

        self.file_list_frame = ctk.CTkFrame(self)
        self.file_list_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=0)
        self.file_list_frame.grid_rowconfigure(0, weight=1)
        self.file_list_frame.grid_columnconfigure(0, weight=1)

        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)
        
        # Create listbox to display directories
        self.folder_listbox = tk.Listbox(
            self.folder_list_frame,
            selectmode=tk.SINGLE,
            activestyle="none",
            bg="#212121",
            fg="#ffffff",
            selectbackground="#0078d7",
            highlightthickness=0,
            bd=0,
            font=("Segoe UI", 12)   
        )
        self.folder_listbox.configure(exportselection=False)
        self.folder_listbox.grid(row=0, column=0, columnspan=2, sticky="nsew")
        self.folder_listbox.bind("<<ListboxSelect>>", self.dir_window_click_action)
        
        # Create scrollbar for directory listbox
        self.folder_scrollbar = tk.Scrollbar(self.folder_list_frame, orient=tk.VERTICAL, command=self.folder_listbox.yview)
        self.folder_scrollbar.grid(row=0, column=2, sticky="nse")
        self.folder_scrollbar.config(width="12")
        self.folder_listbox.config(yscrollcommand=self.folder_scrollbar.set)

        # Create a button to go up a directory
        self.home_button = ctk.CTkButton(master=self.folder_list_frame, text="Home", command=self.go_home_directory, width=100)
        self.home_button.grid(row=1, column=0, sticky="sw", padx=15, pady=15)

        # Create a button to go up a directory
        self.up_button = ctk.CTkButton(master=self.folder_list_frame, text="Up", command=self.go_up_directory, width=100)
        self.up_button.grid(row=1, column=1, sticky="se", padx=15, pady=15)

        # Create listbox to display files
        self.file_listbox = tk.Listbox(
            self.file_list_frame,
            selectmode=tk.SINGLE,
            activestyle="none",
            bg="#2e2e2e",
            fg="#ffffff",
            selectbackground="#0078d7",
            highlightthickness=0,
            bd=0,
            font=("Segoe UI", 12),
            exportselection=False,
        )
        self.file_listbox.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=0, pady=5)
        self.file_listbox.bind("<<ListboxSelect>>", self.file_window_click_action)

        # Create scrollbar for file listbox
        self.file_scrollbar = tk.Scrollbar(self.file_list_frame, orient=tk.VERTICAL, command=self.file_listbox.yview)
        self.file_scrollbar.grid(row=0, column=1, sticky="ns")
        self.file_scrollbar.config(width="12")
        self.file_listbox.config(yscrollcommand=self.file_scrollbar.set)       

        # Create a text widget to display the file content
        self.content_text = ctk.CTkTextbox(self.content_frame)
        self.content_text.grid(row=0, column=0, sticky="nsew")

        self.select_button = ctk.CTkButton(master=self, text="Select Directory", command=self.select_home_directory)
        self.select_button.grid(row=2, column=1, sticky="es", padx=10, pady=10)

        # Configure grid weights for resizing
        self.grid_rowconfigure((0, 1), weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Populate the folder listbox with folders from the default parent folder
        self.update_current_folder(self.parent_folder_path)        

    def update_current_folder(self, new_folder_path):        
        if not os.path.isdir(new_folder_path):
            self.folder_listbox.insert(0, "Select valid directory")
            return
        
        self.content_text.configure(state="normal")
        self.content_text.delete("0.0", "end")
        self.content_text.configure(state="disabled")

        subdir_list = [d for d in os.listdir(new_folder_path) if os.path.isdir(os.path.join(new_folder_path, d))]
        if len(subdir_list) != 0:
            self.current_folder_path = new_folder_path
            if self.folder_listbox.size() > 0:
                self.folder_listbox.delete(0, tk.END)

            if self.file_listbox.size() > 0:
                self.file_listbox.delete(0, tk.END)

            self.folder_listbox.insert(tk.END, *subdir_list)
            self.file_flag_path = None
            #print(f"dir: {new_folder_path}")
        else:
            self.file_flag_path = new_folder_path
            
            #print(f"dir: {self.file_flag_path}")


    def select_home_directory(self):
        """Allows the user to select a new home directory."""
        selected_directory = tk.filedialog.askdirectory()
        if selected_directory:
            self.path_tree.clear()
            self.parent_folder_path = selected_directory
            self.update_current_folder(selected_directory)
            self.file_flag_path = None

            self.content_text.configure(state="normal")
            self.content_text.delete("0.0", "end")
            self.content_text.configure(state="disabled")

    def go_home_directory(self):
        self.path_tree.clear()
        self.update_current_folder(self.parent_folder_path)
        self.file_flag_path = None

    def go_up_directory(self):
        """Goes up to the parent directory."""
        target_path = os.path.dirname(self.current_folder_path)
        if os.path.normpath(os.path.commonpath([target_path, self.parent_folder_path])) == os.path.normpath(self.parent_folder_path):
            self.update_current_folder(target_path)

        if len(self.path_tree):
            self.folder_listbox.see(self.path_tree[-1])
            self.folder_listbox.select_set(self.path_tree[-1])
            del self.path_tree[-1]
            #print(self.path_tree)

    def dir_window_click_action(self, evt):
        selected_index = self.folder_listbox.curselection()
        if not selected_index:
            return
        
        selection = self.folder_listbox.get(selected_index[0])
        
        new_path = os.path.join(self.current_folder_path, selection)
        if(os.path.isdir(new_path)):
            self.update_current_folder(new_path)
            
            subdir_list = [d for d in os.listdir(new_path) if os.path.isdir(os.path.join(new_path, d))]
            if len(subdir_list) != 0 and new_path != self.parent_folder_path:
                self.path_tree.append(selected_index[0])
                #print(self.path_tree)
        
        if self.file_listbox.size() > 0:
            self.file_listbox.delete(0, tk.END)
        
        """Get a list of .docx, .pdf, and .txt files in the specified directory."""
        valid_extensions = {'.docx', '.pdf', '.txt'}
        file_list = [f for f in os.listdir(new_path) if os.path.isfile(os.path.join(new_path, f)) and os.path.splitext(f)[1] in valid_extensions]
        
        self.file_listbox.insert("end", *file_list)
        
        if self.file_listbox.size() == 0:
            self.file_listbox.insert(0, "No files found...")  # Message for no valid files

    def file_window_click_action(self, evt):
        """Displays the content of the selected file in the text widget."""
        selected_index = self.file_listbox.curselection()
        if selected_index:
            selection = self.file_listbox.get(selected_index)
            
            if selection:
                if self.file_flag_path:
                    file_path = os.path.join(self.file_flag_path, selection)
                else:
                    file_path = os.path.join(self.current_folder_path, selection)
                #print(f"file: {file_path}")
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

def create_empty_directories(base_path, num_dirs):
    # Create the base directory if it doesn't exist
    os.makedirs(base_path, exist_ok=True)

    # Create the specified number of empty directories
    for i in range(num_dirs):
        dir_name = os.path.join(base_path, f'directory_{i+1}')
        os.makedirs(dir_name, exist_ok=True)
        print(f'Created: {dir_name}')

# Set the base path and number of directories
base_path = 'test/directory_1'
num_dirs = 1000

# Create the directories
#create_empty_directories(base_path, num_dirs)

if __name__ == "__main__":
    app = FileViewerApp()
    app.mainloop()