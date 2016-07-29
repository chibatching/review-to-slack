# review-to-slack

Post application review on Google Play Store to Slack

## Install dependent add ons

```
heroku addons:create scheduler:standard
heroku addons:create heroku-redis:hobby-dev
```

## Set environment variable to heroku

```
heroku config:set SLACK_TOKEN=YOUR_SLACK_TOKEN
heroku config:set REDIS_URL=YOUR_REDIS_URL
heroku config:set PACKAGE_CHANNEL="{\"YOUR_APP_PACKAGE_NAME\":\"YOUR_SLACK_CHANNEL_TO_POST\"}"
python reviewtoslack/credential_helper.py YOUR_CREDENTIAL_JSON_FILE
```

## Add task to Heroku Scheduler

```
python reviewtoslack/tasks.py
```
