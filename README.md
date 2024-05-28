# ETL Project

This project automates the process of extracting data from a CSV file, transforming it, and loading it into a PostgreSQL database using Docker and a Makefile. The project assumes the use of a Cloud Provider's OAuth method for authentication.

## Prerequisites

- Docker: Ensure Docker is installed on your system. [Install Docker](https://docs.docker.com/get-docker/)
- Make: Ensure Make is installed on your system. [Install Make](https://www.gnu.org/software/make/)
- OAuth Token: Obtain an OAuth token from your Cloud Provider.

## Directory Structure

/your-project-directory
|-- Dockerfile
|-- requirements.txt
|-- etl_script.py
|-- config.yaml
|-- Makefile
|-- README.md
