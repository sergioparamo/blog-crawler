"""Blog crawling utilities."""
from bs4 import BeautifulSoup
import time

from src.api.utils.connection_utils import get_request_with_proxies
from src.api.utils.date_utils import format_date
from src.api.utils.socketio_utils import socketio
from src.api.utils.context.context import request_id_var

def check_if_month_exists(base_url, year, month):
    try:
        response = get_request_with_proxies(f"{base_url}/{year}/{str(month).zfill(2)}")
        return response.status_code == 200
    except Exception as e:
        socketio.emit('log', {'log': f"Error checking if month {year}-{month} exists: {e}", 'requestId': request_id_var.get()})
        return False

def check_if_year_exists(base_url, year):
    try:
        response = get_request_with_proxies(f"{base_url}/{year}")
        return response.status_code == 200
    except Exception as e:
        socketio.emit('log', {'log': f"Error checking if year {year} exists: {e}", 'requestId': request_id_var.get()})
        return False

def extract_post_data(post_url):
    try:
        response = get_request_with_proxies(post_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract the date
        date_element = soup.find('time')
        date = date_element.text.strip() if date_element else 'No date'

        # Extract the title
        title_element = soup.find('h1', class_='entry-title')
        title = title_element.text.strip() if title_element else 'No title'

        socketio.emit('log', {'log': f"Crawling post: {title} ({date})", 'requestId': request_id_var.get()})

        # Extract the content
        article_element = soup.find('article')
        if not article_element:
            socketio.emit('log', {'log': f"Missing article element for {post_url}", 'requestId': request_id_var.get()})
            return None

        content_div = article_element.find('div', class_='entry-content')
        if not content_div:
            socketio.emit('log', {'log': f"Missing entry-content for {post_url}", 'requestId': request_id_var.get()})
            return None
            
        content = []
        for element in content_div:
            content.append(str(element))
        
        return {
            "date": format_date(date),
            "title": title,
            "content": content,
            "url": post_url
        }
    except Exception as e:
        socketio.emit('log', {'log': f"Error extracting post data from {post_url}: {e}", 'requestId': request_id_var.get()})
        return None

def find_last_page_from_nav(base_url):
    try:
        response = get_request_with_proxies(base_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Locate the navigation element
        nav = soup.find('nav', class_='navigation pagination')
        if not nav:
            socketio.emit('log', {'log': "No navigation element found.", 'requestId': request_id_var.get()})
            return None

        # Find dots and page numbers
        dots = nav.find('span', class_='page-numbers dots')
        if dots:
            # Get the last `a` after the dots span
            last_page_link = dots.find_next('a', class_='page-numbers')
            if last_page_link:
                last_page_url = last_page_link['href']
                # Extract the last page number from the URL
                last_page = int(last_page_url.split('/page/')[-1].strip('/'))
                return last_page

        # If no dots span, find the last `a` with page-numbers class
        last_page_link = nav.find_all('a', class_='page-numbers')[-1]
        last_page_url = last_page_link['href']
        last_page = int(last_page_url.split('/page/')[-1].strip('/'))
        return last_page

    except Exception as e:
        socketio.emit('log', {'log': f"Error extracting last page from navigation: {e}", 'requestId': request_id_var.get()})
        return None

def find_last_page(base_url):
    socketio.emit('log', {'log': "Using fallback method to find last page.", 'requestId': request_id_var.get()})
    current_page = 1

    while True:
        page_url = f"{base_url}/page/{current_page}/"
        response = get_request_with_proxies(page_url)

        if response.status_code != 200:
            break  # Stop when no next page exists (404 or similar)

        current_page += 1

    socketio.emit('log', {'log': f"Last page found: {current_page - 1}", 'requestId': request_id_var.get()})
    return current_page - 1  # The last valid page number

def find_last_page_dynamic(base_url):
    last_page = find_last_page_from_nav(base_url)
    if last_page:
        socketio.emit('log', {'log': f"Last page found from navigation: {last_page}", 'requestId': request_id_var.get()})
        return last_page
    else:
        return find_last_page(base_url)

def crawl_blog_month(blog_url, year, month):
    socketio.emit('log', {'log': f"Processing {year}/{month}", 'requestId': request_id_var.get()})
    base_url = f"{blog_url}/{year}/{str(month).zfill(2)}"
    last_page = find_last_page_dynamic(base_url)

    if last_page is None:  # Check if the process was stopped
        return {"month": month, "posts": []}

    month_data = {"month": month, "posts": []}

    # Start from the last page and work backwards
    for page in range(last_page, 0, -1):

        page_url = f"{base_url}/page/{page}/" if page > 1 else base_url
        socketio.emit('log', {'log': f"Processing page {last_page - page + 1} of {last_page}", 'requestId': request_id_var.get()})

        try:
            response = get_request_with_proxies(page_url)
            if response.status_code == 404:
                continue

            soup = BeautifulSoup(response.text, 'html.parser')
            posts = soup.find_all('h2', class_='entry-title')

            for post in reversed(posts):
                post_url = post.find('a')['href']
                post_data = extract_post_data(post_url)
                if post_data:
                    month_data['posts'].append(post_data)
                time.sleep(0.5)
        except Exception as e:
            socketio.emit('log', {'log': f"Error processing {page_url}: {e}", 'requestId': request_id_var.get()})
            continue

    return month_data
