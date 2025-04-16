import os

base_url = "https://intranet.vu.edu.au/TAFE/"
templates_url = base_url + "pageTemplates.asp"
namespaces = {
    "a": "http://www.authorit.com/xml/authorit",
    "xsi": "http://www.w3.org/2001/XMLSchema-instance",
}

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
    Assessment_Mapping = "VETAssessmentMapping(CurrentUoC).docx"


class Paths:
    root = "../"
    Units = "../Units/"
    Templates = "../Templates/"
    Jinja_Templates = "../Templates/Jinja/"
    VU_Templates = "../Templates/VU/"


def unit_path_from_code(unit_code):
    return os.path.join(Paths.Units, unit_code)


# Get the URL of the XML file for a unit code
def get_unit_xml_url(unit_code):
    # Get the industry code from the unit code
    industry_code = unit_code[:3]
    # Return the URL of the XML file
    return f"https://training.gov.au/assets/{industry_code}/{unit_code}_Complete_R1.xml"


class StopExecution(Exception):
    def _render_traceback_(self):
        return []
