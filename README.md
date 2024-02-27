# Typora to Wiki.js Image Path Converter V2

The Typora-To-Wiki-Path-Converter V2 is an enhanced Python script designed to bridge the gap between Typora, a popular Markdown editor, and Wiki.js, a powerful open-source wiki software. This version introduces significant improvements over its predecessor, focusing on accurate path adjustments for image files within Markdown documents to ensure seamless integration with Wiki.js's content management system.

## Key Features
- **Full Path Adjustment**: Dynamically prepends user-specified path prefixes to all relative image paths, ensuring images display correctly in Wiki.js.
- **Advanced Path Detection**: Includes logic to identify and exclude image paths located within code blocks, preventing unintended modifications of code snippets.
- **Graphical User Interface (GUI)**: Simplifies file selection and path prefix input through a user-friendly GUI, eliminating the need for command-line interaction.
- **Clipboard Functionality**: Facilitates easy copying of the adjusted Markdown content to the clipboard for immediate use in Wiki.js.
- **Temporary File Management**: Generates a temporary file for review, allowing users to copy the adjusted content. This file is automatically deleted upon script closure, keeping the original document intact.
- **Ease of Use**: Tailored for simplicity, requiring minimal user input and no prior command-line experience.

## How It Works
- **Initial Setup**: The user is prompted to input the full path prefix where images will be hosted in Wiki.js (e.g., `/intern/dokumentationsrichtlinien/typora-einrichtung/assets/`).
- **Markdown File Selection**: Through the GUI, users select the Markdown document needing path adjustments.
- **Content Adjustment and Review**: The script processes the document, appending the specified path prefix to each relative image path while excluding paths within code blocks for accurate content presentation. Users can then review and copy the modified content.
- **Final Steps**: After copying the adjusted Markdown, the temporary file is deleted, ensuring no residual clutter.

## Limitations
- Currently, the script does not distinguish image paths inside inline code marked with single backticks (`). As a result, image paths within inline code will still be adjusted. Users should be aware of this behavior and manually verify any inline code containing image paths.

## Requirements
- Python 3.6 or higher

## Installation
To get started, clone this repository or download the .py file directly:

`git clone https://github.com/realrichter/Typora-To-Wiki-Path-Converter.git`

## Usage
Run the script to launch the GUI, and follow the on-screen prompts to:
- Input the complete path prefix for the images as per your Wiki.js structure.
- Select the Markdown file you wish to adjust.
- Copy the adjusted content and paste it into your Wiki.js page.
- Ensure images are uploaded to the corresponding directory in Wiki.js.

For assistance or inquiries, please reach out to the creator at rr@com-con.net.
