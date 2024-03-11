"""
Typora to Wiki.js Image Path Converter

This program automates the process of adjusting image paths in Markdown files 
created with Typora for compatibility with Wiki.js. It features a graphical 
user interface (GUI) that enables the user to specify a base path 
for images and to select a Markdown file for conversion. The script 
then dynamically updates all relative image paths within the document by prepending the
specified base path, ensuring that images are correctly displayed when uploaded to Wiki.js.

Features:
- Graphical User Interface for ease of use.
- Ability to specify a custom base path for image assets.
- Detection of images in the form ![alt text](path/to/image/) and since v4.0.0 also <img src="path/to/image/" alt="alt text" />.
- Automatic adjustment of relative image paths in Markdown files.
- Option to review and copy the adjusted content to the clipboard.

Dependencies:
- Python 3.x
- customtkinter (an enhanced version of tkinter for a modern and customizable UI)

Author: Raffael Richter
Date: 11.03.2024
Version: 4.0.0
"""

import customtkinter as ctk
from tkinter import filedialog, messagebox, scrolledtext
import re
import os

class PathConverterApp:
    def __init__(self, root):
        """Initialize the application with the root CustomTkinter window."""
        self.root = root
        self.file_path = ""  # Store the selected file path
        self.base_path = ""  # Store the base path input by the user
        self.setup_home_screen()


    def setup_home_screen(self):
        """Set up the initial home screen GUI layout."""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.root.deiconify()
        self.root.title("Typora to Wiki.js Path Converter")

        # Document Path
        ctk.CTkLabel(self.root, text="Document Path:").pack(padx=20, pady=(20, 0))
        self.doc_path_entry = ctk.CTkEntry(self.root, width=400)
        self.doc_path_entry.pack(padx=20, pady=5)
        ctk.CTkButton(self.root, text="Browse", command=self.browse_file).pack(padx=20, pady=(0, 20))

        # Base Path
        ctk.CTkLabel(self.root, text="Base Path for Images:").pack(padx=20, pady=(20, 0))
        self.base_path_entry = ctk.CTkEntry(self.root, width=400)
        self.base_path_entry.pack(padx=20, pady=5)

        # Start Conversion Button
        ctk.CTkButton(self.root, text="Start Conversion", command=self.start_conversion).pack(pady=20)

        # Bind the Return key to the start_conversion method
        self.root.bind('<Return>', self.start_conversion)


    def browse_file(self):
        """Open a file dialog to select a Markdown file and update the document path entry."""
        self.file_path = filedialog.askopenfilename(title="Select a Markdown file", filetypes=[("Markdown files", "*.md")])
        if self.file_path:
            self.doc_path_entry.delete(0, ctk.END)  # Clear the existing entry
            self.doc_path_entry.insert(0, self.file_path)  # Insert the selected file path


    def start_conversion(self, event=None):
        """Initiate the conversion process using the specified base path and file."""
        base_path_input = self.base_path_entry.get().strip()
        self.base_path = self.normalize_base_path(base_path_input)
        self.file_path = self.doc_path_entry.get().strip()

        if not self.file_path or not self.base_path:
            messagebox.showerror("Error", "Both document path and base path are required.")
            return

        adjusted_content, changes_count = self.adjust_paths(self.file_path, self.base_path)
        if adjusted_content:
            self.show_adjusted_content(adjusted_content, changes_count)  # Pass changes_count to the method
        else:
            messagebox.showerror("Error", "Failed to adjust paths. Please check the document path and base path.")


    def normalize_base_path(self, base_path):
        """Normalize the base path to ensure it is properly formatted for insertion."""
        base_path = base_path.strip().rstrip("/")

        if not base_path.startswith('/'):
            base_path = '/' + base_path

        if base_path.endswith('/assets'):
            base_path = base_path[:-7]
        
        base_path += '/'

        return base_path


    def adjust_paths(self, file_path, base_path):
        """Adjust the image paths in the selected Markdown file using the specified base path."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.readlines()
            in_code_block = False
            adjusted_lines = []
            changes_count = 0  # Initialize the counter for changes made

            for line in content:
                if line.strip().startswith("```"):
                    in_code_block = not in_code_block
                elif not in_code_block:
                    # Adjust Markdown image paths
                    def markdown_repl(match):
                        nonlocal changes_count
                        if not match.group(3).startswith('/'):
                            changes_count += 1
                            return match.group(1) + base_path + match.group(3) + match.group(4)
                        return match.group(0)

                    line = re.sub(r'(\!\[(.*?)\]\()(?!http)(.*?)(\))', markdown_repl, line)
                    
                    # Adjust HTML-embedded image paths
                    def html_repl(match):
                        nonlocal changes_count
                        if not match.group(2).startswith('/'):
                            changes_count += 1
                            return match.group(1) + base_path + match.group(2) + match.group(3)
                        return match.group(0)

                    line = re.sub(r'(<img\s.*?src=")(?!http)(.*?)(".*?>)', html_repl, line)

                adjusted_lines.append(line)

            return ''.join(adjusted_lines), changes_count
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while adjusting paths: {e}")
            return "", 0


    def show_adjusted_content(self, adjusted_content, changes_count):
        """Show the adjusted content in a new window with option to copy the adjusted content to the clipboard."""
        new_window = ctk.CTkToplevel(self.root)
        new_window.title("Adjusted Markdown Paths")

        # Ensure the new window grabs focus and input
        new_window.focus_force()
        new_window.grab_set()

        text_area = scrolledtext.ScrolledText(new_window, wrap=ctk.WORD, width=100, height=30)
        text_area.pack(padx=10, pady=10)
        text_area.insert(ctk.INSERT, adjusted_content)
        text_area.config(state=ctk.DISABLED)

        # Display the number of changes made
        changes_label = ctk.CTkLabel(new_window, text=f"Total changes made: {changes_count}")
        changes_label.pack(pady=(0, 10))

        ctk.CTkButton(new_window, text="Copy All", command=lambda: self.copy_to_clipboard(adjusted_content)).pack(side=ctk.LEFT, padx=10, pady=10)
        ctk.CTkButton(new_window, text="Exit", command=lambda: [new_window.grab_release(), new_window.destroy()]).pack(side=ctk.RIGHT, padx=10, pady=10)


    def copy_to_clipboard(self, content):
        """Copy the adjusted content to clipboard."""
        self.root.clipboard_clear()
        self.root.clipboard_append(content)
        self.root.update()
        messagebox.showinfo("Copied", "The text has been copied to the clipboard.")

if __name__ == "__main__":
    root = ctk.CTk()
    app = PathConverterApp(root)
    root.mainloop()