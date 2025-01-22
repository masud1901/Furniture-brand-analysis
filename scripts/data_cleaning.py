"""Data cleaning module for furniture survey data."""
import pandas as pd
import re
from pathlib import Path


class FurnitureDataCleaner:
    """Class to handle furniture survey data cleaning pipeline."""
    
    def __init__(self):
        """Initialize data cleaner with mapping dictionaries."""
        self.age_map = {
            'Under 18': 17,
            '18-24': 21,
            '25-34': 29.5,
            '35-44': 39.5,
            '45 and above': 55
        }
        
        self.income_map = {
            'Below BDT 25,000': 12500,
            'BDT 25,001-50,000': 37500,
            'BDT 50,001-100,000': 75000,
            'BDT 100,001-200,000': 150000,
            'Above 200,000': 250000
        }

        self.familiarity_map = {
            1: 'Not at all familiar',
            2: 'Slightly familiar',
            3: 'Moderately familiar',
            4: 'Very familiar',
            5: 'Extremely familiar'
        }
        
        self.multiple_choice_mapping = {
            'what_type_of_furniture_do_you_prefer': {
                'prefix': 'furniture_type',
                'choices': [
                    'Modern',
                    'Traditional',
                    'Minimalist',
                    'Multipurpose',
                    'Eclectic'
                ]
            },
            'which_room_do_you_prioritise_when_buying_furniture': {
                'prefix': 'priority_room',
                'choices': [
                    'Living/ Drawing Room',
                    'Bedroom',
                    'Dining Room',
                    'Guest Room',
                    'Kid\'s room',
                    'Kitchen'
                ]
            },
            'why_do_you_usually_buy_furniture': {
                'prefix': 'purchase_reason',
                'choices': [
                    'For home decoration',
                    'For Marriage or Family Changes',
                    'When old furniture needs replacement',
                    'Moving out and home shifting',
                    'Personal Preference',
                    'Style & comfort'
                ]
            }
        }

    def _clean_column_names(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and standardize column names."""
        # First, create a mapping of old to new column names
        column_mapping = {}
        for col in df.columns:
            # Clean the column name
            new_col = (col.strip()
                      .lower()
                      .replace('?', '')
                      .replace('/', '_')
                      .replace('[', '')
                      .replace(']', '')
                      .replace('(', '')
                      .replace(')', '')
                      .replace(',', '')
                      .replace('  ', ' ')
                      .replace(' ', '_'))
            column_mapping[col] = new_col
        
        # Rename columns using the mapping
        df = df.rename(columns=column_mapping)
        
        # Create a log of the column name changes
        print("\nColumn name changes:")
        for old_col, new_col in column_mapping.items():
            if old_col != new_col:
                print(f"'{old_col}' -> '{new_col}'")
        
        return df

    def _handle_multiple_choice_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Process multiple-choice columns into binary indicators."""
        for column, config in self.multiple_choice_mapping.items():
            if column in df.columns:
                prefix = config['prefix']
                choices = config['choices']
                
                for choice in choices:
                    col_name = (f"{prefix}_{choice.lower()}"
                              .replace(' ', '_')
                              .replace('/', '_'))
                    df[col_name] = (df[column]
                                  .fillna('')
                                  .str.contains(re.escape(choice), 
                                              case=False, 
                                              regex=True)
                                  .astype(int))
        return df

    def _create_numeric_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create numeric features from categorical data."""
        # Convert age to numeric
        df['age_numeric'] = df['what_is_your_age_group'].map(self.age_map)
        
        # Convert income to numeric
        df['income_numeric'] = df['what_is_your_monthly_income_range'].map(
            self.income_map)
        
        # Convert Isho familiarity to numeric (already numeric 1-5)
        df['isho_familiarity_score'] = pd.to_numeric(
            df['how_familiar_are_you_with_the_isho_brand_rate_on_a_scale_of_1_to_5'],
            errors='coerce')
        
        # Convert recommendation score to numeric (already numeric 1-5)
        df['recommendation_score'] = pd.to_numeric(
            df['would_you_recommend_isho_to_others_rank_on_a_scale_of_1_to_5'],
            errors='coerce')
        
        return df

    def _clean_text_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean text columns by removing special characters and standardizing case."""
        text_columns = df.select_dtypes(include=['object']).columns
        for col in text_columns:
            df[col] = (df[col]
                      .astype(str)
                      .str.replace(r'[^\x00-\x7F]+', '', regex=True)
                      .str.strip())
        return df

    def _handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """Handle missing values appropriately."""
        # Fill numeric columns with 0
        numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
        df[numeric_cols] = df[numeric_cols].fillna(0)
        
        # Fill categorical columns with 'Not Specified'
        categorical_cols = df.select_dtypes(include=['object']).columns
        df[categorical_cols] = df[categorical_cols].fillna('Not Specified')
        
        return df

    def _filter_valid_responses(self, df: pd.DataFrame) -> pd.DataFrame:
        """Filter valid responses."""
        return df[
            df['have_you_ever_bought_furniture'].str.lower() == 'yes'
        ].reset_index(drop=True)

    def _save_cleaned_data(self, df: pd.DataFrame):
        """Save cleaned data to processed directory."""
        processed_dir = Path('data/processed')
        processed_dir.mkdir(parents=True, exist_ok=True)
        
        output_path = processed_dir / 'cleaned_furniture_data.csv'
        df.to_csv(output_path, index=False)
        print(f"Cleaned data saved to: {output_path}")

    def run_data_cleaning(self, df: pd.DataFrame, 
                         save_cleaned: bool = True) -> pd.DataFrame:
        """Main entry point for data cleaning pipeline."""
        print("Starting data cleaning process...")
        
        df_clean = df.copy()
        
        # Run cleaning steps in logical order
        df_clean = self._clean_column_names(df_clean)
        df_clean['timestamp'] = pd.to_datetime(df_clean['timestamp'])
        df_clean = self._handle_multiple_choice_columns(df_clean)
        df_clean = self._create_numeric_features(df_clean)
        df_clean = self._clean_text_columns(df_clean)
        df_clean = self._handle_missing_values(df_clean)
        df_clean = self._filter_valid_responses(df_clean)
        
        if save_cleaned:
            self._save_cleaned_data(df_clean)
        
        print("Data cleaning completed successfully!")
        return df_clean