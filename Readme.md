uv run uvicorn main:app --reload

## Requirements 📋
- Python 3.11+

## Setup 🛠️
1. Install uv (follow instructions [here](https://docs.astral.sh/uv/#getting-started))

2. Clone the repository:
```bash
git clone <>
cd api-restful\ejercicio1
```

3. Install dependencies with uv:
```bash
uv sync
```

4. Set up environment variables:
```bash
cp .env.example .env
```
5. Start the application:

```bash
uv run uvicorn main:app --reload
```


## Open the browser

Go to `http://localhost:8000/docs` to see the API documentation.

## Docker Deployment

The application can be easily containerized using Docker. Follow these steps to build and run the container:

### 1. Build the Docker Image
From the project root directory, run:

```bash
docker build -t api-restful -f Dockerfile .
```

This command will:
- Use the `Dockerfile` to build the image
- Tag the image as `api-restful`
- Install all dependencies using `uv`
- Set up the environment variables

### 2. Run the Docker Container
After building the image, start the container with:

```bash
docker run -p 8000:8000 api-restful
```

This command will:
- Map port 80 from the container to port 8000 on your host machine
- Start the FastAPI application using Uvicorn
- Make the API available at `http://localhost:8000`
