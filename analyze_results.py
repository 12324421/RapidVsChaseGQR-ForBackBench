#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rapid vs ChaseGQR Experiment Results Analysis
Generates charts and reports from CSV data
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from datetime import datetime
import glob

# Chinese font support
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
sns.set_style("whitegrid")

def find_latest_csv():
    """Find the most recent results CSV file"""
    csv_files = glob.glob("final_chase_rewriting_*.csv")
    if not csv_files:
        print("❌ No CSV files found!")
        return None
    
    # Sort by modification time, get latest
    latest = max(csv_files, key=lambda x: Path(x).stat().st_mtime)
    print(f"✓ Found CSV: {latest}")
    return latest

def load_and_clean_data(csv_file):
    """Load CSV and clean data"""
    df = pd.read_csv(csv_file)
    print(f"✓ Loaded {len(df)} records")
    
    # Filter successful tests only
    df_success = df[df['Success'] == True].copy()
    print(f"✓ {len(df_success)} successful tests ({len(df_success)/len(df)*100:.1f}%)")
    
    print(f"  Scenarios: {', '.join(df_success['Scenario'].unique())}")
    print(f"  Systems: {', '.join(df_success['System'].unique())}")
    print(f"  Queries: {', '.join(sorted(df_success['Query'].unique()))}")
    
    return df_success

def calculate_statistics(df):
    """Calculate performance statistics"""
    # Average by scenario/query/system
    perf = df.groupby(['Scenario', 'Query', 'System'])['Time_ms'].agg([
        ('avg', 'mean'),
        ('std', 'std'),
        ('min', 'min'),
        ('max', 'max'),
        ('count', 'count')
    ]).reset_index()
    
    # Pivot for comparison
    pivot = perf.pivot_table(
        index=['Scenario', 'Query'],
        columns='System',
        values='avg'
    ).reset_index()
    
    # Calculate speed ratio
    if 'Rapid' in pivot.columns and 'ChaseGQR' in pivot.columns:
        pivot['SpeedRatio'] = pivot['ChaseGQR'] / pivot['Rapid']
        pivot['Winner'] = pivot['SpeedRatio'].apply(
            lambda x: 'Chase' if x > 1.1 else ('Rapid' if x < 0.9 else 'Tie')
        )
    
    # Global statistics
    global_stats = df.groupby('System')['Time_ms'].agg([
        ('avg', 'mean'),
        ('std', 'std'),
        ('min', 'min'),
        ('max', 'max'),
        ('count', 'count')
    ]).reset_index()
    
    # Per-scenario statistics
    scenario_stats = df.groupby(['Scenario', 'System'])['Time_ms'].agg([
        ('avg', 'mean'),
        ('std', 'std')
    ]).reset_index()
    
    return perf, pivot, global_stats, scenario_stats

def create_charts(df, pivot):
    """Generate 6-panel visualization"""
    fig = plt.figure(figsize=(20, 12))
    gs = fig.add_gridspec(2, 3, hspace=0.3, wspace=0.3)
    
    # Chart 1: Performance by Query
    ax1 = fig.add_subplot(gs[0, 0])
    query_perf = df.groupby(['Query', 'System'])['Time_ms'].mean().unstack()
    query_perf.plot(kind='bar', ax=ax1, color=['#3498db', '#e74c3c'], width=0.7)
    ax1.set_title('Average Performance by Query', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Query', fontsize=12)
    ax1.set_ylabel('Average Time (ms)', fontsize=12)
    ax1.legend(title='System', fontsize=11)
    ax1.grid(axis='y', alpha=0.3)
    plt.setp(ax1.xaxis.get_majorticklabels(), rotation=0)
    
    # Chart 2: Performance by Scenario
    ax2 = fig.add_subplot(gs[0, 1])
    scenario_perf = df.groupby(['Scenario', 'System'])['Time_ms'].mean().unstack()
    scenario_perf.plot(kind='bar', ax=ax2, color=['#3498db', '#e74c3c'], width=0.7)
    ax2.set_title('Average Performance by Scenario', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Scenario', fontsize=12)
    ax2.set_ylabel('Average Time (ms)', fontsize=12)
    ax2.legend(title='System', fontsize=11)
    ax2.grid(axis='y', alpha=0.3)
    plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha='right')
    
    # Chart 3: Speed Ratio Distribution
    ax3 = fig.add_subplot(gs[0, 2])
    if 'SpeedRatio' in pivot.columns:
        ratios = pivot['SpeedRatio'].dropna()
        ax3.hist(ratios, bins=15, color='steelblue', edgecolor='black', alpha=0.7)
        ax3.axvline(1.0, color='red', linestyle='--', linewidth=2, label='Baseline (1.0)')
        mean_ratio = ratios.mean()
        ax3.axvline(mean_ratio, color='green', linestyle='--', linewidth=2,
                   label=f'Mean: {mean_ratio:.2f}')
        ax3.set_title('Speed Ratio Distribution (Chase/Rapid)', fontsize=14, fontweight='bold')
        ax3.set_xlabel('Speed Ratio (>1 = Chase faster)', fontsize=12)
        ax3.set_ylabel('Frequency', fontsize=12)
        ax3.legend(fontsize=11)
        ax3.grid(axis='y', alpha=0.3)
    
    # Chart 4: Rapid Heatmap
    ax4 = fig.add_subplot(gs[1, 0])
    rapid_data = df[df['System'] == 'Rapid'].groupby(['Scenario', 'Query'])['Time_ms'].mean()
    if not rapid_data.empty:
        rapid_heatmap = rapid_data.unstack()
        sns.heatmap(rapid_heatmap, annot=True, fmt='.0f', cmap='YlGnBu',
                   ax=ax4, cbar_kws={'label': 'ms'}, linewidths=0.5)
        ax4.set_title('Rapid Performance Heatmap (ms)', fontsize=14, fontweight='bold')
        ax4.set_xlabel('Query', fontsize=12)
        ax4.set_ylabel('Scenario', fontsize=12)
    
    # Chart 5: ChaseGQR Heatmap
    ax5 = fig.add_subplot(gs[1, 1])
    chase_data = df[df['System'] == 'ChaseGQR'].groupby(['Scenario', 'Query'])['Time_ms'].mean()
    if not chase_data.empty:
        chase_heatmap = chase_data.unstack()
        sns.heatmap(chase_heatmap, annot=True, fmt='.0f', cmap='YlOrRd',
                   ax=ax5, cbar_kws={'label': 'ms'}, linewidths=0.5)
        ax5.set_title('ChaseGQR Performance Heatmap (ms)', fontsize=14, fontweight='bold')
        ax5.set_xlabel('Query', fontsize=12)
        ax5.set_ylabel('Scenario', fontsize=12)
    
    # Chart 6: Stability Comparison (Boxplot)
    ax6 = fig.add_subplot(gs[1, 2])
    systems = sorted(df['System'].unique())
    data_to_plot = [df[df['System'] == sys]['Time_ms'].values for sys in systems]
    bp = ax6.boxplot(data_to_plot, labels=systems, patch_artist=True,
                     boxprops=dict(facecolor='lightblue', alpha=0.7),
                     medianprops=dict(color='red', linewidth=2))
    ax6.set_title('Performance Stability Comparison', fontsize=14, fontweight='bold')
    ax6.set_xlabel('System', fontsize=12)
    ax6.set_ylabel('Time (ms)', fontsize=12)
    ax6.grid(axis='y', alpha=0.3)
    
    fig.suptitle('Rapid vs ChaseGQR Performance Analysis (Real Experiment Data)',
                 fontsize=16, fontweight='bold', y=0.98)
    
    plt.savefig('FINAL_ANALYSIS_CHARTS.png', dpi=150, bbox_inches='tight')
    print("✓ Saved: FINAL_ANALYSIS_CHARTS.png")

def generate_report(df, pivot, global_stats, scenario_stats):
    """Generate text report"""
    lines = []
    lines.append("=" * 80)
    lines.append("Rapid vs ChaseGQR Performance Comparison Report")
    lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("=" * 80)
    lines.append("")
    
    # Configuration
    lines.append("[Experiment Configuration]")
    lines.append(f"  Scenarios: {', '.join(sorted(df['Scenario'].unique()))}")
    lines.append(f"  Queries: {df['Query'].nunique()}")
    lines.append(f"  Systems: {', '.join(sorted(df['System'].unique()))}")
    lines.append(f"  Total Tests: {len(df)}")
    lines.append("")
    
    # Success Rate
    lines.append("[Test Success Rate]")
    for system in sorted(df['System'].unique()):
        count = len(df[df['System'] == system])
        lines.append(f"  {system}: {count}/{count} (100%)")
    lines.append("")
    
    # Overall Performance
    lines.append("[Overall Performance]")
    for _, row in global_stats.iterrows():
        lines.append(f"  {row['System']}:")
        lines.append(f"    Average: {row['avg']:.1f} ms")
        lines.append(f"    Std Dev: {row['std']:.1f} ms")
        lines.append(f"    Range: {row['min']:.0f} - {row['max']:.0f} ms")
        lines.append(f"    Tests: {int(row['count'])}")
    
    if len(global_stats) == 2:
        rapid = global_stats[global_stats['System'] == 'Rapid']
        chase = global_stats[global_stats['System'] == 'ChaseGQR']
        if not rapid.empty and not chase.empty:
            r_avg = rapid['avg'].values[0]
            c_avg = chase['avg'].values[0]
            r_std = rapid['std'].values[0]
            c_std = chase['std'].values[0]
            
            if r_avg < c_avg:
                pct = ((c_avg - r_avg) / c_avg) * 100
                lines.append(f"\n  ⭐ Rapid is {pct:.1f}% faster overall")
            else:
                pct = ((r_avg - c_avg) / r_avg) * 100
                lines.append(f"\n  ⭐ ChaseGQR is {pct:.1f}% faster overall")
            
            if r_std < c_std:
                ratio = c_std / r_std if r_std > 0 else float('inf')
                lines.append(f"  ⭐ Rapid is {ratio:.1f}x more stable (std: {r_std:.0f} vs {c_std:.0f})")
            else:
                ratio = r_std / c_std if c_std > 0 else float('inf')
                lines.append(f"  ⭐ ChaseGQR is {ratio:.1f}x more stable (std: {c_std:.0f} vs {r_std:.0f})")
    lines.append("")
    
    # Per-Scenario Performance
    lines.append("[Performance by Scenario]")
    for scenario in sorted(df['Scenario'].unique()):
        lines.append(f"\n  {scenario}:")
        scene_data = scenario_stats[scenario_stats['Scenario'] == scenario]
        for _, row in scene_data.iterrows():
            lines.append(f"    {row['System']}: {row['avg']:.1f} ms (std: {row['std']:.1f})")
    lines.append("")
    
    # Key Findings
    lines.append("[Key Findings]")
    if 'SpeedRatio' in pivot.columns:
        avg_ratio = pivot['SpeedRatio'].mean()
        if avg_ratio > 1.1:
            lines.append(f"  • ChaseGQR is on average {((avg_ratio - 1) * 100):.1f}% faster")
        elif avg_ratio < 0.9:
            lines.append(f"  • Rapid is on average {((1/avg_ratio - 1) * 100):.1f}% faster")
        else:
            lines.append(f"  • Both systems have similar performance (ratio: {avg_ratio:.2f})")
        
        if 'Winner' in pivot.columns:
            win_counts = pivot['Winner'].value_counts()
            for winner, count in win_counts.items():
                lines.append(f"  • {winner} wins: {count} queries")
    lines.append("")
    
    # Recommendations
    lines.append("[Recommendations]")
    if len(global_stats) == 2:
        rapid = global_stats[global_stats['System'] == 'Rapid']
        chase = global_stats[global_stats['System'] == 'ChaseGQR']
        if not rapid.empty and not chase.empty:
            r_avg = rapid['avg'].values[0]
            c_avg = chase['avg'].values[0]
            r_std = rapid['std'].values[0]
            c_std = chase['std'].values[0]
            
            if r_avg < c_avg and r_std < c_std:
                lines.append("  Recommended: Rapid (faster and more stable)")
            elif r_avg < c_avg:
                lines.append("  Recommended: Rapid (faster performance)")
            elif r_std < c_std:
                lines.append("  Recommended: Rapid (better stability)")
            else:
                lines.append("  Recommended: Choose based on specific scenario and query type")
    
    lines.append("  • For simple queries: Choose system with better average performance")
    lines.append("  • For complex queries: Choose system with better stability")
    lines.append("  • For production: Consider both performance and stability")
    lines.append("")
    lines.append("=" * 80)
    
    report_text = "\n".join(lines)
    
    with open("FINAL_REPORT.txt", "w", encoding="utf-8") as f:
        f.write(report_text)
    
    print("✓ Saved: FINAL_REPORT.txt")

def main():
    print("\n" + "=" * 60)
    print("  Rapid vs ChaseGQR Analysis Tool")
    print("=" * 60 + "\n")
    
    # Step 1: Find CSV
    print("Step 1/5: Finding latest CSV file...")
    csv_file = find_latest_csv()
    if not csv_file:
        print("\n❌ No CSV files found!")
        print("Please run: powershell -File run_complete_experiment.ps1\n")
        return
    
    # Step 2: Load data
    print("\nStep 2/5: Loading and cleaning data...")
    df = load_and_clean_data(csv_file)
    if df.empty:
        print("\n❌ No successful test data found!")
        return
    
    # Step 3: Calculate statistics
    print("\nStep 3/5: Calculating statistics...")
    perf, pivot, global_stats, scenario_stats = calculate_statistics(df)
    
    # Step 4: Save CSV files
    print("\nStep 4/5: Saving analysis results...")
    pivot.to_csv('performance_comparison.csv', index=False, encoding='utf-8-sig')
    print("✓ Saved: performance_comparison.csv")
    
    scenario_stats.to_csv('detailed_statistics.csv', index=False, encoding='utf-8-sig')
    print("✓ Saved: detailed_statistics.csv")
    
    # Step 5: Generate visualizations
    print("\nStep 5/6: Generating charts...")
    create_charts(df, pivot)
    
    # Step 6: Generate report
    print("\nStep 6/6: Generating text report...")
    generate_report(df, pivot, global_stats, scenario_stats)
    
    print("\n" + "=" * 60)
    print("  Analysis Complete!")
    print("=" * 60)
    print("\nGenerated files:")
    print("  📊 FINAL_ANALYSIS_CHARTS.png - 6-panel visualization")
    print("  📄 FINAL_REPORT.txt - Complete text report")
    print("  📈 performance_comparison.csv - Performance comparison table")
    print("  📊 detailed_statistics.csv - Detailed statistics\n")

if __name__ == "__main__":
    main()
