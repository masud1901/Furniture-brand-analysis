"""Demographic analysis module for furniture survey data."""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from . import utils
from typing import Dict


class DemographicAnalyzer:
    """Class for analyzing demographic data from furniture survey."""

    def __init__(self, df: pd.DataFrame):
        """Initialize with survey dataframe."""
        self.df = df

    def plot_basic_distribution(
            self, data, title, is_horizontal=False, 
            figsize=(10, 6), show_plot=False):
        """Create a basic distribution plot using seaborn."""
        fig = plt.figure(figsize=figsize)
        
        if is_horizontal:
            sns.barplot(x=data.values, y=data.index, palette='viridis')
        else:
            sns.barplot(x=data.index, y=data.values, palette='viridis')
        
        plt.title(title, fontsize=12, pad=15)
        plt.xlabel('Count' if is_horizontal else 'Category')
        plt.ylabel('Category' if is_horizontal else 'Count')
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        if show_plot:
            plt.show()
        else:
            utils.save_and_close_figure(
                fig, 
                f"{title.lower().replace(' ', '_')}", 
                'demographics'
            )

    def create_pie_chart(self, data, title, show_plot=False):
        """Create a pie chart with percentages."""
        fig = plt.figure(figsize=(10, 8))
        plt.pie(
            data.values, 
            labels=data.index,
            autopct='%1.1f%%',
            colors=sns.color_palette('pastel')
        )
        plt.title(title, fontsize=12, pad=15)
        plt.axis('equal')
        
        if show_plot:
            plt.show()
        else:
            utils.save_and_close_figure(
                fig, 
                f"{title.lower().replace(' ', '_')}", 
                'demographics'
            )

    def create_stacked_bar(self, data, title, figsize=(12, 6), show_plot=False):
        """Create a stacked bar chart."""
        fig = plt.figure(figsize=figsize)
        data.plot(kind='bar', stacked=True, color=sns.color_palette('pastel'))
        plt.title(title, fontsize=12, pad=15)
        plt.xlabel('Category')
        plt.ylabel('Count')
        plt.legend(title='Groups', bbox_to_anchor=(1.05, 1))
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        if show_plot:
            plt.show()
        else:
            utils.save_and_close_figure(
                fig, 
                f"{title.lower().replace(' ', '_')}", 
                'demographics'
            )

    def create_heatmap(self, data, title, figsize=(12, 8), show_plot=False):
        """Create a heatmap for cross-analysis."""
        fig = plt.figure(figsize=figsize)
        sns.heatmap(
            data, 
            annot=True, 
            fmt='d', 
            cmap='YlOrRd',
            cbar_kws={'label': 'Count'}
        )
        plt.title(title, fontsize=12, pad=15)
        plt.tight_layout()
        
        if show_plot:
            plt.show()
        else:
            utils.save_and_close_figure(
                fig, 
                f"{title.lower().replace(' ', '_')}", 
                'demographics'
            )

    def get_basic_distributions(self):
        """Calculate basic demographic distributions."""
        return {
            'age': self.df['what_is_your_age_group'].value_counts(),
            'gender': self.df['what_is_your_gender'].value_counts(),
            'occupation': self.df['what_is_your_occupation'].value_counts(),
            'income': self.df['what_is_your_monthly_income_range'].value_counts()
        }

    def get_cross_tabulations(self):
        """Calculate demographic cross-tabulations."""
        return {
            'age_gender': pd.crosstab(
                self.df['what_is_your_age_group'],
                self.df['what_is_your_gender']
            ),
            'income_occupation': pd.crosstab(
                self.df['what_is_your_monthly_income_range'],
                self.df['what_is_your_occupation']
            ),
            'age_income': pd.crosstab(
                self.df['what_is_your_age_group'],
                self.df['what_is_your_monthly_income_range']
            )
        }

    def print_summary_statistics(self, distributions):
        """Print summary statistics for demographics."""
        print("\nDemographic Summary:")
        print("-" * 50)
        for name, dist in distributions.items():
            print(f"\n{name.replace('_', ' ').title()} Distribution:")
            print(dist)

    def create_distribution_plots(self, distributions: Dict, show_plots: bool = False):
        """Create plots for basic demographic distributions."""
        # Age distribution
        self.plot_basic_distribution(
            distributions['age'],
            'Age Distribution',
            is_horizontal=True,
            show_plot=show_plots
        )
        
        # Gender distribution
        self.create_pie_chart(
            distributions['gender'],
            'Gender Distribution',
            show_plot=show_plots
        )
        
        # Occupation distribution
        self.plot_basic_distribution(
            distributions['occupation'],
            'Occupation Distribution',
            is_horizontal=True,
            show_plot=show_plots
        )
        
        # Income distribution
        self.plot_basic_distribution(
            distributions['income'],
            'Income Distribution',
            is_horizontal=True,
            show_plot=show_plots
        )

    def create_cross_analysis_plots(self, cross_tabs: Dict, show_plots: bool = False):
        """Create plots for demographic cross-analyses."""
        # Age vs Gender
        self.create_stacked_bar(
            cross_tabs['age_gender'],
            'Age Distribution by Gender',
            show_plot=show_plots
        )
        
        # Income vs Occupation
        self.create_heatmap(
            cross_tabs['income_occupation'],
            'Income Distribution by Occupation',
            show_plot=show_plots
        )
        
        # Age vs Income
        self.create_heatmap(
            cross_tabs['age_income'],
            'Age Distribution by Income',
            show_plot=show_plots
        )

    def print_demographic_summary(self, distributions: Dict, cross_tabs: Dict):
        """Print comprehensive demographic summary."""
        print("\nDemographic Summary")
        print("=" * 50)
        
        # Basic distributions
        print("\nBasic Distributions:")
        print("-" * 20)
        for name, dist in distributions.items():
            print(f"\n{name.replace('_', ' ').title()}:")
            total = dist.sum()
            for category, count in dist.items():
                percentage = (count / total * 100).round(1)
                print(f"{category}: {count} ({percentage}%)")
        
        # Cross-tabulations
        print("\nCross-Tabulation Analysis:")
        print("-" * 20)
        print("\nAge vs Gender Distribution:")
        print(cross_tabs['age_gender'])
        print("\nIncome vs Occupation Distribution:")
        print(cross_tabs['income_occupation'])
        print("\nAge vs Income Distribution:")
        print(cross_tabs['age_income'])

    def run_demographic_analysis(self, show_plots: bool = False) -> Dict:
        """Main entry point for demographic analysis."""
        print("Starting demographic analysis...")
        
        # Get distributions
        distributions = self.get_basic_distributions()
        cross_tabs = self.get_cross_tabulations()
        
        # Create visualizations
        self.create_distribution_plots(distributions, show_plots)
        self.create_cross_analysis_plots(cross_tabs, show_plots)
        
        # Print summary
        self.print_demographic_summary(distributions, cross_tabs)
        
        # Save results
        results = {
            'distributions': distributions,
            'cross_tabs': cross_tabs
        }
        utils.save_analysis_results(results, 'demographic_analysis')
        
        print("Demographic analysis completed!")
        return results