# Text Inserter v2.0

A Windows application for managing and quickly inserting text templates into any application. This tool is particularly useful for customer support, help desk, or any role that requires frequent use of standardized text responses.

## Features

- **Template Management**
  - Create, edit, and delete text templates
  - Organize templates into categories (Notifications and Chat)
  - Copy templates to clipboard with one click

- **Hotkey Support**
  - Quick access to templates using customizable hotkeys
  - Automatically paste templates into any application

- **User-Friendly Interface**
  - Clean and intuitive design
  - Easy template selection and management
  - Large text preview area

## Installation

1. Download the latest release.
2. Extract the downloaded ZIP file
3. Run `TextFileInserter.exe`

## Building from Source

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/TextInserter.git
   ```

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Build the executable:
   ```bash
   build.bat
   ```

4. The executable will be created in the `dist` folder

## Usage

1. **Creating Templates**
   - Click "New Template"
   - Select template type (Notification or Chat)
   - Enter template name and content
   - Save the template

2. **Using Templates**
   - Select a template from the dropdown
   - Click "Copy to Clipboard" or use the assigned hotkey
   - Paste the template where needed

3. **Managing Templates**
   - Edit existing templates using the "Edit Template" button
   - Delete templates using the "Delete Template" button
   - All changes are saved automatically

## Directory Structure

```
TextInserter/
├── v2.0/
│   ├── Files/
│   │   ├── TicketNotifications/
│   │   └── ChatTemplates/
├── TextFileInserter.py
├── build.bat
└── README.md
```

## Requirements

- Windows 10 or later
- Python 3.8 or later (for building from source)
- Required Python packages:
  - keyboard
  - pyperclip
  - tkinter

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

- **Dobrin Mihai-Alexandru**
  - GitHub: [@Dobrin Mihai-Alexandru](https://github.com/pewfike)

## Acknowledgments

- Thanks to all contributors and users for their feedback and support
