"""Advanced statistical analysis module for furniture survey data."""
import pandas as pd
import numpy as np
from scipy import stats
from scipy.stats import chi2, f, t, norm
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, Any
from . import utils


class AdvancedAnalyzer:
    """Class for performing advanced statistical analysis on furniture survey data."""

    def __init__(self, df: pd.DataFrame):
        """Initialize with survey dataframe."""
        self.df = df
        self.df_clean = self.handle_missing_data(df)

    def handle_missing_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Handle missing data through imputation."""
        df_clean = df.copy()
        
        # Numeric imputation
        num_cols = ['age_numeric', 'income_numeric', 
                   'isho_familiarity_score', 'recommendation_score']
        num_imputer = SimpleImputer(strategy='mean')
        df_clean[num_cols] = num_imputer.fit_transform(df_clean[num_cols])
        
        return df_clean

    def detect_outliers(self, columns: list) -> Dict[str, Any]:
        """Detect outliers using IQR method."""
        outliers = {}
        
        for col in columns:
            Q1 = self.df_clean[col].quantile(0.25)
            Q3 = self.df_clean[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers[col] = {
                'outliers': self.df_clean[
                    (self.df_clean[col] < lower_bound) | 
                    (self.df_clean[col] > upper_bound)
                ][col],
                'bounds': (lower_bound, upper_bound)
            }
        
        return outliers

    def run_pca_analysis(self, columns: list) -> Dict[str, Any]:
        """Perform PCA on numeric features."""
        # Standardize the features
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(self.df_clean[columns])
        
        # Apply PCA
        pca = PCA()
        pca_result = pca.fit_transform(scaled_data)
        
        # Calculate explained variance
        explained_var = pca.explained_variance_ratio_
        cumulative_var = np.cumsum(explained_var)
        
        # Create scree plot
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(range(1, len(explained_var) + 1), cumulative_var, 'bo-')
        ax.set_xlabel('Number of Components')
        ax.set_ylabel('Cumulative Explained Variance')
        ax.set_title('PCA Scree Plot')
        
        utils.save_and_close_figure(fig, 'pca_scree_plot', 'advanced')
        
        return {
            'pca_components': pca_result,
            'explained_variance': explained_var,
            'cumulative_variance': cumulative_var,
            'feature_importance': pd.DataFrame(
                pca.components_,
                columns=columns
            )
        }

    def perform_cluster_analysis(self, features: list) -> Dict[str, Any]:
        """Perform k-means clustering on furniture preferences."""
        # Prepare data
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(self.df_clean[features])
        
        # Find optimal number of clusters using elbow method
        inertias = []
        K = range(1, 10)
        for k in K:
            kmeans = KMeans(n_clusters=k, random_state=42)
            kmeans.fit(scaled_data)
            inertias.append(kmeans.inertia_)
        
        # Plot elbow curve
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(K, inertias, 'bo-')
        ax.set_xlabel('Number of Clusters (k)')
        ax.set_ylabel('Inertia')
        ax.set_title('Elbow Method for Optimal k')
        
        utils.save_and_close_figure(fig, 'kmeans_elbow', 'advanced')
        
        # Perform clustering with optimal k
        optimal_k = 3  # This should be determined from elbow plot
        kmeans = KMeans(n_clusters=optimal_k, random_state=42)
        clusters = kmeans.fit_predict(scaled_data)
        
        return {
            'clusters': clusters,
            'inertias': inertias,
            'cluster_centers': kmeans.cluster_centers_,
            'optimal_k': optimal_k
        }

    def analyze_correlations(self) -> Dict[str, Any]:
        """Perform advanced correlation analysis."""
        numeric_cols = [
            'age_numeric', 'income_numeric',
            'isho_familiarity_score', 'recommendation_score'
        ]
        
        # Calculate correlations
        pearson_corr = self.df_clean[numeric_cols].corr(method='pearson')
        spearman_corr = self.df_clean[numeric_cols].corr(method='spearman')
        
        # Create correlation heatmaps
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        sns.heatmap(
            pearson_corr, 
            ax=ax1, 
            annot=True, 
            fmt='.2f', 
            cmap='coolwarm'
        )
        ax1.set_title('Pearson Correlation')
        
        sns.heatmap(
            spearman_corr, 
            ax=ax2, 
            annot=True, 
            fmt='.2f', 
            cmap='coolwarm'
        )
        ax2.set_title('Spearman Correlation')
        
        plt.tight_layout()
        utils.save_and_close_figure(fig, 'correlation_heatmaps', 'advanced')
        
        return {
            'pearson': pearson_corr,
            'spearman': spearman_corr
        }

    def calculate_effect_sizes(self) -> Dict[str, Any]:
        """Calculate effect sizes for key relationships."""
        results = {}
        
        # Effect size for income vs familiarity score
        income_fam_corr = stats.pearsonr(
            self.df_clean['income_numeric'],
            self.df_clean['isho_familiarity_score']
        )
        
        results['income_familiarity'] = {
            'correlation': income_fam_corr[0],
            'p_value': income_fam_corr[1],
            'effect_size': abs(income_fam_corr[0])
        }
        
        # Effect size for age vs recommendation score
        age_rec_corr = stats.pearsonr(
            self.df_clean['age_numeric'],
            self.df_clean['recommendation_score']
        )
        
        results['age_recommendation'] = {
            'correlation': age_rec_corr[0],
            'p_value': age_rec_corr[1],
            'effect_size': abs(age_rec_corr[0])
        }
        
        return results

    def perform_bootstrap_analysis(self, n_iterations: int = 1000) -> Dict[str, Any]:
        """Perform bootstrap analysis for key metrics."""
        results = {}
        
        # Bootstrap for mean recommendation score
        rec_scores = self.df_clean['recommendation_score'].dropna()
        original_mean = rec_scores.mean()
        bootstrap_means = []
        
        for _ in range(n_iterations):
            sample = np.random.choice(
                rec_scores, 
                size=len(rec_scores), 
                replace=True
            )
            bootstrap_means.append(np.mean(sample))
        
        ci_lower = np.percentile(bootstrap_means, 2.5)
        ci_upper = np.percentile(bootstrap_means, 97.5)
        
        # Plot bootstrap distribution
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.histplot(bootstrap_means, kde=True, ax=ax)
        ax.axvline(original_mean, color='r', linestyle='--', 
                  label='Original Mean')
        ax.axvline(ci_lower, color='g', linestyle=':', label='95% CI')
        ax.axvline(ci_upper, color='g', linestyle=':')
        ax.set_title('Bootstrap Distribution of Mean Recommendation Score')
        ax.legend()
        
        utils.save_and_close_figure(
            fig, 
            'bootstrap_recommendation_score', 
            'advanced'
        )
        
        results['recommendation_bootstrap'] = {
            'original_mean': original_mean,
            'bootstrap_means': bootstrap_means,
            'ci_lower': ci_lower,
            'ci_upper': ci_upper
        }
        
        return results

    def run_advanced_analysis(self, show_plots: bool = False) -> Dict[str, Any]:
        """Main entry point for advanced analysis."""
        print("Starting advanced statistical analysis...")
        
        numeric_cols = [
            'age_numeric', 'income_numeric',
            'isho_familiarity_score', 'recommendation_score'
        ]
        
        # Run analyses
        results = {
            'outliers': self.detect_outliers(numeric_cols),
            'correlations': self.analyze_correlations(),
            'effect_sizes': self.calculate_effect_sizes(),
            'bootstrap': self.perform_bootstrap_analysis(),
            'pca': self.run_pca_analysis(numeric_cols),
            'clustering': self.perform_cluster_analysis(numeric_cols)
        }
        
        # Print summary
        print("\nAdvanced Analysis Summary")
        print("=" * 50)
        
        # Correlation summary
        print("\nKey Correlations:")
        corr_matrix = results['correlations']['pearson']
        for i in range(len(numeric_cols)):
            for j in range(i+1, len(numeric_cols)):
                corr = corr_matrix.iloc[i, j]
                print(f"{numeric_cols[i]} vs {numeric_cols[j]}: {corr:.3f}")
        
        # Effect sizes
        print("\nEffect Sizes:")
        for relation, stats in results['effect_sizes'].items():
            print(f"\n{relation}:")
            print(f"Correlation: {stats['correlation']:.3f}")
            print(f"Effect Size: {stats['effect_size']:.3f}")
            print(f"P-value: {stats['p_value']:.3f}")
        
        # Bootstrap results
        boot = results['bootstrap']['recommendation_bootstrap']
        print("\nBootstrap Analysis:")
        print(f"Mean Recommendation Score: {boot['original_mean']:.2f}")
        print(f"95% CI: [{boot['ci_lower']:.2f}, {boot['ci_upper']:.2f}]")
        
        # Save results
        utils.save_analysis_results(results, 'advanced_analysis')
        
        print("\nAdvanced statistical analysis completed!")
        return results