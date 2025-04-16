"""
Main interface for Unit of Competency Creator
"""
import getpass
import re
from typing import Dict, Optional

from .template_preparer import TemplatePreparer
from .template_scraper import TemplatesScraper
from .uoc_scraper import UoCData


class UoCCreator:
    """Main interface for creating Unit of Competency documentation"""
    
    DEFAULT_DETAILS = {
        'file_version': 'v1.0',
        'course_code': "22589VIC",
        'course_title': "Certificate III in Emerging Technologies"
    }
    
    def __init__(self):
        self.template_scraper = None
        self.uoc_data = None
        self.unit_code = None
    
    @staticmethod
    def validate_staff_id(username: str) -> bool:
        """Validate VU staff ID format"""
        return bool(re.match(r"e\d{7}", username))
    
    def setup_templates(self, force_download: bool = False):
        """Set up templates by downloading from VU intranet"""
        username = input("Enter your staff e-number: ")
        if not self.validate_staff_id(username):
            raise ValueError("Invalid staff ID format")
        
        self.template_scraper = TemplatesScraper()
        
        while True:
            password = getpass.getpass("Enter your staff password: ")
            if not password:
                raise InterruptedError("Session aborted by user")
            
            try:
                if self.template_scraper.authenticate(username, password):
                    break
            except ConnectionError as e:
                raise e
            
            print("Authorization failed. Please check your credentials and try again.")
        
        # Download templates
        downloaded = self.template_scraper.download_all_templates()
        return downloaded
    
    def prepare_unit(self, unit_code: str, additional_details: Optional[Dict] = None):
        """Prepare all documentation for a unit"""
        self.unit_code = unit_code
        
        # Get UoC data
        uoc = UoCData(unit_code)
        self.uoc_data = uoc.extract_all()
        uoc.save_to_file()  # Save JSON for reference
        
        # Prepare context for templates
        if additional_details is None:
            additional_details = {}
        
        template_details = self.DEFAULT_DETAILS.copy()
        template_details.update(additional_details)
        
        # Prepare templates
        preparer = TemplatePreparer(unit_code, self.uoc_data, template_details)
        preparer.prepare_all_templates()
    
    @classmethod
    def interactive_prepare_unit(cls):
        """Interactive workflow for preparing unit documentation"""
        creator = cls()
        
        # Get unit code
        while True:
            unit_code = input("Enter the unit of competency code: ")
            if not unit_code:
                raise InterruptedError("Input aborted by user")
            
            if UoCData.validate_unit_code(unit_code):
                break
            print("Invalid unit code format. Please try again.")
        
        # Get additional details
        course_code = input(f"Enter course code (default: {cls.DEFAULT_DETAILS['course_code']}): ")
        course_title = input(f"Enter course title (default: {cls.DEFAULT_DETAILS['course_title']}): ")
        
        additional_details = {}
        if course_code:
            additional_details['course_code'] = course_code
        if course_title:
            additional_details['course_title'] = course_title
        
        # Prepare unit documentation
        creator.prepare_unit(unit_code, additional_details)
        return creator
