# Data Directory

This directory contains the furniture market survey data files.

## Structure

- `raw/`: Contains original survey data
  - `Furniture_Survey.csv`: Raw survey responses

- `processed/`: Contains cleaned and transformed data
  - `cleaned_furniture_data.csv`: Processed dataset with:
    - Standardized column names
    - Handled missing values
    - Created numeric features
    - Processed multiple-choice responses
    - Cleaned text data

## Data Features

### Raw Data
- Survey responses about furniture preferences
- Isho brand perceptions
- Demographic information
- Shopping behaviors
- Purchase patterns

### Processed Data
- Cleaned and standardized text
- Numeric conversions for:
  - Age groups
  - Income ranges
  - Brand familiarity scores
  - Recommendation scores
- Binary indicators for multiple-choice responses
- Handled missing values
- Filtered valid responses 