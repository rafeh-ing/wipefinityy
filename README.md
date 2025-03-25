# wipefinityy
Wipefinity is a secure file deletion tool built with Python and PyQt5 that provides multiple methods for permanently removing files from your system
Key Features
Multiple Deletion Methods:

Standard Deletion (simple file removal)

Secure Overwrite (overwrites file contents with random data before deletion)

User-Friendly Interface:

Clean, modern GUI with intuitive controls

Progress bar for tracking deletion progress

Confirmation dialogs to prevent accidental deletions

Dark/light mode toggle

Security Features:

Uses Python's secrets module for cryptographically secure random data generation

Comprehensive error handling

Logging system that records all operations

Visual Design:

Custom styling with hover effects and animations

Custom application icon

Themed progress bars and buttons

Technical Implementation
The application is built using:

PyQt5 for the graphical interface

Python's os module for file operations

secrets module for secure random data generation

logging module for operation tracking

Usage Workflow
User selects a file through the file dialog

Chooses a deletion method from the dropdown

Confirms the deletion in a verification dialog

The application performs the deletion with progress updates

Success/failure message is displayed upon completion

Security Considerations
The secure overwrite method provides protection against file recovery tools by:

Overwriting file contents byte-by-byte with random data

Ensuring complete destruction of original content

Finally removing the file metadata through standard deletion

Potential Enhancements
Additional overwrite patterns (DoD 5220.22-M, Gutmann method)

Support for multiple file/folder deletion

Integration with system recycle bin

File shredding animation effects

More detailed progress reporting

This application is particularly useful for:

Securely deleting sensitive documents

Preparing devices for disposal

Maintaining privacy when sharing storage media

Complying with data protection regulations

The combination of a simple interface with robust security features makes Wipefinity a practical tool for both casual and security-conscious users.
