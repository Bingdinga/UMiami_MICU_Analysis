# Report Analysis Project

A Python-based data analysis project for processing and analyzing text-based reports. This project includes data parsing, statistical analysis, and visualization capabilities.

## Project Overview

This project processes raw text report files, extracts structured data, and performs analysis to identify patterns and generate insights through data visualizations.

## Project Structure
```
.
├── data/
│   ├── raw/              # Original .txt report files (not tracked in git)
│   └── processed/        # Parsed and cleaned data (not tracked in git)
├── notebooks/            # Jupyter notebooks for analysis
├── scripts/              # Standalone Python scripts
├── src/                  # Core Python modules and functions
├── tests/                # Unit tests
├── requirements.txt      # Python dependencies
├── venv_start.sh         # Virtual environment activation script
└── README.md            # This file
```

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- Git
- SSH access to Raspberry Pi 5 (if developing remotely)

### Installation

1. **Clone the repository:**
```bash
   git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   cd YOUR_REPO_NAME
```

2. **Set up virtual environment and install dependencies:**
```bash
   source ./venv_start.sh
```
   
   This script will automatically:
   - Create a virtual environment in `.venv/`
   - Activate the environment
   - Install all required packages from `requirements.txt`

3. **For subsequent sessions, simply run:**
```bash
   source ./venv_start.sh
```

### VSCode Remote Development Setup

1. Install the "Remote - SSH" extension in VSCode
2. Connect to your Raspberry Pi via SSH
3. Open the project folder
4. Select the Python interpreter: `Ctrl+Shift+P` → "Python: Select Interpreter" → `.venv/bin/python`

## Usage

### Running Analysis

1. Activate the virtual environment:
```bash
   source ./venv_start.sh
```

2. Launch Jupyter Notebook:
```bash
   jupyter notebook notebooks/
```

3. Open the analysis notebook and run the cells

### Adding New Dependencies
```bash
pip install package_name
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Add package_name dependency"
```

## Data

### Raw Data

- Raw report files should be placed in `data/raw/`
- These files are **not tracked in version control** for privacy/security
- File format: `.txt` with structured report entries

### Processed Data

- Parsed and cleaned data is stored in `data/processed/`
- Formats: CSV, Parquet, or Pickle files
- These files are **not tracked in version control**

**Note:** To maintain data privacy, actual report files and processed data are excluded from version control. Only code and documentation are tracked.

## Development

### Workflow

1. Pull latest changes: `git pull`
2. Activate virtual environment: `source ./venv_start.sh`
3. Make your changes
4. Test your changes
5. Commit and push:
```bash
   git add .
   git commit -m "Description of changes"
   git push
```

### Code Organization

- **`notebooks/`**: Interactive analysis and visualization notebooks
- **`scripts/`**: Standalone scripts for data processing or automation
- **`src/`**: Reusable Python modules and functions
- **`tests/`**: Unit tests for core functionality

## Dependencies

Key packages used in this project:

- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computing
- **matplotlib/seaborn**: Data visualization
- **jupyter**: Interactive notebook environment
- **pyarrow**: Efficient data serialization

See `requirements.txt` for complete list with version constraints.

## Analysis Pipeline

1. **Data Parsing**: Extract structured data from raw text reports
2. **Data Cleaning**: Handle missing values, standardize formats
3. **Exploratory Analysis**: Statistical summaries and initial insights
4. **Visualization**: Create charts and graphs for findings
5. **Reporting**: Document insights and conclusions

## Contributing

This is a personal project. For development guidelines:

1. Keep commits atomic and well-described
2. Update README when adding new features
3. Document complex functions and analysis steps
4. Keep sensitive data out of version control

## Security & Privacy

⚠️ **Important**: This project processes potentially sensitive report data.

- Never commit actual report files
- Never commit processed data containing real information
- Use dummy/anonymized data in code examples
- Be cautious with error messages that might expose data

## License

[Add your license here]

## Contact

[Add your contact information here]

## Changelog

### Initial Setup
- Created project structure
- Set up virtual environment management
- Configured git repository and remote connection