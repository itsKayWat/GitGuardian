GitGuardian-Uploader
===================

A GUI tool for creating properly structured and protected GitHub repositories.

Purpose
-------
This tool automates the process of creating GitHub repositories with proper licensing, documentation, and intellectual property protection. It's designed for developers who want to ensure their projects are properly protected and structured from the start.

Requirements
-----------
- Python 3.7+
- GitHub Personal Access Token
- PyQt5
- PyGithub
- Internet connection

Installation
-----------
1. Clone the repository:
   git clone https://github.com/yourusername/GitGuardian-Uploader
2. Navigate to the directory:
   cd GitGuardian-Uploader
3. Install requirements:
   python requirements.py

Usage
-----
1. Run: python protect_code_gui.py
2. Enter your GitHub token
3. Select your project directory
4. Fill in repository details
5. Choose a license
6. Click "Upload to GitHub"

The tool will automatically:
- Create the repository
- Add license protection
- Generate README
- Add patent notices (if specified)
- Upload all project files

Use Case Example
--------------
A developer has created a new software tool and wants to share it on GitHub while ensuring proper licensing and protection. Instead of manually creating files and uploading content, they can use GitGuardian-Uploader to handle everything in one step, ensuring nothing is forgotten.