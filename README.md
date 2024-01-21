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

practicing with docker & pg & github codespaces as it is described @ https://www.youtube.com/watch?v=XOSUt8Ih3zA&list=PL3MmuxUbc_hKihpnNQ9qtTmWYy26bPrSb&index=2


make postgres containr:
docker run -it --rm \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v $(pwd)/week_1_data/database_files:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:13

  how to run pgcli:
  pip install pgcli && pgcli -h localhost -p 5432 -u root -d ny_taxi


  wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz 
  gunzip
  

  df = pd.read_csv('yellow_tripdata_2021-01.csv', \
                 parse_dates=['tpep_pickup_datetime', 'tpep_dropoff_datetime'], \
                 iterator=True, chunksize=100000 )


docker run -it --rm \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -p 8080:80 \
  dpage/pgadmin4



```bash Запуск двух контейнеров в одной сети
docker network create pg-network

docker run -it \
-e POSTGRES_USER="root" \
-e POSTGRES_PASSWORD="root" \
-e POSTGRES_DB="ny_taxi" \
-v $(pwd)/pgdb_data:/var/lib/postgresql/data \
-p 5432:5432 \
--network=pg-network \
--name pg-database \
postgres:13


docker run -it \
-e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
-e PGADMIN_DEFAULT_PASSWORD="root" \
-p 8080:80 \
--network=pg-network \
--name pgadm \
dpage/pgadmin4
```


jupyter nbconvert --to=script Untitled.ipynb

pip install sqlalchemy psycopg2

python pipeline.py \
--user root \
--password root \
--host localhost \
--port 5432 \
--db ny_taxi \
--table_name ny_taxi \
--url "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"

wget $URL -O $ARCH_NAME && gzip -d -c $ARCH_NAME > $CSV_NAME && rm $ARCH_NAME

docker run -it --network=pg-network test:v1 \
--user root \
--password root \
--host pg-database \
--port 5432 \
--db ny_taxi \
--table_name ny_taxi \
--url "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"


### task 3 

apt-get install docker-compose

docker run -it --network=week1_data_default test:v1 \
--user root \
--password root \
--host pgdatabase \
--port 5432 \
--db ny_taxi \
--table_name ny_taxi \
--url "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"
