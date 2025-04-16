"""
Utility functions and constants shared across modules
"""
import os
import pathlib

# VU Template URLs
base_url = "https://intranet.vu.edu.au/TAFE/"
templates_url = base_url + "pageTemplates.asp"

# XML namespaces for parsing training.gov.au data
namespaces = {
    "a": "http://www.authorit.com/xml/authorit",
    "xsi": "http://www.w3.org/2001/XMLSchema-instance",
}

# Template names to download from VU intranet
template_titles = [
    # Assessment
    "Assessor Guide",
    "Assessment Map (Current Unit of Competency Format)",
    "TAFE Assessment Cover Sheet",
    "Practical Observation Assessment Template (Portrait)",
    "Practical Observation Assessment Template (Landscape)",
    # Delivery
    "Learning and Assessment Plan",
    "Learning Activity Template",
    "Written Assessment Template",
    "Unit Guide",
]

class FileNames:
    """Constants for file names used in the project"""
    Assessment_Mapping = "VETAssessmentMapping(CurrentUoC).docx"

class Paths:
    """Class managing paths used in the project"""
    def __init__(self, base_dir=None):
        if base_dir is None:
            # Default to project root (parent of src directory)
            base_dir = pathlib.Path(__file__).parent.parent
        
        self.root = base_dir
        self.Units = os.path.join(base_dir, "Units")
        self.Templates = os.path.join(base_dir, "Templates")
        self.Jinja_Templates = os.path.join(self.Templates, "Jinja")
        self.VU_Templates = os.path.join(self.Templates, "VU")

# Initialize paths relative to project root
Paths = Paths()

def unit_path_from_code(unit_code: str) -> str:
    """Get the path to a unit's directory from its code"""
    return os.path.join(Paths.Units, unit_code)

def get_unit_xml_url(unit_code: str) -> str:
    """Get the URL of the XML file for a unit code from training.gov.au"""
    industry_code = unit_code[:3]
    return f"https://training.gov.au/assets/{industry_code}/{unit_code}_Complete_R1.xml"

class StopExecution(Exception):
    """Exception used to cleanly stop execution"""
    pass
