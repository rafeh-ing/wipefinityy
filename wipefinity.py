import sys
import os
import secrets
import logging
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog, QLabel, QComboBox, QProgressBar, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QCursor, QIcon


logging.basicConfig(filename='wipefinity.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class WipefinityApp(QWidget):
    def __init__(self):
        super().__init__()
        self.is_dark_mode = False 
        self.selected_file = None  
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Wipefinity - Secure File Deletion")
        
        
        self.setWindowIcon(QIcon("C:/Users/rafeh/OneDrive/Desktop/python/icon.png"))
        
        self.setGeometry(100, 100, 500, 600)

      
        font = QFont("Arial", 18)  
        self.setFont(font)

       
        self.label = QLabel("WIPEFINITY : YOUR ETERNAL SHREDDER", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 30px; color: #333333; margin: 15px; font-weight: bold;")

        
        self.select_button = QPushButton("Select File", self)
        self.select_button.setStyleSheet(self.button_style("#4CAF50"))
        self.select_button.clicked.connect(self.select_file)

       
        self.method_combo = QComboBox(self)
        self.method_combo.addItem("Select Deletion Method")
        self.method_combo.addItem("Standard Deletion")
        self.method_combo.addItem("Secure Overwrite")
        self.method_combo.setStyleSheet("background-color: #ffffff; padding: 15px; border-radius: 10px; font-size: 20px; color: #4CAF50;")

       
        self.delete_button = QPushButton("Delete File", self)
        self.delete_button.setStyleSheet(self.button_style("#FF5722"))
        self.delete_button.clicked.connect(self.confirm_deletion)
        self.delete_button.setEnabled(False)  

        
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)  
        self.progress_bar.setStyleSheet("QProgressBar {background-color: #dcdcdc; border-radius: 10px; }"
                                        "QProgressBar::chunk {background-color: #FF5722; border-radius: 10px;}")

        
        self.toggle_layout = QHBoxLayout()
        
        
        self.dark_mode_button = QPushButton("Switch to Dark Mode", self)
        self.dark_mode_button.setStyleSheet("background-color: #FF6347; color: white; font-size: 12px; font-weight: bold; border-radius: 5px; padding: 8px 16px;")
        self.dark_mode_button.clicked.connect(self.toggle_dark_mode)

        
        self.toggle_layout.addWidget(self.dark_mode_button)
        self.toggle_layout.setAlignment(Qt.AlignRight)  

       
        main_layout = QVBoxLayout()
        main_layout.addLayout(self.toggle_layout)
        main_layout.addWidget(self.label)
        main_layout.addWidget(self.select_button)
        main_layout.addWidget(self.method_combo)
        main_layout.addWidget(self.delete_button)
        main_layout.addWidget(self.progress_bar)

        self.setLayout(main_layout)

        
        self.set_custom_cursor()

        self.update_ui()

    def button_style(self, color):
        return f"""
        QPushButton {{
            background-color: {color};
            color: white;
            padding: 15px;
            border-radius: 10px;
            font-size: 20px;
            font-weight: bold;
            transition: all 0.3s ease;
        }}
        QPushButton:hover {{
            background-color: #FF9800;  
            transform: scale(1.1); 
        }}
        QPushButton:pressed {{
            background-color: #FF5722;  
            transform: scale(1.05);
        }}
        """

    def set_custom_cursor(self):
       
        self.setCursor(QCursor(Qt.PointingHandCursor))

    def select_file(self):
        file, _ = QFileDialog.getOpenFileName(self, "Select File", "", "All Files (*)")
        if file:
            self.label.setText(f"Selected file: {file}")
            self.selected_file = file
            self.delete_button.setEnabled(True)

    def confirm_deletion(self):
        
        if not self.selected_file:
            self.show_message("Error", "No file selected.", QMessageBox.Critical)
            return

        reply = QMessageBox.question(self, 'Confirm Deletion', 
                                     f"Are you sure you want to delete {self.selected_file}?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.delete_file()
        else:
            logging.info(f"User cancelled the deletion of {self.selected_file}")
            self.show_message("Deletion Cancelled", "The file was not deleted.", QMessageBox.Information)

    def delete_file(self):
        if self.selected_file:
            method = self.method_combo.currentText()

            if method == "Secure Overwrite":
                self.run_task(self.secure_overwrite, self.selected_file)
            
            elif method == "Standard Deletion":
                self.run_task(self.standard_delete, self.selected_file)
            else:
                self.show_message("Error", "Please select a valid deletion method.", QMessageBox.Critical)

    def run_task(self, task_function, *args):
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.delete_button.setEnabled(False)
        try:
            task_function(*args)
        except Exception as e:
            logging.error(f"Error during task: {e}")
            self.show_message("Error", f"An unexpected error occurred: {e}", QMessageBox.Critical)
            self.reset_ui()

    def update_progress(self, progress):
        self.progress_bar.setValue(progress)
        if progress == 100:
            self.delete_button.setEnabled(True)
            self.show_message("Success", "File deleted successfully.", QMessageBox.Information)
            self.reset_ui()

    def reset_ui(self):
        self.label.setText("WIPEFINITY : YOUR ETERNAL SHREDDER")
        self.progress_bar.setValue(0)
        self.delete_button.setEnabled(False)
        self.method_combo.setCurrentIndex(0)
        self.progress_bar.setVisible(False)

    def show_message(self, title, message, icon):
        msg = QMessageBox(self)
        msg.setIcon(icon)
        msg.setText(message)
        msg.setWindowTitle(title)
        msg.exec_()

    def standard_delete(self, file_path):
        try:
            os.remove(file_path)
            logging.info(f"Deleted file: {file_path}")
            self.update_progress(100)
        except FileNotFoundError:
            logging.error(f"File not found: {file_path}")
            self.show_message("Error", f"File not found: {file_path}", QMessageBox.Critical)
        except PermissionError:
            logging.error(f"Permission denied: {file_path}")
            self.show_message("Error", f"Permission denied: {file_path}", QMessageBox.Critical)
        except OSError:
            logging.error(f"File in use or other OS error: {file_path}")
            self.show_message("Error", f"File in use or other OS error: {file_path}", QMessageBox.Critical)
        except Exception as e:
            logging.error(f"Unexpected error deleting file: {e}")
            self.show_message("Error", f"Unexpected error: {e}", QMessageBox.Critical)

    def secure_overwrite(self, file_path):
        try:
            with open(file_path, 'r+b') as f:
                length = os.path.getsize(file_path)
                for i in range(length):
                    f.write(secrets.token_bytes(1))  # Overwrite with random data
                    if i % 100 == 0:  # Update progress every 100 bytes
                        self.update_progress(int(i / length * 100))
            os.remove(file_path)
            logging.info(f"Securely overwritten and deleted file: {file_path}")
            self.update_progress(100)
        except FileNotFoundError:
            logging.error(f"File not found: {file_path}")
            self.show_message("Error", f"File not found: {file_path}", QMessageBox.Critical)
        except Exception as e:
            logging.error(f"Error during secure overwrite: {e}")
            self.show_message("Error", f"Error during secure overwrite: {e}", QMessageBox.Critical)
            self.reset_ui()

    
    def toggle_dark_mode(self):
        self.is_dark_mode = not self.is_dark_mode
        self.update_ui()

    def update_ui(self):
        if self.is_dark_mode:
            self.setStyleSheet("background-color: #2e2e2e; color: white;")
            self.label.setStyleSheet("font-size: 30px; color: white; margin: 15px; font-weight: bold;")
            self.select_button.setStyleSheet(self.button_style("#4CAF50"))
            self.delete_button.setStyleSheet(self.button_style("#FF5722"))
        else:
            self.setStyleSheet("background-color: #ffffff; color: black;")
            self.label.setStyleSheet("font-size: 30px; color: #333333; margin: 15px; font-weight: bold;")
            self.select_button.setStyleSheet(self.button_style("#4CAF50"))
            self.delete_button.setStyleSheet(self.button_style("#FF5722"))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = WipefinityApp()
    window.show()
    sys.exit(app.exec_())
        
