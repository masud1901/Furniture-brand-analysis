"""Brand analysis module for furniture survey data."""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, Tuple
from . import utils


class BrandAnalyzer:
    """Class for analyzing Isho brand perceptions and preferences."""

    def __init__(self, df: pd.DataFrame):
        """Initialize with survey dataframe."""
        self.df = df

    def get_brand_awareness(self) -> Dict[str, pd.Series]:
        """Analyze Isho brand awareness and familiarity."""
        # Get familiarity scores
        familiarity = self.df[
            'how_familiar_are_you_with_the_isho_brand_rate_on_a_scale_of_1_to_5'
        ].value_counts().sort_index()
        
        # Get feedback heard
        feedback = self.df[
            'have_you_heard_any_specific_feedback_or_reviews_about_isho_from_friends_or_family'
        ].value_counts()
        
        # Purchase history
        purchase = self.df[
            'have_you_ever_bought_any_furniture_from_isho'
        ].value_counts()
        
        return {
            'familiarity': {
                'counts': familiarity,
                'percentages': (familiarity / len(self.df) * 100).round(1)
            },
            'feedback': {
                'counts': feedback,
                'percentages': (feedback / len(self.df) * 100).round(1)
            },
            'purchase': {
                'counts': purchase,
                'percentages': (purchase / len(self.df) * 100).round(1)
            }
        }

    def get_brand_perceptions(self) -> Dict[str, Dict[str, pd.Series]]:
        """Analyze Isho brand perceptions."""
        # Brand associations for those who bought from Isho
        buyers_associations = self.df[
            self.df['have_you_ever_bought_any_furniture_from_isho'] == 'Yes'
        ]['when_you_think_of_isho_which_of_the_following_words_or_phrases_come_to_mind'].value_counts()
        
        # Brand associations for those who didn't buy
        non_buyers_associations = self.df[
            self.df['have_you_ever_bought_any_furniture_from_isho'] == 'No'
        ]['when_you_think_of_isho_which_of_the_following_words_or_phrases_come_to_mind'].value_counts()
        
        # Important factors for buyers
        factors = self.df[
            self.df['have_you_ever_bought_any_furniture_from_isho'] == 'Yes'
        ]['what_factors_do_you_consider_most_important_when_evaluating_isho_as_a_furniture_brand'].str.get_dummies(sep=',').sum()
        
        # Brand comparison for buyers
        comparison = self.df[
            self.df['have_you_ever_bought_any_furniture_from_isho'] == 'Yes'
        ]['what_is_your_perception_of_isho_compared_to_other_brands'].value_counts()
        
        # Brand comparison for non-buyers
        non_buyer_comparison = self.df[
            self.df['have_you_ever_bought_any_furniture_from_isho'] == 'No'
        ]['what_is_your_perception_of_isho_compared_to_other_brands'].value_counts()
        
        # Recommendation score
        recommendation = self.df[
            'would_you_recommend_isho_to_others_rank_on_a_scale_of_1_to_5'
        ].value_counts().sort_index()
        
        return {
            'buyers_associations': {
                'counts': buyers_associations,
                'percentages': (buyers_associations / len(self.df) * 100).round(1)
            },
            'non_buyers_associations': {
                'counts': non_buyers_associations,
                'percentages': (non_buyers_associations / len(self.df) * 100).round(1)
            },
            'factors': {
                'counts': factors,
                'percentages': (factors / len(self.df) * 100).round(1)
            },
            'buyer_comparison': {
                'counts': comparison,
                'percentages': (comparison / len(self.df) * 100).round(1)
            },
            'non_buyer_comparison': {
                'counts': non_buyer_comparison,
                'percentages': (non_buyer_comparison / len(self.df) * 100).round(1)
            },
            'recommendation': {
                'counts': recommendation,
                'percentages': (recommendation / len(self.df) * 100).round(1)
            }
        }

    def analyze_non_purchase_reasons(self) -> Dict[str, pd.Series]:
        """Analyze reasons for not purchasing from Isho."""
        reasons = self.df[
            "what_is_the_primary_reason_you_didn't_buy_anything_from_isho"
        ].value_counts()
        
        return {
            'counts': reasons,
            'percentages': (reasons / len(self.df) * 100).round(1)
        }

    def plot_brand_metrics(
        self,
        data: pd.Series,
        title: str,
        figsize: Tuple[int, int] = (10, 6),
        show_plot: bool = False
    ) -> None:
        """Create bar plot for brand metrics."""
        fig = plt.figure(figsize=figsize)
        sns.barplot(x=data.values, y=data.index, palette='viridis')
        plt.title(title, pad=15, fontsize=12)
        plt.xlabel('Number of Responses')
        plt.ylabel('Category')
        plt.tight_layout()
        
        if show_plot:
            plt.show()
        else:
            utils.save_and_close_figure(
                fig, 
                f"{title.lower().replace(' ', '_')}", 
                'brands'
            )

    def create_brand_plots(
        self,
        awareness: Dict,
        perceptions: Dict,
        non_purchase: Dict,
        show_plots: bool = False
    ) -> None:
        """Create all brand-related plots."""
        # Plot familiarity distribution
        plt.figure(figsize=(10, 6))
        sns.barplot(
            x=awareness['familiarity']['counts'].index,
            y=awareness['familiarity']['counts'].values
        )
        plt.title('Isho Brand Familiarity Distribution')
        plt.xlabel('Familiarity Score (1-5)')
        plt.ylabel('Number of Responses')
        if not show_plots:
            utils.save_and_close_figure(plt.gcf(), 'brand_familiarity', 'brands')
        
        # Plot brand associations for buyers
        if not perceptions['buyers_associations']['counts'].empty:
            self.plot_brand_metrics(
                perceptions['buyers_associations']['counts'],
                'Isho Brand Associations (Buyers)',
                figsize=(12, 6),
                show_plot=show_plots
            )
        
        # Plot brand associations for non-buyers
        if not perceptions['non_buyers_associations']['counts'].empty:
            self.plot_brand_metrics(
                perceptions['non_buyers_associations']['counts'],
                'Isho Brand Associations (Non-Buyers)',
                figsize=(12, 6),
                show_plot=show_plots
            )
        
        # Plot recommendation distribution
        plt.figure(figsize=(10, 6))
        sns.barplot(
            x=perceptions['recommendation']['counts'].index,
            y=perceptions['recommendation']['counts'].values
        )
        plt.title('Isho Recommendation Score Distribution')
        plt.xlabel('Recommendation Score (1-5)')
        plt.ylabel('Number of Responses')
        if not show_plots:
            utils.save_and_close_figure(
                plt.gcf(), 
                'recommendation_distribution', 
                'brands'
            )
        
        # Plot non-purchase reasons
        if not non_purchase['counts'].empty:
            self.plot_brand_metrics(
                non_purchase['counts'],
                'Reasons for Not Purchasing from Isho',
                figsize=(12, 6),
                show_plot=show_plots
            )

    def print_brand_summary(
        self,
        awareness: Dict,
        perceptions: Dict,
        non_purchase: Dict
    ) -> None:
        """Print comprehensive brand analysis summary."""
        print("\nIsho Brand Analysis Summary")
        print("=" * 50)
        
        # Brand awareness
        print("\nBrand Awareness:")
        print("-" * 20)
        print("\nFamiliarity Scores (1-5):")
        for score, pct in awareness['familiarity']['percentages'].items():
            print(f"Score {score}: {pct}%")
        
        print("\nFeedback Heard:")
        for feedback, pct in awareness['feedback']['percentages'].items():
            print(f"{feedback}: {pct}%")
        
        # Brand perceptions
        print("\nBrand Perceptions:")
        print("-" * 20)
        
        if not perceptions['buyers_associations']['counts'].empty:
            print("\nBuyers' Brand Associations:")
            for assoc, pct in perceptions['buyers_associations']['percentages'].head().items():
                print(f"{assoc}: {pct}%")
        
        if not perceptions['non_buyers_associations']['counts'].empty:
            print("\nNon-Buyers' Brand Associations:")
            for assoc, pct in perceptions['non_buyers_associations']['percentages'].head().items():
                print(f"{assoc}: {pct}%")
        
        print("\nBrand Comparison (Buyers):")
        for comp, pct in perceptions['buyer_comparison']['percentages'].items():
            print(f"{comp}: {pct}%")
        
        print("\nBrand Comparison (Non-Buyers):")
        for comp, pct in perceptions['non_buyer_comparison']['percentages'].items():
            print(f"{comp}: {pct}%")
        
        # Non-purchase reasons
        if not non_purchase['counts'].empty:
            print("\nTop Reasons for Not Purchasing:")
            print("-" * 20)
            for reason, pct in non_purchase['percentages'].head().items():
                print(f"{reason}: {pct}%")

    def run_brand_analysis(self, show_plots: bool = False) -> Dict:
        """Main entry point for brand analysis."""
        print("Starting brand analysis...")
        
        # Get brand analyses
        awareness = self.get_brand_awareness()
        perceptions = self.get_brand_perceptions()
        non_purchase = self.analyze_non_purchase_reasons()
        
        # Create visualizations
        self.create_brand_plots(awareness, perceptions, non_purchase, show_plots)
        
        # Print summary
        self.print_brand_summary(awareness, perceptions, non_purchase)
        
        # Save results
        results = {
            'awareness': awareness,
            'perceptions': perceptions,
            'non_purchase_reasons': non_purchase
        }
        utils.save_analysis_results(results, 'brand_analysis')
        
        print("Brand analysis completed!")
        return results