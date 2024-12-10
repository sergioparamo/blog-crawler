from bs4 import BeautifulSoup
from weasyprint import HTML
from flask import g
import concurrent.futures
from src.api.utils.socketio_utils import socketio
from src.api.utils.context.context import request_id_var

user_folder = None

def generate_pdf_with_weasyprint(content, year):
    """Generate a PDF from blog content for a specific year."""
    socketio.emit('log', {'log': f"Generating PDF for {year}", 'requestId': request_id_var.get()})
    file_name = user_folder + f"/blog_{year}.pdf"

    html_content = """
    <html>
    <head>
        <style>
            body { font-family: Arial, sans-serif; margin: 2cm; }
            h1 { font-size: 24px; color: #333; }
            h2 { font-size: 20px; color: #555; }
            p { font-size: 14px; color: #333; margin: 0.5em 0; }
            img { max-width: 100%; margin: 1em 0; display: block; }
        </style>
    </head>
    <body>
    """
    
    html_content += f"<h1>Blog Posts from {year}</h1>"

    for month_data in content['months']:
        if not month_data['posts']:
            continue
        html_content += f"<h2>Month {month_data['month']}</h2>"

        for post in month_data['posts']:
            html_content += f"<h3>{post['date']} - {post['title']}</h3>"
            for item in post['content']:
                html_content += f"<p>{item}</p>"

    html_content += "</body></html>"
    
    final_soup = BeautifulSoup(html_content, "html.parser")
    HTML(string=str(final_soup)).write_pdf(file_name)

def generate_pdfs_in_parallel(content, given_user_folder):
    global user_folder
    user_folder = given_user_folder
    """Generate PDFs for all years in parallel."""
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for year_data in content:
            year = year_data['year']
            futures.append(executor.submit(generate_pdf_with_weasyprint, year_data, year))
        for future in futures:
            future.result()