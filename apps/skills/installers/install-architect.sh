#!/usr/bin/env bash

################################################################################
# Hymoex Architect Skill - Universal Installer
#
# Detects and installs the skill for:
# - Claude Code
# - Cursor
# - Other AI coding agents
#
# Usage: curl -fsSL https://raw.githubusercontent.com/Pymut/hymoex/master/apps/skills/installers/install-architect.sh | bash
################################################################################

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Skill name
SKILL_NAME="hymoex-architect"
REPO_URL="https://github.com/Pymut/hymoex.git"
TEMP_DIR="/tmp/hymoex-architect-install"

################################################################################
# Helper Functions
################################################################################

print_header() {
    echo -e "${BLUE}"
    echo "╔═══════════════════════════════════════════════════════════╗"
    echo "║                                                           ║"
    echo "║          Hymoex Architect Skill - Installer              ║"
    echo "║                                                           ║"
    echo "╚═══════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

################################################################################
# Agent Detection
################################################################################

detect_claude_code() {
    # Check if Claude Code is installed
    if command -v claude &> /dev/null; then
        echo "claude_code"
        return 0
    fi

    # Check if Claude Code skills directory exists
    if [ -d "$HOME/.claude/skills" ]; then
        echo "claude_code"
        return 0
    fi

    return 1
}

detect_cursor() {
    # Check if Cursor is installed
    if [ -d "$HOME/.cursor" ]; then
        echo "cursor"
        return 0
    fi

    if command -v cursor &> /dev/null; then
        echo "cursor"
        return 0
    fi

    return 1
}

detect_windsurf() {
    # Check if Windsurf is installed
    if [ -d "$HOME/.windsurf" ]; then
        echo "windsurf"
        return 0
    fi

    return 1
}

detect_agents() {
    local agents=()

    if detect_claude_code &> /dev/null; then
        agents+=("claude_code")
    fi

    if detect_cursor &> /dev/null; then
        agents+=("cursor")
    fi

    if detect_windsurf &> /dev/null; then
        agents+=("windsurf")
    fi

    echo "${agents[@]}"
}

################################################################################
# Installation Paths
################################################################################

get_install_path() {
    local agent=$1

    case $agent in
        "claude_code")
            echo "$HOME/.claude/skills/$SKILL_NAME"
            ;;
        "cursor")
            echo "$HOME/.cursor/skills/$SKILL_NAME"
            ;;
        "windsurf")
            echo "$HOME/.windsurf/skills/$SKILL_NAME"
            ;;
        *)
            echo "$HOME/.agents/skills/$SKILL_NAME"
            ;;
    esac
}

get_shared_path() {
    echo "$HOME/.agents/skills/$SKILL_NAME"
}

################################################################################
# Installation Functions
################################################################################

clone_skill() {
    print_info "Cloning skill repository..."

    rm -rf "$TEMP_DIR"

    if git clone --depth 1 "$REPO_URL" "$TEMP_DIR" 2>/dev/null; then
        print_success "Repository cloned successfully"
        return 0
    else
        print_error "Failed to clone repository. Trying alternative method..."

        # Try downloading as zip if git clone fails
        mkdir -p "$TEMP_DIR"
        if curl -L "${REPO_URL%.git}/archive/main.zip" -o "$TEMP_DIR/skill.zip" 2>/dev/null; then
            unzip -q "$TEMP_DIR/skill.zip" -d "$TEMP_DIR"
            mv "$TEMP_DIR"/*/* "$TEMP_DIR/"
            print_success "Repository downloaded successfully"
            return 0
        else
            print_error "Failed to download repository"
            return 1
        fi
    fi
}

install_for_agent() {
    local agent=$1
    local install_path=$(get_install_path "$agent")

    print_info "Installing for $agent at: $install_path"

    # Create parent directory
    mkdir -p "$(dirname "$install_path")"

    # Copy skill files
    if [ -d "$TEMP_DIR/skill" ]; then
        cp -R "$TEMP_DIR/skill" "$install_path"
    else
        cp -R "$TEMP_DIR" "$install_path"
    fi

    print_success "Installed for $agent"
}

install_shared() {
    local shared_path=$(get_shared_path)

    print_info "Installing to shared location: $shared_path"

    mkdir -p "$(dirname "$shared_path")"

    # Copy skill files
    if [ -d "$TEMP_DIR/skill" ]; then
        cp -R "$TEMP_DIR/skill" "$shared_path"
    else
        cp -R "$TEMP_DIR" "$shared_path"
    fi

    print_success "Installed to shared location"
}

create_symlinks() {
    local agents=("$@")
    local shared_path=$(get_shared_path)

    for agent in "${agents[@]}"; do
        local agent_path=$(get_install_path "$agent")

        # If agent path already exists as directory, skip
        if [ -d "$agent_path" ] && [ ! -L "$agent_path" ]; then
            continue
        fi

        # Remove existing symlink if any
        rm -f "$agent_path"

        # Create symlink
        mkdir -p "$(dirname "$agent_path")"
        ln -s "$shared_path" "$agent_path"

        print_success "Created symlink for $agent"
    done
}

################################################################################
# Main Installation Logic
################################################################################

main() {
    print_header

    # Detect agents
    print_info "Detecting AI coding agents..."
    agents=($(detect_agents))

    if [ ${#agents[@]} -eq 0 ]; then
        print_warning "No AI coding agents detected"
        print_info "Installing to default location: $HOME/.agents/skills/$SKILL_NAME"
        agents=("default")
    else
        print_success "Detected agents: ${agents[*]}"
    fi

    # Clone skill
    if ! clone_skill; then
        print_error "Installation failed: Could not download skill"
        exit 1
    fi

    # Choose installation strategy
    if [ ${#agents[@]} -gt 1 ]; then
        # Multiple agents - use shared installation with symlinks
        print_info "Multiple agents detected. Using shared installation with symlinks."

        install_shared
        create_symlinks "${agents[@]}"
    else
        # Single agent - direct installation
        install_for_agent "${agents[0]}"
    fi

    # Cleanup
    rm -rf "$TEMP_DIR"

    # Success message
    echo ""
    print_success "Installation complete!"
    echo ""
    print_info "The /hymoex-architect skill is now available in:"

    for agent in "${agents[@]}"; do
        local path=$(get_install_path "$agent")
        echo "  • $agent: $path"
    done

    echo ""
    print_info "Usage:"
    echo "  /hymoex-architect \"Your requirements here\""
    echo ""
    print_info "Documentation:"
    if [ ${#agents[@]} -gt 1 ]; then
        echo "  $(get_shared_path)/README.md"
    else
        echo "  $(get_install_path "${agents[0]}")/README.md"
    fi
    echo ""

    print_success "Happy architecting! 🚀"
}

# Run main
main
