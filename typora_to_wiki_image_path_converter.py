"""
Typora to Wiki.js Path Converter

This program automates the process of adjusting image paths in Markdown files 
created with Typora for compatibility with Wiki.js. It features a graphical 
user interface (GUI) that guides the user through the process of specifying 
a base path for images and selecting a Markdown file for conversion. The script 
then dynamically updates all relative image paths within the document, ensuring 
they are correctly displayed when uploaded to Wiki.js.

Features:
- Graphical User Interface for ease of use.
- Ability to specify a custom base path for image assets.
- Automatic adjustment of relative image paths in Markdown files.
- Option to review and copy the adjusted content to the clipboard.

Dependencies:
- Python 3.x
- tkinter

Author: [Raffael Richter]
Date: [28.02.2024]
Version: 3.0
"""

import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox, simpledialog, Entry, Label, Button
import re
import os

class PathConverterApp:
    def __init__(self, root):
        """Initialize the application with the root Tkinter window."""
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
        Label(self.root, text="Document Path:").pack(padx=20, pady=(20, 0))
        self.doc_path_entry = Entry(self.root, width=50)
        self.doc_path_entry.pack(padx=20, pady=5)
        Button(self.root, text="Browse", command=self.browse_file).pack(padx=20, pady=(0, 20))

        # Base Path
        Label(self.root, text="Base Path for Images:").pack(padx=20, pady=(20, 0))
        self.base_path_entry = Entry(self.root, width=50)
        self.base_path_entry.pack(padx=20, pady=5)

        # Start Conversion Button
        Button(self.root, text="Start Conversion", command=self.start_conversion).pack(pady=20)

    def browse_file(self):
        """Open a file dialog to select a Markdown file and update the document path entry."""
        self.file_path = filedialog.askopenfilename(title="Select a Markdown file", filetypes=[("Markdown files", "*.md")])
        if self.file_path:
            self.doc_path_entry.delete(0, tk.END)  # Clear the existing entry
            self.doc_path_entry.insert(0, self.file_path)  # Insert the selected file path

    def start_conversion(self):
        """Initiate the conversion process using the specified base path and file."""
        # Fetch the base path from the entry widget and clean it
        base_path_input = self.base_path_entry.get().strip()
        self.base_path = self.normalize_base_path(base_path_input)

        # Use the path from the entry if not empty, otherwise use the path from browsing
        self.file_path = self.doc_path_entry.get().strip()
        if not self.file_path or not self.base_path:
            messagebox.showerror("Error", "Both document path and base path are required.")
            return

        adjusted_content = self.adjust_paths(self.file_path, self.base_path)
        if adjusted_content:
            self.show_adjusted_content(adjusted_content)
        else:
            messagebox.showerror("Error", "Failed to adjust paths. Please check the document path and base path.")

    def normalize_base_path(self, base_path):
        """Normalize the base path to ensure it is properly formatted for insertion."""
        # Normalize base_path: remove leading/trailing spaces and ensure it starts with a slash
        base_path = base_path.strip().rstrip("/")
        if not base_path.startswith('/'):
            base_path = '/' + base_path
        
        # Remove any accidental inclusion of "/assets/" at the end to prevent duplication
        if base_path.endswith('/assets'):
            base_path = base_path[:-7]

        # Ensure base_path ends with a '/'
        base_path += '/'

        return base_path

    def adjust_paths(self, file_path, base_path):
        """Adjust the image paths in the selected Markdown file using the specified base path."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.readlines()
            in_code_block = False
            adjusted_lines = []
            for line in content:
                if line.strip().startswith("```"):
                    in_code_block = not in_code_block
                elif not in_code_block:
                    line = re.sub(r'(\!\[(.*?)\]\()(?!http)(.*?)(\))', 
                                  lambda match: match.group(1) + base_path + match.group(3) + match.group(4) 
                                  if not match.group(3).startswith('/') else match.group(0), line)
                adjusted_lines.append(line)
            return ''.join(adjusted_lines)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while adjusting paths: {e}")
            return ""

    def show_adjusted_content(self, adjusted_content):
        """Show the adjusted content in a new window with option to copy the adjusted content to the clipboard."""
        new_window = tk.Toplevel(self.root)
        new_window.title("Adjusted Markdown Paths")
        text_area = scrolledtext.ScrolledText(new_window, wrap=tk.WORD, width=100, height=30)
        text_area.pack(padx=10, pady=10)
        text_area.insert(tk.INSERT, adjusted_content)
        text_area.config(state=tk.DISABLED)
        Button(new_window, text="Copy All", command=lambda: self.copy_to_clipboard(adjusted_content)).pack(side=tk.LEFT, padx=10, pady=10)
        Button(new_window, text="Exit", command=new_window.destroy).pack(side=tk.RIGHT, padx=10, pady=10)

    def copy_to_clipboard(self, content):
        """Copy the adjusted content to clipboard."""
        self.root.clipboard_clear()
        self.root.clipboard_append(content)
        self.root.update()
        messagebox.showinfo("Copied", "The text has been copied to the clipboard.")

if __name__ == "__main__":
    root = tk.Tk()
    app = PathConverterApp(root)
    root.mainloop()