"""Preference analysis module for furniture survey data."""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, Tuple
from . import utils


class PreferenceAnalyzer:
    """Class for analyzing furniture preferences from survey data."""

    def __init__(self, df: pd.DataFrame):
        """Initialize with survey dataframe."""
        self.df = df

    def plot_horizontal_preferences(
        self,
        data: pd.Series,
        title: str,
        xlabel: str,
        ylabel: str,
        figsize: Tuple[int, int] = (10, 6),
        show_plot: bool = False
    ):
        """Create horizontal bar plot for preferences."""
        fig, ax = plt.subplots(figsize=figsize)
        
        data.plot(
            kind='barh',
            ax=ax,
            color='skyblue'
        )
        
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        
        # Add value labels
        for i, v in enumerate(data):
            ax.text(v, i, f' {v}', va='center')
        
        plt.tight_layout()
        
        if show_plot:
            plt.show()
        else:
            utils.save_and_close_figure(
                fig, 
                f"{title.lower().replace(' ', '_')}", 
                'preferences'
            )

    def analyze_furniture_types(self) -> Dict[str, pd.Series]:
        """Analyze furniture type preferences."""
        furniture_types = (
            self.df['what_type_of_furniture_do_you_prefer']
            .str.get_dummies(sep=',')
        )
        
        type_preferences = furniture_types.sum().sort_values(ascending=False)
        type_percentages = (type_preferences / len(self.df) * 100).round(1)
        
        return {
            'counts': type_preferences,
            'percentages': type_percentages
        }

    def analyze_purchase_factors(self) -> Dict[str, pd.Series]:
        """Analyze factors influencing purchase decisions."""
        purchase_factors = (
            self.df['what_factors_are_most_important_to_you_when_buying_furniture']
            .str.get_dummies(sep=',')
        )
        
        factor_counts = purchase_factors.sum().sort_values(ascending=False)
        factor_percentages = (factor_counts / len(self.df) * 100).round(1)
        
        return {
            'counts': factor_counts,
            'percentages': factor_percentages
        }

    def analyze_room_priorities(self) -> Dict[str, pd.Series]:
        """Analyze room priorities when buying furniture."""
        room_priorities = (
            self.df['which_room_do_you_prioritise_when_buying_furniture']
            .str.get_dummies(sep=',')
        )
        
        priority_counts = room_priorities.sum().sort_values(ascending=False)
        priority_percentages = (priority_counts / len(self.df) * 100).round(1)
        
        return {
            'counts': priority_counts,
            'percentages': priority_percentages
        }

    def analyze_shopping_preferences(self) -> Dict[str, Dict]:
        """Analyze shopping preferences and patterns."""
        # Ready-made vs Custom-made
        make_preference = self.df[
            'do_you_prefer_ready-made_or_custom-made_furniture'
        ].value_counts()
        
        # Shopping channel preference
        channel_preference = self.df[
            'how_do_you_typically_shop_for_furniture'
        ].value_counts()
        
        # Information sources
        info_sources = (
            self.df['what_sources_of_information_do_you_rely_on_when_choosing_furniture']
            .str.get_dummies(sep=',')
        ).sum().sort_values(ascending=False)
        
        # Purchase timing
        timing_preference = self.df[
            'in_which_time_of_the_year_do_you_prefer_buying_new_furniture'
        ].value_counts()
        
        # Purchase reasons
        purchase_reasons = (
            self.df['why_do_you_usually_buy_furniture']
            .str.get_dummies(sep=',')
        ).sum().sort_values(ascending=False)
        
        return {
            'make_preference': {
                'counts': make_preference,
                'percentages': (make_preference / len(self.df) * 100).round(1)
            },
            'channel_preference': {
                'counts': channel_preference,
                'percentages': (channel_preference / len(self.df) * 100).round(1)
            },
            'info_sources': {
                'counts': info_sources,
                'percentages': (info_sources / len(self.df) * 100).round(1)
            },
            'timing_preference': {
                'counts': timing_preference,
                'percentages': (timing_preference / len(self.df) * 100).round(1)
            },
            'purchase_reasons': {
                'counts': purchase_reasons,
                'percentages': (purchase_reasons / len(self.df) * 100).round(1)
            }
        }

    def create_preference_summary(self, results: Dict) -> None:
        """Print summary of all preference analyses."""
        print("\nFurniture Preference Analysis")
        print("=" * 50)
        
        # Furniture type preferences
        print("\nTop Furniture Types:")
        for type_name, percentage in results['types']['percentages'].items():
            print(f"{type_name}: {percentage}%")
        
        # Purchase factors
        print("\nMost Important Purchase Factors:")
        for factor, percentage in results['factors']['percentages'].items():
            print(f"{factor}: {percentage}%")
        
        # Room priorities
        print("\nRoom Priorities:")
        for room, percentage in results['room_priorities']['percentages'].items():
            print(f"{room}: {percentage}%")
        
        # Shopping preferences
        print("\nShopping Preferences:")
        print("\nReady-made vs Custom-made:")
        for pref, percentage in results['shopping']['make_preference']['percentages'].items():
            print(f"{pref}: {percentage}%")
        
        print("\nShopping Channels:")
        for channel, percentage in results['shopping']['channel_preference']['percentages'].items():
            print(f"{channel}: {percentage}%")
        
        print("\nPreferred Purchase Timing:")
        for timing, percentage in results['shopping']['timing_preference']['percentages'].items():
            print(f"{timing}: {percentage}%")

    def create_preference_plots(self, results: Dict, show_plots: bool = False) -> None:
        """Create all preference-related plots."""
        # Plot furniture type preferences
        self.plot_horizontal_preferences(
            results['types']['counts'],
            'Furniture Type Preferences',
            'Number of Consumers',
            'Furniture Type',
            show_plot=show_plots
        )
        
        # Plot purchase factors
        self.plot_horizontal_preferences(
            results['factors']['counts'],
            'Important Purchase Factors',
            'Number of Consumers',
            'Factor',
            show_plot=show_plots
        )
        
        # Plot room priorities
        self.plot_horizontal_preferences(
            results['room_priorities']['counts'],
            'Room Priorities',
            'Number of Consumers',
            'Room',
            show_plot=show_plots
        )
        
        # Plot shopping preferences
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        
        # Ready-made vs Custom-made
        make_data = results['shopping']['make_preference']['counts']
        sns.barplot(x=make_data.index, y=make_data.values, ax=ax1)
        ax1.set_title('Ready-made vs Custom-made Preference')
        ax1.set_xlabel('Preference')
        ax1.set_ylabel('Number of Consumers')
        ax1.tick_params(axis='x', rotation=45)
        
        # Shopping channels
        channel_data = results['shopping']['channel_preference']['counts']
        sns.barplot(x=channel_data.index, y=channel_data.values, ax=ax2)
        ax2.set_title('Shopping Channel Preference')
        ax2.set_xlabel('Channel')
        ax2.set_ylabel('Number of Consumers')
        ax2.tick_params(axis='x', rotation=45)
        
        # Purchase timing
        timing_data = results['shopping']['timing_preference']['counts']
        sns.barplot(x=timing_data.index, y=timing_data.values, ax=ax3)
        ax3.set_title('Preferred Purchase Timing')
        ax3.set_xlabel('Time of Year')
        ax3.set_ylabel('Number of Consumers')
        ax3.tick_params(axis='x', rotation=45)
        
        # Purchase reasons
        reason_data = results['shopping']['purchase_reasons']['counts'].head()
        sns.barplot(x=reason_data.index, y=reason_data.values, ax=ax4)
        ax4.set_title('Top 5 Purchase Reasons')
        ax4.set_xlabel('Reason')
        ax4.set_ylabel('Number of Consumers')
        ax4.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        
        if show_plots:
            plt.show()
        else:
            utils.save_and_close_figure(fig, 'shopping_preferences', 'preferences')

    def run_preference_analysis(self, show_plots: bool = False) -> Dict:
        """Main entry point for preference analysis."""
        print("Starting preference analysis...")
        
        # Run analyses
        results = {
            'types': self.analyze_furniture_types(),
            'factors': self.analyze_purchase_factors(),
            'room_priorities': self.analyze_room_priorities(),
            'shopping': self.analyze_shopping_preferences()
        }
        
        # Create visualizations
        self.create_preference_plots(results, show_plots)
        
        # Print summary
        self.create_preference_summary(results)
        
        # Save results
        utils.save_analysis_results(results, 'preference_analysis')
        
        print("Preference analysis completed!")
        return results