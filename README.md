Skills Folder Manager
A PyQt6-based desktop application for managing candidate skills folder and matching them with job offers using AI-powered analysis.
Overview
This application helps teams efficiently manage candidate profiles, generate comprehensive skills folders with CVs, and automatically match candidates to job opportunities using artificial intelligence.
Features

Skills Folder Generation: Create organized skills folder containing candidate CVs and competency profiles
AI-Powered Matching: Intelligent comparison between job offers and candidate profiles to identify the best fits
Candidate Management: Centralized database for storing and organizing candidate information
Job Offer Analysis: Parse and analyze job requirements to find optimal candidates
User-Friendly Interface: Intuitive PyQt6 GUI for seamless navigation and operation

Requirements

Python 3.8 or higher
PyQt6
Additional dependencies (see requirements.txt)

Installation

Clone this repository:

bashgit clone <repository-url>
cd <project-folder>

Create a virtual environment :

bashpython -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

Install dependencies:

bashpip install -r requirements.txt
Usage

Launch the application:

bashpython main.py

Adding Candidates: Import candidate CVs and profiles into the system
Creating Skills Folders: Generate comprehensive skills portfolios for selected candidates
Matching Candidates to Jobs: Input job offer details and let the AI analyze and rank the best-fit candidates

Configuration
[to get api keys and database contact me]
Project Structure
project-folder/
├── main.py              # Application entry point
├── requirements.txt     # Python dependencies
├── /treatments          # to controll actions
├── /data                # to handly data
└── /ressources          # Images, icons, etc.
AI Integration
The application uses AI algorithms to:

Parse and extract key information from CVs
Analyze job offer requirements
Score and rank candidate-job matches based on skills, experience, and qualifications

Contributing
This is an internal company tool. For questions or suggestions, contact develop [i.kouici@insta.fr].

Internal use only - [Nava engineering]
Support
For technical issues or feature requests, please contact [i.kouici@insta.fr]
