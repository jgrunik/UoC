"""
Module for scraping VU templates from the intranet
"""
import os
import shutil
import urllib.parse
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from requests_ntlm import HttpNtlmAuth

from .utils import (Paths, StopExecution, base_url, template_titles,
                    templates_url)


class TemplatesScraper:
    """Class for scraping VU templates from the intranet"""
    
    def __init__(self):
        self.session = requests.Session()
        self._setup_output_dir()
    
    def _setup_output_dir(self):
        """Create VU Templates directory if it doesn't exist"""
        os.makedirs(Paths.VU_Templates, exist_ok=True)
    
    @staticmethod
    def _clean_text(text):
        """Clean and normalize text"""
        return ' '.join(text.strip().split())

    def authenticate(self, username: str, password: str) -> bool:
        """Authenticate with VU intranet"""
        self.session.auth = HttpNtlmAuth(username, password)
        
        try:
            response = self.session.get(templates_url)
            return response.status_code == 200
        except requests.exceptions.ConnectionError as e:
            if "Failed to resolve" in str(e) or "[Errno 11001] getaddrinfo failed" in str(e):
                raise ConnectionError(
                    "Unable to connect to VU intranet.\n"
                    "Please ensure you are:\n"
                    "    > Connected directly to a VU network, or\n"
                    "    > Connected remotely using Cisco AnyConnect"
                )
            raise
    
    def find_matching_templates(self) -> list:
        """Find templates matching predefined titles"""
        response = self.session.get(templates_url)
        soup = BeautifulSoup(response.text, "html.parser")
        
        matching_hrefs = []
        for anchor in soup.find_all('a', href=True):
            parent_tr = anchor.find_parent('tr')
            sibling_td = parent_tr.find('td')
            template_title = self._clean_text(sibling_td.get_text())
            
            if template_title in template_titles:
                matching_hrefs.append(anchor['href'])
        
        return matching_hrefs

    def download_template(self, href: str) -> str:
        """Download a single template file"""
        file_name = urllib.parse.unquote(os.path.basename(href))
        file_path = os.path.join(Paths.VU_Templates, file_name)
        
        with self.session.get(base_url + href, stream=True) as r:
            with open(file_path, 'wb') as f:
                shutil.copyfileobj(r.raw, f)
        
        return file_name
    
    def download_all_templates(self) -> list:
        """Download all matching templates"""
        hrefs = self.find_matching_templates()
        if not hrefs:
            raise ValueError("No matching templates found")
        
        downloaded = []
        for href in hrefs:
            file_name = self.download_template(href)
            downloaded.append(file_name)
        
        # Save timestamp
        with open(os.path.join(Paths.VU_Templates, "last_downloaded.txt"), "w") as f:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(timestamp)
        
        return downloaded
