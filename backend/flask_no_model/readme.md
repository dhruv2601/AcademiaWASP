# Minor docker image

For light-weight experiments locally or on cloud providers without models.

## Requirements

**get gcloud command-line tools:**

1. install https://cloud.google.com/sdk/docs/install
2. authentical with valid user (might change with time. Ask.)


**secret file:**

```bash
# Download key file into secret/ folder
mkdir secret
mv "apes---key---.json" secret/
```
The secret key is stored on google drive: https://drive.google.com/drive/folders/1hTMQoX-d9qkm-iAadnHWm0jBOFBSaXHe

## Development

```bash
# upload main.py to google cloud storage
gsutil cp main.py gs://academia-assistant/backend-vm/main.py

# building docker image
make build

# running docker image with interactive shell
make run
```

To login into the running docker container, open new terminal window and run:

```bash
### show all running docker containers + copy container id of wasp/tmp
docker ps

# insert here and run
docker exec -it <container_ID> /bin/bash
```
