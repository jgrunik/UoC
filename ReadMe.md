# Unit of Competency Creator

## Requirements

- Python
- Jupyter Notebook Viewer

## Setup

1. Install python dependencies:  
   `python -m pip install -r ./requirements.txt`

2. Open notebook:  
   ` ./notebooks/prepare_templates.ipynb`

3. Click Run All  
   `Run All`

## Notebooks

> _Notebooks are located in: `./notebooks/`_

---

### Prepare Templates (`prepare_uoc.ipynb`)

Prepopulates VU templates with Unit of Competency details from training.gov.au  
 _Note: this runs `scrape_uoc.ipnyb`_

> _Output files are located in:_ `./Units/[UNIT_CODE]/`

---

### Scrape UOC (`scrape_uoc.ipynb`)

Downloads Unit of Competency details from training.gov.au

> _Output file is located at:_ `./Units/[UNIT_CODE]/[UNIT_CODE]_details.json`

---

### Scrape Templates (`scrape_templates.ipynb`)

Downloads Templates from the VU intranet  
_Note: Requires VU network and staff credentials_

> _Output files are located in:_ `./Templates/VU/`
