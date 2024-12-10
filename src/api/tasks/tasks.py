import json
import os
import shutil
from zipfile import ZipFile
from urllib import request
from celery import Celery
from flask import Flask
from src.api.utils.crawler_utils import check_if_year_exists, crawl_blog_month, check_if_month_exists
from src.api.utils.pdf_generator import generate_pdfs_in_parallel
from src.api.utils.files_utils import downloads_folder, zip_files
from src.api.utils.socketio_utils import socketio
from src.api.utils.context.context import request_id_var

# Flask app factory
def create_app():
    app = Flask(__name__)
    return app

# Create Celery instance
app = Celery(
    __name__,
    broker='amqp://user:password@localhost:5672/test',
    backend='rpc://'
)

@app.task(bind=True)
def crawl_task(self, blog_url, years, populate_between, context):
    app = create_app()
    with app.app_context():
        request_id_var.set(context.get('request_id'))
        
        request.headers = context.get('headers', {})
                
        """Background process for crawling."""
        try:      
            
            if populate_between and len(years) >= 2:
                years = list(range(min(years), max(years) + 1))
            
            years = list(set(years))
            years.sort()
            socketio.emit('log', {'log': f"Years to crawl: {years}", 'requestId': request_id_var.get()})

            all_content = []
            total_years = len(years)
            total_steps = total_years * 12
            current_step = 0

            socketio.emit('log', {'log': f"Starting crawl process for {blog_url}", 'requestId': request_id_var.get()})

            for year in years:
                if not check_if_year_exists(blog_url, year):
                    socketio.emit('log', {'log': f"No content found for year {year}", 'requestId': request_id_var.get()})
                    continue

                year_data = {"year": year, "months": []}
                socketio.emit('log', {'log': f"Processing year {year}", 'requestId': request_id_var.get()})

                for month in range(1, 13):

                    if not check_if_month_exists(blog_url, year, month):
                        socketio.emit('log', {'log': f"No content found for {year}/{month:02}", 'requestId': request_id_var.get()})
                        continue

                    current_step += 1
                    current_progress = (current_step / total_steps) * 100
                    socketio.emit('progress', {'progress': current_progress, 'requestId': request_id_var.get()})
                    
                    try:
                        # Crawl the month
                        month_data = crawl_blog_month(blog_url, year, month)
                        if month_data['posts']:
                            year_data["months"].append(month_data)
                            socketio.emit('log', {'log': f"Found {len(month_data['posts'])} posts for {year}/{month:02}", 'requestId': request_id_var.get()})
                        else:
                            socketio.emit('log', {'log': f"No posts found for {year}/{month:02}", 'requestId': request_id_var.get()})
                    except Exception as e:
                        socketio.emit('log', {'log': f"Error processing {year}/{month}: {e}", 'requestId': request_id_var.get()})
                        continue

                if year_data["months"]:
                    all_content.append(year_data)
                    socketio.emit('log', {'log': f"Completed year {year}", 'requestId': request_id_var.get()})

            # Create a folder for the user based on the request_id (UUID)
            user_folder = os.path.join(downloads_folder, request_id_var.get())
            os.makedirs(user_folder, exist_ok=True)
            
            socketio.emit('log', {'log': "Saving data...", 'requestId': request_id_var.get()})
            
            # Save JSON data in the user's folder
            json_path = os.path.join(user_folder, 'blog_data.json')
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(all_content, f, ensure_ascii=False, indent=2)
        
            socketio.emit('log', {'log': "JSON data saved", 'requestId': request_id_var.get()})
        
            socketio.emit('log', {'log': "Generating PDFs...", 'requestId': request_id_var.get()})
            
            generate_pdfs_in_parallel(all_content, user_folder)
            socketio.emit('log', {'log': "PDF generation complete", 'requestId': request_id_var.get()})
    
            socketio.emit('log', {'log': "Crawling complete", 'requestId': request_id_var.get()})
            
            socketio.emit('finished', {'requestId': request_id_var.get()})

        except Exception as e:
            socketio.emit('log', {'log': f"Error: {str(e)}", 'requestId': request_id_var.get()})
        finally:
            # using zipfile
            zip_files(user_folder, os.path.join(downloads_folder, request_id_var.get() + "_blog_data.zip"))
            # remove the folder
            shutil.rmtree(user_folder)
            socketio.emit('progress', {'progress': 100, 'requestId': request_id_var.get()})
            socketio.emit('finished', {'requestId': request_id_var.get()})