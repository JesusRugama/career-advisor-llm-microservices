# Tiltfile for Career Advisor Development
# This provides fast development with live reload for all microservices

# Define which services to enable (comment out services you don't want to run)
services = [
    {'name': 'users-service', 'port': 8001},
    {'name': 'conversations-service', 'port': 8002},
    {'name': 'prompts-service', 'port': 8004},
]

# Build list of k8s yaml files
k8s_files = [
    'k8s/namespace.yaml',
    'k8s/configmap.yaml',
    'k8s/secrets.yaml',
    'k8s/postgres.yaml',
]

# Add service yaml files for enabled services
for service in services:
    k8s_files.append('k8s/{}.yaml'.format(service['name']))
    k8s_files.append('k8s/{}-hpa.yaml'.format(service['name']))

# Optionally add ingress if multiple services are enabled
if len(services) > 1:
    k8s_files.append('k8s/ingress.yaml')

# Load Kubernetes YAML files
k8s_yaml(k8s_files)

# Build Docker images and configure k8s resources for enabled services
for service in services:
    service_name = service['name']
    service_port = service['port']
    
    # Build Docker image with live reload
    docker_build(
        'career-advisor/{}'.format(service_name),
        context='.',
        dockerfile='microservices/services/{}/Dockerfile'.format(service_name),
        live_update=[
            sync('microservices/services/{}/src'.format(service_name), '/app/microservices/services/{}/src'.format(service_name)),
            sync('microservices/shared', '/app/microservices/shared'),
            run('pkill -f "fastapi dev" || true', trigger=['microservices/services/{}/src/**/*.py'.format(service_name)]),
        ]
    )
    
    # Configure k8s resource with port forwarding and dependencies
    k8s_resource(service_name, port_forwards='{}:8000'.format(service_port))
    k8s_resource(service_name, resource_deps=['postgres'])

# Port forward postgres
k8s_resource('postgres', port_forwards='5432:5432')

print("🚀 Tilt is configured for Career Advisor development!")
print("📋 Enabled Services with Live Reload:")
for service in services:
    service_name = service['name'].replace('-', ' ').title()
    service_port = service['port']
    print("  • {}: http://localhost:{}".format(service_name, service_port))
print("  • PostgreSQL: localhost:5432")
print("💡 File changes will sync instantly with live reload for enabled services!")
