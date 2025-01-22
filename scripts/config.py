"""Configuration settings for furniture market analysis."""
from pathlib import Path

# Base directories
BASE_DIR = Path('.')
DATA_DIR = BASE_DIR / 'data'
OUTPUT_DIR = BASE_DIR / 'output'

# Data directories
RAW_DATA_DIR = DATA_DIR / 'raw'
PROCESSED_DATA_DIR = DATA_DIR / 'processed'

# Output directories
FIGURES_DIR = OUTPUT_DIR / 'figures'
REPORTS_DIR = OUTPUT_DIR / 'reports'

# Data files
RAW_DATA_FILE = RAW_DATA_DIR / 'Furniture_Survey.csv'
PROCESSED_DATA_FILE = PROCESSED_DATA_DIR / 'cleaned_furniture_data.csv'

# Plot settings
FIGURE_SIZE = (12, 6)
STYLE_SHEET = 'seaborn'
DPI = 300

# Analysis settings
RANDOM_STATE = 42
CONFIDENCE_LEVEL = 0.95


def verify_data_file():
    """Verify that the data file exists."""
    if not RAW_DATA_FILE.exists():
        raise FileNotFoundError(
            f"\nData file not found at {RAW_DATA_FILE}\n"
            f"Please place your data file at: {RAW_DATA_FILE}"
        )


def verify_directory_structure():
    """Verify that all required directories exist."""
    directories = [
        RAW_DATA_DIR,
        PROCESSED_DATA_DIR,
        REPORTS_DIR,
        FIGURES_DIR
    ]
    
    for directory in directories:
        if not directory.exists():
            directory.mkdir(parents=True) 