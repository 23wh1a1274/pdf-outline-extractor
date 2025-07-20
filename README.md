# Adobe India Hackathon 2025 - Round 2

## 🚀 Overview
An intelligent PDF reading web app using Adobe PDF Embed API and smart outline/persona extraction.

## 🛠 Tech Stack
- Frontend: React + Adobe Embed API
- Backend: Flask + PyMuPDF
- Containerized with Docker

## 📦 How to Run

### Backend
```bash
cd backend
docker build -t adobe-backend .
docker run -p 5000:5000 adobe-backend
