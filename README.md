
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

- **Dynamic Blog Crawling**: Crawl any blog by providing its base URL and the years to scrape.
- **Content Parsing**: Extracts post titles, dates, and content (including images).
- **PDF Generation**: Creates beautifully formatted PDFs for each year's posts.
- **Content Archival**: Saves scraped data in a JSON file for reuse.
- **Queue Processing**: Uses Celery for long-running tasks, backed by RabbitMQ.
- **Real-time Updates**: Uses Socket.IO for real-time progress updates.
- **Downloadable Results**: Provides a downloadable ZIP file containing the generated PDFs.
- **Reset and Clean-up**: Allows users to reset the crawler and clear the data.
- **Stop Crawling**: Provides a stop button to interrupt ongoing crawls.

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

## Blog format

### URL Format sample:

The blog posts follow a consistent URL format across all years. Each URL is structured hierarchically to organize posts by year, month, pagination (if applicable), and individual post titles. Here's the breakdown:

- **Base URL**: The base URL of the blog, e.g., `https://www.test.com/`.
- **Year**: The year of the blog post, e.g., `2024`.
- **Month**: The month of the blog post, e.g., `12`.
- **Pagination**: Optional pagination for multiple posts in a single month, e.g., `page/2/`.
- **Title**: The title of the blog post, e.g., `post-title`.

For example, the URL for a blog post on December 20, 2024, is `https://www.test.com/2024/12/post-title`.

Or in the case of pagination, `https://www.test.com/2024/12/page/2/post-title`.

### HTML Format sample:

The format of the blog posts is expected to be the same. The script will scrape the blog page for each year and month and extract the necessary information for each post (title, date, and content).

```html
<article class="post">
  <header class="entry-header">
    <h1 class="entry-title">Blog Post Title</h1>
    <div class="entry-meta">
      <span class="screen-reader-text">Posted on</span>
      <a href="https://www.test.com/2024/12/post-title" rel="bookmark"
        ><time
          class="entry-date published updated"
          datetime="2024-12-20T12:44:12+09:00"
          >December 20, 2024</time
        ></a
      >
    </div>
  </header>
  <div class="entry-content">
    <p>This is the content of the blog post...</p>
  </div>
</article>
```

## Format breakdown:

- `<article class="post">`: The main container for the blog post.
- `<header class="entry-header">`: The header section containing the post title and date.
- `<div class="entry-content">`: The content of the blog post.

## Running the Project

### Docker

1. Clone the repository:
   ```bash
   git clone https://github.com/sergioparamo/blog-crawler.git
   cd blog-crawler
   ```

2. Build and run the Docker containers:
   ```bash
   docker-compose build
   docker-compose up -d
   ```

3. Access the frontend at http://localhost:80

4. Access the backend API at http://localhost:5000

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
   ```bash
   curl -u username:password -X PUT http://localhost:15672/api/vhosts/test
   ```

6. Run the Flask API:
   ```bash
   python3 -m src.api.app
   ```

6. Start Celery Worker:
   ```bash
   celery -A src.api.tasks.tasks worker --loglevel=info --pool=eventlet
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

### `/api/stop/<task_id>` (POST)
- **Description**: Stops the Celery task with the given task ID.

---