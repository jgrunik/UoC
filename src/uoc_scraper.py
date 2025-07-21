"""
Module for scraping Unit of Competency data from training.gov.au
"""
import json
import os
import re

import requests
from lxml import etree

from .utils import get_unit_xml_url, namespaces, unit_path_from_code


class UoCData:
    """Class for fetching and parsing Unit of Competency data"""
    
    @staticmethod
    def validate_unit_code(unit_code: str) -> bool:
        """Validate unit code format"""
        return bool(re.match(r'[A-Z]{3}[A-Z]{3}\d{3}', unit_code))
    
    def __init__(self, unit_code: str):
        if not self.validate_unit_code(unit_code):
            raise ValueError("Invalid unit code format")
        self.unit_code = unit_code
        self.root = None
        self._fetch_xml()
    
    def _fetch_xml(self):
        """Fetch XML data from training.gov.au"""
        url = get_unit_xml_url(self.unit_code)
        response = requests.get(url)
        
        if response.status_code == 200:
            self.root = etree.fromstring(response.content)
        elif response.status_code == 404:
            raise ValueError(f"Unit code {self.unit_code} not found")
        else:
            raise Exception(f"Failed to retrieve XML. Status code: {response.status_code}")

    def _extract_unit_title(self):
        """Extract unit title from XML"""
        xpath = './/a:Book[.//a:Description[contains(text(), "Release")]]//a:VariableAssignments/a:VariableAssignment[./a:Name/text()="Title"]/a:Value/text()'
        return self.root.xpath(xpath, namespaces=namespaces)[0]

    def _extract_elements(self):
        """Extract elements and performance criteria"""
        xpath = './/a:Topic[.//a:Description[text()="Elements and Performance Criteria"]]'
        topic = self.root.xpath(xpath, namespaces=namespaces)[0]
        rows = topic.xpath('./a:Text/a:table/a:tr[position() > 2]', namespaces=namespaces)
        
        elements = []
        for row in rows:
            element = row.xpath('./a:td[1]/a:p/text()', namespaces=namespaces)[0]
            element_index, element_title = re.split(r'\.\s*', element, 1)
            performance_criteria = row.xpath('./a:td[2]/a:p/text()', namespaces=namespaces)
            
            pc_items = []
            for pc in performance_criteria:
                index, description = pc.split(' ', 1)
                pc_items.append({'index': index, 'description': description})
            
            elements.append({
                'index': element_index,
                'title': element_title,
                'performance_criteria': pc_items
            })
        
        return elements

    def _extract_foundation_skills(self):
        """Extract foundation skills"""
        xpath = './/a:Topic[.//a:Description[text()="Foundation Skills"]]'
        topic = self.root.xpath(xpath, namespaces=namespaces)[0]
        rows = topic.xpath('./a:Text/a:table/a:tr[position() > 1]', namespaces=namespaces)
        
        skills = []
        for row in rows:
            skill = row.xpath('./a:td[1]/a:p/text()', namespaces=namespaces)[0]
            descriptions = row.xpath('./a:td[last()]/a:p/text()', namespaces=namespaces)
            
            pc_references = []
            if row.xpath('./a:td[2]', namespaces=namespaces) != row.xpath('./a:td[last()]', namespaces=namespaces):
                pc_references = row.xpath('./a:td[2]/a:p/text()', namespaces=namespaces)[0].split(', ')
            
            skills.append({
                'skill': skill,
                'performance_criteria': pc_references,
                'descriptions': descriptions
            })
        
        return skills

    def _extract_topic_text(self, topic_title):
        """Extract text content from a topic"""
        xpath = f'.//a:Topic[.//a:Description[text()="{topic_title}"]]'
        topic = self.root.xpath(xpath, namespaces=namespaces)[0]
        return topic.xpath('./a:Text/a:p/text()', namespaces=namespaces)

    def extract_all(self):
        """Extract all UoC data"""
        data = {
            'unit_code': self.unit_code,
            'unit_title': self._extract_unit_title(),
            'elements': self._extract_elements(),
            'foundational_skills': self._extract_foundation_skills(),
            'performance_evidence': self._extract_topic_text('Performance Evidence'),
            'knowledge_evidence': self._extract_topic_text('Knowledge Evidence'),
            'assessment_conditions': self._extract_topic_text('Assessment Conditions')
        }
        return data

    def save_to_file(self, folder_path=None):
        """Save extracted data to JSON file"""
        if folder_path is None:
            folder_path = unit_path_from_code(self.unit_code)
        
        os.makedirs(folder_path, exist_ok=True)
        filename = os.path.join(folder_path, f"{self.unit_code}_details.json")
        
        with open(filename, 'w') as f:
            json.dump(self.extract_all(), f, indent=2)
        
        return filename
