# NayePankh AI NGO Assistant

## Project Overview

NayePankh AI NGO Assistant is a Flask-based web application developed to support NGO operations through conversational AI, volunteer management, donation registration, and administrative monitoring.

The system enables users to interact with an AI-powered chatbot, register as volunteers, express donation interest, and learn about NGO programs through a user-friendly interface.

---

## Problem Statement

Non-Governmental Organizations often face challenges in:

* Managing volunteer registrations efficiently
* Handling donor inquiries
* Providing instant responses to user questions
* Maintaining volunteer and donor records
* Offering 24/7 support without increasing operational costs

This project addresses these challenges through an AI-powered chatbot and workflow automation system.

---

## Objectives

* Develop a 24/7 NGO support chatbot
* Automate volunteer registration
* Automate donation inquiry collection
* Store volunteer and donor information in a database
* Provide an administrative dashboard
* Integrate Generative AI for intelligent responses

---

## Features

### AI Chatbot

* Conversational NGO assistant
* AI-powered responses using Google Gemini API
* NGO-specific contextual responses

### Volunteer Registration Workflow

Multi-step registration process:

1. Name
2. Email
3. Phone Number
4. Skills
5. Weekly Availability

Data is stored in SQLite database.

### Donation Workflow

Multi-step donation inquiry process:

1. Name
2. Email
3. Phone Number
4. Donation Amount
5. Supported Cause

Data is stored in SQLite database.

### Admin Dashboard
(for navigation use :..localhost../admin)
* View volunteer records
* View donation records
* Centralized management interface

### Database Integration

SQLite database used for:

* Volunteer records
* Donation records

### User-Friendly Interface

* Responsive chatbot UI
* Real-time interaction
* Simple navigation

---

## Technologies Used

### Frontend

* HTML5
* CSS3
* JavaScript

### Backend

* Python
* Flask

### Database

* SQLite

### AI Integration

* Google Gemini API

### Development Tools

* Visual Studio Code
* Git
* GitHub

---

## System Architecture

User
↓
Web Interface
↓
Flask Application
↓
├── Volunteer Workflow
├── Donation Workflow
├── Gemini AI Engine
└── SQLite Database
↓
Admin Dashboard

---

## Database Tables

### Volunteers

| Field  | Type    |
| ------ | ------- |
| id     | Integer |
| name   | Text    |
| email  | Text    |
| phone  | Text    |
| skills | Text    |
| hours  | Text    |

### Donations

| Field  | Type    |
| ------ | ------- |
| id     | Integer |
| name   | Text    |
| email  | Text    |
| phone  | Text    |
| amount | Text    |
| cause  | Text    |

---

## Installation

### Clone Repository

git clone <repository_url>

### Navigate to Project

cd NayePankh_AI_Chatbot_Project

### Install Dependencies

pip install -r requirements.txt

### Run Application

python app.py

### Open Browser

http://127.0.0.1:5000

---

## Future Enhancements

* AI-powered NGO analytics
* Email notifications
* Volunteer recommendation system
* Online payment gateway integration
* User authentication
* Cloud database deployment
* Report generation
* Sentiment analysis

---

## Learning Outcomes

This project demonstrates:

* Full-stack web development
* AI API integration
* Workflow automation
* Database management
* Flask framework implementation
* NGO technology solutions

---

##  

Developed as an AI-powered NGO Management and Support System for NayePankh Foundation.
