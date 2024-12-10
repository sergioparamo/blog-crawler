
# 📚🔎 Blog Crawler Project

## Overview

The Blog Crawler is a system designed to scrape blog content based on specified years and generate JSON and PDF files. The project consists of a **Frontend**, a **Backend API**, and **Background Task Processing**.

---

## Architecture

The project architecture follows a **microservices-inspired** approach:
1. **Frontend**: React-based UI for user interactions.
2. **API Backend**: Flask-based API for processing requests and managing crawls.
3. **Task Queue**: Celery handles long-running crawling tasks, backed by RabbitMQ.
4. **Real-Time Updates**: Socket.IO for real-time progress, logs and state updates.

---

## Features

- Crawl blogs by specifying years or ranges.
- Generate JSON and PDF files of blog data.
- Real-time logs and progress updates.
- Downloadable ZIP files containing results.
- Reset and clean-up functionality.

---

## Tools and Technologies

### Backend:
- **Flask**: Web framework for building APIs.
- **Celery**: Distributed task queue for background processing.
- **RabbitMQ**: Broker and result backend for Celery.
- **Socket.IO**: Real-time communication.

### Frontend:
- **React**: For building the user interface.
- **Axios**: For API communication.

### Others:
- **Gunicorn**: Production-grade WSGI server.
- **Eventlet**: For asynchronous support in Flask.

---

## File Structure

### Backend API

- **`src/api`**
  - **`controllers`**: Controllers for API endpoints.
  - **`services`**: Services for business logic.
  - **`tasks`**: Celery tasks for background processing.
  - **`utils`**: Helper functions for file management, crawling logic, and PDF generation.
   - **`requirements.txt`**: Python dependencies.

### Frontend
- **`src/app`**: React components for the UI.
   - **`components`**: Custom components for the UI.
      - **`Icons.tsx`**: SVG icons used in the UI.
      - **`Logs.tsx`**: Component for displaying logs.
      - **`ProgressBar.tsx`**: Component for displaying progress bars.
      - **`YearSelector.tsx`**: Component for year selection.
   - **`App.tsx`**: Main React component for the UI.
   - **`index.css`**: Custom styles for the UI.
   - **`main.tsx`**: Entry point for the React app.

### Downloads Folder

- **`/data/downloads`**: Directory where user-specific folders are created for results.
   - **`<user_id>`**: User-specific folder for temporary files.
   - **`<user_id>_blog_data.zip`**: Generated data with JSON and PDF files.

---

## Pre-requisites

- Python 3.12+
- Node.js 22+
- Docker

## Installation

### Backend

1. Clone the repository:
   ```bash
   git clone https://github.com/sergioparamo/blog-crawler.git
   cd blog-crawler
   ```

2. Set up a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   cd src/api
   pip install -r requirements.txt
   ```

4. Start RabbitMQ on docker:
   ```bash
   docker run -d --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:management
   ```

5. Create a RabbitMQ virtual host named "test". See this link for more info: https://www.rabbitmq.com/docs/vhosts

6. Run the Flask API:
   ```bash
   python3 -m src.api.app
   ```

6. Start Celery Worker:
   ```bash
   celery -A src.api.tasks.tasks worker --loglevel=info
   ```

### Frontend

2. Install dependencies:
   ```bash
   npm install
   ```

3. Run the development server:
   ```bash
   npm start
   ```

---

## API Endpoints

### `/api/crawl` (POST)
- **Description**: Starts a crawling task.
- **Request Body**:
  ```json
  {
    "blogUrl": "http://example.com",
    "years": [2021, 2022],
    "populateBetween": true
  }
  ```

### `/api/download/<request_id>` (GET)
- **Description**: Downloads the results as a ZIP file.

### `/api/reset/<request_id>` (POST)
- **Description**: Resets the process for the given request ID and removes the user-specific file.

---