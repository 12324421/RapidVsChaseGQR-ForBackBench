# Rapid vs ChaseGQR Performance Comparison

## Overview

This repository contains a comprehensive benchmark comparing **Rapid (Query Rewriting)** and **ChaseGQR (Chase-based)** systems across multiple scenarios. The benchmark evaluates performance, stability, and query execution time using real-world ontology-based data access (OBDA) scenarios.

**Key Features:**
- 3 test scenarios: Deep100, StockExchange, University
- 15 queries across different complexity levels
- Automated experiment execution with PowerShell scripts
- Comprehensive analysis with visualization and statistical reports
- 100% reproducible results

## Table of Contents
- [Project Structure](#project-structure)
- [Dependencies](#dependencies)
- [Installation](#installation)
- [Running Experiments](#running-experiments)
- [Results and Analysis](#results-and-analysis)
- [Experiment Configuration](#experiment-configuration)
- [Troubleshooting](#troubleshooting)

## Project Structure

```
ForBackBench/
├── scenarios/              # Test scenarios with queries and data
│   ├── Deep100/           # One-to-One mapping scenario
│   ├── StockExchange/     # GAV mapping scenario
│   └── University/        # LAV mapping scenario
├── systems/               # System JAR files
│   ├── rapid/            # Rapid (Query Rewriting)
│   │   └── Rapid2.jar
│   └── ChaseGQR/         # ChaseGQR (Chase-based)
│       └── ChaseGQR.jar
├── scripts/              # Bash scripts for individual mappings
│   ├── runTrivialMapping.sh
│   ├── runGAVMapping.sh
│   └── runLAVMapping.sh
├── experiments/          # Generated results (created after running)
│   ├── scenarios/       # CSV results by scenario
│   └── outputs/         # System outputs
├── run_complete_experiment.ps1  # Main experiment script
├── analyze_results.py           # Analysis and visualization
│
├── FINAL_ANALYSIS_CHARTS.png    # 📊 6-panel visualization (generated)
├── FINAL_REPORT.txt             # 📄 Complete statistical report (generated)
├── performance_comparison.csv   # 📈 15-row query comparison table (generated)
├── detailed_statistics.csv      # 📊 Statistical summary (generated)
└── final_chase_rewriting_<timestamp>.csv  # 📋 90-row raw data (generated)
```

**Note:** Files marked with `(generated)` are created automatically after running the experiment.

### Scenario Details

| Scenario | Mapping Type | Data Size | Queries | Description |
|----------|-------------|-----------|---------|-------------|
| Deep100 | One-to-One | medium | Q1-Q5 | Simple 1:1 entity mappings |
| StockExchange | GAV | small | Q1-Q5 | Global-As-View mappings |
| University | LAV | large | Q1-Q5 | Local-As-View mappings |

## Dependencies

### Required Software

1. **Java** (JRE 8 or higher)
   - Required to run Rapid2.jar and ChaseGQR.jar
   - Verify installation: `java -version`
   
2. **PostgreSQL** (10 or higher)
   - Used for database operations in scenarios
   - Required environment variable: `PGPASSWORD`
   - Verify installation: `psql --version`
   
3. **Python 3** (3.7 or higher)
   - Required packages: `pandas`, `matplotlib`, `numpy`
   - Install via: `pip install pandas matplotlib numpy`
   - Verify installation: `python --version`

4. **PowerShell** (Windows) or **Bash** (Linux/Mac)
   - PowerShell 5.1+ for Windows
   - Bash for running scenario scripts

5. **Git Bash** (Windows only)
   - Required to run bash scripts on Windows
   - Download: https://git-scm.com/downloads

## Installation

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd ForBackBench
```

### Step 2: Install Python Dependencies
```bash
pip install pandas matplotlib numpy
```

### Step 3: Configure PostgreSQL

1. **Install PostgreSQL** and ensure it's running
   
2. **Create database** (if needed):
   ```bash
   createdb obdabenchmark
   ```

3. **Configure credentials** in scenario files:
   - `scenarios/Deep100/postgres-config.ini`
   - `scenarios/Deep100/dependencies/ChaseGQR/db.properties`
   
   Default configuration:
   ```ini
   PGUSER=postgres
   PGPASSWORD=password
   PGDATABASE=obdabenchmark
   PGHOST=localhost
   PGPORT=5432
   ```

4. **Update configurations** if your PostgreSQL uses different credentials

### Step 4: Set Environment Variable

**Windows (PowerShell):**
```powershell
# Temporary (current session only)
$env:PGPASSWORD='password'

# Permanent (requires admin)
[System.Environment]::SetEnvironmentVariable('PGPASSWORD', 'password', 'User')
```

**Linux/Mac (Bash):**
```bash
export PGPASSWORD='password'
```

## Running Experiments

### Quick Start - Run Complete Experiment

**One-Command Execution:**

```powershell
# Windows PowerShell
cd ForBackBench
$env:PGPASSWORD='password'
powershell -ExecutionPolicy Bypass -File run_complete_experiment.ps1
```

```bash
# Linux/Mac (requires adapting the script to bash)
cd ForBackBench
export PGPASSWORD='password'
bash run_complete_experiment.sh  # Note: PowerShell script needs conversion
```

### What the Experiment Does

The complete experiment:
- ✅ Runs **3 scenarios** (Deep100, StockExchange, University)
- ✅ Tests **5 queries** per scenario (Q1-Q5)
- ✅ Executes **3 repetitions** per query
- ✅ Tests **2 systems** (Rapid and ChaseGQR)
- ✅ **Total: 90 tests**
- ✅ Automatically generates analysis and charts

### Expected Runtime

- Deep100: ~2-3 minutes
- StockExchange: ~5-8 minutes (Q5 is complex)
- University: ~3-5 minutes
- **Total: ~15-20 minutes**

### Expected Output

After completion, you'll see:
```
✅ Experiment Complete!
   Total: 90 tests
   Success: 90/90 (100%)
   Duration: ~15 minutes
   
Generated files:
  📊 FINAL_ANALYSIS_CHARTS.png - 6-panel visualization
  📄 FINAL_REPORT.txt - Complete text report
  📈 performance_comparison.csv - Performance comparison table
  📊 detailed_statistics.csv - Detailed statistics
  📋 final_chase_rewriting_<timestamp>.csv - Raw data (90 rows)
```

**File Descriptions:**

| Icon | File | Rows/Size | Use Case |
|------|------|-----------|----------|
| 📊 | `FINAL_ANALYSIS_CHARTS.png` | 230 KB | Quick visual overview, presentations, papers |
| 📄 | `FINAL_REPORT.txt` | 1.5 KB | Executive summary, conclusions |
| 📈 | `performance_comparison.csv` | 15 rows | Per-query analysis in Excel/Pandas |
| 📊 | `detailed_statistics.csv` | 6 rows | Statistical summary, tables |
| 📋 | `final_chase_rewriting_*.csv` | 90 rows | Raw data for custom analysis |

**Quick View Commands:**
```powershell
# Windows
start FINAL_ANALYSIS_CHARTS.png        # Open image
notepad FINAL_REPORT.txt               # Read report
excel performance_comparison.csv       # Analyze in Excel

# Linux/Mac
xdg-open FINAL_ANALYSIS_CHARTS.png     # or: open
cat FINAL_REPORT.txt                   # or: less
libreoffice --calc performance_comparison.csv
```

### Manual Execution (Advanced)

If you want to run scenarios individually:

#### 1. Deep100 (One-to-One mapping, medium data)
```bash
cd scripts
./runTrivialMapping.sh
```

#### 2. StockExchange (GAV mapping, small data)
```bash
cd scripts
./runGAVMapping.sh
```

#### 3. University (LAV mapping, large data)
```bash
cd scripts
./runLAVMapping.sh
```

**Note:** Edit the `SCENARIOS` and `SIZES` arrays in each script before running.

## Results and Analysis

### Generated Files

| File | Size | Description |
|------|------|-------------|
| `FINAL_ANALYSIS_CHARTS.png` | ~230 KB | 6-panel visualization with performance comparisons |
| `FINAL_REPORT.txt` | ~1.5 KB | Complete statistical analysis and recommendations |
| `performance_comparison.csv` | ~1 KB | Per-query comparison table (15 rows) |
| `detailed_statistics.csv` | ~350 B | Statistical summary by scenario and system |
| `final_chase_rewriting_<timestamp>.csv` | ~5.5 KB | Raw experimental data (90 rows) |

### File Content Examples

#### performance_comparison.csv
```csv
Scenario,Query,ChaseGQR,Rapid,SpeedRatio,Winner
Deep100,Q1,520.0,772.3,0.67,Rapid
Deep100,Q2,526.7,761.7,0.69,Rapid
Deep100,Q3,550.7,789.3,0.70,Rapid
Deep100,Q4,558.0,783.7,0.71,Rapid
Deep100,Q5,539.3,765.3,0.70,Rapid
StockExchange,Q1,450.0,799.0,0.56,Rapid
StockExchange,Q2,599.0,748.0,0.80,Rapid
StockExchange,Q3,790.7,745.3,1.06,Tie
StockExchange,Q4,1118.7,733.3,1.53,Chase
StockExchange,Q5,4783.0,719.3,6.65,Chase
University,Q1,453.7,724.7,0.63,Rapid
University,Q2,592.0,862.7,0.69,Rapid
University,Q3,483.7,851.7,0.57,Rapid
University,Q4,1379.7,723.7,1.91,Chase
University,Q5,1999.7,772.0,2.59,Chase
```

#### detailed_statistics.csv
```csv
Scenario,System,Count,Mean,Std,Min,Max
Deep100,ChaseGQR,15,538.9,27.1,455,558
Deep100,Rapid,15,774.5,20.3,734,813
StockExchange,ChaseGQR,15,1548.3,1690.9,374,4784
StockExchange,Rapid,15,749.0,47.2,675,799
University,ChaseGQR,15,981.7,634.1,446,2011
University,Robust,15,786.9,78.1,674,965
Overall,ChaseGQR,45,1023.0,1101.1,374,4784
Overall,Rapid,45,770.1,55.1,674,965
```

#### final_chase_rewriting_<timestamp>.csv (first 10 rows)
```csv
Scenario,Mapping,Size,Query,System,Run,Time_ms,Success
Deep100,oneToOne,medium,Q1,Rapid,1,742,True
Deep100,oneToOne,medium,Q1,Rapid,2,741,True
Deep100,oneToOne,medium,Q1,Rapid,3,742,True
Deep100,oneToOne,medium,Q1,ChaseGQR,1,546,True
Deep100,oneToOne,medium,Q1,ChaseGQR,2,482,True
Deep100,oneToOne,medium,Q1,ChaseGQR,3,515,True
Deep100,oneToOne,medium,Q2,Rapid,1,793,True
Deep100,oneToOne,medium,Q2,Rapid,2,753,True
Deep100,oneToOne,medium,Q2,Rapid,3,770,True
...
(90 rows total)
```

#### FINAL_REPORT.txt (excerpt)
```
================================================================================
Rapid vs ChaseGQR Performance Comparison Report
Generated: 2025-12-03 04:57:41
================================================================================

[Experiment Configuration]
  Scenarios: Deep100, StockExchange, University
  Queries: 5
  Systems: ChaseGQR, Rapid
  Total Tests: 90

[Test Success Rate]
  ChaseGQR: 45/45 (100%)
  Rapid: 45/45 (100%)

[Overall Performance]
  ChaseGQR:
    Average: 1023.0 ms
    Std Dev: 1101.1 ms
    Range: 399 - 4913 ms
    Tests: 45
  Rapid:
    Average: 770.1 ms
    Std Dev: 55.1 ms
    Range: 658 - 965 ms
    Tests: 45

  ⭐ Rapid is 24.7% faster overall
  ⭐ Rapid is 20.0x more stable (std: 55 vs 1101)

[Performance by Scenario]
  Deep100:
    ChaseGQR: 538.9 ms (std: 27.1)
    Rapid: 774.5 ms (std: 20.3)
  ...
```

### 1. FINAL_ANALYSIS_CHARTS.png

Six-panel visualization showing:

**Panel 1: Performance by Query**
- Bar chart comparing Rapid vs ChaseGQR execution time for each query
- X-axis: Query names (Deep100_Q1, ..., University_Q5)
- Y-axis: Execution time (ms)
- Blue bars: Rapid, Orange bars: ChaseGQR

**Panel 2: Performance by Scenario**
- Average execution time per scenario
- Compares overall scenario performance
- Groups: Deep100, StockExchange, University

**Panel 3: Speed Ratio Distribution**
- Histogram of Chase/Rapid speed ratios
- Values > 1: Chase slower
- Values < 1: Chase faster
- Dashed line at 1.0: equal performance

**Panel 4: Rapid Heatmap**
- Execution time heatmap (scenario × query)
- Rows: Deep100, StockExchange, University
- Columns: Q1, Q2, Q3, Q4, Q5
- Color intensity shows execution time (yellow=fast, red=slow)

**Panel 5: ChaseGQR Heatmap**
- Execution time heatmap (scenario × query)
- Same structure as Panel 4
- Highlights performance hotspots (especially StockExchange Q5)

**Panel 6: Stability Comparison**
- Box plot comparing variance between systems
- Shows median, quartiles, and outliers
- Demonstrates Rapid's superior stability

**Example Chart:**
```
┌─────────────────────────────────────────────────────┐
│ Panel 1: Performance by Query                       │
│ ████ Rapid   ███ ChaseGQR                          │
│ 800ms│  ██     ██   ██   ██   ██                   │
│ 600ms│  ██ ██  ██ ██ ██ ██ ██ ██                   │
│ 400ms│  ██ ██  ██ ██ ██ ██ ██ ██                   │
│ 200ms│  ██ ██  ██ ██ ██ ██ ██ ██                   │
│    0 └────────────────────────────────────          │
│       D_Q1 D_Q2 S_Q1 S_Q2 U_Q1 U_Q2 ...           │
└─────────────────────────────────────────────────────┘
```

### 2. FINAL_REPORT.txt

Contains:
- Experiment configuration summary
- Test success rates
- Overall performance metrics (mean, std, range)
- Performance breakdown by scenario
- Key findings and recommendations

### 3. performance_comparison.csv

Format:
```csv
Scenario,Query,ChaseGQR,Rapid,SpeedRatio,Winner
Deep100,Q1,520.0,772.3,0.67,Rapid
...
```

- **ChaseGQR/Rapid**: Average execution time (ms)
- **SpeedRatio**: Chase time / Rapid time
- **Winner**: System with better (lower) execution time

### 4. Raw Data CSV

Contains all 90 individual test runs:
```csv
Scenario,Mapping,Size,Query,System,Run,Time_ms,Success
Deep100,oneToOne,medium,Q1,Rapid,1,742,True
...
```

### Viewing Results

**Windows:**
```powershell
# Open chart
start FINAL_ANALYSIS_CHARTS.png

# View report
notepad FINAL_REPORT.txt

# Open CSV in Excel
start performance_comparison.csv
```

**Linux/Mac:**
```bash
# Open chart
xdg-open FINAL_ANALYSIS_CHARTS.png  # or: open FINAL_ANALYSIS_CHARTS.png

# View report
cat FINAL_REPORT.txt

# Open CSV
libreoffice performance_comparison.csv  # or: open performance_comparison.csv
```

### Re-generating Analysis

If you want to regenerate charts/reports from existing data:

```bash
python analyze_results.py
```

This will:
- Read existing CSV files from `experiments/` directory
- Regenerate all charts and reports
- Overwrite previous analysis files

## Experiment Configuration

### Modify Number of Repetitions

Edit `run_complete_experiment.ps1` (line 7):
```powershell
param(
    [int]$NumRuns = 3  # Change to 5, 10, etc.
)
```

**Note:** Increasing repetitions improves statistical reliability but increases runtime proportionally.

### Modify Test Scenarios

Edit the `$scenarios` array in `run_complete_experiment.ps1`:

```powershell
$scenarios = @(
    @{
        Name = "Deep100"
        Mapping = "oneToOne"
        Size = "medium"
        Queries = @("Q1", "Q2", "Q3", "Q4", "Q5")
    },
    @{
        Name = "StockExchange"
        Mapping = "GAV"
        Size = "small"
        Queries = @("Q1", "Q2", "Q3", "Q4", "Q5")
    },
    @{
        Name = "University"
        Mapping = "LAV"
        Size = "large"
        Queries = @("Q1", "Q2", "Q3", "Q4", "Q5")
    }
    # Add or remove scenarios as needed
)
```

### Customize Analysis

Edit `analyze_results.py` to:
- Modify chart colors: Search for `color=` parameters
- Change chart size: Modify `figsize=(18, 10)`
- Add statistical tests: Import scipy.stats
- Change output format: Modify `plt.savefig()` parameters
- Add custom metrics: Extend the analysis functions

Example - Change chart colors:
```python
# Line 150-ish in analyze_results.py
colors = ['#2E86AB', '#A23B72']  # Change these hex colors
```

## Troubleshooting

### Common Issues

#### 1. "psql: command not found"

**Problem:** PostgreSQL bin directory not in PATH

**Solution (Windows):**
```powershell
# Add to PATH (replace version number)
$env:Path += ";C:\Program Files\PostgreSQL\14\bin"
```

**Solution (Linux/Mac):**
```bash
# Add to .bashrc or .zshrc
export PATH="/usr/local/pgsql/bin:$PATH"
```

#### 2. "Java not found"

**Problem:** Java not installed or not in PATH

**Solution:**
1. Download and install Java: https://www.java.com/download/
2. Verify: `java -version`
3. Add to PATH if necessary

#### 3. Python Import Errors

**Problem:** Missing Python packages

**Solution:**
```bash
pip install pandas matplotlib numpy

# If using conda:
conda install pandas matplotlib numpy
```

#### 4. Database Connection Failed

**Problem:** PostgreSQL not running or credentials incorrect

**Solutions:**
- Check PostgreSQL is running:
  ```bash
  # Windows
  Get-Service postgresql*
  
  # Linux/Mac
  pg_ctl status
  ```
- Verify credentials in `scenarios/*/postgres-config.ini`
- Ensure `PGPASSWORD` environment variable is set
- Check database exists: `psql -l`

#### 5. Permission Denied on Bash Scripts

**Problem:** Scripts not executable

**Solution (Linux/Mac):**
```bash
chmod +x scripts/*.sh
```

#### 6. PowerShell Execution Policy Error

**Problem:** Script execution disabled

**Solution:**
```powershell
# Temporary (current session)
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

# Or run with bypass flag
powershell -ExecutionPolicy Bypass -File run_complete_experiment.ps1
```

#### 7. Chinese Characters in Output

**Problem:** PowerShell encoding issues with Chinese text

**Solution:** This is cosmetic only - the experiment still runs correctly. The English-only version in the latest script should avoid this.

### Debug Mode

Run with verbose output to diagnose issues:

**PowerShell:**
```powershell
$VerbosePreference = "Continue"
$ErrorActionPreference = "Stop"
.\run_complete_experiment.ps1
```

**Check Individual Components:**

1. Test Java:
   ```bash
   java -version
   ```

2. Test Rapid directly:
   ```bash
   cd scenarios/Deep100
   java -jar ../../systems/rapid/Rapid2.jar DU SHORT owl/ontology.owl queries/iqaros/Q1.txt
   ```

3. Test ChaseGQR directly:
   ```bash
   cd scenarios/Deep100/dependencies/ChaseGQR
   java -jar ../../../../systems/ChaseGQR/ChaseGQR.jar -t cgqr-t-tgds.txt -v ../oneToOne-st-tgds.txt -q ../../queries/CGQR/Q1.txt -d db.properties
   ```

4. Test database connection:
   ```bash
   psql -U postgres -d obdabenchmark -c "SELECT 1;"
   ```

### Getting Help

If issues persist:
1. Check the generated log files in `experiments/outputs/`
2. Review the CSV files to see which tests failed
3. Run individual scenarios manually to isolate the problem
4. Check that all data files exist in `scenarios/*/data/`

## Expected Results Summary

Based on our experiments, you should expect:

| Metric | Rapid | ChaseGQR | Conclusion |
|--------|-------|----------|------------|
| **Average Time** | ~770 ms | ~1023 ms | Rapid 25% faster |
| **Std Deviation** | ~55 ms | ~1101 ms | Rapid 20x more stable |
| **Success Rate** | 100% | 100% | Both reliable |
| **Best Scenario** | StockExchange | Deep100 | Varies by mapping |
| **Worst Case** | University Q5 | StockExchange Q5 | Different hotspots |

**Key Findings:**
- ✅ Rapid wins 10/15 queries overall
- ✅ Chase wins 4/15 queries (mostly simple queries)
- ✅ Rapid is significantly more stable (lower variance)
- ✅ Chase performs better on simple One-to-One mappings
- ✅ Rapid excels at complex queries (e.g., StockExchange Q5: 6.7x faster)

## Citation

If you use this benchmark in your research, please cite:

```bibtex
@misc{rapidvsChase2025,
  title={Performance Comparison of Rapid and ChaseGQR Systems},
  author={[Your Name]},
  year={2025},
  howpublished={GitHub Repository},
  url={[Repository URL]}
}
```

## License

[Add your license information - e.g., MIT, Apache 2.0, etc.]

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Contact

For questions, issues, or collaborations:
- Email: [Your Email]
- GitHub Issues: [Repository Issues URL]

---

## Appendix: Advanced ForBackBench Features

This benchmark is built on the **ForBackBench framework**, which supports many additional features beyond the Rapid vs ChaseGQR comparison. Below are advanced features for researchers who want to extend the benchmark.

### Data Generation

If you need to regenerate data for scenarios:

#### One-to-One Mappings
```bash
./scripts/generate.sh scenarios/Deep100 medium oneToOne
```

#### LAV Mappings
```bash
java -jar utilityTools/GenerateDataFromTGD.jar \
  --tgd scenarios/University/dependencies/lav.txt \
  --rows 500 \
  --output scenarios/University/data/LAV/large
```

#### GAV Mappings
```bash
./scripts/generateGAVData.sh scenarios/StockExchange small
```

### Adding New Systems

To add a new OBDA system to the comparison:

1. Add JAR file to `systems/<newsystem>/`
2. Update query scripts (`scripts/queryTrivialMapping.sh`, etc.)
3. Add invocation logic following Rapid/ChaseGQR patterns
4. Update `run_complete_experiment.ps1` to include new system

### Creating New Scenarios

Use the bootstrap script:

```bash
# For DL-Lite scenarios
./scripts/bootstrap.sh scenarios/NewScenario dllite

# For ChaseBench scenarios
./scripts/bootstrap.sh scenarios/NewScenario chasebench
```

### Full Scenario Structure

```
scenario_name/
├── data/                    # CSV data files
│   ├── oneToOne/
│   ├── LAV/
│   └── GAV/
├── dependencies/
│   ├── oneToOne-st-tgds.txt
│   ├── lav.txt
│   ├── gav.txt
│   └── ChaseGQR/
│       ├── cgqr-t-tgds.txt
│       └── db.properties
├── owl/
│   └── ontology.owl
├── queries/
│   ├── SPARQL/
│   ├── iqaros/
│   ├── CGQR/
│   └── Chasebench/
├── schema/
│   ├── oneToOne/
│   ├── LAV/
│   └── GAV/
└── postgres-config.ini
```

### Running Additional Systems

The original ForBackBench supports:
- Iqaros
- Graal
- Ontop
- RDFox
- Rulewerk
- GQR

See individual script files in `scripts/` for invocation examples.

---

**Last Updated:** December 2025
**Version:** 1.0
