"""
Meta-Analysis Script for Mann-Kendall Trend Tests on Multi-Repository Hourly Commit Data

This script addresses the hierarchical nature of commit data by:
1. Performing Mann-Kendall tests separately for each repository
2. Aggregating results using meta-analysis techniques
3. Providing overall trend assessments with proper statistical inference
4. Including detailed group statistics based on repository metadata (e.g., type, size)

The script reads a list of repository names from a text file, then looks for corresponding
CSV files (one per repository) containing commit data across hours of the day over multiple years.
It performs individual Mann-Kendall tests, and then combines the results to provide overall
trend conclusions. It also leverages a separate metadata CSV to provide aggregate statistics
for different groups of repositories (e.g., significant trends vs. non-significant,
corporate vs. volunteering).

Usage:
    python multi_repo_mann_kendall_hours.py <directory_path> <time_block_start> <time_block_end> <repo_list_txt> <repo_metadata_csv> [--output_dir <output_directory>] [--alpha <significance_level>] [--plot]

Arguments:
    directory_path: Directory containing CSV files (one per repository), typically named like 'ownername_CommitPercentagesPerHour.csv'.
    time_block_start: The starting hour block for analysis (0=00:00-01:00, 23=23:00-00:00).
    time_block_end: The ending hour block for analysis (inclusive).
    repo_list_txt: Path to a text file containing one repository 'owner/name' per line.
    repo_metadata_csv: Path to the CSV file with repository metadata (e.g., 'repository' for owner/name, 'type' for corporate/volunteering, 'size_kb', 'contributors', 'commits', 'stars', 'language').
    --output_dir: Directory to save output files (default: current directory).
    --alpha: Significance level for tests (default: 0.05).
    --plot: Generate visualization plot (optional).
"""
import os
import sys
import argparse
import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import norm
import pymannkendall as mk
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Ensure stdout encoding is utf-8 for broad compatibility
if os.name == 'nt':
    sys.stdout.reconfigure(encoding='utf-8')

def clean_repo_name_for_filename_and_lookup(repo_identifier):
    """
    Cleans a repository identifier string to a consistent format suitable
    for filename creation and metadata lookup.
    Handles 'owner/name', 'ownername_CommitPercentagesPerDay.csv', 'ownername_CommitPercentagesPerHour.csv'
    or just 'ownername'.
    Removes slashes, dots, and common suffixes. Converts to lowercase.
    Examples:
    - 'eclipse-platform/eclipse.platform.swt' -> 'eclipseplatformeclipseplatformswt'
    - 'eclipse-platformeclipseplatformswt_CommitPercentagesPerHour' -> 'eclipseplatformeclipseplatformswt'
    """
    cleaned_name = repo_identifier.replace('/', '')
    cleaned_name = cleaned_name.replace('.', '')
    # Remove common suffixes from generated filenames if they exist
    # Convert to lowercase before checking suffix for case-insensitivity
    lower_cleaned_name = cleaned_name.lower()
    
    if '_commitpercentagesperday' in lower_cleaned_name:
        cleaned_name = lower_cleaned_name.replace('_commitpercentagesperday', '')
    if '_commitpercentagesperhour' in lower_cleaned_name: # NEW SUFFIX
        cleaned_name = lower_cleaned_name.replace('_commitpercentagesperhour', '')
    
    return cleaned_name.strip().lower() # Ensure final output is always lowercase

class RepositoryAnalyzer:
    """Handles analysis for individual repositories."""
    
    def __init__(self, filepath, time_block_start, time_block_end):
        self.filepath = filepath
        # Extract base name from filepath and clean it for consistent matching
        self.original_filename_stem = Path(filepath).stem # e.g., 'eclipse-platformeclipse.platform.swt_CommitPercentagesPerHour'
        self.cleaned_repo_name = clean_repo_name_for_filename_and_lookup(self.original_filename_stem) # e.g., 'eclipseplatformeclipseplatformswt'
        self.repo_name = self.cleaned_repo_name # Use this cleaned name for reporting
        self.time_block_start = time_block_start
        self.time_block_end = time_block_end
        self.data = None
        self.periods = None
        self.hours = None
        self.result = None
        
    def load_data(self):
        """Load and parse CSV data for the repository."""
        try:
            df = pd.read_csv(self.filepath, index_col=0)
            self.periods = df.columns.tolist()
            self.hours = df.index.tolist()
            self.data = df.values  # 24 hours x n_years
            return True
        except Exception as e:
            print(f"Error loading {self.filepath}: {e}")
            return False
    
    def process_time_range(self):
        """Process commit data to compute totals for specified time blocks."""
        if self.data is None:
            return None
            
        time_series_data = []
        
        for period_idx in range(len(self.periods)):
            if self.time_block_start != self.time_block_end:
                # Sum across the time range
                if self.time_block_start < self.time_block_end:
                    # Normal range (e.g., 9-17 for business hours)
                    total = np.sum(self.data[self.time_block_start:self.time_block_end+1, period_idx])
                else:
                    # Wraparound range (e.g., 22-6 for night hours)
                    # Sum from start to 23, and from 0 to end
                    total = (np.sum(self.data[self.time_block_start:, period_idx]) + 
                             np.sum(self.data[:self.time_block_end+1, period_idx]))
            else:
                # Single hour
                total = self.data[self.time_block_start, period_idx]
            
            time_series_data.append(total)
        
        return time_series_data
    
    def analyze_trend(self):
        """Perform Mann-Kendall test for the time range."""
        if self.data is None:
            if not self.load_data():
                return False
                
        time_series_data = self.process_time_range()
        if time_series_data is None:
            return False
        
        # Handle missing or invalid data
        valid_data = np.array([x for x in time_series_data if not np.isnan(x)])
        if len(valid_data) < 3: # Mann-Kendall needs at least 3 data points
            # print(f"DEBUG: Not enough valid data points ({len(valid_data)}) for Mann-Kendall test for {self.repo_name}.")
            return False
            
        try:
            mk_result = mk.original_test(valid_data)
            self.result = {
                'trend': mk_result[0],
                'p_value': mk_result[2],
                'tau': mk_result[4],
                'slope': mk_result[7] if len(mk_result) > 7 else None,
                'data_points': len(valid_data),
                'time_series': time_series_data,
                'mean_percentage': np.mean(valid_data),
                'std_percentage': np.std(valid_data)
            }
            return True
        except Exception as e:
            print(f"Error analyzing {self.repo_name}: {e}")
            return False

class MetaAnalyzer:
    """Handles meta-analysis across repositories."""
    
    def __init__(self, time_block_start, time_block_end, alpha=0.05, repo_metadata_df=None):
        self.time_block_start = time_block_start
        self.time_block_end = time_block_end
        self.alpha = alpha
        self.repo_analyzers = []
        self.meta_result = None
        self.repo_metadata_df = repo_metadata_df # Store the full metadata DataFrame
        
    def add_repository(self, filepath):
        """Add a repository for analysis."""
        analyzer = RepositoryAnalyzer(filepath, self.time_block_start, self.time_block_end)
        if analyzer.analyze_trend():
            self.repo_analyzers.append(analyzer)
            return True
        return False
    
    def calculate_effect_size(self, tau):
        """Calculate effect size from Kendall's tau."""
        # Convert tau to Cohen's d equivalent for meta-analysis
        # Using approximation: d ≈ 2 * tau / sqrt(1 - tau²)
        if abs(tau) >= 1:
            return np.sign(tau) * 3  # Cap extreme values
        return 2 * tau / np.sqrt(1 - tau**2)
    
    def get_time_range_description(self):
        """Get human-readable description of the time range."""
        if self.time_block_start == self.time_block_end:
            return f"{self.time_block_start:02d}:00-{self.time_block_start+1:02d}:00"
        elif self.time_block_start < self.time_block_end:
            return f"{self.time_block_start:02d}:00-{self.time_block_end+1:02d}:00"
        else:
            # This handles wraparound, e.g., 22-06
            return f"{self.time_block_start:02d}:00-24:00 and 00:00-{self.time_block_end+1:02d}:00"
    
    def perform_meta_analysis(self):
        """Perform meta-analysis across all repositories."""
        if len(self.repo_analyzers) < 2:
            print("Error: Need at least 2 repositories for meta-analysis")
            return False
            
        print(f"Performing meta-analysis on {len(self.repo_analyzers)} repositories...")
        print(f"Time range: {self.get_time_range_description()}")

        if self.repo_metadata_df is None:
            print("Warning: Repository metadata CSV not loaded. Group statistics will not be generated.")
        
        valid_results = []
        
        for analyzer in self.repo_analyzers:
            result = analyzer.result
            if result is not None and result['p_value'] is not None:
                valid_results.append({
                    'repo': analyzer.repo_name, # This is the cleaned repo name from analyzer
                    'repo_cleaned_name_for_lookup': analyzer.cleaned_repo_name, # Key for metadata join
                    'tau': result['tau'],
                    'p_value': result['p_value'],
                    'n': result['data_points'],
                    'effect_size': self.calculate_effect_size(result['tau']),
                    'trend': result['trend'],
                    'mean_pct': result['mean_percentage'],
                    'std_pct': result['std_percentage'],
                    'time_series': result['time_series']
                })
        
        if len(valid_results) < 2:
            print("Error: Need at least 2 valid results for meta-analysis")
            return False
            
        # Extract statistics
        effect_sizes = np.array([r['effect_size'] for r in valid_results])
        p_values = np.array([r['p_value'] for r in valid_results])
        sample_sizes = np.array([r['n'] for r in valid_results])
        taus = np.array([r['tau'] for r in valid_results])
        
        # Meta-analysis using inverse variance weighting
        weights = sample_sizes - 3  # Approximate standard error weighting
        weights = np.maximum(weights, 1)  # Ensure positive weights
        
        # Weighted mean effect size
        weighted_effect = np.average(effect_sizes, weights=weights)
        
        # Weighted mean tau
        weighted_tau = np.average(taus, weights=weights)
        
        # Combined p-value using Fisher's method
        try:
            # Filter out p-values that are exactly 0 or 1, which cause issues with log
            # Add a small epsilon to 0 p-values, subtract epsilon from 1 p-values
            p_values_for_fisher = np.clip(p_values, 1e-300, 1 - 1e-15) # Smallest float is around 1e-308
            chi2_stat = -2 * np.sum(np.log(p_values_for_fisher))
            combined_p = 1 - stats.chi2.cdf(chi2_stat, 2 * len(p_values_for_fisher))
        except Exception as e:
            print(f"Warning: Error calculating combined p-value (Fisher's method): {e}. Setting to NaN.")
            combined_p = np.nan
            
        # Heterogeneity assessment (I²)
        mean_effect = np.mean(effect_sizes)
        Q = np.sum(weights * (effect_sizes - mean_effect)**2)
        df_heterogeneity = len(effect_sizes) - 1 # Renamed to avoid conflict with pandas df
        I_squared = max(0, (Q - df_heterogeneity) / Q) if Q > 0 else 0
        
        # Confidence interval for weighted effect
        se_weighted = 1 / np.sqrt(np.sum(weights))
        ci_lower = weighted_effect - 1.96 * se_weighted
        ci_upper = weighted_effect + 1.96 * se_weighted
        
        # Count significant results
        n_significant = np.sum(p_values < self.alpha)
        
        # Count significant positive and negative trends
        n_positive_significant = np.sum((p_values < self.alpha) & (taus > 0))
        n_negative_significant = np.sum((p_values < self.alpha) & (taus < 0))

        n_positive = np.sum(taus > 0)
        n_negative = np.sum(taus < 0)
        
        self.meta_result = {
            'time_range': self.get_time_range_description(),
            'n_repositories': len(valid_results),
            'weighted_tau': weighted_tau,
            'weighted_effect_size': weighted_effect,
            'combined_p_value': combined_p,
            'i_squared': I_squared,
            'ci_lower': ci_lower,
            'ci_upper': ci_upper,
            'n_significant': n_significant,
            'n_positive_trend': n_positive, # Total positive trends (significant or not)
            'n_negative_trend': n_negative, # Total negative trends (significant or not)
            'n_positive_significant_trend': n_positive_significant, # Significant positive trends
            'n_negative_significant_trend': n_negative_significant, # Significant negative trends
            'proportion_significant': n_significant / len(valid_results),
            'individual_results': valid_results,
            'mean_percentage': np.mean([r['mean_pct'] for r in valid_results]),
            'std_percentage': np.std([r['mean_pct'] for r in valid_results])
        }
        
        return True
    
    def generate_report(self, output_file="meta_analysis_hours_report.txt"):
        """Generate comprehensive report for academic paper."""
        if self.meta_result is None:
            print("Error: No meta-analysis results to report")
            return False
            
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("META-ANALYSIS REPORT: TEMPORAL TRENDS IN COMMIT ACTIVITY BY HOUR RANGE\n")
            f.write("=" * 80 + "\n\n")
            
            f.write("METHODOLOGY SUMMARY:\n")
            f.write(f"- Repository-level analysis followed by meta-analysis\n")
            f.write(f"- Total repositories analyzed: {self.meta_result['n_repositories']}\n")
            f.write(f"- Time range analyzed: {self.meta_result['time_range']}\n")
            f.write(f"- Statistical test: Mann-Kendall trend test per repository\n")
            f.write(f"- Meta-analysis: Inverse variance weighted combination\n")
            f.write(f"- Significance level: α = {self.alpha}\n\n")
            
            f.write("RESULTS:\n")
            f.write("-" * 40 + "\n\n")
            
            # Call the detailed analysis method for the single time block result
            self._write_detailed_hour_analysis(f, self.meta_result)
            
            # Individual repository results (still useful to have)
            f.write("INDIVIDUAL REPOSITORY RESULTS:\n")
            f.write("-" * 40 + "\n")
            f.write(f"{'Repository':<30} {'Kendall τ':<12} {'P-value':<12} {'Trend':<15}\n")
            f.write("-" * 80 + "\n")
            
            for repo_result in self.meta_result['individual_results']:
                trend_desc = "Increasing" if repo_result['tau'] > 0 else "Decreasing"
                if repo_result['p_value'] >= self.alpha:
                    trend_desc = "Not significant"
                    
                f.write(f"{repo_result['repo']:<30} {repo_result['tau']:<12.4f} "
                        f"{repo_result['p_value']:<12.4f} {trend_desc:<15}\n")
            
            # Overall conclusions
            f.write(f"\nOVERALL CONCLUSIONS:\n")
            f.write("-" * 40 + "\n")
            
            if self.meta_result['combined_p_value'] < self.alpha:
                trend_direction = "increasing" if self.meta_result['weighted_tau'] > 0 else "decreasing"
                f.write(f"Significant temporal trend detected for time range {self.meta_result['time_range']}:\n")
                f.write(f"- {trend_direction.capitalize()} trend (τ = {self.meta_result['weighted_tau']:.4f}, "
                        f"p = {self.meta_result['combined_p_value']:.4f})\n")
            else:
                f.write(f"No statistically significant temporal trend detected for time range {self.meta_result['time_range']}.\n")
            
            f.write(f"\nHeterogeneity assessment suggests ")
            if self.meta_result['i_squared'] < 0.25:
                f.write("low heterogeneity between repositories.\n")
            elif self.meta_result['i_squared'] < 0.50:
                f.write("moderate heterogeneity between repositories.\n")
            else:
                f.write("high heterogeneity between repositories.\n")
            
            f.write(f"\nThis analysis addresses the hierarchical structure of the data by treating ")
            f.write(f"repositories as independent units and combining results using established ")
            f.write(f"meta-analysis techniques.\n")
        
        return True
    
    def _interpret_result(self, result):
        """Interpret meta-analysis result."""
        if result['combined_p_value'] < self.alpha:
            if result['weighted_tau'] > 0:
                return "Significant increasing trend"
            else:
                return "Significant decreasing trend"
        else:
            return "No significant trend"

    def _write_detailed_hour_analysis(self, f, result):
        """Write detailed analysis for a specific hour range and group stats."""
        f.write(f"TIME RANGE: {result['time_range']}\n")
        f.write(f"  Repositories analyzed: {result['n_repositories']}\n")
        f.write(f"  Weighted Kendall's τ: {result['weighted_tau']:.4f}\n")
        f.write(f"  Combined p-value: {result['combined_p_value']:.4f}\n")
        f.write(f"  95% CI for effect size: [{result['ci_lower']:.4f}, {result['ci_upper']:.4f}]\n")
        f.write(f"  I² (heterogeneity): {result['i_squared']:.3f}\n")
        f.write(f"  Repositories with significant trends: {result['n_significant']}/{result['n_repositories']} "
                        f"({result['proportion_significant']:.1%})\n")
        f.write(f"  Significant positive trends: {result['n_positive_significant_trend']}\n")
        f.write(f"  Significant negative trends: {result['n_negative_significant_trend']}\n")
        f.write(f"  Total positive trends (all p-values): {result['n_positive_trend']}\n")
        f.write(f"  Total negative trends (all p-values): {result['n_negative_trend']}\n")
        f.write(f"  Mean commit percentage: {result['mean_percentage']:.2f}% ± {result['std_percentage']:.2f}%\n")
        
        interpretation = self._interpret_result(result)
        f.write(f"  Interpretation: {interpretation}\n\n")

        # --- Group Statistics based on Significance ---
        if self.repo_metadata_df is not None:
            f.write("  GROUP STATISTICS BY TREND SIGNIFICANCE:\n")
            grouped_repos = {
                'significant_increase': [],
                'significant_decrease': [],
                'non_significant': []
            }

            for individual_repo_result in result['individual_results']:
                repo_cleaned_name_for_lookup = individual_repo_result['repo_cleaned_name_for_lookup']
                p_value = individual_repo_result['p_value']
                tau = individual_repo_result['tau']

                if p_value < self.alpha:
                    if tau > 0:
                        grouped_repos['significant_increase'].append(repo_cleaned_name_for_lookup)
                    else: # tau < 0
                        grouped_repos['significant_decrease'].append(repo_cleaned_name_for_lookup)
                else:
                    grouped_repos['non_significant'].append(repo_cleaned_name_for_lookup)

            for group_name, repo_cleaned_names_list in grouped_repos.items():
                if repo_cleaned_names_list:
                    # Filter metadata DataFrame for repos in the current group
                    group_df = self.repo_metadata_df[
                        self.repo_metadata_df['cleaned_repo_name_for_matching'].isin(repo_cleaned_names_list)
                    ]
                    
                    if not group_df.empty:
                        num_repos = len(group_df)
                        total_size_kb = group_df['size_kb'].sum() if 'size_kb' in group_df.columns else 0
                        total_contributors = group_df['contributors'].sum() if 'contributors' in group_df.columns else 0
                        total_commits = group_df['commits'].sum() if 'commits' in group_df.columns else 0
                        total_stars = group_df['stars'].sum() if 'stars' in group_df.columns else 0
                        unique_languages = group_df['language'].dropna().unique().tolist() if 'language' in group_df.columns else [] # Dropna to handle NaNs
                        
                        # Count specific types
                        num_volunteering = 0
                        num_corporate = 0
                        if 'type' in group_df.columns:
                            num_volunteering = (group_df['type'].astype(str).str.lower() == 'volunteering').sum()
                            num_corporate = (group_df['type'].astype(str).str.lower() == 'corporate').sum()
                        
                        f.write(f"    - {group_name.replace('_', ' ').title()} ({num_repos} Repositories):\n")
                        f.write(f"      Total Size (KB): {total_size_kb:,.0f}\n")
                        f.write(f"      Total Contributors: {total_contributors:,.0f}\n")
                        f.write(f"      Total Commits: {total_commits:,.0f}\n")
                        f.write(f"      Total Stars: {total_stars:,.0f}\n")
                        f.write(f"      Languages: {', '.join(unique_languages) if unique_languages else 'N/A'}\n")
                        f.write(f"      Types: Volunteering: {num_volunteering}, Corporate: {num_corporate}\n")
                    else:
                        f.write(f"    - {group_name.replace('_', ' ').title()} (0 Repositories - Mismatch or missing metadata for this subgroup, or metadata filtering issue)\n")
                        f.write(f"      Attempted to match: {repo_cleaned_names_list}\n")
                        f.write(f"      Available in metadata: {self.repo_metadata_df['cleaned_repo_name_for_matching'].values.tolist()}\n")

                else:
                    f.write(f"    - {group_name.replace('_', ' ').title()} (0 Repositories)\n")
            f.write("\n")
        else:
            f.write("  GROUP STATISTICS NOT AVAILABLE (Repository metadata not provided).\n\n")
    
    def save_summary_csv(self, output_file="meta_analysis_hours_summary.csv"):
        """Save summary statistics to CSV."""
        if self.meta_result is None:
            print("Error: No meta-analysis results to save")
            return False
            
        result = self.meta_result
        summary_data = [{
            'Time_Range': result['time_range'],
            'N_Repositories': result['n_repositories'],
            'Weighted_Tau': result['weighted_tau'],
            'Combined_P_Value': result['combined_p_value'],
            'I_Squared': result['i_squared'],
            'N_Significant': result['n_significant'],
            'N_Positive_Significant_Trend': result['n_positive_significant_trend'],
            'N_Negative_Significant_Trend': result['n_negative_significant_trend'],
            'Proportion_Significant': result['proportion_significant'],
            'Mean_Percentage': result['mean_percentage'],
            'Std_Percentage': result['std_percentage'],
            'Interpretation': self._interpret_result(result)
        }]
        
        df = pd.DataFrame(summary_data)
        df.to_csv(output_file, index=False)
        print(f"Summary saved to {output_file}")
        return True
    
    def create_visualization(self, output_file="meta_analysis_hours_plot.png"):
        """Create visualization of the meta-analysis results."""
        if self.meta_result is None:
            print("Error: No meta-analysis results to visualize")
            return False
            
        try:
            # Get time series data from first repository (for periods)
            if not self.repo_analyzers:
                return False
                
            periods = self.repo_analyzers[0].periods # Assuming all repos have the same periods (years)
            
            # Calculate mean time series across repositories
            all_time_series = []
            for analyzer in self.repo_analyzers:
                if analyzer.result and analyzer.result['time_series']:
                    all_time_series.append(analyzer.result['time_series'])
            
            if not all_time_series:
                print("Warning: No valid time series data to plot.")
                return False
                
            # Ensure all time series have the same length before converting to array
            min_len = min(len(ts) for ts in all_time_series)
            all_time_series_aligned = [ts[:min_len] for ts in all_time_series]
            
            if len(periods) < min_len:
                print("Warning: Periods array is shorter than aligned time series data. Adjusting periods.")
                periods_aligned = periods # Use original periods if smaller
            else:
                periods_aligned = periods[:min_len] # Align periods to the shortest time series

            mean_time_series = np.mean(all_time_series_aligned, axis=0)
            std_time_series = np.std(all_time_series_aligned, axis=0)
            
            # Create plot
            plt.figure(figsize=(12, 8))
            
            # Plot mean with error bars
            plt.errorbar(range(len(periods_aligned)), mean_time_series, yerr=std_time_series, 
                         marker='o', linestyle='-', linewidth=2, markersize=8, capsize=5)
            
            # Add trend line if significant
            if self.meta_result['combined_p_value'] is not None and self.meta_result['combined_p_value'] < self.alpha:
                z = np.polyfit(range(len(periods_aligned)), mean_time_series, 1)
                p = np.poly1d(z)
                plt.plot(range(len(periods_aligned)), p(range(len(periods_aligned))), 
                         'r--', linewidth=2, alpha=0.8, label='Trend Line')
                plt.legend()
            
            plt.xlabel('Year', fontsize=14)
            plt.ylabel('Commits (%)', fontsize=14)
            plt.title(f'Temporal Trend Analysis: {self.meta_result["time_range"]}\n'
                      f'Meta-analysis across {self.meta_result["n_repositories"]} repositories', 
                      fontsize=16)
            plt.grid(True, alpha=0.3)
            
            # Set x-axis labels
            step = max(1, len(periods_aligned) // 10)  # Show at most 10 labels
            plt.xticks(range(0, len(periods_aligned), step), 
                       [periods_aligned[i] for i in range(0, len(periods_aligned), step)], 
                       rotation=45)
            
            plt.tight_layout()
            plt.savefig(output_file, dpi=300, bbox_inches='tight')
            plt.close()
            
            print(f"Visualization saved to {output_file}")
            return True
            
        except Exception as e:
            print(f"Error creating visualization: {e}")
            return False

def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Meta-analysis of Mann-Kendall trend tests for hourly commit data across multiple repositories"
    )
    parser.add_argument("directory", help="Directory containing CSV files (one per repository)")
    parser.add_argument("time_block_start", type=int, help="Starting hour block (0-23)")
    parser.add_argument("time_block_end", type=int, help="Ending hour block (0-23, inclusive)")
    parser.add_argument("repo_list_txt", help="Path to a text file containing one repository 'owner/name' per line.")
    parser.add_argument("repo_metadata_csv", help="Path to the CSV file with repository metadata (e.g., size_kb, contributors)")
    parser.add_argument("--output_dir", default=".", help="Output directory for results")
    parser.add_argument("--alpha", type=float, default=0.05, help="Significance level")
    parser.add_argument("--plot", action="store_true", help="Generate visualization plot")
    return parser.parse_args()

def main():
    """Main execution function."""
    args = parse_arguments()
    
    # Validate input directory
    if not os.path.isdir(args.directory):
        print(f"Error: {args.directory} is not a valid directory")
        sys.exit(1)
    
    # Validate time blocks
    if not (0 <= args.time_block_start <= 23) or not (0 <= args.time_block_end <= 23):
        print("Error: Time blocks must be between 0 and 23")
        sys.exit(1)

    # Validate repo list TXT
    if not Path(args.repo_list_txt).is_file():
        print(f"Error: Repository list TXT not found at {args.repo_list_txt}")
        sys.exit(1)

    # Validate metadata CSV
    if not Path(args.repo_metadata_csv).is_file():
        print(f"Error: Repository metadata CSV not found at {args.repo_metadata_csv}")
        sys.exit(1)
    
    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    # 1. Load repository metadata and clean names consistently for matching
    repo_metadata_df = pd.read_csv(args.repo_metadata_csv)
    # Apply cleaning to the 'repository' column from metadata to match cleaned filenames
    repo_metadata_df['cleaned_repo_name_for_matching'] = repo_metadata_df['repository'].apply(clean_repo_name_for_filename_and_lookup)
    
    # 2. Read repository names from the TXT file
    repos_to_analyze = []
    try:
        with open(args.repo_list_txt, 'r', encoding='utf-8') as f:
            for line in f:
                repo_identifier = line.strip()
                if repo_identifier and not repo_identifier.startswith('#'): # Ignore empty lines and comments
                    repos_to_analyze.append(repo_identifier)
        if not repos_to_analyze:
            print(f"Error: No repository names found in {args.repo_list_txt}")
            sys.exit(1)
    except Exception as e:
        print(f"Error reading repository list from {args.repo_list_txt}: {e}")
        sys.exit(1)

    print(f"Found {len(repos_to_analyze)} repositories in {args.repo_list_txt}.")

    # Initialize meta-analyzer, passing the metadata DataFrame
    meta_analyzer = MetaAnalyzer(args.time_block_start, args.time_block_end, alpha=args.alpha, repo_metadata_df=repo_metadata_df)
    
    successful_loads = 0
    # Process only the CSV files that correspond to the repositories in the list
    for repo_full_name in repos_to_analyze:
        # Construct the expected filename for the CSV
        # Assuming the CSV filenames are like "ownername_CommitPercentagesPerHour.csv"
        # from "owner/name" in repo_list.txt
        cleaned_repo_name_for_filename = clean_repo_name_for_filename_and_lookup(repo_full_name)
        
        # --- IMPORTANT CHANGE HERE ---
        csv_filename_pattern = f"{cleaned_repo_name_for_filename}_CommitPercentagesPerHour.csv" 
        
        # Look for the exact file in the directory
        csv_file_path = Path(args.directory) / csv_filename_pattern
        
        if csv_file_path.is_file():
            # Get the cleaned name from the file's stem (e.g., "ownername_CommitPercentagesPerHour" -> "ownername")
            cleaned_name_from_file_stem = clean_repo_name_for_filename_and_lookup(csv_file_path.stem)
            print(f"DEBUG: Cleaned name from CSV filename '{csv_file_path.name}': '{cleaned_name_from_file_stem}'")

            # Check if this repository exists in the metadata using the consistently cleaned name
            if cleaned_name_from_file_stem in repo_metadata_df['cleaned_repo_name_for_matching'].values:
                print(f"DEBUG: Found metadata for '{cleaned_name_from_file_stem}'. Attempting to add repository.")
                if meta_analyzer.add_repository(csv_file_path):
                    successful_loads += 1
                else:
                    print(f"Failed to process commit data for: {csv_file_path.name} (Mann-Kendall error or insufficient data points)")
            else:
                print(f"Skipping {csv_file_path.name}: No metadata found in {args.repo_metadata_csv} "
                      f"for cleaned name '{cleaned_name_from_file_stem}'.")
                print(f"DEBUG: Available cleaned metadata names: {repo_metadata_df['cleaned_repo_name_for_matching'].values.tolist()}")
        else:
            print(f"Skipping {repo_full_name}: Corresponding CSV file '{csv_filename_pattern}' not found in {args.directory}.")
    
    print(f"Successfully loaded {successful_loads} repositories with available commit data and metadata.")
    
    if successful_loads < 2:
        print("Error: Need at least 2 repositories with both commit data and metadata for meta-analysis.")
        sys.exit(1)
    
    # Perform meta-analysis
    if meta_analyzer.perform_meta_analysis():
        # Generate outputs
        time_range_safe = meta_analyzer.get_time_range_description().replace(":", "_").replace("-", "_").replace(" ", "_")
        report_file = os.path.join(args.output_dir, f"meta_analysis_hours_{time_range_safe}_report.txt")
        csv_file = os.path.join(args.output_dir, f"meta_analysis_hours_{time_range_safe}_summary.csv")
        
        meta_analyzer.generate_report(report_file)
        meta_analyzer.save_summary_csv(csv_file)
        
        if args.plot:
            plot_file = os.path.join(args.output_dir, f"meta_analysis_hours_{time_range_safe}_plot.png")
            meta_analyzer.create_visualization(plot_file)
        
        print(f"\nAnalysis complete!")
        print(f"Report saved to: {report_file}")
        print(f"Summary saved to: {csv_file}")
        
        # Print quick summary to console
        result = meta_analyzer.meta_result
        print(f"\nQUICK SUMMARY:")
        print(f"Time range: {result['time_range']}")
        print(f"Repositories analyzed: {result['n_repositories']}")
        print(f"Weighted Kendall's τ: {result['weighted_tau']:.4f}")
        print(f"Combined p-value: {result['combined_p_value']:.4f}")
        
        if result['combined_p_value'] is not None and result['combined_p_value'] < args.alpha:
            trend = "increasing" if result['weighted_tau'] > 0 else "decreasing"
            print(f"Result: Significant {trend} trend detected")
        else:
            print("Result: No significant temporal trend detected")
            
    else:
        print("Error: Meta-analysis failed")
        sys.exit(1)

if __name__ == "__main__":
    main()