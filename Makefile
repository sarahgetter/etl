# Makefile for ETL Project
# This Makefile provides commands to build, run, stop, and clean up the Docker environment for the ETL script.

# Variables
IMAGE_NAME = etl-script         # Docker image name
CONTAINER_NAME = etl-container  # Docker container name
CONFIG_FILE = config.yaml       # Configuration file
DB_USER = your_db_username      # Database username (set this to your actual username)
DB_PASS = your_db_password      # Database password (set this to your actual password)
OAUTH_TOKEN = your_oauth_token  # OAuth token for authentication (set this to your actual token)

# Default target: build the Docker image
all: build

# Build the Docker image
# Usage: make build
build:
	docker build -t $(IMAGE_NAME) .

# Run the Docker container with environment variables
# Usage: make run
run:
	docker run -it --rm --name $(CONTAINER_NAME) \
		-e DB_USER=$(DB_USER) \
		-e DB_PASS=$(DB_PASS) \
		-e OAUTH_TOKEN=$(OAUTH_TOKEN) \
		-v $(PWD)/$(CONFIG_FILE):/app/$(CONFIG_FILE) \
		$(IMAGE_NAME)

# Stop the Docker container
# Usage: make stop
stop:
	docker stop $(CONTAINER_NAME)

# Clean up Docker resources
# Usage: make clean
clean:
	docker rmi $(IMAGE_NAME)

# Help target to display available commands
# Usage: make help
help:
	@echo "Makefile commands:"
	@echo "  make          Build the Docker image (default)"
	@echo "  make build    Build the Docker image"
	@echo "  make run      Run the Docker container with environment variables"
	@echo "  make stop     Stop the Docker container"
	@echo "  make clean    Clean up Docker resources"
	@echo "  make help     Display this help message"
