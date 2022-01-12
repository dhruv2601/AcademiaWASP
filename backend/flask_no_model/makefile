#Dockerfile vars

#vars
IMAGENAME=tmp
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
run:
		gsutil cp main.py gs://academia-assistant/backend-vm/main.py
		docker run -it --rm -p 8080:8080 -e PORT=8080 ${IMAGEFULLNAME_NOVERSION}
build:
		gsutil cp main.py gs://academia-assistant/backend-vm/main.py
		docker build -t ${IMAGEFULLNAME_NOVERSION} .
deploy:
		gsutil cp main.py gs://academia-assistant/backend-vm/main.py
		gcloud builds submit --tag eu.gcr.io/apes-313514/flasktmp

all: help