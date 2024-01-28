import sys
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urlunparse

# Assuming the 'webpage2markdown_callable' module is correctly set up in the 'web2markdown' directory
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'web2markdown'))
from webpage2markdown_callable import convert_url_to_markdown

def get_domain_name(url):
    """
    Extract the full domain name from a URL to use for naming the output folder and URL list file.
    """
    parsed_url = urlparse(url)
    return parsed_url.netloc

def is_valid_url(url, valid_url_prefix):
    """
    Check if the URL starts with the specified valid URL prefix.
    """
    return url.startswith(valid_url_prefix)

def get_base_url(url):
    parsed_url = urlparse(url)
    return f"{parsed_url.scheme}://{parsed_url.netloc}"

def strip_fragment(url):
    """
    Remove the fragment from a URL, preserving other components including parameters.
    """
    parsed_url = urlparse(url)
    return urlunparse(parsed_url._replace(fragment=""))

def get_links(url, valid_url_prefix):
    """
    Fetch all valid links from a given URL, excluding anchor links to the same page.
    Updated to use a dynamic valid_url_prefix.
    """
    urls = set()
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            base_url = get_base_url(url)
            for link in soup.find_all('a', href=True):
                href = link['href']
                full_url = urljoin(base_url, href)
                full_url = strip_fragment(full_url)
                if is_valid_url(full_url, valid_url_prefix):
                    urls.add(full_url)
    except Exception as e:
        print(f"Error fetching {url}: {e}")
    return urls

def append_urls_to_file(urls, filename):
    """
    Append a list of URLs to a file.
    """
    with open(filename, 'a') as file:
        for url in urls:
            file.write(url + '\n')

def crawl_website(start_url, valid_url_prefix, url_filename):
    """
    Crawl a website starting from a given URL, following only valid links.
    Updated to use a dynamic valid_url_prefix.
    """
    visited = set()
    queue = [start_url]

    while queue:
        current_url = queue.pop(0)
        current_url = strip_fragment(current_url)
        if current_url not in visited:
            visited.add(current_url)
            print(f"Crawling: {current_url}")
            for new_url in get_links(current_url, valid_url_prefix):
                if new_url not in visited:
                    queue.append(new_url)
                    append_urls_to_file([new_url], url_filename)
    return visited

def convert_and_save(urls, output_dir):
    """
    Convert each URL in a list to markdown and save the output in a specified directory.
    """
    for url in urls:
        print(f"Converting: {url}")
        filename = os.path.basename(strip_fragment(url)).replace('.html', '') or "index"
        filename += ".md"
        output_path = os.path.join(output_dir, filename)
        convert_url_to_markdown(url, output_path)


def main():
    """
    Main function to initiate the crawling and conversion process.
    Now asks the user for the starting URL and valid URL prefix.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    start_url = input("Enter the starting URL: ")
    valid_url_prefix = input("Enter the URL prefix for valid links: ")
    domain_name = get_domain_name(start_url)
    output_dir = os.path.join(script_dir, domain_name)

    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    url_filename = os.path.join(output_dir, f"{domain_name}_urls.txt")
    
    # Ensure the URL file exists
    with open(url_filename, 'a') as file:
        pass

    urls = crawl_website(start_url, valid_url_prefix, url_filename)
    convert_and_save(urls, output_dir)

if __name__ == '__main__':
    main()