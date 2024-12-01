.PHONY : build-gcp build-gcp-init build run test deploy-gcp-run

# Builds a docker container based on the Dockerfile
build:
	echo "Building..."
	sudo docker build . -t inter-maps-backend:latest

# Runs the application locally using port 8000 and the local .env file
run:
	echo "Running..."
	uvicorn app.main:app --host localhost --port 8000 --reload --env-file .env

# Runs all tests under the tests/ folder
# -pytest makes sure the execution is not interrupted if a test fails
test:
	echo "Testing..."
	-pytest -s -p no:warnings tests/
	
# Initialize gcloud for deployment. Normally this is only needed to be done once. 
# You can perform this initialization manually on the browser but it is much faster to script it and reuse it.
build-gcp-init:
	gcloud config set project aerospacelab-interactive-maps
	gcloud config set run/region europe-west1
	gcloud artifacts repositories list --project=aerospacelab-interactive-maps
	-gcloud artifacts repositories create inter-maps-backend \
    --repository-format=docker \
    --location=europe-west1 \
    --description="Interactive Maps Backend Container"
	gcloud artifacts repositories list --project=aerospacelab-interactive-maps
	-gcloud compute networks create aerospacelab-interactive-maps

# Builds the application in a gcloud container
build-gcp:
	echo "Building GCP..."
	gcloud config set project aerospacelab-interactive-maps
	gcloud config set run/region europe-west1
	gcloud builds submit --tag europe-west1-docker.pkg.dev/aerospacelab-interactive-maps/inter-maps-backend/inter-maps-backend:latest

# First builds the application in a gcloud container and then runs it using Google Cloud Run
deploy-gcp-run: build-gcp
	gcloud run deploy inter-maps-backend --port 8080 --image europe-west1-docker.pkg.dev/aerospacelab-interactive-maps/inter-maps-backend/inter-maps-backend:latest --allow-unauthenticated --network aerospacelab-interactive-maps --subnet aerospacelab-interactive-maps --vpc-egress private-ranges-only
