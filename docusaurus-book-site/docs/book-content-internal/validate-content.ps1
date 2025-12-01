#!/usr/bin/env pwsh
# This script runs all content validation checks

$ErrorActionPreference = 'Stop'

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location $scriptDir

Write-Host "--- Running Content Validation Checks ---"

# Ensure Python dependencies are installed
Write-Host "Installing Python dependencies (jsonschema)..."
try {
    pip install -r requirements.txt
    Write-Host "Python dependencies installed successfully."
} catch {
    Write-Error "Failed to install Python dependencies: $($_.Exception.Message)"
    exit 1
}

# Run metadata validation
Write-Host "`n--- Running Metadata Validation ---"
try {
    python validate_metadata.py
    Write-Host "Metadata validation completed."
} catch {
    Write-Error "Metadata validation failed: $($_.Exception.Message)"
    exit 1
}

# Run internal link check
Write-Host "`n--- Running Internal Link Check ---"
try {
    python check_links.py
    Write-Host "Internal link check completed."
} catch {
    Write-Error "Internal link check failed: $($_.Exception.Message)"
    exit 1
}

# Run template compliance check
Write-Host "`n--- Running Template Compliance Check ---"
try {
    python check_template_compliance.py
    Write-Host "Template compliance check completed."
} catch {
    Write-Error "Template compliance check failed: $($_.Exception.Message)"
    exit 1
}

# Run file structure check
Write-Host "`n--- Running File Structure Check ---"
try {
    python check_structure.py
    Write-Host "File structure check completed."
} catch {
    Write-Error "File structure check failed: $($_.Exception.Message)"
    exit 1
}

Write-Host "`n--- All Content Validation Checks Completed Successfully! ---"