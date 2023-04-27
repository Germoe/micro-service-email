GMail Micro Service on Google Cloud Run

This is a self-hosted micro-service that allows you to send emails using your own GMail account. It is hosted in your Google Cloud Project and requires almost no configuration. It is perfect for quick prototyping where you need to send out e-mail via a POST request without the hassle of setting up new accounts etc.

## Setup 

This setup assumes you don't have a Google Cloud Project or Google App Password yet. If you do just skip ahead to the [Deploy](#deploy) section.

### Google Cloud Project
1. Create a new Google Cloud Project at https://console.cloud.google.com/projectcreate
2. Enable the Google Cloud Run API at https://console.cloud.google.com/apis/library/run.googleapis.com
3. Configure your Google Cloud Project locally:
   1. Install Google Cloud SDK: https://cloud.google.com/sdk/docs/install
   2. Login to your Google Cloud Account: `gcloud auth login`
   3. Create a Project Config: `gcloud config configurations create micro-service-email`
   4. Activate the new Project Config: `gcloud config configurations activate micro-service-email`
   5. Set the Project ID: `gcloud config set project <your-project-id>`

### Google App Password
The service works with Google Gmail so in order to use it you need to get an App Password from Google. You can do that here: https://myaccount.google.com/apppasswords (note that this requires 2FA to be enabled on your account).

1. Select "Other (Custom name)" from the dropdown
2. Give it a name (e.g. "Micro Service Email")
3. Copy the generated password for later

### Environment Variables
The service requires the following environment variables to be set:
- `GMAIL_USER` - Your Gmail address (e.g. `test.user@gmail.com`)
- `GMAIL_PASSWORD` - The App Password you generated above (e.g. `abc123def456`)
- `API_KEY` - A random string that will be used to secure the service (e.g. `abc123def456`)
  - You can generate one here for example: https://codepen.io/corenominal/pen/rxOmMJ

These variables will be attached directly to the deployment in the next section. 

## Deploy

There is two options to deploy to cloud run:
  1. The Google Cloud Registry (GCR) image `gcr.io/micro-services-385011/micro-service-email:latest` 
  2. Build your own image from the Dockerfile in this repo.

### Deploy from GCR (recommended / easier)
  1. Deploy the service to Cloud Run: 

```bash
gcloud run deploy micro-service-email
    --image gcr.io/micro-services-385011/micro-service-email:latest 
    --platform managed 
    --region us-central1 
    --allow-unauthenticated 
    --set-env-vars GMAIL_USER={{ GMAIL_USER }},GMAIL_PASSWORD={{ GMAIL_PASSWORD }},API_KEY={{ API_KEY }}
```

### Deploy from Dockerfile
First we'll build the image locally and test it, then we'll push it to GCR and deploy it to Cloud Run.

#### Build and Test Locally
  1. Build the image: `docker build -t micro-service-email .`
  2. Test the image: `docker run -p 8080:8080 -e GMAIL_USER={{ GMAIL_USER }} -e GMAIL_APP_PASSWORD={{ GMAIL_APP_PASSWORD }} -e API_KEY={{ API_KEY }} micro-service-email`
  3. Send a test request:

```bash
curl --location 'http://127.0.0.1:8080/send-email' \
--header 'x-api-key: {{ API_KEY }}' \
--form 'subject="{{ TEST_SUBJECT }}"' \
--form 'body="{{ TEST_CONTENT (HTML) }}"' \
--form 'to="{{ TO_EMAIL }}"'
```

#### Push to GCR and Deploy

1. Activate Google Container Registry API https://console.cloud.google.com/apis/library/containerregistry.googleapis.com
2. Configure Docker: `gcloud auth configure-docker`
3. Rebuild the image for the Google Platform: `docker build -t micro-service-email . --platform=linux/amd64`
4. Tag the image: `docker tag micro-service-email gcr.io/{{ PROJECT_ID }}/micro-service-email`
5. Push the docker image to the path defined by your tag above (need to be identical): `docker push gcr.io/{{ PROJECT_ID }}/micro-service-email`
6. You can check whether the artifact was uploaded successfully by navigating to https://console.cloud.google.com/gcr/images/ and selecting your project

#### Deploy to Cloud Run from your own image

1. Deploy the service to Cloud Run
```bash
gcloud run deploy micro-service-email
    --image gcr.io/{{ PROJECT_ID }}/micro-service-email 
    --platform managed 
    --region us-central1 
    --allow-unauthenticated 
    --set-env-vars GMAIL_USER={{ GMAIL_USER }},GMAIL_PASSWORD={{ GMAIL_PASSWORD }},API_KEY={{ API_KEY }}
```

## Usage

Once the service is deployed you can send emails by sending a POST request to the `/send-email` endpoint. The request must contain the following headers:
- `x-api-key` - The API key you defined in the environment variables

Example:
```bash
curl --location 'https://{{ CLOUD_RUN_ADDRESS }}.a.run.app/send-email' \
--header 'x-api-key: {{ API_KEY }}' \
--form 'subject="{{ TEST_SUBJECT }}"' \
--form 'body="{{ TEST_CONTENT (HTML) }}"' \
--form 'to="{{ TO_EMAIL }}"'
```
