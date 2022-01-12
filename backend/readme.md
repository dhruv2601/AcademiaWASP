# Backend for Academia Assistant


## tl;dr - Calling the API

**Health and reachability check:**

The `ping` endpoint returns a simple string: `pong`.

```
34.147.33.58:8080/ping
```

**Scientific style transfer:**

To perform the style tranfer, two parameters are needed:

- `sentence`: (string) The input sentence you would like to transfer.
- `n_output`: (int) Number of sentences that should be provided in the output from the beam search.
- `max_len`: (int) **optional** Maximum length of output sentences. Default if not set: 256 characters.

```
http://34.147.33.58:8080/style?sentence=i%20am%20happy&n_output=3
http://34.147.33.58:8080/style?sentence=i%20am%20happy&n_output=3&max_len=42
```

remarks:

- Make sure to URL-encode the sentence
- In case of an error, the API returns a JSON object with details, e.g.:

```json
request: 34.147.33.58:8080/style

response:
{
    "code": 400,
    "name": "InvalidAPIUsage",
    "description": "No sentence provided! ?sentence="
}
```



## Maintenance

### Requirements

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

### Setup

Currently, the API and the model are managed using a flask server, which is deployed using a docker image from the container registry on a VM (Compute Instance) of the Google Cloud Platform. The flask code is contained in main.py. Its latest version is pushed to cloud storage and ingested into the deployment process to avoid a docker build on every new flask update.

Docker image on [Container Registry](https://console.cloud.google.com/gcr/images/apes-313514?project=apes-313514): 
`eu.gcr.io/apes-313514/flaskmrp`


VM

| option    | value
| --------- | ------------------------------------------------------
| name      | flask-mrp
| region    | europe-west4
| zone      | europe-west4-a
| machine   | general-purpose; N1; custom; 2vCPU 9GB memory
| container | tick: Deploy a container image to this VM instance
|           | container: `eu.gcr.io/apes-313514/flaskmrp`
|           | advanced options -> environment variables: PORT 8080
| boot disk | 20GB standard disk
| firewall  | allow HTTP-traffic

remarks:

- ports are automatically assigned from host to docker container, see https://cloud.google.com/compute/docs/containers/configuring-options-to-run-containers#publishing_container_ports

### Developing new flask features (main.js)
Implement your changes to the main.py file and test it locally. Building and deploying in the cloud for testing will get expensive. Execute following lines of commands to publish the new changes:

```bash
# publish the main.py file to google cloud storage
gsutil cp main.py gs://academia-assistant/backend-vm/main.py

# restart the docker container
### login to ssh console
gcloud beta compute ssh flask-mrp --zone europe-west4-a --project "apes-313514"
### show all running docker containers + copy container id of eu.gcr.io/apes-313514/flaskmrp
docker ps
### restart container (remembers the initial parameters, so all good)
docker restart <INPUT_CONTAINER_ID>
```


### Developing new docker features (all other files)
After all changes to the files are done, do:

```bash
# Build and submit docker image to container registry in Europe
gcloud builds submit --tag eu.gcr.io/apes-313514/flaskmrp --timeout=900

# Prune all old docker images to avoid filling up the disk
gcloud compute instances update-container flask-mrp --zone europe-west4-a --container-image=eu.gcr.io/apes-313514/flaskmrp --project "apes-313514"

# Update the docker container on the vm
gcloud beta compute ssh flask-mrp --zone europe-west4-a --project "apes-313514" --command 'docker system prune -f -a'
```





### Testing the software locally

For the flask system with model, do:

```bash
# build
make build

# run debug
docker run -it --rm -p 8080:8080 -e PORT=8080 wasp/backend
docker run -d -p 8080:8080 -e PORT=8080 wasp/backend
```

**For a flask system without model, see folder flask_no_model/**


## Open work

### Warnings to solve

```bash
/usr/local/lib/python3.9/site-packages/transformers/tokenization_utils_base.py:2126: FutureWarning: The `pad_to_max_length` argument is deprecated and will be removed in a future version, use `padding=True` or `padding='longest'` to pad to the longest sequence in the batch, or use `padding='max_length'` to pad to a max length. In this case, you can give a specific length with `max_length` (e.g. `max_length=45`) or leave max_length to None to pad to the maximal input size of the model (e.g. 512 for Bert).
  warnings.warn(
/usr/local/lib/python3.9/site-packages/transformers/models/t5/tokenization_t5.py:190: UserWarning: This sequence already has </s>. In future versions this behavior may lead to duplicated eos tokens being added.
```

### VM

#### devops - monitoring
- create alert for errors

- check metrics for the VM for disk, CPU & RAM (migrate to N2 instance for RAM?)
https://stackoverflow.com/questions/43991246/google-cloud-platform-how-to-monitor-memory-usage-of-vm-instances
extra costs: https://cloud.google.com/stackdriver/pricing#monitoring-costs

#### devops - public IP address
https://stackoverflow.com/questions/49501329/google-compute-engine-assigning-static-ip-pricing


### switching to AI platform and cloud functions

see resources below


## Resources

**VM**

- https://github.com/Julian-Nash/simple-flask-demo
- https://www.youtube.com/watch?v=a2g9pDleGQk
- https://pythonise.com/series/learning-flask/deploy-a-flask-app-nginx-uwsgi-virtual-machine

**AI platform**

- https://cloud.google.com/ai-platform/prediction/docs
- https://cloud.google.com/ai-platform/prediction/docs/machine-types-online-prediction#available_machine_types
- prices: https://cloud.google.com/ai-platform/prediction/pricing#prediction-prices
- price calculator: https://cloud.google.com/products/calculator
- https://cloud.google.com/sdk/gcloud/reference/ai-platform

**AI platform - custom container because of pyTorch**

- https://cloud.google.com/ai-platform/prediction/docs/use-custom-container


## Archive

First trials of deploying were done using Google Cloud Run (serverless system):

gcloud run deploy flaskmrp \
--image=eu.gcr.io/apes-313514/flaskmrp \
--concurrency=1 \
--cpu=2 \
--memory=4096Mi \
--max-instances=1 \
--platform=managed \
--region=us-east1 \
--project=apes-313514