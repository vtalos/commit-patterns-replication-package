"""
Meta-Analysis Script for Mann-Kendall Trend Tests on Multi-Repository Commit Data

This script addresses the hierarchical nature of commit data by:
1. Performing Mann-Kendall tests separately for each repository
2. Aggregating results using meta-analysis techniques
3. Providing overall trend assessments with proper statistical inference

The script reads multiple CSV files (one per repository) containing commit data
across days of the week over multiple years, performs individual Mann-Kendall tests,
and then combines the results to provide overall trend conclusions.

Usage:
    python multi_repo_mann_kendall_days.py <directory_path> [--output_dir <output_directory>] [--alpha <significance_level>]

Arguments:
    directory_path: Directory containing CSV files (one per repository)
    --output_dir: Directory to save output files (default: current directory)
    --alpha: Significance level for tests (default: 0.05)
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

import os
if os.name == 'nt':
    sys.stdout.reconfigure(encoding='utf-8')

# Day names for reporting
DAY_NAMES = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

class RepositoryAnalyzer:
    """Handles analysis for individual repositories."""
    
    def __init__(self, filepath):
        self.filepath = filepath
        self.repo_name = Path(filepath).stem
        self.data = None
        self.periods = None
        self.results = {}
        
    def load_data(self):
        """Load and parse CSV data for the repository."""
        try:
            df = pd.read_csv(self.filepath, index_col=0)
            self.periods = df.columns.tolist()
            self.data = df.values  # 7 days x n_years
            return True
        except Exception as e:
            print(f"Error loading {self.filepath}: {e}")
            return False
    
    def analyze_day(self, day_idx):
        """Perform Mann-Kendall test for a specific day."""
        day_data = self.data[day_idx, :]
        
        # Handle missing or invalid data
        valid_data = day_data[~np.isnan(day_data)]
        if len(valid_data) < 3:
            return None
            
        try:
            result = mk.original_test(valid_data)
            return {
                'trend': result[0],
                'p_value': result[2],
                'tau': result[4],
                'slope': result[7] if len(result) > 7 else None,
                'data_points': len(valid_data),
                'mean_percentage': np.mean(valid_data),
                'std_percentage': np.std(valid_data)
            }
        except Exception as e:
            print(f"Error analyzing {self.repo_name}, day {day_idx}: {e}")
            return None
    
    def analyze_all_days(self):
        """Perform analysis for all days of the week."""
        if self.data is None:
            if not self.load_data():
                return False
                
        for day_idx in range(7):
            self.results[day_idx] = self.analyze_day(day_idx)
            
        return True

class MetaAnalyzer:
    """Handles meta-analysis across repositories."""
    
    def __init__(self, alpha=0.05):
        self.alpha = alpha
        self.repo_analyzers = []
        self.meta_results = {}
        
    def add_repository(self, filepath):
        """Add a repository for analysis."""
        analyzer = RepositoryAnalyzer(filepath)
        if analyzer.analyze_all_days():
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
    
    def meta_analyze_day(self, day_idx):
        """Perform meta-analysis for a specific day across all repositories."""
        valid_results = []
        
        for analyzer in self.repo_analyzers:
            result = analyzer.results.get(day_idx)
            if result is not None and result['p_value'] is not None:
                valid_results.append({
                    'repo': analyzer.repo_name,
                    'tau': result['tau'],
                    'p_value': result['p_value'],
                    'n': result['data_points'],
                    'effect_size': self.calculate_effect_size(result['tau']),
                    'trend': result['trend'],
                    'mean_pct': result['mean_percentage'],
                    'std_pct': result['std_percentage']
                })
        
        if len(valid_results) < 2:
            return None
            
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
            chi2_stat = -2 * np.sum(np.log(p_values))
            combined_p = 1 - stats.chi2.cdf(chi2_stat, 2 * len(p_values))
        except:
            combined_p = np.nan
            
        # Heterogeneity assessment (I²)
        mean_effect = np.mean(effect_sizes)
        Q = np.sum(weights * (effect_sizes - mean_effect)**2)
        df = len(effect_sizes) - 1
        I_squared = max(0, (Q - df) / Q) if Q > 0 else 0
        
        # Confidence interval for weighted effect
        se_weighted = 1 / np.sqrt(np.sum(weights))
        ci_lower = weighted_effect - 1.96 * se_weighted
        ci_upper = weighted_effect + 1.96 * se_weighted
        
        # Count significant results
        n_significant = np.sum(p_values < self.alpha)
        n_positive = np.sum(taus > 0)
        n_negative = np.sum(taus < 0)
        
        return {
            'day': DAY_NAMES[day_idx],
            'n_repositories': len(valid_results),
            'weighted_tau': weighted_tau,
            'weighted_effect_size': weighted_effect,
            'combined_p_value': combined_p,
            'i_squared': I_squared,
            'ci_lower': ci_lower,
            'ci_upper': ci_upper,
            'n_significant': n_significant,
            'n_positive_trend': n_positive,
            'n_negative_trend': n_negative,
            'proportion_significant': n_significant / len(valid_results),
            'individual_results': valid_results,
            'mean_percentage': np.mean([r['mean_pct'] for r in valid_results]),
            'std_percentage': np.std([r['mean_pct'] for r in valid_results])
        }
    
    def perform_meta_analysis(self):
        """Perform meta-analysis for all days."""
        print(f"Performing meta-analysis on {len(self.repo_analyzers)} repositories...")
        
        for day_idx in range(7):
            result = self.meta_analyze_day(day_idx)
            if result:
                self.meta_results[day_idx] = result
                
        return len(self.meta_results) > 0
    
    def generate_report(self, output_file="meta_analysis_report.txt"):
        """Generate comprehensive report for academic paper."""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("META-ANALYSIS REPORT: TEMPORAL TRENDS IN COMMIT ACTIVITY BY DAY OF WEEK\n")
            f.write("=" * 80 + "\n\n")
            
            f.write("METHODOLOGY SUMMARY:\n")
            f.write(f"- Repository-level analysis followed by meta-analysis\n")
            f.write(f"- Total repositories analyzed: {len(self.repo_analyzers)}\n")
            f.write(f"- Statistical test: Mann-Kendall trend test per repository\n")
            f.write(f"- Meta-analysis: Inverse variance weighted combination\n")
            f.write(f"- Significance level: α = {self.alpha}\n\n")
            
            f.write("RESULTS BY DAY OF WEEK:\n")
            f.write("-" * 40 + "\n\n")
            
            # Summary table
            f.write("SUMMARY TABLE:\n")
            f.write(f"{'Day':<12} {'N_Repos':<8} {'Weighted_τ':<12} {'Combined_p':<12} {'I²':<8} {'Interpretation':<20}\n")
            f.write("-" * 80 + "\n")
            
            significant_days = []
            
            for day_idx in range(7):
                if day_idx in self.meta_results:
                    result = self.meta_results[day_idx]
                    interpretation = self._interpret_result(result)
                    
                    f.write(f"{result['day']:<12} {result['n_repositories']:<8} "
                           f"{result['weighted_tau']:<12.4f} {result['combined_p_value']:<12.4f} "
                           f"{result['i_squared']:<8.3f} {interpretation:<20}\n")
                    
                    if result['combined_p_value'] < self.alpha:
                        significant_days.append((result['day'], result))
            
            f.write("\n" + "DETAILED RESULTS:\n")
            f.write("-" * 40 + "\n\n")
            
            for day_idx in range(7):
                if day_idx in self.meta_results:
                    result = self.meta_results[day_idx]
                    self._write_detailed_day_analysis(f, result)
            
            # Overall conclusions
            f.write("\nOVERALL CONCLUSIONS:\n")
            f.write("-" * 40 + "\n")
            
            if significant_days:
                f.write(f"Significant temporal trends detected for {len(significant_days)} day(s):\n")
                for day_name, result in significant_days:
                    trend_direction = "increasing" if result['weighted_tau'] > 0 else "decreasing"
                    f.write(f"- {day_name}: {trend_direction} trend (τ = {result['weighted_tau']:.4f}, "
                           f"p = {result['combined_p_value']:.4f})\n")
            else:
                f.write("No statistically significant temporal trends detected across days of the week.\n")
            
            f.write(f"\nHeterogeneity assessment suggests ")
            avg_i_squared = np.mean([r['i_squared'] for r in self.meta_results.values()])
            if avg_i_squared < 0.25:
                f.write("low heterogeneity between repositories.\n")
            elif avg_i_squared < 0.50:
                f.write("moderate heterogeneity between repositories.\n")
            else:
                f.write("high heterogeneity between repositories.\n")
            
            f.write(f"\nThis analysis addresses the hierarchical structure of the data by treating ")
            f.write(f"repositories as independent units and combining results using established ")
            f.write(f"meta-analysis techniques.\n")
    
    def _interpret_result(self, result):
        """Interpret meta-analysis result."""
        if result['combined_p_value'] < self.alpha:
            if result['weighted_tau'] > 0:
                return "Increasing trend"
            else:
                return "Decreasing trend"
        else:
            return "No significant trend"
    
    def _write_detailed_day_analysis(self, f, result):
        """Write detailed analysis for a specific day."""
        f.write(f"{result['day'].upper()}:\n")
        f.write(f"  Repositories analyzed: {result['n_repositories']}\n")
        f.write(f"  Weighted Kendall's τ: {result['weighted_tau']:.4f}\n")
        f.write(f"  Combined p-value: {result['combined_p_value']:.4f}\n")
        f.write(f"  95% CI for effect size: [{result['ci_lower']:.4f}, {result['ci_upper']:.4f}]\n")
        f.write(f"  I² (heterogeneity): {result['i_squared']:.3f}\n")
        f.write(f"  Repositories with significant trends: {result['n_significant']}/{result['n_repositories']} "
               f"({result['proportion_significant']:.1%})\n")
        f.write(f"  Positive trends: {result['n_positive_trend']}, "
               f"Negative trends: {result['n_negative_trend']}\n")
        f.write(f"  Mean commit percentage: {result['mean_percentage']:.2f}% ± {result['std_percentage']:.2f}%\n")
        
        interpretation = self._interpret_result(result)
        f.write(f"  Interpretation: {interpretation}\n\n")
    
    def save_summary_csv(self, output_file="meta_analysis_summary.csv"):
        """Save summary statistics to CSV."""
        summary_data = []
        
        for day_idx in range(7):
            if day_idx in self.meta_results:
                result = self.meta_results[day_idx]
                summary_data.append({
                    'Day': result['day'],
                    'N_Repositories': result['n_repositories'],
                    'Weighted_Tau': result['weighted_tau'],
                    'Combined_P_Value': result['combined_p_value'],
                    'I_Squared': result['i_squared'],
                    'N_Significant': result['n_significant'],
                    'Proportion_Significant': result['proportion_significant'],
                    'Mean_Percentage': result['mean_percentage'],
                    'Std_Percentage': result['std_percentage'],
                    'Interpretation': self._interpret_result(result)
                })
        
        df = pd.DataFrame(summary_data)
        df.to_csv(output_file, index=False)
        print(f"Summary saved to {output_file}")

def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Meta-analysis of Mann-Kendall trend tests across multiple repositories"
    )
    parser.add_argument("directory", help="Directory containing CSV files (one per repository)")
    parser.add_argument("--output_dir", default=".", help="Output directory for results")
    parser.add_argument("--alpha", type=float, default=0.05, help="Significance level")
    return parser.parse_args()

def main():
    """Main execution function."""
    args = parse_arguments()
    
    # Validate input directory
    if not os.path.isdir(args.directory):
        print(f"Error: {args.directory} is not a valid directory")
        sys.exit(1)
    
    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Initialize meta-analyzer
    meta_analyzer = MetaAnalyzer(alpha=args.alpha)
    
    # Process all CSV files in directory
    csv_files = list(Path(args.directory).glob("*.csv"))
    
    if not csv_files:
        print(f"No CSV files found in {args.directory}")
        sys.exit(1)
    
    print(f"Found {len(csv_files)} CSV files")
    
    successful_loads = 0
    for csv_file in csv_files:
        if meta_analyzer.add_repository(csv_file):
            successful_loads += 1
        else:
            print(f"Failed to process: {csv_file}")
    
    print(f"Successfully loaded {successful_loads} repositories")
    
    if successful_loads < 2:
        print("Error: Need at least 2 repositories for meta-analysis")
        sys.exit(1)
    
    # Perform meta-analysis
    if meta_analyzer.perform_meta_analysis():
        # Generate outputs
        report_file = os.path.join(args.output_dir, "meta_analysis_report.txt")
        csv_file = os.path.join(args.output_dir, "meta_analysis_summary.csv")
        
        meta_analyzer.generate_report(report_file)
        meta_analyzer.save_summary_csv(csv_file)
        
        print(f"\nAnalysis complete!")
        print(f"Report saved to: {report_file}")
        print(f"Summary saved to: {csv_file}")
        
        # Print quick summary to console
        print(f"\nQUICK SUMMARY:")
        print(f"Repositories analyzed: {len(meta_analyzer.repo_analyzers)}")
        
        significant_results = []
        for day_idx, result in meta_analyzer.meta_results.items():
            if result['combined_p_value'] < args.alpha:
                trend = "↑" if result['weighted_tau'] > 0 else "↓"
                significant_results.append(f"{result['day']} {trend}")
        
        if significant_results:
            print(f"Significant trends: {', '.join(significant_results)}")
        else:
            print("No significant temporal trends detected")
            
    else:
        print("Error: Meta-analysis failed")
        sys.exit(1)

if __name__ == "__main__":
    main()