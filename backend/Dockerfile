# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.9-slim

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# Install production dependencies.
RUN pip install -U \
    Flask \
    gunicorn \
    gdown \
    gsutil \
    sentencepiece \
    torch \
    transformers

# get model files
ARG MODEL_FOLDER=t5_model
RUN mkdir ${MODEL_FOLDER} && cd ${MODEL_FOLDER} \
    && gdown "https://drive.google.com/uc?id=1RrgKJAXK3lujRKSfCgo7CA2bqvOQUhup" \
    && gdown "https://drive.google.com/uc?id=1RXLJgNpjBKMmc5-F781NZBmxRV9WJ2xM" \
    && cd ..

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
# Timeout is set to 0 to disable the timeouts of the workers to allow Cloud Run to handle instance scaling.
#CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app
EXPOSE 8080
ENTRYPOINT ["./script/entrypoint.sh"]