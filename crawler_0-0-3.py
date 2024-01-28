import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QPushButton, QProgressBar, QLabel
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, QRunnable, QThreadPool, QObject
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urlunparse

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'web2markdown'))
from webpage2markdown_callable import convert_url_to_markdown

def get_domain_name(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc

def is_valid_url(url, valid_url_prefix):
    return url.startswith(valid_url_prefix)

def get_base_url(url):
    parsed_url = urlparse(url)
    return f"{parsed_url.scheme}://{parsed_url.netloc}"

def strip_fragment(url):
    parsed_url = urlparse(url)
    return urlunparse(parsed_url._replace(fragment=""))

def get_links(url, valid_url_prefix):
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

class SignalEmitter(QObject):
    update_progress = pyqtSignal(int, int)  # signal for progress update
    finished = pyqtSignal(set)  # signal for task completion

class CrawlerWorker(QRunnable):
    def __init__(self, start_url, valid_url_prefix):
        super(CrawlerWorker, self).__init__()
        self.signals = SignalEmitter()
        self.start_url = start_url
        self.valid_url_prefix = valid_url_prefix
        self.output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), get_domain_name(start_url))
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    @pyqtSlot()
    def run(self):
        visited = set()
        queue = [self.start_url]
        total_urls = 1  # Initial count for the starting URL

        while queue:
            current_url = queue.pop(0)
            current_url = strip_fragment(current_url)
            if current_url not in visited:
                # Convert and save the current URL content to markdown
                filename = os.path.basename(current_url).replace('.html', '') or "index"
                filename += ".md"
                output_path = os.path.join(self.output_dir, filename)
                convert_url_to_markdown(current_url, output_path)  # Assuming this function takes the URL and output path as arguments

                visited.add(current_url)
                new_urls = get_links(current_url, self.valid_url_prefix)
                for new_url in new_urls:
                    if new_url not in visited:
                        queue.append(new_url)
                        total_urls += 1
                self.signals.update_progress.emit(len(visited), total_urls)
        self.signals.finished.emit(visited)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Web Crawler and Markdown Converter')
        layout = QVBoxLayout()

        self.startUrlLineEdit = QLineEdit()
        self.startUrlLineEdit.setPlaceholderText("Enter the starting URL")
        layout.addWidget(self.startUrlLineEdit)

        self.urlPrefixLineEdit = QLineEdit()
        self.urlPrefixLineEdit.setPlaceholderText("Enter the URL prefix for valid links")
        layout.addWidget(self.urlPrefixLineEdit)

        self.startButton = QPushButton('Start')
        self.startButton.clicked.connect(self.onStartButtonClick)
        layout.addWidget(self.startButton)

        self.progressBar = QProgressBar()
        layout.addWidget(self.progressBar)

        self.statusLabel = QLabel('Ready')
        layout.addWidget(self.statusLabel)

        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

        self.setMinimumWidth(400)  # Set the minimum width of the main window

        self.threadPool = QThreadPool()

    def onStartButtonClick(self):
        start_url = self.startUrlLineEdit.text()
        valid_url_prefix = self.urlPrefixLineEdit.text()

        self.worker = CrawlerWorker(start_url, valid_url_prefix)
        self.worker.signals.update_progress.connect(self.updateProgressBar)
        self.worker.signals.finished.connect(self.onTaskCompleted)
        self.threadPool.start(self.worker)

    def updateProgressBar(self, visited_count, total_count):
        progress = int((visited_count / total_count) * 100) if total_count else 0
        self.progressBar.setValue(progress)

    def onTaskCompleted(self, visited_urls):
        self.statusLabel.setText('Task Completed')
        # Here you could call a function to convert and save URLs to markdown

def main():
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()