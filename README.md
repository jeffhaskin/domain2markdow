# Domain2Markdown

This project provides a Python application that crawls web pages starting from a given URL, extracts links that match a specified prefix (in case you only want the pages with a url that starts with "https://www.website.com/docs" or something), and converts the content of each page into Markdown file which it saves to an output folder on you computer. The application is built using PyQt5 for the GUI, allowing users to input a starting URL and a valid URL prefix for crawling. It is not asyncchronous and does this sequencially.

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

You can install the necessary libraries using pip:

```
pip install PyQt5 requests beautifulsoup4 markdownify
```

## Usage
**Starting URL:** Enter the URL where you want the crawler to start.
**URL Prefix:** Specify the URL prefix to filter the links that the crawler should follow. Only links that start with this prefix will be considered.
**Start:** Click the "Start" button to initiate the crawling and conversion process. The progress will be displayed in real-time, and the converted Markdown files will be saved in the specified output directory.

## Output
The converted Markdown files will be saved in a directory named after the domain of the starting URL, located in the current working directory. Each file's name is derived from the original web page's title or its URL if the title is not available.

## Customization
The code can be easily modified to adjust the depth of crawling, the criteria for valid links, or the Markdown conversion settings.

## Contribution
Contributions to improve the application are welcome. Please feel free to fork the repository, make your changes, and submit a pull request.
