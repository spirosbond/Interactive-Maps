.PHONY : build-gcp build-gcp-init build build-container run-dev run-prod deploy-gcp-run

# Builds a docker container based on the Dockerfile
build-container:
	echo "Building..."
	sudo docker build . -t inter-maps-frontend:latest

# Runs the application locally in dev mode using port 3000 and the local .env file
run-dev:
	echo "Running Dev..."
	npm run dev

# Builds the application for production
build:
	echo "Building..."
	npm run build

# Runs the application locally in prod mode using port 3000 and the local .env file
run-prod: build
	echo "Running Prod..."
	npm run start

# Initialize gcloud for deployment. Normally this is only needed to be done once. 
# You can perform this initialization manually on the browser but it is much faster to script it and reuse it.
build-gcp-init:
	gcloud config set project aerospacelab-interactive-maps
	gcloud config set run/region europe-west1
	gcloud artifacts repositories list --project=aerospacelab-interactive-maps
	-gcloud artifacts repositories create inter-maps-frontend \
    --repository-format=docker \
    --location=europe-west1 \
    --description="Interactive Maps Frontend Container"
	gcloud artifacts repositories list --project=aerospacelab-interactive-maps
	-gcloud compute networks create aerospacelab-interactive-maps

# Builds the application in a gcloud container
build-gcp:
	echo "Building GCP..."
	gcloud config set project aerospacelab-interactive-maps
	gcloud config set run/region europe-west1
	gcloud builds submit --tag europe-west1-docker.pkg.dev/aerospacelab-interactive-maps/inter-maps-frontend/inter-maps-frontend:latest

# First builds the application in a gcloud container and then runs it using Google Cloud Run
deploy-gcp-run: build-gcp
	gcloud run deploy inter-maps-frontend --port 3000 --image europe-west1-docker.pkg.dev/aerospacelab-interactive-maps/inter-maps-frontend/inter-maps-frontend:latest --allow-unauthenticated --network aerospacelab-interactive-maps --subnet aerospacelab-interactive-maps --vpc-egress private-ranges-only
