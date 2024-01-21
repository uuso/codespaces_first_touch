# codespaces_first_touch

## week1 docker
```Dockerfile
FROM python:3.9

RUN pip install pandas

ENTRYPOINT ["bash"]
```
```bash
docker build -t test:pandas .
docker run -it --rm test:pandas
```

```Dockerfile
FROM python:3.9

RUN pip install pandas
WORKDIR /app

COPY pipeline.py pipeline.py

ENTRYPOINT ["python", "pipeline.py"]
```
```bash
docker build -t test:pandas .
docker run -it --rm test:pandas 2023-04-04
```
