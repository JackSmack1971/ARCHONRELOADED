#!/bin/bash

# ARCHON RELOADED - Development Environment Installer
# Optimized for comprehensive setup with error handling and validation
#
# Usage:
#   ./install.sh                    # Standard installation
#   CONTAINER=true ./install.sh     # Force container mode
#   SKIP_DOCKER=true ./install.sh   # Skip Docker installation
#
# Container Environments (Codex, GitHub Codespaces, etc.):
#   The script automatically detects container environments and adapts accordingly.
#   It will allow running as root and skip Docker if the socket isn't available.

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
    local env_type
    env_type=$(detect_environment)
    
    # Allow running as root in container environments
    if [[ $EUID -eq 0 ]]; then
        case $env_type in
            codex)
                info "Running in OpenAI Codex environment - root access is normal"
                export RUNNING_IN_CODEX=true
                export RUNNING_IN_CONTAINER=true
                ;;
            container)
                warn "Running as root in container environment - this is expected"
                export RUNNING_IN_CONTAINER=true
                ;;
            *)
                error "This script should not be run as root for security reasons"
                info "If you're in a container environment, set CONTAINER=true: CONTAINER=true ./install.sh"
                exit 1
                ;;
        esac
    else
        export RUNNING_IN_CONTAINER=false
        export RUNNING_IN_CODEX=false
    fi
}

# Detect operating system and environment
detect_environment() {
    # Debug: Show current environment info
    echo "DEBUG: PWD=$PWD, HOME=$HOME, USER=${USER:-$(whoami)}" >&2
    echo "DEBUG: CODEX_ENV vars: PYTHON=${CODEX_ENV_PYTHON_VERSION:-unset}, NODE=${CODEX_ENV_NODE_VERSION:-unset}" >&2
    
    # Check if we're in OpenAI Codex environment (multiple detection methods)
    # Method 1: CODEX_ENV environment variables
    if [[ -n "${CODEX_ENV_PYTHON_VERSION:-}" ]] || [[ -n "${CODEX_ENV_NODE_VERSION:-}" ]]; then
        echo "codex"
        return
    fi
    
    # Method 2: Working directory in /workspace/*
    if [[ "$PWD" == /workspace/* ]]; then
        echo "codex"
        return
    fi
    
    # Method 3: Repository cloned to /workspace/* (check if we're inside such a directory)
    if [[ "$(pwd)" == /workspace/* ]]; then
        echo "codex"
        return
    fi
    
    # Method 4: Universal image indicators (Ubuntu 24.04 + root + universal tools)
    if [[ "$HOME" == "/root" && -f "/usr/bin/uv" && -f "/usr/bin/node" && -f "/etc/os-release" ]]; then
        if grep -q "Ubuntu 24.04" /etc/os-release 2>/dev/null; then
            echo "codex"
            return
        fi
    fi
    
    # Method 5: Check if running in universal image specifically
    if [[ -f "/usr/bin/mise" && -f "/usr/bin/uv" && "$USER" == "root" ]]; then
        echo "codex" 
        return
    fi
    
    # Check for other container environments
    if [[ -f /.dockerenv ]] || [[ -n "${CONTAINER:-}" ]] || [[ -n "${CODESPACE_NAME:-}" ]] || [[ -n "${GITHUB_CODESPACES:-}" ]] || [[ "$USER" == "root" && -n "${DEBIAN_FRONTEND:-}" ]]; then
        echo "container"
        return
    fi
    
    # Detect host OS
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
    
    local env_type
    env_type=$(detect_environment)
    
    case $env_type in
        codex)
            success "OpenAI Codex environment detected"
            info "Ubuntu 24.04 with pre-installed development tools"
            info "Python ${CODEX_ENV_PYTHON_VERSION:-3.12}, Node.js ${CODEX_ENV_NODE_VERSION:-20}"
            ;;
        container)
            info "Container environment detected"
            if ! command -v curl >/dev/null 2>&1; then
                error "curl is required but not installed"
                exit 1
            fi
            ;;
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
            warn "Unknown environment detected. Proceeding with caution..."
            ;;
    esac
    
    # Check available disk space (require at least 5GB for Codex, 10GB for others)
    local required_space
    if [[ "${RUNNING_IN_CODEX:-false}" == "true" ]]; then
        required_space=5242880  # 5GB in KB
    else
        required_space=10485760  # 10GB in KB
    fi
    
    local available_space
    available_space=$(df "${PROJECT_ROOT}" | awk 'NR==2 {print $4}')
    if [[ $available_space -lt $required_space ]]; then
        error "Insufficient disk space. At least $((required_space / 1048576))GB required."
        exit 1
    fi
    
    success "System requirements check passed"
}

# Install Docker and Docker Compose
install_docker() {
    log "Checking Docker installation..."
    
    # Skip Docker in Codex environment (Docker-in-Docker not supported)
    if [[ "${RUNNING_IN_CODEX:-false}" == "true" ]]; then
        warn "Skipping Docker installation in OpenAI Codex environment"
        warn "Docker-in-Docker is not supported in Codex sandboxes"
        info "You can run the application in development mode without Docker"
        export SKIP_DOCKER=true
        return 0
    fi
    
    # In some container environments, Docker might not be available or needed
    if [[ "${RUNNING_IN_CONTAINER:-false}" == "true" ]] && [[ -n "${SKIP_DOCKER:-}" ]]; then
        warn "Skipping Docker installation in container environment (SKIP_DOCKER is set)"
        return 0
    fi
    
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
        local env_type
        env_type=$(detect_environment)
        
        case $env_type in
            ubuntu|linux|container)
                curl -fsSL https://get.docker.com -o get-docker.sh
                if [[ "${RUNNING_IN_CONTAINER:-false}" == "true" ]]; then
                    # In container, run without sudo
                    sh get-docker.sh
                else
                    sudo sh get-docker.sh
                fi
                
                # Only try to modify user groups if not in container
                if [[ "${RUNNING_IN_CONTAINER:-false}" != "true" ]] && command -v usermod >/dev/null 2>&1; then
                    sudo usermod -aG docker "$USER" || warn "Could not add user to docker group"
                fi
                rm get-docker.sh
                ;;
            macos)
                warn "Please install Docker Desktop for macOS from https://docs.docker.com/desktop/mac/install/"
                warn "After installation, restart the terminal and run this script again"
                exit 1
                ;;
            *)
                error "Automatic Docker installation not supported for your environment"
                error "Please install Docker manually: https://docs.docker.com/get-docker/"
                exit 1
                ;;
        esac
    fi
    
    # Check Docker Compose
    if ! command -v docker-compose >/dev/null 2>&1 && ! docker compose version >/dev/null 2>&1; then
        log "Installing Docker Compose..."
        local env_type
        env_type=$(detect_environment)
        
        case $env_type in
            ubuntu|linux|container)
                if [[ "${RUNNING_IN_CONTAINER:-false}" == "true" ]]; then
                    curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
                    chmod +x /usr/local/bin/docker-compose
                else
                    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
                    sudo chmod +x /usr/local/bin/docker-compose
                fi
                ;;
            macos)
                brew install docker-compose
                ;;
        esac
    fi
    
    # Test Docker (skip if in container and Docker socket not available)
    if ! docker ps >/dev/null 2>&1; then
        if [[ "${RUNNING_IN_CONTAINER:-false}" == "true" ]]; then
            warn "Docker daemon not accessible in container environment"
            warn "This is normal for some container setups. Proceeding without Docker tests."
        else
            error "Docker is not running or current user lacks permissions"
            info "Try: sudo usermod -aG docker $USER && newgrp docker"
            exit 1
        fi
    else
        success "Docker installation verified"
    fi
}

# Install Node.js and npm
install_nodejs() {
    log "Checking Node.js installation..."
    
    # In Codex environment, Node.js is pre-installed
    if [[ "${RUNNING_IN_CODEX:-false}" == "true" ]]; then
        local node_version
        node_version=$(node --version | sed 's/v//')
        success "Node.js $node_version is pre-installed in Codex environment"
        
        # Verify npm
        if ! command -v npm >/dev/null 2>&1; then
            error "npm not found in Codex environment"
            exit 1
        fi
        return 0
    fi
    
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
        local env_type
        env_type=$(detect_environment)
        
        case $env_type in
            ubuntu|linux|container)
                curl -fsSL https://deb.nodesource.com/setup_20.x | if [[ "${RUNNING_IN_CONTAINER:-false}" == "true" ]]; then bash -; else sudo -E bash -; fi
                if [[ "${RUNNING_IN_CONTAINER:-false}" == "true" ]]; then
                    apt-get install -y nodejs
                else
                    sudo apt-get install -y nodejs
                fi
                ;;
            macos)
                if command -v brew >/dev/null 2>&1; then
                    brew install node@20
                else
                    warn "Homebrew not found. Please install Node.js manually"
                fi
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
    
    # In Codex environment, Python and uv are pre-installed
    if [[ "${RUNNING_IN_CODEX:-false}" == "true" ]]; then
        local python_version
        python_version=$(python3 --version | grep -oE '[0-9]+\.[0-9]+\.[0-9]+')
        success "Python $python_version is pre-installed in Codex environment"
        
        # Verify uv is available
        if command -v uv >/dev/null 2>&1; then
            success "uv package manager is pre-installed in Codex environment"
        else
            warn "uv not found in Codex environment, installing..."
            curl -LsSf https://astral.sh/uv/install.sh | sh
            source "$HOME/.cargo/env" 2>/dev/null || true
            export PATH="$HOME/.cargo/bin:$PATH"
        fi
        return 0
    fi
    
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
        local env_type
        env_type=$(detect_environment)
        
        case $env_type in
            ubuntu|linux|container)
                if [[ "${RUNNING_IN_CONTAINER:-false}" == "true" ]]; then
                    apt-get update
                    apt-get install -y software-properties-common
                    add-apt-repository ppa:deadsnakes/ppa -y
                    apt-get update
                    apt-get install -y python3.12 python3.12-venv python3.12-dev python3-pip
                    update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.12 1 || true
                else
                    sudo apt-get update
                    sudo apt-get install -y software-properties-common
                    sudo add-apt-repository ppa:deadsnakes/ppa -y
                    sudo apt-get update
                    sudo apt-get install -y python3.12 python3.12-venv python3.12-dev python3-pip
                    sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.12 1
                fi
                ;;
            macos)
                if command -v brew >/dev/null 2>&1; then
                    brew install python@3.12
                else
                    warn "Homebrew not found. Please install Python manually"
                fi
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
        
        # Handle different shell environments
        if [[ -f "$HOME/.cargo/env" ]]; then
            source "$HOME/.cargo/env" 2>/dev/null || true
        fi
        export PATH="$HOME/.cargo/bin:$PATH"
        
        # Alternative installation if first method fails
        if ! command -v uv >/dev/null 2>&1; then
            log "Trying alternative uv installation method..."
            if [[ "${RUNNING_IN_CONTAINER:-false}" == "true" ]]; then
                pip3 install uv || python3 -m pip install uv
            else
                pip3 install --user uv || python3 -m pip install --user uv
            fi
        fi
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

# Install Node.js dependencies with Codex optimizations
install_nodejs_dependencies() {
    log "Installing Node.js dependencies..."
    
    # Frontend dependencies
    if [[ -d "${PROJECT_ROOT}/archon-ui-main" ]]; then
        cd "${PROJECT_ROOT}/archon-ui-main"
        
        # Use faster installation in Codex environment
        if [[ "${RUNNING_IN_CODEX:-false}" == "true" ]]; then
            npm ci --prefer-offline --no-audit --no-fund
        else
            npm ci --prefer-offline --no-audit
        fi
        
        cd "$PROJECT_ROOT"
        success "Frontend dependencies installed"
    fi
    
    # Documentation dependencies
    if [[ -d "${PROJECT_ROOT}/docs" ]]; then
        cd "${PROJECT_ROOT}/docs"
        
        # Use faster installation in Codex environment
        if [[ "${RUNNING_IN_CODEX:-false}" == "true" ]]; then
            npm ci --prefer-offline --no-audit --no-fund
        else
            npm ci --prefer-offline --no-audit
        fi
        
        cd "$PROJECT_ROOT"
        success "Documentation dependencies installed"
    fi
}

# Setup development mode (for environments without Docker)
setup_development_mode() {
    log "Setting up development mode..."
    
    # Create AGENTS.md file for Codex environment
    if [[ "${RUNNING_IN_CODEX:-false}" == "true" ]]; then
        cat > "${PROJECT_ROOT}/AGENTS.md" << 'EOF'
# ARCHON RELOADED Development Environment

## Environment Setup
- **OS**: Ubuntu 24.04 LTS
- **Python**: 3.12+ with uv, poetry, black, mypy
- **Node.js**: 20.x with npm, yarn, pnpm
- **Runtime**: Containerized sandbox environment

## Development Workflow
### Running Services Individually

```bash
# Backend API Server (FastAPI + Socket.IO)
cd python
uv run python -m src.server.main

# MCP Server 
cd python  
uv run python -m src.mcp.server

# AI Agents Server
cd python
uv run python -m src.agents.server

# Frontend Development Server
cd archon-ui-main
npm run dev

# Documentation Server
cd docs
npm run start
```

### Testing
```bash
# Python tests
cd python && uv run pytest

# Frontend tests  
cd archon-ui-main && npm test

# Type checking
cd python && uv run mypy src/
cd archon-ui-main && npm run type-check
```

### Environment Variables
- Set SUPABASE_URL and SUPABASE_SERVICE_KEY in .env
- Configure OPENAI_API_KEY in Settings UI
- Use SERVICE_DISCOVERY_MODE=local for development

## Notes
- This environment runs services individually rather than in Docker
- Database connections use Supabase (cloud-hosted PostgreSQL)
- Real-time features via Socket.IO on localhost
- Hot reload enabled for both Python and React components
EOF
        info "Created AGENTS.md file for Codex environment guidance"
    fi
    
    # Setup development environment file
    local dev_env_file="${PROJECT_ROOT}/.env.development"
    cat > "$dev_env_file" << 'EOF'
# ARCHON RELOADED Development Mode Configuration

# Service Discovery
SERVICE_DISCOVERY_MODE=local

# Service URLs for development
API_URL=http://localhost:8080
MCP_URL=http://localhost:8051  
AGENTS_URL=http://localhost:8052
FRONTEND_URL=http://localhost:3737
DOCS_URL=http://localhost:3838

# Development Features
LOG_LEVEL=DEBUG
LOGFIRE_ENABLED=false
PYTHONPATH=./python/src

# Hot Reload
VITE_HMR_ENABLED=true
UVICORN_RELOAD=true
EOF
    
    info "Created development environment configuration"
    
    # Create startup script for development mode
    cat > "${PROJECT_ROOT}/dev-start.sh" << 'EOF'
#!/bin/bash
# ARCHON RELOADED Development Mode Startup

echo "🚀 Starting ARCHON RELOADED in Development Mode"
echo ""

# Load environment
source .env.development

# Function to start service in background
start_service() {
    local name="$1"
    local command="$2"
    local dir="$3"
    
    echo "Starting $name..."
    if [[ -n "$dir" ]]; then
        (cd "$dir" && $command) &
    else
        $command &
    fi
    echo "  ✓ $name started (PID: $!)"
}

# Start backend services
start_service "API Server" "uv run python -m src.server.main" "python"
start_service "MCP Server" "uv run python -m src.mcp.server" "python"  
start_service "Agents Server" "uv run python -m src.agents.server" "python"

# Start frontend services
start_service "Frontend" "npm run dev" "archon-ui-main"
start_service "Documentation" "npm run start" "docs"

echo ""
echo "🎉 All services started!"
echo ""
echo "Access URLs:"
echo "  🌐 Web Interface:     http://localhost:3737"
echo "  📚 Documentation:     http://localhost:3838"
echo "  ⚡ API Docs:          http://localhost:8080/docs"
echo "  🔧 MCP Connection:    http://localhost:8051/sse"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for user interrupt
trap 'echo "Stopping services..."; pkill -f "uv run python"; pkill -f "npm run"; exit' INT
wait
EOF
    
    chmod +x "${PROJECT_ROOT}/dev-start.sh"
    success "Created development mode startup script (dev-start.sh)"
}
    log "Building Docker images..."
    
    # Check if Docker is available
    if ! command -v docker >/dev/null 2>&1 || ! docker ps >/dev/null 2>&1; then
        error "Docker is not available for building images"
        if [[ "${RUNNING_IN_CONTAINER:-false}" == "true" ]]; then
            warn "This is normal in some container environments"
            warn "Images can be built later when Docker is available"
            return 0
        else
            exit 1
        fi
    fi
    
    # Build images with proper caching
    if docker-compose build --parallel 2>/dev/null; then
        success "Docker images built successfully"
    elif docker compose build --parallel 2>/dev/null; then
        success "Docker images built successfully"
    else
        error "Failed to build Docker images"
        if [[ "${RUNNING_IN_CONTAINER:-false}" == "true" ]]; then
            warn "Build failed in container environment - this may be expected"
            warn "Try building manually later: docker-compose build"
            return 0
        else
            exit 1
        fi
    fi
}

# Verify installation
verify_installation() {
    log "Verifying installation..."
    
    # Check if Docker is available
    if ! command -v docker >/dev/null 2>&1 || ! docker ps >/dev/null 2>&1; then
        warn "Docker not available for verification"
        if [[ "${RUNNING_IN_CONTAINER:-false}" == "true" ]]; then
            info "This is normal in container environments"
            info "Manual verification will be needed once Docker is available"
            return 0
        else
            error "Cannot verify installation without Docker"
            exit 1
        fi
    fi
    
    # Start services
    log "Starting services..."
    if docker-compose up -d 2>/dev/null || docker compose up -d 2>/dev/null; then
        success "Services started"
    else
        error "Failed to start services"
        warn "You can try starting manually later with: docker-compose up -d"
        return 0
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

# Build Docker images
build_docker_images() {
    log "Building Docker images..."
    
    # Check if Docker is available
    if ! command -v docker >/dev/null 2>&1 || ! docker ps >/dev/null 2>&1; then
        error "Docker is not available for building images"
        if [[ "${RUNNING_IN_CONTAINER:-false}" == "true" ]]; then
            warn "This is normal in some container environments"
            warn "Images can be built later when Docker is available"
            return 0
        else
            exit 1
        fi
    fi
    
    # Build images with proper caching
    if docker-compose build --parallel 2>/dev/null; then
        success "Docker images built successfully"
    elif docker compose build --parallel 2>/dev/null; then
        success "Docker images built successfully"
    else
        error "Failed to build Docker images"
        if [[ "${RUNNING_IN_CONTAINER:-false}" == "true" ]]; then
            warn "Build failed in container environment - this may be expected"
            warn "Try building manually later: docker-compose build"
            return 0
        else
            exit 1
        fi
    fi
}
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
    
    # Container environment detection and messaging
    if [[ "${RUNNING_IN_CODEX:-false}" == "true" ]]; then
        info "OpenAI Codex environment detected"
        info "Optimizing installation for containerized sandbox environment"
        info "Docker services will be skipped - using development mode instead"
        export SKIP_DOCKER=true
    elif [[ "${RUNNING_IN_CONTAINER:-false}" == "true" ]]; then
        info "Container environment detected"
        info "Some installation steps will be adapted for container use"
        
        # Check if we should skip Docker
        if [[ ! -S /var/run/docker.sock ]] && [[ -z "${DOCKER_HOST:-}" ]]; then
            warn "Docker socket not available in container"
            warn "Setting SKIP_DOCKER=true to skip Docker installation"
            export SKIP_DOCKER=true
        fi
    fi
    
    # Core dependencies
    install_docker
    install_nodejs
    install_python
    
    # Project setup
    setup_environment
    install_python_dependencies
    install_nodejs_dependencies
    
    # Setup based on environment
    if [[ "${RUNNING_IN_CODEX:-false}" == "true" ]] || [[ -n "${SKIP_DOCKER:-}" ]]; then
        setup_development_mode
        
        if [[ "${RUNNING_IN_CODEX:-false}" == "true" ]]; then
            echo -e "${GREEN}"
            echo "╔═══════════════════════════════════════════════════════════════╗"
            echo "║              CODEX INSTALLATION COMPLETE!                    ║"
            echo "╚═══════════════════════════════════════════════════════════════╝"
            echo -e "${NC}"
            
            echo -e "${CYAN}ARCHON RELOADED is ready for OpenAI Codex!${NC}"
            echo ""
            echo -e "${YELLOW}Development Mode Setup:${NC}"
            echo -e "  ${GREEN}Environment Type:${NC}     OpenAI Codex Sandbox"
            echo -e "  ${GREEN}Python Version:${NC}       $(python3 --version | grep -oE '[0-9]+\.[0-9]+\.[0-9]+')"
            echo -e "  ${GREEN}Node.js Version:${NC}      $(node --version | sed 's/v//')"
            echo -e "  ${GREEN}Package Manager:${NC}      uv (Python) + npm (Node.js)"
            echo ""
            echo -e "${BLUE}Quick Start Commands:${NC}"
            echo -e "  ${GREEN}Start all services:${NC}   ./dev-start.sh"
            echo -e "  ${GREEN}API Server only:${NC}      cd python && uv run python -m src.server.main"
            echo -e "  ${GREEN}Frontend only:${NC}        cd archon-ui-main && npm run dev"
            echo -e "  ${GREEN}Run tests:${NC}            cd python && uv run pytest"
            echo ""
            echo -e "${PURPLE}Codex Integration:${NC}"
            echo -e "  📖 AGENTS.md file created with Codex-specific guidance"
            echo -e "  🔧 Development environment optimized for sandbox execution"
            echo -e "  ⚡ Hot reload enabled for rapid iteration"
        else
            echo -e "${GREEN}"
            echo "╔═══════════════════════════════════════════════════════════════╗"
            echo "║                   INSTALLATION COMPLETE!                     ║"
            echo "╚═══════════════════════════════════════════════════════════════╝"
            echo -e "${NC}"
            
            echo -e "${CYAN}Dependencies installed successfully!${NC}"
            echo -e "${YELLOW}Note: Docker services were skipped in container environment${NC}"
            echo ""
            echo -e "${BLUE}To start services manually:${NC}"
            echo -e "  ${GREEN}Development mode:${NC}     ./dev-start.sh"
            echo -e "  ${GREEN}Build images:${NC}         docker-compose build"
            echo -e "  ${GREEN}Start services:${NC}       docker-compose up -d"
            echo -e "  ${GREEN}Check status:${NC}         docker-compose ps"
        fi
    else
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
        echo -e "${BLUE}Useful commands:${NC}"
        echo -e "  ${GREEN}View logs:${NC}            docker-compose logs -f"
        echo -e "  ${GREEN}Restart services:${NC}     docker-compose restart"
        echo -e "  ${GREEN}Stop services:${NC}        docker-compose down"
        echo -e "  ${GREEN}Update services:${NC}      docker-compose pull && docker-compose up -d"
    fi
    
    echo ""
    echo -e "${YELLOW}Next steps:${NC}"
    echo -e "  1. Edit .env file with your Supabase credentials"
    echo -e "  2. Set up database using migration scripts (see docs)"
    echo -e "  3. Configure API keys in Settings page"
    echo -e "  4. Start developing with MCP integration!"
    echo ""
    echo -e "${PURPLE}For support and documentation, visit:${NC}"
    if [[ "${RUNNING_IN_CODEX:-false}" == "true" ]]; then
        echo -e "  📖 Local docs: npm run start (in docs directory)"
    else
        echo -e "  📖 Local docs: http://localhost:3838"
    fi
    echo -e "  🐙 Repository: https://github.com/JackSmack1971/ARCHONRELOADED"
    
    success "ARCHON RELOADED installation completed successfully!"
}

# Run main function
main "$@"
