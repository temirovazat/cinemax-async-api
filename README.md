## Cinemax Async API

[![python](https://img.shields.io/static/v1?label=python&message=3.8%20|%203.9%20|%203.10&color=informational)](https://github.com/temirovazat/cinemax-async-api/actions/workflows/main.yml)
[![dockerfile](https://img.shields.io/static/v1?label=dockerfile&message=published&color=2CB3E8)](https://hub.docker.com/r/temirovazat/async_api)
[![lint](https://img.shields.io/static/v1?label=lint&message=flake8%20|%20mypy&color=brightgreen)](https://github.com/temirovazat/cinemax-async-api/actions/workflows/main.yml)
[![code style](https://img.shields.io/static/v1?label=code%20style&message=WPS&color=orange)](https://wemake-python-styleguide.readthedocs.io/en/latest/)
[![tests](https://img.shields.io/static/v1?label=tests&message=%E2%9C%94%2015%20|%20%E2%9C%98%200&color=critical)](https://github.com/temirovazat/cinemax-async-api/actions/workflows/main.yml)

### **Description**

_The purpose of this project is to implement an asynchronous API for full-text movie search. To achieve this, an application was developed based on the specialized framework [FastAPI](https://fastapi.tiangolo.com). Elasticsearch is used as the storage engine. To avoid unnecessary load on the full-text search system, data caching is applied using [Redis](https://redis.io). The project is run under the control of an ASGI server (uvicorn) in conjunction with the HTTP server [NGINX](https://nginx.org). Functional tests using the [pytest](https://pytest.org) library have been written to verify the API's performance._

### **Technologies**

```Python``` ```FastAPI``` ```Elasticsearch``` ```Redis``` ```NGINX``` ```Gunicorn``` ```PyTest``` ```Docker```

### **How to Run the Project:**

Clone the repository and navigate to the `/infra` directory:

```bash
git clone https://github.com/temirovazat/cinemax-async-api.git
```

```bash
cd cinemax-async-api/infra/
```

Create a `.env` file and add project settings:

```bash
nano .env
```

```bash
# Elasticsearch
ELASTIC_HOST=elastic
ELASTIC_PORT=9200

# Redis
REDIS_HOST=redis
REDIS_PORT=6379
```

Deploy and run the project in containers:

```bash
docker-compose up
```

The API documentation will be available at:

```
http://127.0.0.1/openapi
```