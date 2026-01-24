# Report Analysis Project

Python-based analysis of text report files with data visualization.

## Setup

1. **Clone and navigate to the project:**
```bash
   git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   cd YOUR_REPO_NAME
```

2. **Activate virtual environment and install dependencies:**
```bash
   source ./venv_start.sh
```

## Project Structure
```
├── data/
│   ├── raw/              # Original .txt reports (not tracked)
│   └── processed/        # Parsed data (not tracked)
├── notebooks/            # Jupyter notebooks for analysis
├── scripts/              # Standalone Python scripts
├── src/                  # Core Python modules
└── requirements.txt      # Dependencies
```

## Usage

**Start working:**
```bash
source ./venv_start.sh
jupyter notebook notebooks/
```

**Add dependencies:**
```bash
pip install package_name
pip freeze > requirements.txt
```

## Key Dependencies

- pandas, numpy - Data processing
- matplotlib, seaborn - Visualization
- jupyter - Interactive notebooks

## Important

⚠️ Raw data files and processed outputs are **not tracked in git** for privacy. Only code is version-controlled.

## License

[Your license]