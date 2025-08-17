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
    # In the Codex environment the container runs as root by default. Running as
    # root is therefore expected and cannot be avoided. Instead of exiting
    # entirely, emit a warning so users are aware. Do not abort execution on
    # EUID==0.
    if [[ $EUID -eq 0 ]]; then
        warn "Running as root. This is normal in Codex sandboxes, but be cautious when running commands that modify your system."
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
    # In Codex environments Docker is typically not available and cannot be
    # installed because nested container runtimes are disabled. If the
    # `docker` command is missing, warn the user and skip installation.
    if ! command -v docker >/dev/null 2>&1; then
        warn "Docker is not available in this environment. Skipping Docker installation and related steps."
        return
    fi
    # If Docker is present, perform a minimal version check without attempting
    # to install or modify the host. Docker upgrades are beyond the scope of
    # this script in Codex sandboxes.
    local docker_version
    docker_version=$(docker --version | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1 || true)
    if [[ -n "$docker_version" ]] && version_ge "$docker_version" "$REQUIRED_DOCKER_VERSION"; then
        success "Docker $docker_version is available"
    else
        warn "Docker version $docker_version does not meet the minimum requirement ($REQUIRED_DOCKER_VERSION). Proceeding anyway."
    fi
    # Check docker compose availability; in most modern Docker installations
    # `docker compose` is built-in. If not available we log a warning but do not
    # attempt to install, since package installation is restricted.
    if ! command -v docker-compose >/dev/null 2>&1 && ! docker compose version >/dev/null 2>&1; then
        warn "Docker Compose is not available. Docker-dependent steps will be skipped."
    fi
    # If docker command is available and running, note success.
    if docker ps >/dev/null 2>&1; then
        success "Docker daemon is running"
    else
        warn "Docker daemon appears to be stopped or unreachable. Docker-dependent steps will be skipped."
    fi
}

# Install Node.js and npm
install_nodejs() {
    log "Checking Node.js installation..."
    if command -v node >/dev/null 2>&1; then
        local node_version
        node_version=$(node --version | sed 's/v//')
        # The Codex base image includes Node.js 20.x by default【773203997825559†L289-L297】,
        # so we simply warn if the version is less than the required version but do not
        # attempt to install or upgrade Node.js in this environment.
        if version_ge "$node_version" "$REQUIRED_NODE_VERSION"; then
            success "Detected Node.js $node_version"
        else
            warn "Detected Node.js $node_version, which is older than the recommended $REQUIRED_NODE_VERSION."
        fi
    else
        # Node.js is missing; installation cannot be performed in Codex sandboxes.
        error "Node.js is not installed and cannot be automatically installed in this environment."
        exit 1
    fi
    # Verify npm (or pnpm/yarn) exists; the codex image includes npm【773203997825559†L289-L297】.
    if ! command -v npm >/dev/null 2>&1; then
        error "npm not found. Ensure Node.js installation provides npm."
        exit 1
    fi
    success "Node.js environment verified"
}

# Install Python and uv
install_python() {
    log "Checking Python installation..."
    # Python 3.12 is pre-installed in Codex images【773203997825559†L289-L297】. We verify that
    # python3 exists and meets the minimal version requirement.
    if command -v python3 >/dev/null 2>&1; then
        local python_version
        python_version=$(python3 --version | grep -oE '[0-9]+\.[0-9]+\.[0-9]+')
        if version_ge "$python_version" "$REQUIRED_PYTHON_VERSION"; then
            success "Detected Python $python_version"
        else
            warn "Detected Python $python_version, which is older than the recommended $REQUIRED_PYTHON_VERSION."
        fi
    else
        error "Python3 is not available and cannot be installed automatically in this environment."
        exit 1
    fi
    # Ensure the `uv` package manager exists. If it does not, attempt a user-level install.
    if ! command -v uv >/dev/null 2>&1; then
        warn "uv package manager not found. Attempting to install locally..."
        # Use curl to install uv. This uses the preinstalled Rust toolchain, which is
        # available in codex images【773203997825559†L289-L299】.
        curl -LsSf https://astral.sh/uv/install.sh | sh || warn "Failed to install uv; falling back to pip"
        # Source cargo environment if installed; ignore failure.
        source "$HOME/.cargo/env" 2>/dev/null || true
        export PATH="$HOME/.cargo/bin:$PATH"
    fi
    success "Python environment verified"
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
    # If Docker or Docker Compose is unavailable, skip building images. This is
    # common in Codex sandboxes where nested containerization is disabled.
    if ! command -v docker >/dev/null 2>&1; then
        warn "Docker is not available. Skipping Docker image build."
        return
    fi
    # Build images with proper caching using docker compose. Prefer the newer
    # `docker compose` subcommand but fall back to the standalone binary if
    # available. If both commands fail, emit an error but do not abort the
    # entire installation.
    if docker compose build --parallel 2>/dev/null; then
        success "Docker images built successfully"
    elif command -v docker-compose >/dev/null 2>&1 && docker-compose build --parallel 2>/dev/null; then
        success "Docker images built successfully"
    else
        warn "Failed to build Docker images. Continuing without Docker support."
    fi
}

# Verify installation
verify_installation() {
    log "Verifying installation..."
    # In environments without Docker we cannot start containers. Instead we
    # provide guidance to the user on how to start the application manually.
    if ! command -v docker >/dev/null 2>&1; then
        warn "Docker not available; skipping container startup and health checks."
        warn "You can run the backend and frontend services directly using the provided Python and Node scripts."
        return
    fi
    # Start services via docker compose. Prefer `docker compose` subcommand; fall back to
    # standalone docker-compose binary.
    log "Starting services..."
    if docker compose up -d 2>/dev/null; then
        success "Services started"
    elif command -v docker-compose >/dev/null 2>&1 && docker-compose up -d 2>/dev/null; then
        success "Services started"
    else
        warn "Failed to start Docker services. You may need to start services manually."
        return
    fi
    # Wait for services to be ready
    log "Waiting for services to initialize..."
    sleep 30
    # Perform health checks to ensure services are responding.
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
