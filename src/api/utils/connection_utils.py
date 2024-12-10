import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import re

ua = UserAgent()

proxies = []

should_use_proxies=False

def fetch_proxies_spys():
    """Fetch proxies from spys.me."""
    url = "https://spys.me/proxy.txt"
    response = simple_get(url)
    if response and response.status_code == 200:
        proxies = re.findall(r"[0-9]+(?:\.[0-9]+){3}:[0-9]+", response.text)
        return proxies
    return []

def fetch_proxies_free_proxy_list():
    """Fetch proxies from free-proxy-list.net."""
    url = "https://free-proxy-list.net/"
    response = simple_get(url)
    if response and response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        td_elements = soup.select('.fpl-list .table tbody tr td')
        proxies = []
        for j in range(0, len(td_elements), 8):
            ip = td_elements[j].text.strip()
            port = td_elements[j + 1].text.strip()
            proxies.append(f"{ip}:{port}")
        return proxies
    return []

def load_proxies():
    """Load proxies from multiple sources and store them in the global variable."""
    global proxies
    proxies = fetch_proxies_spys() + fetch_proxies_free_proxy_list()
    #add_log(f"Loaded {len(proxies)} proxies.")
    proxies = list(set(proxies))

def simple_get(url):
    """Perform a GET request"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        return response

def proxy_get(url):
    """Perform a GET request with a persistent proxy and User-Agent until the proxy fails."""
    global proxies

    if not proxies:
        #add_log("No proxies available using normal get.")
        return simple_get(url)

    current_proxy = proxies[0]
    random_ua = ua.random
    headers = {"User-Agent": random_ua}
    proxy_dict = {"http": current_proxy, "https": current_proxy}

    while proxies:
        try:
            #add_log(f"Using proxy: {current_proxy} and User-Agent: {random_ua}")
            response = get_request_with_proxies(url, headers=headers, proxies=proxy_dict, timeout=10)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            proxies.remove(current_proxy)
            if not proxies:
                #add_log("No proxies left to try.")
                return None
            else:
                current_proxy = proxies[0]
                proxy_dict = {"http": current_proxy, "https": current_proxy}
    return None

def get_request_with_proxies(url):
    """Decide whether to use proxies or not for a request."""
    global should_use_proxies
    if should_use_proxies == True:
        if not proxies:
            #add_log("No proxies available.")
            return None
        return proxy_get(url)
    else:
        return simple_get(url)