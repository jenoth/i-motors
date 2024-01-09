# Python version installed; we need 3.8-3.11
PYTHON=`command -v python3.11 || command -v python3.10 || command -v python3.9 || command -v python3.8`

build-and-run-docker-locally:
	docker build -t i-motors .
	docker run -p 8000:8000  i-motors:latest
