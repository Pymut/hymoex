################################################################################
# Hymoex Architect Skill - Windows Installer (PowerShell)
#
# Detects and installs the skill for:
# - Claude Code
# - Cursor
# - Other AI coding agents
#
# Usage: irm https://raw.githubusercontent.com/Pymut/hymoex/master/apps/skills/installers/install-architect.ps1 | iex
################################################################################

$ErrorActionPreference = "Stop"

# Configuration
$SkillName = "hymoex-architect"
$RepoUrl = "https://github.com/Pymut/hymoex.git"
$TempDir = "$env:TEMP\hymoex-architect-install"

################################################################################
# Helper Functions
################################################################################

function Write-Header {
    Write-Host ""
    Write-Host "╔═══════════════════════════════════════════════════════════╗" -ForegroundColor Blue
    Write-Host "║                                                           ║" -ForegroundColor Blue
    Write-Host "║          Hymoex Architect Skill - Installer              ║" -ForegroundColor Blue
    Write-Host "║                                                           ║" -ForegroundColor Blue
    Write-Host "╚═══════════════════════════════════════════════════════════╝" -ForegroundColor Blue
    Write-Host ""
}

function Write-Success {
    param([string]$Message)
    Write-Host "✓ $Message" -ForegroundColor Green
}

function Write-Error-Msg {
    param([string]$Message)
    Write-Host "✗ $Message" -ForegroundColor Red
}

function Write-Warning-Msg {
    param([string]$Message)
    Write-Host "⚠ $Message" -ForegroundColor Yellow
}

function Write-Info {
    param([string]$Message)
    Write-Host "ℹ $Message" -ForegroundColor Blue
}

################################################################################
# Agent Detection
################################################################################

function Test-ClaudeCode {
    # Check if Claude Code skills directory exists
    $claudePath = Join-Path $env:USERPROFILE ".claude\skills"
    return Test-Path $claudePath
}

function Test-Cursor {
    # Check if Cursor is installed
    $cursorPath = Join-Path $env:USERPROFILE ".cursor"
    if (Test-Path $cursorPath) { return $true }

    # Check if cursor command exists
    try {
        Get-Command cursor -ErrorAction Stop | Out-Null
        return $true
    } catch {
        return $false
    }
}

function Test-Windsurf {
    # Check if Windsurf is installed
    $windsurfPath = Join-Path $env:USERPROFILE ".windsurf"
    return Test-Path $windsurfPath
}

function Get-DetectedAgents {
    $agents = @()

    if (Test-ClaudeCode) {
        $agents += "claude_code"
    }

    if (Test-Cursor) {
        $agents += "cursor"
    }

    if (Test-Windsurf) {
        $agents += "windsurf"
    }

    return $agents
}

################################################################################
# Installation Paths
################################################################################

function Get-InstallPath {
    param([string]$Agent)

    switch ($Agent) {
        "claude_code" {
            return Join-Path $env:USERPROFILE ".claude\skills\$SkillName"
        }
        "cursor" {
            return Join-Path $env:USERPROFILE ".cursor\skills\$SkillName"
        }
        "windsurf" {
            return Join-Path $env:USERPROFILE ".windsurf\skills\$SkillName"
        }
        default {
            return Join-Path $env:USERPROFILE ".agents\skills\$SkillName"
        }
    }
}

function Get-SharedPath {
    return Join-Path $env:USERPROFILE ".agents\skills\$SkillName"
}

################################################################################
# Installation Functions
################################################################################

function Get-Skill {
    Write-Info "Downloading skill..."

    # Remove temp directory if exists
    if (Test-Path $TempDir) {
        Remove-Item -Path $TempDir -Recurse -Force
    }

    # Try git clone first
    if (Get-Command git -ErrorAction SilentlyContinue) {
        try {
            git clone --depth 1 $RepoUrl $TempDir 2>&1 | Out-Null
            Write-Success "Repository cloned successfully"
            return $true
        } catch {
            Write-Warning-Msg "Git clone failed, trying alternative method..."
        }
    }

    # Fallback to downloading zip
    try {
        $zipUrl = $RepoUrl -replace '\.git$', '/archive/main.zip'
        $zipPath = Join-Path $TempDir "skill.zip"

        New-Item -ItemType Directory -Path $TempDir -Force | Out-Null
        Invoke-WebRequest -Uri $zipUrl -OutFile $zipPath

        # Extract zip
        Expand-Archive -Path $zipPath -DestinationPath $TempDir -Force

        # Move files from extracted folder to temp root
        $extractedFolder = Get-ChildItem -Path $TempDir -Directory | Select-Object -First 1
        Get-ChildItem -Path $extractedFolder.FullName -Recurse | Move-Item -Destination $TempDir -Force

        Remove-Item -Path $extractedFolder.FullName -Recurse -Force
        Remove-Item -Path $zipPath -Force

        Write-Success "Repository downloaded successfully"
        return $true
    } catch {
        Write-Error-Msg "Failed to download repository: $_"
        return $false
    }
}

function Install-ForAgent {
    param([string]$Agent)

    $installPath = Get-InstallPath -Agent $Agent

    Write-Info "Installing for $Agent at: $installPath"

    # Create parent directory
    $parentDir = Split-Path -Parent $installPath
    New-Item -ItemType Directory -Path $parentDir -Force | Out-Null

    # Copy skill files
    $skillSource = Join-Path $TempDir "skill"
    if (Test-Path $skillSource) {
        Copy-Item -Path $skillSource -Destination $installPath -Recurse -Force
    } else {
        Copy-Item -Path $TempDir -Destination $installPath -Recurse -Force
    }

    Write-Success "Installed for $Agent"
}

function Install-Shared {
    $sharedPath = Get-SharedPath

    Write-Info "Installing to shared location: $sharedPath"

    $parentDir = Split-Path -Parent $sharedPath
    New-Item -ItemType Directory -Path $parentDir -Force | Out-Null

    # Copy skill files
    $skillSource = Join-Path $TempDir "skill"
    if (Test-Path $skillSource) {
        Copy-Item -Path $skillSource -Destination $sharedPath -Recurse -Force
    } else {
        Copy-Item -Path $TempDir -Destination $sharedPath -Recurse -Force
    }

    Write-Success "Installed to shared location"
}

function New-SymbolicLinks {
    param([array]$Agents)

    $sharedPath = Get-SharedPath

    foreach ($agent in $Agents) {
        $agentPath = Get-InstallPath -Agent $agent

        # If agent path already exists as directory, skip
        if ((Test-Path $agentPath) -and !(Get-Item $agentPath).Attributes.HasFlag([System.IO.FileAttributes]::ReparsePoint)) {
            continue
        }

        # Remove existing symlink if any
        if (Test-Path $agentPath) {
            Remove-Item -Path $agentPath -Force
        }

        # Create parent directory
        $parentDir = Split-Path -Parent $agentPath
        New-Item -ItemType Directory -Path $parentDir -Force | Out-Null

        # Create junction (Windows equivalent of symlink for directories)
        try {
            New-Item -ItemType Junction -Path $agentPath -Target $sharedPath -Force | Out-Null
            Write-Success "Created symlink for $agent"
        } catch {
            Write-Warning-Msg "Could not create symlink for $agent, copying instead..."
            Copy-Item -Path $sharedPath -Destination $agentPath -Recurse -Force
        }
    }
}

################################################################################
# Main Installation Logic
################################################################################

function Main {
    Write-Header

    # Detect agents
    Write-Info "Detecting AI coding agents..."
    $agents = Get-DetectedAgents

    if ($agents.Count -eq 0) {
        Write-Warning-Msg "No AI coding agents detected"
        Write-Info "Installing to default location: $(Join-Path $env:USERPROFILE '.agents\skills\$SkillName')"
        $agents = @("default")
    } else {
        Write-Success "Detected agents: $($agents -join ', ')"
    }

    # Download skill
    if (-not (Get-Skill)) {
        Write-Error-Msg "Installation failed: Could not download skill"
        exit 1
    }

    # Choose installation strategy
    if ($agents.Count -gt 1) {
        # Multiple agents - use shared installation with symlinks
        Write-Info "Multiple agents detected. Using shared installation with symlinks."

        Install-Shared
        New-SymbolicLinks -Agents $agents
    } else {
        # Single agent - direct installation
        Install-ForAgent -Agent $agents[0]
    }

    # Cleanup
    if (Test-Path $TempDir) {
        Remove-Item -Path $TempDir -Recurse -Force
    }

    # Success message
    Write-Host ""
    Write-Success "Installation complete!"
    Write-Host ""
    Write-Info "The /hymoex-architect skill is now available in:"

    foreach ($agent in $agents) {
        $path = Get-InstallPath -Agent $agent
        Write-Host "  • $agent`: $path"
    }

    Write-Host ""
    Write-Info "Usage:"
    Write-Host '  /hymoex-architect "Your requirements here"'
    Write-Host ""
    Write-Info "Documentation:"
    if ($agents.Count -gt 1) {
        Write-Host "  $(Join-Path (Get-SharedPath) 'README.md')"
    } else {
        Write-Host "  $(Join-Path (Get-InstallPath -Agent $agents[0]) 'README.md')"
    }
    Write-Host ""

    Write-Success "Happy architecting! 🚀"
}

# Run main
Main
