# ==========================================
# Rapid vs ChaseGQR Complete Experiment
# 3 Scenarios x 5 Queries x 3 Runs x 2 Systems = 90 Tests
# ==========================================

param(
    [int]$NumRuns = 3  # Number of runs per query
)

$ErrorActionPreference = "Continue"
$root = "c:\Users\21764\CodeBuddy\20251201055436\ForBackBench"

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Rapid vs ChaseGQR Complete Experiment" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Scenarios: Deep100, StockExchange, University" -ForegroundColor White
Write-Host "Systems: Rapid (Rewriting) vs ChaseGQR (Chase)" -ForegroundColor White
Write-Host "Runs per query: $NumRuns" -ForegroundColor White
Write-Host "========================================`n" -ForegroundColor Cyan

# Set database password
$env:PGPASSWORD = 'password'

# Results storage
$allResults = @()
$testCount = 0
$successCount = 0

# Define scenarios
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
)

# Function to run Rapid
function Run-Rapid {
    param($ScenarioPath, $Query)
    
    $startTime = Get-Date
    try {
        Set-Location $ScenarioPath
        $output = java -jar "..\..\systems\rapid\Rapid2.jar" DU SHORT "owl\ontology.owl" "queries\iqaros\$Query.txt" 2>&1
        $endTime = Get-Date
        $duration = ($endTime - $startTime).TotalMilliseconds
        
        if ($output -match "Q\(|<-") {
            return @{
                Success = $true
                Time = [int]$duration
                Output = ($output | Out-String)
            }
        } else {
            return @{ Success = $false; Time = 0; Output = "No valid output" }
        }
    }
    catch {
        return @{ Success = $false; Time = 0; Output = $_.Exception.Message }
    }
    finally {
        Set-Location $root
    }
}

# Function to run ChaseGQR
function Run-ChaseGQR {
    param($ScenarioName, $Query)
    
    $startTime = Get-Date
    try {
        $tgdPath = "scenarios\$ScenarioName\dependencies\ChaseGQR\cgqr-t-tgds.txt"
        $stPath = "scenarios\$ScenarioName\dependencies\oneToOne-st-tgds.txt"
        $queryPath = "scenarios\$ScenarioName\queries\Chasebench\$Query\$Query.txt"
        $dbPath = "scenarios\$ScenarioName\dependencies\ChaseGQR\db.properties"
        
        $output = java -jar "systems\ChaseGQR\ChaseGQR.jar" -t $tgdPath -v $stPath -q $queryPath -d $dbPath 2>&1
        $endTime = Get-Date
        $duration = ($endTime - $startTime).TotalMilliseconds
        
        if ($output -match "Total number of solutions|GQR") {
            return @{
                Success = $true
                Time = [int]$duration
                Output = ($output | Out-String)
            }
        } else {
            return @{ Success = $false; Time = 0; Output = "No valid output" }
        }
    }
    catch {
        return @{ Success = $false; Time = 0; Output = $_.Exception.Message }
    }
}

# Main experiment loop
$totalTests = 0
foreach ($scenario in $scenarios) {
    $totalTests += $scenario.Queries.Count * 2 * $NumRuns
}

Write-Host "Total tests to run: $totalTests`n" -ForegroundColor Yellow

foreach ($scenario in $scenarios) {
    $scenName = $scenario.Name
    $mapping = $scenario.Mapping
    $size = $scenario.Size
    
    Write-Host "`n========================================" -ForegroundColor Green
    Write-Host "Scenario: $scenName ($mapping, $size)" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    
    $scenarioPath = Join-Path $root "scenarios\$scenName"
    
    foreach ($query in $scenario.Queries) {
        Write-Host "`n  Query: $query" -ForegroundColor Cyan
        
        # Run Rapid
        Write-Host "    [Rapid]" -ForegroundColor Yellow -NoNewline
        for ($run = 1; $run -le $NumRuns; $run++) {
            $testCount++
            $result = Run-Rapid -ScenarioPath $scenarioPath -Query $query
            
            if ($result.Success) {
                Write-Host " ." -ForegroundColor Green -NoNewline
                $successCount++
            } else {
                Write-Host " X" -ForegroundColor Red -NoNewline
            }
            
            $allResults += [PSCustomObject]@{
                Scenario = $scenName
                Mapping = $mapping
                Size = $size
                Query = $query
                System = "Rapid"
                Run = $run
                Time_ms = $result.Time
                Success = $result.Success
            }
        }
        Write-Host " ($NumRuns runs, avg: $([int](($allResults | Where-Object { $_.Scenario -eq $scenName -and $_.Query -eq $query -and $_.System -eq 'Rapid' -and $_.Success }).Time_ms | Measure-Object -Average).Average)ms)" -ForegroundColor Gray
        
        # Run ChaseGQR
        Write-Host "    [Chase]" -ForegroundColor Yellow -NoNewline
        for ($run = 1; $run -le $NumRuns; $run++) {
            $testCount++
            $result = Run-ChaseGQR -ScenarioName $scenName -Query $query
            
            if ($result.Success) {
                Write-Host " ." -ForegroundColor Green -NoNewline
                $successCount++
            } else {
                Write-Host " X" -ForegroundColor Red -NoNewline
            }
            
            $allResults += [PSCustomObject]@{
                Scenario = $scenName
                Mapping = $mapping
                Size = $size
                Query = $query
                System = "ChaseGQR"
                Run = $run
                Time_ms = $result.Time
                Success = $result.Success
            }
        }
        Write-Host " ($NumRuns runs, avg: $([int](($allResults | Where-Object { $_.Scenario -eq $scenName -and $_.Query -eq $query -and $_.System -eq 'ChaseGQR' -and $_.Success }).Time_ms | Measure-Object -Average).Average)ms)" -ForegroundColor Gray
        
        # Progress
        $progress = [int](($testCount / $totalTests) * 100)
        Write-Host "    Progress: $testCount/$totalTests ($progress%)" -ForegroundColor DarkGray
    }
}

# Save results
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$csvFile = "final_chase_rewriting_$timestamp.csv"
$allResults | Export-Csv -Path $csvFile -NoTypeInformation -Encoding UTF8

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Experiment Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Total tests: $testCount" -ForegroundColor White
Write-Host "Successful: $successCount" -ForegroundColor Green
Write-Host "Failed: $($testCount - $successCount)" -ForegroundColor $(if ($testCount -eq $successCount) { "Green" } else { "Red" })
Write-Host "Success rate: $([int](($successCount / $testCount) * 100))%" -ForegroundColor White
Write-Host "`nResults saved to: $csvFile" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Run analysis if Python script exists
if (Test-Path "analyze_results.py") {
    Write-Host "Running analysis..." -ForegroundColor Yellow
    # Copy CSV to expected location for analyzer
    Copy-Item $csvFile "final_chase_rewriting_current.csv" -Force
    python analyze_results.py
} else {
    Write-Host "Note: analyze_results.py not found. Skipping analysis." -ForegroundColor Yellow
}

Write-Host "`nDone!`n" -ForegroundColor Green
