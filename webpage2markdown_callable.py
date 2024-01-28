import sys
import os
import requests
from markdownify import markdownify as md

def convert_html_to_markdown(source, is_url=True):
    if is_url:
        response = requests.get(source)
        html_text = response.text
    else:
        html_text = source

    return md(html_text)

# New function to be used by the web scraping program
def convert_url_to_markdown(url, output_path):
    markdown_text = convert_html_to_markdown(url)
    
    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w') as f:
        f.write(markdown_text)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python webpage2markdown_invokable.py <URL or HTML file> <output_file.md>")
        sys.exit(1)

    source = sys.argv[1]
    output_path = sys.argv[2]
    convert_url_to_markdown(source, output_path)
