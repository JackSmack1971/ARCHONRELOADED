#!/bin/bash

# ARCHON RELOADED - Development Environment Installer
# Optimized for comprehensive setup with error handling and validation

set -euo pipefail  # Exit on error, undefined vars, pipe failures

# Configuration
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly PROJECT_ROOT="${SCRIPT_DIR}"
readonly LOG_FILE="${PROJECT_ROOT}/install.log"
readonly REQUIRED_DOCKER_VERSION="20.10.0"
readonly REQUIRED_NODE_VERSION="20.0.0"
readonly REQUIRED_PYTHON_VERSION="3.12.0"

# Color codes for output
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly BLUE='\033[0;34m'
readonly PURPLE='\033[0;35m'
readonly CYAN='\033[0;36m'
readonly NC='\033[0m' # No Color

# Logging functions
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}" | tee -a "$LOG_FILE"
}

warn() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] WARNING: $1${NC}" | tee -a "$LOG_FILE"
}

error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: $1${NC}" | tee -a "$LOG_FILE"
}

info() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')] INFO: $1${NC}" | tee -a "$LOG_FILE"
}

success() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] SUCCESS: $1${NC}" | tee -a "$LOG_FILE"
}

# Version comparison function
version_ge() {
    [ "$(printf '%s\n' "$1" "$2" | sort -V | head -n1)" = "$2" ]
}

# Check if running as root
check_root() {
    if [[ $EUID -eq 0 ]]; then
        error "This script should not be run as root for security reasons"
        exit 1
    fi
}

# Detect operating system
detect_os() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if command -v apt-get >/dev/null 2>&1; then
            echo "ubuntu"
        elif command -v yum >/dev/null 2>&1; then
            echo "rhel"
        elif command -v pacman >/dev/null 2>&1; then
            echo "arch"
        else
            echo "linux"
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macos"
    elif [[ "$OSTYPE" == "msys" ]]; then
        echo "windows"
    else
        echo "unknown"
    fi
}

# Check system requirements
check_system_requirements() {
    log "Checking system requirements..."
    
    local os_type
    os_type=$(detect_os)
    
    case $os_type in
        ubuntu|linux)
            if ! command -v curl >/dev/null 2>&1; then
                error "curl is required but not installed. Install with: sudo apt-get install curl"
                exit 1
            fi
            ;;
        macos)
            if ! command -v brew >/dev/null 2>&1; then
                warn "Homebrew not found. Installing Homebrew..."
                /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
            fi
            ;;
        windows)
            warn "Windows detected. Ensure you're using WSL2 or Git Bash for best compatibility"
            ;;
        *)
            warn "Unknown OS detected. Proceeding with caution..."
            ;;
    esac
    
    # Check available disk space (require at least 10GB)
    local available_space
    available_space=$(df "${PROJECT_ROOT}" | awk 'NR==2 {print $4}')
    if [[ $available_space -lt 10485760 ]]; then  # 10GB in KB
        error "Insufficient disk space. At least 10GB required."
        exit 1
    fi
    
    success "System requirements check passed"
}

# Install Docker and Docker Compose
install_docker() {
    log "Checking Docker installation..."
    
    if command -v docker >/dev/null 2>&1; then
        local docker_version
        docker_version=$(docker --version | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1)
        
        if version_ge "$docker_version" "$REQUIRED_DOCKER_VERSION"; then
            success "Docker $docker_version is already installed"
        else
            warn "Docker version $docker_version is outdated. Minimum required: $REQUIRED_DOCKER_VERSION"
        fi
    else
        log "Installing Docker..."
        local os_type
        os_type=$(detect_os)
        
        case $os_type in
            ubuntu|linux)
                curl -fsSL https://get.docker.com -o get-docker.sh
                sudo sh get-docker.sh
                sudo usermod -aG docker "$USER"
                rm get-docker.sh
                ;;
            macos)
                warn "Please install Docker Desktop for macOS from https://docs.docker.com/desktop/mac/install/"
                warn "After installation, restart the terminal and run this script again"
                exit 1
                ;;
            *)
                error "Automatic Docker installation not supported for your OS"
                error "Please install Docker manually: https://docs.docker.com/get-docker/"
                exit 1
                ;;
        esac
    fi
    
    # Check Docker Compose
    if ! command -v docker-compose >/dev/null 2>&1 && ! docker compose version >/dev/null 2>&1; then
        log "Installing Docker Compose..."
        local os_type
        os_type=$(detect_os)
        
        case $os_type in
            ubuntu|linux)
                sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
                sudo chmod +x /usr/local/bin/docker-compose
                ;;
            macos)
                brew install docker-compose
                ;;
        esac
    fi
    
    # Test Docker
    if ! docker ps >/dev/null 2>&1; then
        error "Docker is not running or current user lacks permissions"
        info "Try: sudo usermod -aG docker $USER && newgrp docker"
        exit 1
    fi
    
    success "Docker installation verified"
}

# Install Node.js and npm
install_nodejs() {
    log "Checking Node.js installation..."
    
    if command -v node >/dev/null 2>&1; then
        local node_version
        node_version=$(node --version | sed 's/v//')
        
        if version_ge "$node_version" "$REQUIRED_NODE_VERSION"; then
            success "Node.js $node_version is already installed"
        else
            warn "Node.js version $node_version is outdated. Minimum required: $REQUIRED_NODE_VERSION"
        fi
    else
        log "Installing Node.js..."
        local os_type
        os_type=$(detect_os)
        
        case $os_type in
            ubuntu|linux)
                curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
                sudo apt-get install -y nodejs
                ;;
            macos)
                brew install node@20
                ;;
            *)
                warn "Please install Node.js 20.x manually from https://nodejs.org/"
                ;;
        esac
    fi
    
    # Verify npm
    if ! command -v npm >/dev/null 2>&1; then
        error "npm not found after Node.js installation"
        exit 1
    fi
    
    success "Node.js installation verified"
}

# Install Python and uv
install_python() {
    log "Checking Python installation..."
    
    # Check for Python 3.12+
    if command -v python3 >/dev/null 2>&1; then
        local python_version
        python_version=$(python3 --version | grep -oE '[0-9]+\.[0-9]+\.[0-9]+')
        
        if version_ge "$python_version" "$REQUIRED_PYTHON_VERSION"; then
            success "Python $python_version is already installed"
        else
            warn "Python version $python_version is outdated. Minimum required: $REQUIRED_PYTHON_VERSION"
        fi
    else
        log "Installing Python 3.12..."
        local os_type
        os_type=$(detect_os)
        
        case $os_type in
            ubuntu|linux)
                sudo apt-get update
                sudo apt-get install -y software-properties-common
                sudo add-apt-repository ppa:deadsnakes/ppa -y
                sudo apt-get update
                sudo apt-get install -y python3.12 python3.12-venv python3.12-dev python3-pip
                sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.12 1
                ;;
            macos)
                brew install python@3.12
                ;;
            *)
                warn "Please install Python 3.12+ manually from https://python.org/"
                ;;
        esac
    fi
    
    # Install uv (modern Python package manager)
    if ! command -v uv >/dev/null 2>&1; then
        log "Installing uv package manager..."
        curl -LsSf https://astral.sh/uv/install.sh | sh
        source "$HOME/.cargo/env" 2>/dev/null || true
        export PATH="$HOME/.cargo/bin:$PATH"
    fi
    
    success "Python and uv installation verified"
}

# Setup environment file
setup_environment() {
    log "Setting up environment configuration..."
    
    local env_file="${PROJECT_ROOT}/.env"
    local env_example="${PROJECT_ROOT}/.env.example"
    
    if [[ ! -f "$env_file" ]]; then
        if [[ -f "$env_example" ]]; then
            cp "$env_example" "$env_file"
            info "Created .env from .env.example"
        else
            cat > "$env_file" << 'EOF'
# ARCHON RELOADED Environment Configuration

# Required - Get from supabase.com dashboard
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_KEY=your-service-key-here

# Optional - Set via UI Settings page or here
# OPENAI_API_KEY=sk-proj-your-openai-key

# Unified Logging Configuration (Optional)
LOGFIRE_ENABLED=false              # true=Logfire logging, false=standard logging  
# LOGFIRE_TOKEN=pylf_...            # Only required when LOGFIRE_ENABLED=true

# Service Discovery (automatically set for Docker)
SERVICE_DISCOVERY_MODE=docker_compose

# Optional: Custom Ports
API_PORT=8080
MCP_PORT=8051
AGENTS_PORT=8052
FRONTEND_PORT=3737
DOCS_PORT=3838

# Performance Tuning
MAX_CONCURRENT_SESSIONS=250
VECTOR_CACHE_TTL=3600
EMBEDDING_BATCH_SIZE=1024

# Log Level
LOG_LEVEL=INFO
EOF
            info "Created default .env file"
        fi
        
        warn "IMPORTANT: Please edit .env file with your Supabase credentials"
        warn "1. Create a Supabase project at https://supabase.com"
        warn "2. Copy URL and service key from Settings → API"
        warn "3. Update SUPABASE_URL and SUPABASE_SERVICE_KEY in .env"
    else
        success ".env file already exists"
    fi
}

# Ensure an agents.md configuration file is present. Codex uses an `AGENTS.md` or
# `agents.md` file to configure project-specific agent behaviors. If such a file
# already exists in the project root, the installer will leave it untouched.
# Otherwise, it creates a simple template to help users get started.
setup_agents_file() {
    log "Checking for agents configuration file..."
    local agents_lower="${PROJECT_ROOT}/agents.md"
    local agents_upper="${PROJECT_ROOT}/AGENTS.md"
    if [[ -f "$agents_lower" || -f "$agents_upper" ]]; then
        success "Existing agents configuration detected. Skipping creation."
    else
        cat > "$agents_lower" <<'EOF'
# Agents Configuration

This file defines project-specific agent configurations for use with OpenAI Codex.

## Overview

Define your agents here by specifying their roles, capabilities, and any
configuration parameters required by your application. The Codex environment
will read this file at startup to customise agent behaviour.

## Example

```markdown
- name: ExampleAgent
  description: Demonstrates how to define an agent
  language: python
  entrypoint: python examples/example_agent.py
```

See the project documentation for more details on agent configuration.
EOF
        info "Created default agents.md configuration file"
        warn "Please edit agents.md to define your custom agents before running the platform"
    fi
}

# Install Python dependencies
install_python_dependencies() {
    log "Installing Python dependencies..."
    
    if [[ -d "${PROJECT_ROOT}/python" ]]; then
        cd "${PROJECT_ROOT}/python"
        
        # Install with uv
        if command -v uv >/dev/null 2>&1; then
            uv sync --all-extras
        else
            # Fallback to pip
            python3 -m venv venv
            source venv/bin/activate
            pip install --upgrade pip
            pip install -r requirements.txt
            if [[ -f "requirements.dev.txt" ]]; then
                pip install -r requirements.dev.txt
            fi
        fi
        
        cd "$PROJECT_ROOT"
        success "Python dependencies installed"
    else
        warn "Python directory not found, skipping Python dependencies"
    fi
}

# Install Node.js dependencies
install_nodejs_dependencies() {
    log "Installing Node.js dependencies..."
    
    # Frontend dependencies
    if [[ -d "${PROJECT_ROOT}/archon-ui-main" ]]; then
        cd "${PROJECT_ROOT}/archon-ui-main"
        npm ci --prefer-offline --no-audit
        cd "$PROJECT_ROOT"
        success "Frontend dependencies installed"
    fi
    
    # Documentation dependencies
    if [[ -d "${PROJECT_ROOT}/docs" ]]; then
        cd "${PROJECT_ROOT}/docs"
        npm ci --prefer-offline --no-audit
        cd "$PROJECT_ROOT"
        success "Documentation dependencies installed"
    fi
}

# Build Docker images
build_docker_images() {
    log "Building Docker images..."
    
    # Build images with proper caching
    if docker-compose build --parallel 2>/dev/null; then
        success "Docker images built successfully"
    elif docker compose build --parallel 2>/dev/null; then
        success "Docker images built successfully"
    else
        error "Failed to build Docker images"
        exit 1
    fi
}

# Verify installation
verify_installation() {
    log "Verifying installation..."
    
    # Start services
    log "Starting services..."
    if docker-compose up -d 2>/dev/null || docker compose up -d 2>/dev/null; then
        success "Services started"
    else
        error "Failed to start services"
        exit 1
    fi
    
    # Wait for services to be ready
    log "Waiting for services to initialize..."
    sleep 30
    
    # Health checks
    local health_checks=(
        "http://localhost:8080/health|API Server"
        "http://localhost:8051|MCP Server"
        "http://localhost:8052/health|Agents Server"
        "http://localhost:3737|Frontend"
    )
    
    local failed_checks=0
    
    for check in "${health_checks[@]}"; do
        IFS='|' read -r url service <<< "$check"
        if curl -f -s "$url" >/dev/null 2>&1; then
            success "$service is healthy"
        else
            error "$service health check failed"
            ((failed_checks++))
        fi
    done
    
    if [[ $failed_checks -eq 0 ]]; then
        success "All services are healthy"
    else
        warn "$failed_checks service(s) failed health checks"
        info "Check logs with: docker-compose logs"
    fi
}

# Cleanup function
cleanup() {
    if [[ -f get-docker.sh ]]; then
        rm -f get-docker.sh
    fi
}

# Main installation function
main() {
    trap cleanup EXIT
    
    echo -e "${PURPLE}"
    echo "╔═══════════════════════════════════════════════════════════════╗"
    echo "║                  ARCHON RELOADED INSTALLER                    ║"
    echo "║              AI Development Platform Setup                    ║"
    echo "╚═══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    
    log "Starting ARCHON RELOADED installation..."
    log "Installation log: $LOG_FILE"
    
    # Pre-installation checks
    check_root
    check_system_requirements
    
    # Core dependencies
    install_docker
    install_nodejs
    install_python
    
    # Project setup
    setup_environment
    # Ensure an agents.md file exists or create a template
    setup_agents_file
    install_python_dependencies
    install_nodejs_dependencies
    
    # Docker setup
    build_docker_images
    verify_installation
    
    echo -e "${GREEN}"
    echo "╔═══════════════════════════════════════════════════════════════╗"
    echo "║                   INSTALLATION COMPLETE!                     ║"
    echo "╚═══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    
    echo -e "${CYAN}Access your ARCHON RELOADED platform:${NC}"
    echo -e "  ${GREEN}🌐 Web Interface:${NC}     http://localhost:3737"
    echo -e "  ${GREEN}📚 Documentation:${NC}     http://localhost:3838"
    echo -e "  ${GREEN}⚡ API Docs:${NC}          http://localhost:8080/docs"
    echo -e "  ${GREEN}🔧 MCP Connection:${NC}    http://localhost:8051/sse"
    echo ""
    echo -e "${YELLOW}Next steps:${NC}"
    echo -e "  1. Edit .env file with your Supabase credentials"
    echo -e "  2. Set up database using migration scripts (see docs)"
    echo -e "  3. Configure API keys in Settings page"
    echo -e "  4. Start developing with MCP integration!"
    echo ""
    echo -e "${BLUE}Useful commands:${NC}"
    echo -e "  ${GREEN}View logs:${NC}            docker-compose logs -f"
    echo -e "  ${GREEN}Restart services:${NC}     docker-compose restart"
    echo -e "  ${GREEN}Stop services:${NC}        docker-compose down"
    echo -e "  ${GREEN}Update services:${NC}      docker-compose pull && docker-compose up -d"
    echo ""
    echo -e "${PURPLE}For support and documentation, visit:${NC}"
    echo -e "  📖 Local docs: http://localhost:3838"
    echo -e "  🐙 Repository: https://github.com/JackSmack1971/ARCHONRELOADED"
    
    success "ARCHON RELOADED installation completed successfully!"
}

# Run main function
main "$@"
