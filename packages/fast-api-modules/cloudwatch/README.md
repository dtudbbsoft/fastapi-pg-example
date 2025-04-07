## fast-api-cloudwatch

### Description

The Cloudwatch Logger for FastAPI.

### Installation

Install `fast-api-cloudwatch` into fast-api-server application using poetry.

```bash
poetry add ../packages/fast-api-modules/cloudwatch
```

### Type
- Module

### Required environment variables
```bash
LOGS_AWS_ACCESS_KEY_ID: str
LOGS_AWS_SECRET_ACCESS_KEY: str
LOGS_AWS_SESSION_TOKEN: str
```

### Links
[WatchTower logger](https://kislyuk.github.io/watchtower/)

### External dependencies

- boto3
- watchtower
- colorlog

