# Tiltfile for Career Advisor Development
# This provides fast development with live reload for all microservices

# Load Kubernetes YAML files
k8s_yaml([
    'k8s/namespace.yaml',
    'k8s/configmap.yaml',
    'k8s/postgres.yaml',
    'k8s/users-service.yaml',
    'k8s/conversations-service.yaml',
    'k8s/messages-service.yaml',
    'k8s/prompts-service.yaml',
    'k8s/llm-service.yaml',
    'k8s/ingress.yaml'
])

# Users Service
docker_build(
    'career-advisor/users-service',
    context='.',
    dockerfile='microservices/services/users-service/Dockerfile',
    live_update=[
        sync('microservices/services/users-service/src', '/app/microservices/services/users-service/src'),
        sync('microservices/shared', '/app/microservices/shared'),
        run('pkill -f "fastapi dev" || true', trigger=['microservices/services/users-service/src/**/*.py']),
    ]
)

# Conversations Service
docker_build(
    'career-advisor/conversations-service',
    context='.',
    dockerfile='microservices/services/conversations-service/Dockerfile',
    live_update=[
        sync('microservices/services/conversations-service/src', '/app/microservices/services/conversations-service/src'),
        sync('microservices/shared', '/app/microservices/shared'),
        run('pkill -f "fastapi dev" || true', trigger=['microservices/services/conversations-service/src/**/*.py']),
    ]
)

# Messages Service
docker_build(
    'career-advisor/messages-service',
    context='.',
    dockerfile='microservices/services/messages-service/Dockerfile',
    live_update=[
        sync('microservices/services/messages-service/src', '/app/microservices/services/messages-service/src'),
        sync('microservices/shared', '/app/microservices/shared'),
        run('pkill -f "fastapi dev" || true', trigger=['microservices/services/messages-service/src/**/*.py']),
    ]
)

# Prompts Service
docker_build(
    'career-advisor/prompts-service',
    context='.',
    dockerfile='microservices/services/prompts-service/Dockerfile',
    live_update=[
        sync('microservices/services/prompts-service/src', '/app/microservices/services/prompts-service/src'),
        sync('microservices/shared', '/app/microservices/shared'),
        run('pkill -f "fastapi dev" || true', trigger=['microservices/services/prompts-service/src/**/*.py']),
    ]
)

# LLM Service
docker_build(
    'career-advisor/llm-service',
    context='.',
    dockerfile='microservices/services/llm-service/Dockerfile',
    live_update=[
        sync('microservices/services/llm-service/src', '/app/microservices/services/llm-service/src'),
        sync('microservices/shared', '/app/microservices/shared'),
        run('pkill -f "fastapi dev" || true', trigger=['microservices/services/llm-service/src/**/*.py']),
    ]
)

# Port forward all services for local access
k8s_resource('users-service', port_forwards='8001:8000')
k8s_resource('conversations-service', port_forwards='8002:8000')
k8s_resource('messages-service', port_forwards='8003:8000')
k8s_resource('prompts-service', port_forwards='8004:8000')
k8s_resource('llm-service', port_forwards='8005:8000')
k8s_resource('postgres', port_forwards='5432:5432')

# Set resource dependencies - all services wait for postgres
k8s_resource('users-service', resource_deps=['postgres'])
k8s_resource('conversations-service', resource_deps=['postgres'])
k8s_resource('messages-service', resource_deps=['postgres'])
k8s_resource('prompts-service', resource_deps=['postgres'])
k8s_resource('llm-service', resource_deps=['postgres'])

print("🚀 Tilt is configured for Career Advisor development!")
print("📋 All Services with Live Reload:")
print("  • Users Service: http://localhost:8001")
print("  • Conversations Service: http://localhost:8002")
print("  • Messages Service: http://localhost:8003")
print("  • Prompts Service: http://localhost:8004")
print("  • LLM Service: http://localhost:8005")
print("  • PostgreSQL: localhost:5432")
print("💡 File changes will sync instantly with live reload for all services!")
