# Domain2Markdown

This project provides a Python application that crawls web pages starting from a given URL, extracts links that match a specified prefix (in case you only want the pages with a url that starts with "https://www.website.com/docs" or something), and converts the content of each page into Markdown file which it saves to an output folder on you computer. The application is built using PyQt5 for the GUI, allowing users to input a starting URL and a valid URL prefix for crawling. It is not asyncchronous and does this sequencially.

## Installation
### MacOS
Run this terminal command to install and open the program:
```bash
git clone https://github.com/jeffhaskin/domain2markdown.git ~/domain2markdown && cd ~/domain2markdown && pip3 install PyQt5 requests beautifulsoup4 markdownify && python3 crawler_0-0-3.py
```

Run this terminal command to run the program if you have already installed it:
```bash
python3 ~/domain2markdown/crawler_0-0-3.py
```

I don't know what is is for Windows or Linux.

## Usage
**Starting URL:** Enter the URL where you want the crawler to start.
**URL Prefix:** Specify the URL prefix to filter the links that the crawler should follow. Only links that start with this prefix will be considered.
**Start:** Click the "Start" button to initiate the crawling and conversion process. The progress will be displayed in real-time, and the converted Markdown files will be saved in the specified output directory.

## Output
The converted Markdown files will be saved in a directory named after the domain of the starting URL, located in the current working directory. Each file's name is derived from the original web page's title or its URL if the title is not available.

## Versions
0.0.3 is the one you want.

See the versions.txt file for info on 0.0.1 and 0.0.2.

## Features
- Web Crawling: Recursively crawls web pages starting from a user-specified URL, following links that match a given prefix.
- Content Conversion: Converts the HTML content of each crawled page into Markdown format, preserving the essential content structure.
- Output Organization: Saves the converted Markdown files in a directory named after the domain of the starting URL, organizing content efficiently.

## Prerequisites
Before running the application, ensure you have the following installed:

PyQt5
Requests
BeautifulSoup4
Markdownify
os
sys

You can install the necessary libraries using pip:

```
pip install PyQt5 requests beautifulsoup4 markdownify sys os
```

## Customization
The code can be easily modified to adjust the depth of crawling, the criteria for valid links, or the Markdown conversion settings.

## Contribution
Contributions to improve the application are welcome. Please feel free to fork the repository, make your changes, and submit a pull request.
