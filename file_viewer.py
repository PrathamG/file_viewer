import pyperclip
from PIL import Image
import os

import customtkinter as ctk
import tkinter as tk

class FileViewerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("dark")

        self.title("File Viewer")
        self.geometry("1200x500")

        #self.home_icon = ctk.CTkImage(light_image=Image.open(fp="media/home_icon.png"), size=(20,20))
        self.copy_icon = ctk.CTkImage(light_image=Image.open(fp="media/copy_icon.png"), size=(20,20))
        self.sort_icon = ctk.CTkImage(light_image=Image.open(fp="media/sort_icon.png"), size=(20,20))
        self.font_up_icon = ctk.CTkImage(light_image=Image.open(fp="media/font_up_icon.png"), size=(20,20))
        self.font_down_icon = ctk.CTkImage(light_image=Image.open(fp="media/font_down_icon.png"), size=(20,20))

        # Specify the default parent folder path here
        self.parent_folder_path = "C:/Users/Admin/Desktop/Mock_EPS_File/"  # Replace with your desired path
        self.current_folder_path = None
        self.path_tree = []

        self.file_ascending = True
        self.fontsize = 12

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
            font=("Segoe UI", self.fontsize)   
        )
        self.folder_listbox.configure(exportselection=False)
        self.folder_listbox.grid(row=0, column=0, columnspan=2, sticky="nsew")
        self.folder_listbox.bind("<<ListboxSelect>>", self.dir_window_click_action)
        
        self.folder_scrollbar = tk.Scrollbar(self.folder_list_frame, orient=tk.VERTICAL, command=self.folder_listbox.yview)
        self.folder_scrollbar.grid(row=0, column=2, sticky="nse")
        self.folder_scrollbar.config(width="12")
        self.folder_listbox.config(yscrollcommand=self.folder_scrollbar.set)

        self.home_button = ctk.CTkButton(master=self.folder_list_frame, text="Home", command=self.go_home_directory, width=100)
        self.home_button.grid(row=1, column=0, sticky="sw", padx=15, pady=15)

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
            font=("Segoe UI", self.fontsize),
            exportselection=False,
        )
        self.file_listbox.grid(row=0, column=0, sticky="nsew", padx=0, pady=5)
        self.file_listbox.bind("<<ListboxSelect>>", self.file_window_click_action)

        self.file_scrollbar = tk.Scrollbar(self.file_list_frame, orient=tk.VERTICAL, command=self.file_listbox.yview)
        self.file_scrollbar.grid(row=0, column=1, sticky="ns")
        self.file_scrollbar.config(width="12")
        self.file_listbox.config(yscrollcommand=self.file_scrollbar.set)

        self.button_frame = ctk.CTkFrame(self.file_list_frame, fg_color="#2b2b2b")
        self.button_frame.grid(row=0, column=2, sticky="new")
        
        self.filename_sort_btn = ctk.CTkButton(
            master=self.button_frame,
            text="",
            width=50,
            height=28,
            image=self.sort_icon, 
            command=self.toggle_filename_sort
        )
        self.filename_sort_btn.grid(row=0, column=0, padx = 10, pady = 10)

        self.filename_copy_btn = ctk.CTkButton(
            master=self.button_frame, 
            text="",
            width=50,
            height=28,
            image=self.copy_icon,
            command=self.copy_filename
        )
        self.filename_copy_btn.grid(row=1, column=0, padx = 10, pady = 10)

        self.fontsize_up_btn = ctk.CTkButton(
            master=self.button_frame, 
            text="",
            width=50,
            height=28,
            image=self.font_up_icon,
            command=self.up_fontsize
        )
        self.fontsize_up_btn.grid(row=2, column=0, padx = 10, pady = 10)

        self.fontsize_down_btn = ctk.CTkButton(
            master=self.button_frame, 
            text="",
            width=50,
            height=28,
            image=self.font_down_icon,
            command=self.down_fontsize
        )
        self.fontsize_down_btn.grid(row=3, column=0, padx = 10, pady = 10)

        # Create a text widget to display the file content
        self.content_text = ctk.CTkTextbox(self.content_frame)
        self.content_text.grid(row=0, column=0, sticky="nsew")

        self.select_button = ctk.CTkButton(master=self, text="Select Directory", command=self.select_home_directory)
        self.select_button.grid(row=2, column=1, sticky="es", padx=10, pady=10)

        # Configure grid weights for resizing
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=3)

        # Populate the folder listbox with folders from the default parent folder
        self.update_current_folder(self.parent_folder_path)        

    def update_file_listbox(self, new_path):
        if self.file_listbox.size() > 0:
            self.file_listbox.delete(0, tk.END)

        """Get a list of .docx, .pdf, and .txt files in the specified directory."""
        valid_extensions = {'.docx', '.pdf', '.txt', '.PDF', '.DOCX', '.TXT'}
        file_list = [f for f in os.listdir(new_path) if os.path.isfile(os.path.join(new_path, f)) and os.path.splitext(f)[1] in valid_extensions]
        
        if len(file_list) == 0:
            self.file_listbox.insert(0, "No files found...")  # Message for no valid files
            return
        
        file_list = sorted(file_list, reverse=self.file_ascending)
        
        self.file_listbox.insert("end", *file_list)

    # If new_folder_path contains subdirectories: 
    #   - shows the subdirectories in folder listbox
    # else keeps the folder listbox as is
    # Keeps track of paths for folder view and file selection
    # Update file listbox
    def update_current_folder(self, new_folder_path):        
        if not os.path.isdir(new_folder_path):
            self.folder_listbox.insert(0, "Select valid directory")
            return
        
        self.content_text.configure(state="normal")
        self.content_text.delete("0.0", "end")
        self.content_text.configure(state="disabled")

        subdir_list = [d for d in os.listdir(new_folder_path) if os.path.isdir(os.path.join(new_folder_path, d))]
        if len(subdir_list) != 0:
            if self.folder_listbox.size() > 0:
                self.folder_listbox.delete(0, tk.END)

            if self.file_listbox.size() > 0:
                self.file_listbox.delete(0, tk.END)

            self.folder_listbox.insert(tk.END, *subdir_list)

            self.current_folder_view_path = new_folder_path

        self.current_folder_path = new_folder_path
        self.update_file_listbox(self.current_folder_path)

    def select_home_directory(self):
        """Allows the user to select a new home directory."""
        selected_directory = tk.filedialog.askdirectory()
        if selected_directory:
            self.path_tree.clear()
            self.parent_folder_path = selected_directory
            self.current_folder_view_path = selected_directory
            self.update_current_folder(selected_directory)

    def go_home_directory(self):
        self.path_tree.clear()
        self.update_current_folder(self.parent_folder_path)

    def go_up_directory(self):
        """Goes up to the parent directory."""
        target_path = os.path.dirname(self.current_folder_view_path)
        if os.path.normpath(os.path.commonpath([target_path, self.parent_folder_path])) == os.path.normpath(self.parent_folder_path):
            self.update_current_folder(target_path)

        if len(self.path_tree):
            self.folder_listbox.see(self.path_tree[-1])
            self.folder_listbox.select_set(self.path_tree[-1])
            del self.path_tree[-1]
            #print(self.path_tree)

    def toggle_filename_sort(self):
        self.file_ascending = not self.file_ascending
        if self.current_folder_path:
            self.update_file_listbox(self.current_folder_path)

    def copy_filename(self):
        selected_index = self.file_listbox.curselection()
        if selected_index:
            selected_item = self.file_listbox.get(selected_index)
            pyperclip.copy(selected_item)

    def up_fontsize(self):
        if self.fontsize > 17:
            return
        
        self.fontsize += 1
        self.file_listbox.configure(font=("Segoe UI", self.fontsize))
        self.content_text.configure(font=("Segoe UI", self.fontsize))

    def down_fontsize(self):
        if self.fontsize < 9:
            return
        
        self.fontsize -= 1
        self.file_listbox.configure(font=("Segoe UI", self.fontsize))
        self.content_text.configure(font=("Segoe UI", self.fontsize))

    def dir_window_click_action(self, evt):
        selected_index = self.folder_listbox.curselection()
        if not selected_index:
            return
        
        selection = self.folder_listbox.get(selected_index[0])
        
        new_path = os.path.join(self.current_folder_view_path, selection)

        if(os.path.isdir(new_path)):
            self.update_current_folder(new_path)
            
            subdir_list = [d for d in os.listdir(new_path) if os.path.isdir(os.path.join(new_path, d))]
            if len(subdir_list) != 0:
                self.path_tree.append(selected_index[0])
                #print(self.path_tree)
        
    def file_window_click_action(self, evt):
        """Displays the content of the selected file in the text widget."""
        selected_index = self.file_listbox.curselection()
        if selected_index:
            selection = self.file_listbox.get(selected_index)

            file_path = os.path.join(self.current_folder_path, selection)

            try:
                if selection.endswith(".pdf") or selection.endswith(".PDF"):
                    os.startfile(file_path)
                    return
                elif selection.endswith(".docx") or selection.endswith(".DOCX"):
                    import docx
                    doc = docx.Document(file_path)
                    content = "\n".join([paragraph.text for paragraph in doc.paragraphs])
                elif selection.endswith(".txt") or selection.endswith(".TXT"):
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

if __name__ == "__main__":
    app = FileViewerApp()
    app.mainloop()
