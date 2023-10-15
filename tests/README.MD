### **How to Run Tests:**

Clone the repository and navigate to the `/tests` directory:

```shell
git clone https://github.com/temirovazat/cinemax-async-api.git
cd cinemax-async-api/tests/
```

Create a `.env` file and add the test settings:

```shell
nano .env
```

Add the following settings for the tests:

```shell
# Elasticsearch
ELASTIC_HOST=elastic
ELASTIC_PORT=9200

# Redis
REDIS_HOST=redis
REDIS_PORT=6379

# Service
URL_DOMAIN=fastapi
```

Deploy and run the tests in containers:

```shell
docker-compose up --build --exit-code-from tests
```

These instructions guide you on how to run the tests for the project.