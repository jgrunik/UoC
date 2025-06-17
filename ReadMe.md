# Unit of Competency Creator

A command-line tool for automating the creation of Units of Competency (UoC) documentation from training.gov.au data.

> ⚠️ **IMPORTANT NOTICE**  
> Template downloading functionality (`--setup-templates`) is currently not working due to changes in the template source location. Please manually copy the required templates into the `Templates/Jinja/` directory. Contact your administrator for the current template files.

## Quick Start

1. Install dependencies:
   ```powershell
   python -m pip install -r requirements.txt
   ```

2. Set up templates:
   - ⚠️ Manual template setup required
   - Copy the provided template files to `Templates/Jinja/` directory

3. Create UoC documentation in one of three ways:

   a. Interactive Mode (Recommended for new users):
   ```powershell
   python uoc_create.py --interactive
   ```

   b. Direct Mode with Unit Code:
   ```powershell
   python uoc_create.py --unit-code BSBCRT413
   ```

   c. With Course Details:
   ```powershell
   python uoc_create.py --unit-code BSBCRT413 --course-code "22603VIC" --course-title "Certificate IV in Design"
   ```

## Command Line Options

```
uoc_create.py [OPTIONS]

Options:
  --setup-templates    Download required templates from VU intranet
  --unit-code CODE    Unit of Competency code to process (e.g., BSBCRT413)
  --course-code CODE  Course code (optional)
  --course-title TEXT Course title (optional)
  --interactive       Run in interactive mode (recommended)
```

## How It Works

1. **Template Setup**:
   - ⚠️ Automatic template download is currently unavailable
   - Manually copy required templates to `Templates/Jinja/` directory
   - Required templates: `VETAssessmentMapping(CurrentUoC).docx`
   - Contact your administrator for template files

2. **Interactive Mode** (`--interactive`):
   - Guides you through the process step by step
   - Prompts for unit code and course details
   - Recommended for first-time users

3. **Direct Mode** (`--unit-code`):
   - Quickly create documentation for a specific unit
   - Optional course details can be added with --course-code and --course-title
   - Best for batch processing or when you know the exact unit code

## Output

For each unit (e.g., BSBCRT413), the tool generates:
- `Units/BSBCRT413/BSBCRT413_details.json`: Unit details from training.gov.au
- `Units/BSBCRT413/VETAssessmentMapping(CurrentUoC).docx`: Assessment mapping document

## Project Structure

```
├── Templates/             # Template storage
│   └── Jinja/            # Document templates
├── Units/                # Generated documentation
│   └── [UNIT_CODE]/     # Individual unit folders
├── src/                  # Source code
└── uoc_create.py        # Main command-line tool
```

## Requirements

- Python 3.12 or higher
- Internet connection for accessing training.gov.au
- VU network access for template download
- Required packages: beautifulsoup4, docxtpl, python-docx, requests
