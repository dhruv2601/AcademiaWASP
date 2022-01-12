#Dockerfile vars

#vars
IMAGENAME=backend
REPO=wasp
IMAGEVERSION=0.1
IMAGEFULLNAME=${REPO}/${IMAGENAME}:${IMAGEVERSION}
IMAGEFULLNAME_NOVERSION=${REPO}/${IMAGENAME}

.PHONY: help build all

help:
	    @echo "Makefile commands:"
	    @echo "build"
	    @echo "all"
.DEFAULT_GOAL := all
build:
		gsutil cp main.py gs://academia-assistant/backend-vm/main.py
		docker build -t ${IMAGEFULLNAME_NOVERSION} .
deploy:
		gsutil cp main.py gs://academia-assistant/backend-vm/main.py
		gcloud builds submit --tag eu.gcr.io/apes-313514/flaskmrp --timeout=900
all: help