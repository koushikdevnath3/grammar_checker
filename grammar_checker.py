import requests
from bs4 import BeautifulSoup
from language_tool_python import LanguageTool
from urllib.parse import urljoin, urlparse

def fetch_webpage_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the webpage {url}: {e}")
        return None

def check_grammar(url, text):
    tool = LanguageTool('en-US')
    matches = tool.check(text)

    if matches:
        print(f"Grammar Mistakes in {url}:")
        for match in matches:
            print(match)

def get_all_links(url, webpage_content):
    soup = BeautifulSoup(webpage_content, 'html.parser')
    links = [a.get('href') for a in soup.find_all('a', href=True)]
    full_links = [urljoin(url, link) for link in links]
    return set(full_links)

def crawl_and_check(url, visited_urls=set()):
    if url in visited_urls:
        return

    
    webpage_content = fetch_webpage_content(url)
    if webpage_content is None:
        return

    
    check_grammar(url, BeautifulSoup(webpage_content, 'html.parser').get_text())

    
    visited_urls.add(url)

    
    links = get_all_links(url, webpage_content)

    
    for link in links:
        crawl_and_check(link, visited_urls)

def main():
    start_url = input("Enter the starting URL of the website: ")
    crawl_and_check(start_url)

if __name__ == "__main__":
    main()