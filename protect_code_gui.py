import sys
import os
from PyQt5 import QtWidgets, QtCore, QtGui
from github import Github, GithubException
from pathlib import Path
import base64
from datetime import datetime

# Supported licenses mapping (GitHub license API key)
LICENSES = {
    "MIT License": "mit",
    "Apache License 2.0": "apache-2.0",
    "GNU General Public License v3.0": "gpl-3.0",
    "BSD 3-Clause License": "bsd-3-clause",
    # Add more licenses as needed
}

class GitHubUploader(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.github = None
        self.user = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle('GitHub Project Uploader')
        self.setGeometry(100, 100, 700, 600)
        self.setStyleSheet("""
            QWidget {
                background-color: #2e2e2e;
                color: #ffffff;
                font-family: Arial;
                font-size: 14px;
            }
            QLineEdit, QTextEdit, QComboBox {
                background-color: #3e3e3e;
                color: #ffffff;
                border: 1px solid #555555;
                padding: 5px;
            }
            QPushButton {
                background-color: #5e5e5e;
                color: #ffffff;
                border: none;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #7e7e7e;
            }
            QLabel {
                color: #ffffff;
            }
        """)

        layout = QtWidgets.QVBoxLayout()

        # GitHub Token
        token_layout = QtWidgets.QHBoxLayout()
        token_label = QtWidgets.QLabel("GitHub Token:")
        self.token_input = QtWidgets.QLineEdit()
        self.token_input.setEchoMode(QtWidgets.QLineEdit.Password)
        token_layout.addWidget(token_label)
        token_layout.addWidget(self.token_input)
        layout.addLayout(token_layout)

        # Authenticate Button
        self.auth_button = QtWidgets.QPushButton("Authenticate")
        self.auth_button.clicked.connect(self.authenticate)
        layout.addWidget(self.auth_button)

        # Project Directory Selection
        dir_layout = QtWidgets.QHBoxLayout()
        dir_label = QtWidgets.QLabel("Project Directory:")
        self.dir_input = QtWidgets.QLineEdit()
        self.dir_input.setReadOnly(True)
        self.dir_button = QtWidgets.QPushButton("Browse")
        self.dir_button.clicked.connect(self.browse_directory)
        dir_layout.addWidget(dir_label)
        dir_layout.addWidget(self.dir_input)
        dir_layout.addWidget(self.dir_button)
        layout.addLayout(dir_layout)

        # Repository Name
        repo_layout = QtWidgets.QHBoxLayout()
        repo_label = QtWidgets.QLabel("Repository Name:")
        self.repo_input = QtWidgets.QLineEdit()
        repo_layout.addWidget(repo_label)
        repo_layout.addWidget(self.repo_input)
        layout.addLayout(repo_layout)

        # Description
        desc_layout = QtWidgets.QHBoxLayout()
        desc_label = QtWidgets.QLabel("Description:")
        self.desc_input = QtWidgets.QLineEdit()
        desc_layout.addWidget(desc_label)
        desc_layout.addWidget(self.desc_input)
        layout.addLayout(desc_layout)

        # License Selection
        license_layout = QtWidgets.QHBoxLayout()
        license_label = QtWidgets.QLabel("License:")
        self.license_combo = QtWidgets.QComboBox()
        self.license_combo.addItems(LICENSES.keys())
        license_layout.addWidget(license_label)
        license_layout.addWidget(self.license_combo)
        layout.addLayout(license_layout)

        # Author Name
        author_layout = QtWidgets.QHBoxLayout()
        author_label = QtWidgets.QLabel("Author Name:")
        self.author_input = QtWidgets.QLineEdit()
        author_layout.addWidget(author_label)
        author_layout.addWidget(self.author_input)
        layout.addLayout(author_layout)

        # Patent Notice (optional)
        patent_layout = QtWidgets.QHBoxLayout()
        patent_label = QtWidgets.QLabel("Patent Notice (optional):")
        self.patent_input = QtWidgets.QLineEdit()
        patent_layout.addWidget(patent_label)
        patent_layout.addWidget(self.patent_input)
        layout.addLayout(patent_layout)

        # Upload Button
        self.upload_button = QtWidgets.QPushButton("Upload to GitHub")
        self.upload_button.clicked.connect(self.upload_to_github)
        self.upload_button.setEnabled(False)
        layout.addWidget(self.upload_button)

        # Status Display
        self.status_display = QtWidgets.QTextEdit()
        self.status_display.setReadOnly(True)
        layout.addWidget(self.status_display)

        self.setLayout(layout)

    def log_status(self, message):
        self.status_display.append(message)

    def authenticate(self):
        token = self.token_input.text().strip()
        if not token:
            QtWidgets.QMessageBox.warning(self, "Input Error", "Please enter your GitHub Personal Access Token.")
            return
        try:
            self.github = Github(token)
            self.user = self.github.get_user()
            self.log_status(f"Authenticated as {self.user.login}")
            self.upload_button.setEnabled(True)
            QtWidgets.QMessageBox.information(self, "Success", f"Authenticated as {self.user.login}")
        except GithubException as e:
            error_message = e.data['message'] if e.data and 'message' in e.data else str(e)
            self.log_status(f"Authentication failed: {error_message}")
            QtWidgets.QMessageBox.critical(self, "Authentication Failed", f"Failed to authenticate: {error_message}")

    def browse_directory(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Project Directory")
        if directory:
            self.dir_input.setText(directory)

    def upload_to_github(self):
        if not self.github or not self.user:
            QtWidgets.QMessageBox.warning(self, "Authentication Error", "Please authenticate first.")
            return

        project_path = self.dir_input.text().strip()
        if not project_path or not os.path.isdir(project_path):
            QtWidgets.QMessageBox.warning(self, "Directory Error", "Please select a valid project directory.")
            return

        repo_name = self.repo_input.text().strip()
        if not repo_name:
            QtWidgets.QMessageBox.warning(self, "Input Error", "Please enter a repository name.")
            return

        description = self.desc_input.text().strip()
        license_name = self.license_combo.currentText()
        license_key = LICENSES.get(license_name, "mit")
        author = self.author_input.text().strip()
        patent_notice = self.patent_input.text().strip()

        if not author:
            QtWidgets.QMessageBox.warning(self, "Input Error", "Please enter the author name.")
            return

        try:
            # Create repository
            self.log_status("Creating repository on GitHub...")
            repo = self.user.create_repo(
                name=repo_name,
                description=description,
                private=False,  # Modify if you want to create a private repo
                auto_init=False
            )
            self.log_status(f"Repository '{repo_name}' created successfully.")

            # Add License
            self.log_status("Adding license...")
            license_content = self.get_license_content(license_key)
            if license_content:
                repo.create_file("LICENSE", "Add license", license_content)
                self.log_status("License added.")

            # Add README with description and copyright
            self.log_status("Adding README...")
            current_year = datetime.now().year
            readme_content = f"# {repo_name}\n\n{description}\n\n" \
                             f"© {current_year} {author}"
            repo.create_file("README.md", "Add README", readme_content)
            self.log_status("README added.")

            # Add PATENTS file if provided
            if patent_notice:
                self.log_status("Adding PATENTS notice...")
                patent_content = patent_notice
                repo.create_file("PATENTS", "Add PATENTS notice", patent_content)
                self.log_status("PATENTS notice added.")

            # Upload project files
            self.log_status("Uploading project files...")
            self.upload_directory(repo, project_path, "")
            self.log_status("All files uploaded successfully.")

            QtWidgets.QMessageBox.information(self, "Success", f"Project '{repo_name}' uploaded to GitHub successfully!")

        except GithubException as e:
            error_message = e.data['message'] if e.data and 'message' in e.data else str(e)
            self.log_status(f"GitHub Error: {error_message}")
            QtWidgets.QMessageBox.critical(self, "GitHub Error", f"An error occurred: {error_message}")
        except Exception as e:
            self.log_status(f"Error: {str(e)}")
            QtWidgets.QMessageBox.critical(self, "Error", f"An unexpected error occurred: {str(e)}")

    def get_license_content(self, license_key):
        try:
            license_obj = self.github.get_repo("github/choosealicense.com").get_contents(f"licenses/{license_key}.txt")
            license_text = license_obj.decoded_content.decode()
            # Replace placeholders if necessary
            current_year = datetime.now().year
            license_text = license_text.replace("[year]", str(current_year)).replace("[fullname]", self.author_input.text().strip())
            return license_text
        except GithubException as e:
            self.log_status(f"Failed to get license content: {e.data['message'] if e.data else str(e)}")
            QtWidgets.QMessageBox.critical(self, "License Error", f"Failed to retrieve license: {e.data['message'] if e.data else str(e)}")
            return None

    def upload_directory(self, repo, directory_path, repo_path):
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, directory_path)
                target_path = os.path.join(repo_path, relative_path).replace("\\", "/")

                with open(file_path, "rb") as f:
                    content = f.read()

                try:
                    # Check if the file already exists
                    contents = repo.get_contents(target_path)
                    repo.update_file(contents.path, f"Update {relative_path}", content, contents.sha)
                    self.log_status(f"Updated: {target_path}")
                except GithubException as e:
                    if e.status == 404:
                        # File does not exist, create it
                        repo.create_file(target_path, f"Add {relative_path}", content)
                        self.log_status(f"Added: {target_path}")
                    else:
                        self.log_status(f"Failed to add/update {target_path}: {e.data['message'] if e.data else str(e)}")

def main():
    app = QtWidgets.QApplication(sys.argv)
    uploader = GitHubUploader()
    uploader.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
