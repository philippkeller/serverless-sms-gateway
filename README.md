# Installation

(Mostly for myself for whenever I switch laptop in the future and want to get this thing running again)

## Prerequisites

- Set up an IAM user with admin and get AWS_KEY and SECRET_KEY: See [here](https://hackernoon.com/creating-serverless-functions-with-python-and-aws-lambda-901d202d45dc#3dd0) for how to set this up
- Node (minimum version 6 AFAIR)
- Docker: `sudo apt install docker`, `sudo usermod -a -G docker $USER`

## Setup

```
sudo npm install -g serverless
serverless config credentials --provider aws --key AWS_KEY --secret SECRET_KEY
serverless deploy
```

## Initial

```
cp secrets-example.yml secrets.yml
vim secrets.yml # put in twilio secret etc.
```

# Deployment

- Deploy to prod: `serverless deploy --stage prod`
- See logs: `sls logs --stage prod -f sms -t`