"""Statistical analysis module for furniture survey data."""
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
from . import config, utils


class StatisticalAnalyzer:
    """Class to perform statistical analysis on furniture survey data."""
    
    def __init__(self, df: pd.DataFrame):
        """Initialize with cleaned data."""
        self.raw_df = df.copy()
        self.df = self.create_numeric_columns()
        
    def create_numeric_columns(self) -> pd.DataFrame:
        """Create numeric columns for analysis."""
        df = self.raw_df.copy()
        
        # Already created in data cleaning:
        # - age_numeric
        # - income_numeric 
        # - isho_familiarity_score
        # - recommendation_score
        
        return df
    
    def analyze_correlations(self) -> dict:
        """Analyze correlations between numeric variables."""
        numeric_cols = [
            'age_numeric',
            'income_numeric',
            'isho_familiarity_score',
            'recommendation_score'
        ]
        
        # Calculate correlation matrix
        corr_matrix = self.df[numeric_cols].corr()
        
        # Calculate p-values for correlations
        p_values = pd.DataFrame(
            index=numeric_cols,
            columns=numeric_cols,
            dtype=float
        )
        
        for i in numeric_cols:
            for j in numeric_cols:
                if i != j:
                    corr, p_val = stats.pearsonr(
                        self.df[i].fillna(0),
                        self.df[j].fillna(0)
                    )
                    p_values.loc[i, j] = p_val
                else:
                    p_values.loc[i, j] = 1.0
        
        return {
            'correlation_matrix': corr_matrix,
            'p_values': p_values
        }
    
    def analyze_age_income_distribution(self) -> dict:
        """Analyze age and income distributions."""
        age_stats = {
            'mean': self.df['age_numeric'].mean(),
            'median': self.df['age_numeric'].median(),
            'std': self.df['age_numeric'].std(),
            'skew': self.df['age_numeric'].skew(),
            'normality_test': stats.normaltest(
                self.df['age_numeric'].dropna()
            )
        }
        
        income_stats = {
            'mean': self.df['income_numeric'].mean(),
            'median': self.df['income_numeric'].median(),
            'std': self.df['income_numeric'].std(),
            'skew': self.df['income_numeric'].skew(),
            'normality_test': stats.normaltest(
                self.df['income_numeric'].dropna()
            )
        }
        
        return {
            'age_statistics': age_stats,
            'income_statistics': income_stats
        }
    
    def analyze_brand_metrics(self) -> dict:
        """Analyze Isho brand metrics."""
        # Analyze familiarity score distribution
        familiarity_stats = {
            'mean': self.df['isho_familiarity_score'].mean(),
            'median': self.df['isho_familiarity_score'].median(),
            'std': self.df['isho_familiarity_score'].std(),
            'distribution': self.df['isho_familiarity_score'].value_counts()
        }
        
        # Analyze recommendation score distribution
        recommendation_stats = {
            'mean': self.df['recommendation_score'].mean(),
            'median': self.df['recommendation_score'].median(),
            'std': self.df['recommendation_score'].std(),
            'distribution': self.df['recommendation_score'].value_counts()
        }
        
        # Test correlation between familiarity and recommendation
        fam_rec_corr = stats.pearsonr(
            self.df['isho_familiarity_score'].fillna(0),
            self.df['recommendation_score'].fillna(0)
        )
        
        return {
            'familiarity_statistics': familiarity_stats,
            'recommendation_statistics': recommendation_stats,
            'familiarity_recommendation_correlation': {
                'correlation': fam_rec_corr[0],
                'p_value': fam_rec_corr[1]
            }
        }
    
    def create_statistical_plots(self, results: dict, show_plots: bool = False):
        """Create statistical visualization plots."""
        # Correlation heatmap
        plt.figure(figsize=config.FIGURE_SIZE)
        sns.heatmap(
            results['correlations']['correlation_matrix'],
            annot=True,
            cmap='coolwarm',
            center=0,
            fmt='.2f'
        )
        plt.title('Correlation Matrix of Numeric Variables')
        if show_plots:
            plt.show()
        else:
            utils.save_and_close_figure(
                plt.gcf(),
                'correlation_matrix',
                'statistical'
            )
        
        # Age-Income scatter plot
        plt.figure(figsize=config.FIGURE_SIZE)
        sns.scatterplot(
            data=self.df,
            x='age_numeric',
            y='income_numeric',
            alpha=0.6
        )
        plt.title('Age vs Income Distribution')
        plt.xlabel('Age')
        plt.ylabel('Income (BDT)')
        if show_plots:
            plt.show()
        else:
            utils.save_and_close_figure(
                plt.gcf(),
                'age_income_scatter',
                'statistical'
            )
        
        # Brand metrics distributions
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Familiarity score distribution
        sns.histplot(
            data=self.df,
            x='isho_familiarity_score',
            discrete=True,
            ax=ax1
        )
        ax1.set_title('Distribution of Isho Familiarity Scores')
        ax1.set_xlabel('Familiarity Score')
        ax1.set_ylabel('Count')
        
        # Recommendation score distribution
        sns.histplot(
            data=self.df,
            x='recommendation_score',
            discrete=True,
            ax=ax2
        )
        ax2.set_title('Distribution of Recommendation Scores')
        ax2.set_xlabel('Recommendation Score')
        ax2.set_ylabel('Count')
        
        plt.tight_layout()
        if show_plots:
            plt.show()
        else:
            utils.save_and_close_figure(
                plt.gcf(),
                'brand_metrics_distribution',
                'statistical'
            )
    
    def print_statistical_summary(self, results: dict):
        """Print comprehensive statistical summary."""
        print("\nStatistical Analysis Summary")
        print("=" * 50)
        
        # Correlation analysis
        print("\nSignificant Correlations (p < 0.05):")
        corr_matrix = results['correlations']['correlation_matrix']
        p_values = results['correlations']['p_values']
        
        for i in corr_matrix.index:
            for j in corr_matrix.columns:
                if i < j and p_values.loc[i, j] < 0.05:
                    print(
                        f"{i} vs {j}:"
                        f" r = {corr_matrix.loc[i, j]:.3f},"
                        f" p = {p_values.loc[i, j]:.3f}"
                    )
        
        # Age and income statistics
        print("\nAge Statistics:")
        age_stats = results['distributions']['age_statistics']
        print(f"Mean: {age_stats['mean']:.1f}")
        print(f"Median: {age_stats['median']:.1f}")
        print(f"Std Dev: {age_stats['std']:.1f}")
        print(f"Skewness: {age_stats['skew']:.3f}")
        
        print("\nIncome Statistics:")
        income_stats = results['distributions']['income_statistics']
        print(f"Mean: {income_stats['mean']:.0f} BDT")
        print(f"Median: {income_stats['median']:.0f} BDT")
        print(f"Std Dev: {income_stats['std']:.0f} BDT")
        print(f"Skewness: {income_stats['skew']:.3f}")
        
        # Brand metrics
        print("\nBrand Metrics:")
        fam_stats = results['brand_metrics']['familiarity_statistics']
        rec_stats = results['brand_metrics']['recommendation_statistics']
        
        print("\nFamiliarity Score Statistics:")
        print(f"Mean: {fam_stats['mean']:.2f}")
        print(f"Median: {fam_stats['median']:.2f}")
        print(f"Std Dev: {fam_stats['std']:.2f}")
        
        print("\nRecommendation Score Statistics:")
        print(f"Mean: {rec_stats['mean']:.2f}")
        print(f"Median: {rec_stats['median']:.2f}")
        print(f"Std Dev: {rec_stats['std']:.2f}")
        
        fam_rec_corr = results['brand_metrics']['familiarity_recommendation_correlation']
        print("\nFamiliarity-Recommendation Correlation:")
        print(f"r = {fam_rec_corr['correlation']:.3f}")
        print(f"p = {fam_rec_corr['p_value']:.3f}")
    
    def run_statistical_analysis(self, show_plots: bool = False) -> dict:
        """Main entry point for statistical analysis."""
        print("Starting statistical analysis...")
        
        # Run analyses
        results = {
            'correlations': self.analyze_correlations(),
            'distributions': self.analyze_age_income_distribution(),
            'brand_metrics': self.analyze_brand_metrics()
        }
        
        # Create visualizations
        self.create_statistical_plots(results, show_plots)
        
        # Print summary
        self.print_statistical_summary(results)
        
        # Save results
        utils.save_analysis_results(results, 'statistical_analysis')
        
        print("Statistical analysis completed!")
        return results