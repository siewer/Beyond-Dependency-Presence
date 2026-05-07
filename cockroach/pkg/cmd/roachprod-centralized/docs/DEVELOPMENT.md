# roachprod-centralized Development Guide

This guide covers local development setup, testing practices, and contribution guidelines for the roachprod-centralized service.

**📚 Related Documentation:**
- [← Back to Main README](../README.md)
- [🔌 API Reference](API.md) - Complete REST API documentation
- [🏗️ Architecture Guide](ARCHITECTURE.md) - System design and components
- [📋 Examples & Workflows](EXAMPLES.md) - Practical usage examples
- [⚙️ Configuration Examples](../examples/) - Ready-to-use configurations

## Table of Contents

- [Prerequisites](#prerequisites)
- [Development Environment Setup](#development-environment-setup)
- [Project Structure](#project-structure)
- [Building and Running](#building-and-running)
- [Testing](#testing)
- [Code Style and Standards](#code-style-and-standards)
- [Debugging](#debugging)
- [Contributing](#contributing)
- [Common Development Tasks](#common-development-tasks)
- [Troubleshooting](#troubleshooting)

## Prerequisites

Ensure you have the CockroachDB development environment set up:

```bash
# Verify your development environment
./dev doctor
```

### Cloud Provider Access (Optional)

For testing cloud provider integration:
- **GCP**: Service account key or `gcloud` CLI
- **AWS**: AWS credentials configured
- **Azure**: Azure CLI configured
- **IBM**: IBM Cloud CLI configured

## Development Environment Setup

### Local Configuration

Create a development configuration file:

```bash
# Create local config directory
mkdir -p ~/.roachprod

# Create development configuration
cat > ~/.roachprod/dev-config.yaml << EOF
log:
  level: debug
api:
  port: 8080
  authentication:
    disabled: true
database:
  type: memory
tasks:
  workers: 1
EOF
```

## Project Structure

```
pkg/cmd/roachprod-centralized/
├── README.md                    # Main documentation
├── main.go                      # Application entry point
├── config.yml                   # Default configuration
├── BUILD.bazel                  # Bazel build configuration
│
├── app/                         # Application initialization
│   ├── app.go                   # Main app structure
│   ├── api.go                   # API server setup
│   ├── factory.go               # Service factory
│   └── options.go               # App configuration options
│
├── cmd/                         # CLI commands (Cobra)
│   ├── root.go                  # Root command
│   ├── api.go                   # API server command
│   └── workers.go               # Workers-only command
│
├── config/                      # Configuration management
│   ├── env/                     # Environment variable handling
│   ├── flags/                   # CLI flag handling
│   ├── processing/              # Config processing
│   ├── recursive/               # Recursive config handling
│   └── types/                   # Config type definitions
│
├── controllers/                 # HTTP request handlers
│   ├── clusters/                # Cluster endpoints
│   ├── health/                  # Health check endpoints
│   ├── tasks/                   # Task endpoints
│   └── public-dns/              # DNS endpoints
│
├── services/                    # Business logic layer
│   ├── clusters/                # Cluster management
│   │   ├── tasks/               # Cluster-related background tasks
│   │   └── models/              # Cluster-specific models
│   ├── tasks/                   # Task processing
│   ├── health/                  # Health monitoring
│   │   └── tasks/               # Health check tasks
│   └── public-dns/              # DNS management
│       ├── tasks/               # DNS-related background tasks
│       └── models/              # DNS-specific models
│
├── repositories/                # Data access layer
│   ├── clusters/                # Cluster storage
│   │   ├── memory/              # In-memory implementation
│   │   ├── cockroachdb/         # CockroachDB implementation
│   │   └── mocks/               # Test mocks
│   ├── tasks/                   # Task storage
│   │   ├── memory/
│   │   ├── cockroachdb/
│   │   └── mocks/
│   └── health/                  # Health storage
│       ├── memory/
│       ├── cockroachdb/
│       └── mocks/
│
├── utils/                       # Shared utilities
│   ├── api/                     # API utilities
│   │   └── bindings/            # Request binding helpers
│   ├── database/                # Database utilities
│   ├── filters/                 # Query filtering
│   │   ├── types/               # Filter type definitions
│   │   ├── memory/              # In-memory filter implementation
│   │   └── sql/                 # SQL filter implementation
│   └── logger/                  # Logging utilities
│
├── docker/                      # Docker configuration
│   ├── Dockerfile               # Multi-stage build definition
│   ├── cloudbuild.yaml          # Google Cloud Build config
│   ├── README.md                # Docker deployment guide
│   ├── image/                   # Files used during image build
│   │   ├── install-deps.sh      # Install dependencies (Azure CLI, AWS CLI)
│   │   └── entrypoint.sh        # Container entrypoint script
│   └── scripts/                 # Build orchestration scripts
│       ├── build-local.sh       # Local Podman builds (multi-arch)
│       └── build-remote.sh      # Remote Cloud Build (amd64)
│
├── docs/                        # Documentation
│   ├── API.md
│   ├── ARCHITECTURE.md
│   ├── DEVELOPMENT.md           # This file
│   ├── EXAMPLES.md
│   └── CLOUD_PROVIDER_CONFIG.md
│
└── examples/                    # Example configurations
    ├── development-config.yaml
    ├── cloud_config.yaml.example
    └── docker-compose.yml
```

## Building and Running

### Build Commands

```bash
# Build the binary (from CockroachDB root)
./dev build roachprod-centralized

# Build with race detection (for development)
./dev build roachprod-centralized --race
```

### Running Locally

#### All-in-One Mode (Default)

```bash
# Run with development configuration
./bin/roachprod-centralized api --config ~/.roachprod/dev-config.yaml

# Run with in-memory storage
export ROACHPROD_DATABASE_TYPE=memory
export ROACHPROD_API_AUTHENTICATION_METHOD=disabled
./bin/roachprod-centralized api

# Run with debug logging
export ROACHPROD_LOG_LEVEL=debug
./bin/roachprod-centralized api
```

#### Testing Scaled Deployment Locally

To test the horizontally scaled deployment mode locally, you'll need CockroachDB running:

**1. Start a local CockroachDB instance:**

```bash
# Start single-node CockroachDB (in a separate terminal)
cockroach start-single-node --insecure --listen-addr=localhost:26257 --http-addr=localhost:8080

# Create the roachprod database
cockroach sql --insecure -e "CREATE DATABASE IF NOT EXISTS roachprod;"
```

**2. Run API instances (no workers):**

```bash
# Terminal 1: API instance 1
export ROACHPROD_DATABASE_TYPE=cockroachdb
export ROACHPROD_DATABASE_URL="postgresql://root@localhost:26257/roachprod?sslmode=disable"
export ROACHPROD_API_AUTHENTICATION_METHOD=disabled
export ROACHPROD_API_PORT=8090
export ROACHPROD_LOG_LEVEL=debug
./bin/roachprod-centralized api --no-workers

# Terminal 2: API instance 2
export ROACHPROD_DATABASE_TYPE=cockroachdb
export ROACHPROD_DATABASE_URL="postgresql://root@localhost:26257/roachprod?sslmode=disable"
export ROACHPROD_API_AUTHENTICATION_METHOD=disabled
export ROACHPROD_API_PORT=8091
export ROACHPROD_LOG_LEVEL=debug
./bin/roachprod-centralized api --no-workers
```

**3. Run worker instances:**

```bash
# Terminal 3: Worker instance 1
export ROACHPROD_DATABASE_TYPE=cockroachdb
export ROACHPROD_DATABASE_URL="postgresql://root@localhost:26257/roachprod?sslmode=disable"
export ROACHPROD_TASKS_WORKERS=2
export ROACHPROD_API_METRICS_PORT=9091
export ROACHPROD_LOG_LEVEL=debug
./bin/roachprod-centralized workers

# Terminal 4: Worker instance 2
export ROACHPROD_DATABASE_TYPE=cockroachdb
export ROACHPROD_DATABASE_URL="postgresql://root@localhost:26257/roachprod?sslmode=disable"
export ROACHPROD_TASKS_WORKERS=2
export ROACHPROD_API_METRICS_PORT=9092
export ROACHPROD_LOG_LEVEL=debug
./bin/roachprod-centralized workers
```

**4. Verify the setup:**

```bash
# Check API instances
curl http://localhost:8090/health
curl http://localhost:8091/health

# Check worker metrics
curl http://localhost:9091/metrics
curl http://localhost:9092/metrics

# Create a task via API and watch workers process it
curl -X POST http://localhost:8090/clusters/sync

# Check task status
curl http://localhost:8090/tasks
```

**Expected log messages to verify correct mode:**

API instances should log:
```
health service: skipping instance registration (workers disabled)
clusters service: skipping background work (workers disabled)
Task workers disabled (Workers=0), skipping task processing routine
```

Worker instances should log:
```
Starting in metrics-only mode (workers)
Starting tasks processing routine
health service: starting health service
```

## Testing

### Unit Tests

```bash
# Run all tests
./dev test pkg/cmd/roachprod-centralized/...

# Run tests for specific package
./dev test pkg/cmd/roachprod-centralized/services/clusters

# Run tests with race detection
./dev test pkg/cmd/roachprod-centralized/... --race

# Run tests with coverage
./dev test pkg/cmd/roachprod-centralized/... --coverage

# Run specific test
./dev test pkg/cmd/roachprod-centralized/services/clusters -f TestClustersService

# Verbose test output
./dev test pkg/cmd/roachprod-centralized/services/clusters -v
```

### Integration Tests

```bash
# Run integration tests (if available)
./dev test pkg/cmd/roachprod-centralized/... --tags=integration

# Test with real database
export ROACHPROD_DATABASE_TYPE=cockroachdb
export ROACHPROD_DATABASE_URL="postgresql://root@localhost:26257/roachprod_test?sslmode=disable"
./dev test pkg/cmd/roachprod-centralized/repositories/...
```

### Testing Best Practices

1. **Use Mocks**: Mock external dependencies (cloud APIs, databases)
2. **Table Tests**: Use table-driven tests for multiple scenarios
3. **Test Isolation**: Each test should be independent
4. **Error Cases**: Test both success and failure paths

#### Example Test Structure

```go
func TestClustersService_GetAllClusters(t *testing.T) {
    tests := []struct {
        name      string
        filters   filters.FilterSet
        mockData  []cloud.Cluster
        expected  []cloud.Cluster
        wantError bool
    }{
        {
            name:     "success - no filters",
            filters:  filters.FilterSet{},
            mockData: []cloud.Cluster{testCluster1, testCluster2},
            expected: []cloud.Cluster{testCluster1, testCluster2},
        },
        // More test cases...
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            // Test implementation
        })
    }
}
```

## Code Style and Standards

### Go Code Standards

Follow standard Go conventions and CockroachDB coding standards:

```bash
# Format code
./dev generate go

# Run linting
./dev lint

# Run specific linters
./dev lint --short
```

### Code Organization Principles

1. **Package Naming**: Use clear, descriptive package names
2. **Interface Segregation**: Small, focused interfaces
3. **Dependency Injection**: Inject dependencies via constructors
4. **Error Handling**: Comprehensive error handling with context

### Documentation Standards

1. **Godoc Comments**: All public functions and types
2. **Package Documentation**: Clear package purpose
3. **Example Code**: Include examples for complex functions

```go
// ClusterService handles cluster management operations.
// It provides CRUD operations and synchronization with cloud providers.
type ClusterService struct {
    repo   clusters.IRepository
    logger *logger.Logger
}

// GetAllClusters retrieves all clusters matching the provided filters.
// Returns an empty slice if no clusters match the criteria.
func (s *ClusterService) GetAllClusters(ctx context.Context, logger *logger.Logger, input InputGetAllClustersDTO) ([]cloud.Cluster, error) {
    // Implementation...
}
```

## Debugging

### Debug Logging

```bash
# Enable debug logging
export ROACHPROD_LOG_LEVEL=debug

# Log specific operations
curl -X POST http://localhost:8080/clusters/sync
# Check logs for detailed operation traces
```

### Health Monitoring

```bash
# Check API health
curl http://localhost:8080/health

# Monitor metrics
curl http://localhost:8081/metrics | grep roachprod
```

## Contributing

### Development Workflow

1. **Create Feature Branch**:
   ```bash
   git checkout -b feature/new-functionality
   ```

2. **Make Changes**:
   - Write code following style guidelines
   - Add comprehensive tests
   - Update documentation

3. **Test Changes**:
   ```bash
   ./dev test pkg/cmd/roachprod-centralized/...
   ./dev lint
   ```

4. **Commit Changes**:
   ```bash
   git add .
   git commit -m "roachprod-centralized: add new functionality

   This commit adds X functionality to support Y use case.
   - Implement Z feature
   - Add tests for Z
   - Update documentation

   Release notes: None
   Epic: CRDB-12345"
   ```

### Code Review Process

1. **Pre-Review Checklist**:
   - [ ] All tests pass
   - [ ] Code follows style guidelines
   - [ ] Documentation updated
   - [ ] No security vulnerabilities

2. **Review Criteria**:
   - Code correctness and clarity
   - Test coverage and quality
   - Performance implications
   - Security considerations

### Release Process

1. **Version Tagging**: Follow CockroachDB versioning
2. **Release Notes**: Document user-facing changes
3. **Documentation Updates**: Keep docs current
4. **Deployment**: Follow CockroachDB deployment process

## Common Development Tasks

### Adding a New Endpoint

1. **Create Controller Handler**:
   ```go
   // In controllers/clusters/clusters.go
   func (ctrl *Controller) NewOperation(c *gin.Context) {
       // Implementation
   }
   ```

2. **Add Route**:
   ```go
   // In NewController()
   &controllers.ControllerHandler{
       Method: "POST",
       Path:   ControllerPath + "/new-operation",
       Func:   ctrl.NewOperation,
   }
   ```

3. **Add Service Method**:
   ```go
   // In services/clusters/clusters.go
   func (s *Service) NewOperation(ctx context.Context, ...) error {
       // Business logic
   }
   ```

4. **Add Tests**:
   ```go
   func TestController_NewOperation(t *testing.T) {
       // Test implementation
   }
   ```

### Adding a New Cloud Provider

1. **Implement Provider Interface** in the roachprod library

2. **Register Provider**:
   ```go
   // In service factory
   switch providerType {
   case "new-provider":
       return &NewProvider{}, nil
   }
   ```

3. **Add Configuration**:
   ```go
   // In config/config.go
   type CloudProvider struct {
       NewProvider NewProviderOptions `env:"NEWPROVIDER"`
   }
   ```

### Database Schema Changes

1. **Create Migration**:
   ```go
   // In repositories/*/cockroachdb/migrations_definition.go
   func Migration_001_AddNewTable() string {
       return `CREATE TABLE IF NOT EXISTS new_table (...);`
   }
   ```

2. **Update Repository**:
   ```go
   // Add new methods to repository interface and implementation
   ```

3. **Test Migration**:
   ```bash
   # Test with CockroachDB
   ./dev test pkg/cmd/roachprod-centralized/repositories/*/cockroachdb/...
   ```

## Troubleshooting

### Common Issues

#### Build Failures

```bash
# Error: module not found
# Solution: Ensure you're in the CockroachDB repository root
cd /path/to/cockroach
./dev build roachprod-centralized

# Error: Bazel build failed
# Solution: Clean and rebuild
bazel clean
./dev build roachprod-centralized
```

#### Runtime Issues

```bash
# Error: Port already in use
# Solution: Use different port or kill existing process
export ROACHPROD_API_PORT=9090
# Or find and kill the process
lsof -ti:8080 | xargs kill

# Error: Database connection failed
# Solution: Use memory database for development
export ROACHPROD_DATABASE_TYPE=memory
```

#### Test Failures

```bash
# Error: Tests fail with timeout
# Solution: Increase test timeout
./dev test pkg/cmd/roachprod-centralized/... --timeout=60s

# Error: Race conditions detected
# Solution: Fix race conditions or use build constraints
./dev test pkg/cmd/roachprod-centralized/... --race
```

### Performance Issues

#### Memory Usage

```bash
# Monitor memory usage
top -p $(pgrep roachprod-centralized)

# Profile memory usage
go tool pprof http://localhost:8080/debug/pprof/heap
```

#### CPU Usage

```bash
# Profile CPU usage
go tool pprof http://localhost:8080/debug/pprof/profile
```

### Getting Help

1. **CockroachDB Documentation**: https://cockroachlabs.com/docs/
2. **Internal Documentation**: Check `/docs/` in the CockroachDB repository
3. **Team Channels**: Reach out to the roachprod team
4. **Code Review**: Ask for help during code review process

### Development Tips

1. **Use Memory Database**: Faster iteration during development
2. **Enable Debug Logging**: Better insight into operations
3. **Mock External Services**: Avoid rate limits and dependencies
4. **Test Edge Cases**: Comprehensive error handling
5. **Profile Performance**: Regular performance monitoring
6. **Keep Dependencies Updated**: Follow CockroachDB update cycles