# Typora-To-Wiki-Path-Converter
A Python script to automate the customization of relative image paths in Markdown documents for seamless integration with Typora and Wiki.js.

Wiki.js requires image paths in Markdown files to start with a forward slash (/) to display images correctly. However, Typora, a popular Markdown editor, displays images only when their paths start with ./ or no slash at all. This discrepancy can cause issues when Markdown documents created or edited in Typora are uploaded to a Wiki.js platform.

The Typora-To-Wiki-Path-Converter script elegantly solves this problem by adding a forward slash to the beginning of all relative image paths in a Markdown document, ensuring compatibility with Wiki.js without sacrificing the local usability in Typora. After running the script, users can temporarily review and copy the adjusted Markdown content before uploading it to their Wiki.js site. The script generates a temporary edited version of the document, which is automatically deleted upon closing the script, ensuring that the original document remains unchanged.

## Features
- Automated Path Adjustment: Automatically prepends a forward slash to relative image paths in Markdown files.
- GUI for Easy Interaction: Provides a simple graphical user interface to select a Markdown file and view the adjusted content.
- Temporary File Handling: Creates a temporary file with the adjusted paths for review and copying, then deletes it after use to keep your workspace clean.
- Clipboard Support: Includes a "Copy All" button to easily copy the adjusted Markdown content to the clipboard for immediate use.
- User-friendly Design: Designed with ease of use in mind, requiring no command-line interaction.

## How It Works
1. Start Screen: Upon launching the script, a start screen displays information about the tool and its creator.
2. Select Markdown File: Users are prompted to choose a Markdown file for path adjustment.
3. View and Copy Adjusted Content: The script displays the adjusted Markdown content, allowing users to copy it to the clipboard.
4. Cleanup: After copying the content or closing the script, the temporary file is automatically deleted.

## Requirements
Python 3.6 or higher

## Installation
Clone this repository or download the .py file directly.

```
git clone https://github.com/realrichter/Typora-To-Wiki-Path-Converter.git
```

## Usage
After cloning or downloading, run the script. A graphical interface will guide you through selecting a Markdown file and copying the adjusted content.

For any inquiries, contact the creator at rr@com-con.net.

