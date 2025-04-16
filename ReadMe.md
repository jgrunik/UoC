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
> *Notebooks are located in: `./notebooks/`*

---

 ### Prepare Templates (`prepare_uoc.ipynb`)
   Prepopulates VU templates with Unit of Competency details from training.gov.au  
   *Note: this runs `scrape_uoc.ipnyb`*  
   > *Output files are located in:* `./Units/[UNIT_CODE]/`

---

 ### Scrape UOC (`scrape_uoc.ipynb`)
   Downloads Unit of Competency details from training.gov.au
   
> *Output file is located at:* `./Units/[UNIT_CODE]/[UNIT_CODE]_details.json`

---

### Scrape Templates (`scrape_templates.ipynb`)
Downloads Templates from the VU intranet  
*Note: Requires VU network and staff credentials*  
  
> *Output files are located in:* `./Templates/VU/`