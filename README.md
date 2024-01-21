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


## Terraform

https://www.youtube.com/watch?v=Y2ux7gq3Z0o&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=14

Установить yandex cli
https://cloud.yandex.ru/ru/docs/cli/quickstart#install 

```bash
curl -sSL https://storage.yandexcloud.net/yandexcloud-yc/install.sh | bash
echo 'source /home/codespace/yandex-cloud/completion.zsh.inc' >>  ~/.zshrc
source "/home/codespace/.bashrc"
# yc init -- передумал, т.к. даст полные права к аккаунту клауда
```

Буду устанавливать terraform для доступа к яндекс облаку, что-то придумаю вместо BigQuery
https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli

```bash
sudo apt-get update && sudo apt-get install -y gnupg software-properties-common

wget -O- https://apt.releases.hashicorp.com/gpg | \
gpg --dearmor | \
sudo tee /usr/share/keyrings/hashicorp-archive-keyring.gpg

gpg --no-default-keyring \
--keyring /usr/share/keyrings/hashicorp-archive-keyring.gpg \
--fingerprint

echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] \
https://apt.releases.hashicorp.com $(lsb_release -cs) main" | \
sudo tee /etc/apt/sources.list.d/hashicorp.list

sudo apt update

sudo apt-get install terraform

terraform -help

touch ~/.zshrc

terraform -install-autocomplete
```

Создал .gitignore с */key/

https://cloud.yandex.ru/ru/docs/iam/operations/authorized-key/create#cli_1

```bash
yc iam key create --service-account-name terraform-test -o key/terraform-test-api-key.json

yc resource-manager cloud list && yc resource-manager folder list

yc config profile create terraform-test
yc config set service-account-key key/terraform-test-api-key.json
yc config set cloud-id <идентификатор_облака>
yc config set folder-id <идентификатор_каталога>  

export YC_TOKEN=$(yc iam create-token)
export YC_CLOUD_ID=$(yc config get cloud-id)
export YC_FOLDER_ID=$(yc config get folder-id)
```

Настройка работы с YC закончена

### Настройка terraform [@cloud.yandex.ru](https://cloud.yandex.ru/docs/tutorials/infrastructure-management/terraform-quickstart#configure-provider)

```bash
mv ~/.terraformrc ~/.terraformrc.old
nano ~/.terraformrc
```

```
provider_installation {
  network_mirror {
    url = "https://terraform-mirror.yandexcloud.net/"
    include = ["registry.terraform.io/*/*"]
  }
  direct {
    exclude = ["registry.terraform.io/*/*"]
  }
}
```

Заготовка для файлов *.tf:
```
terraform {
  required_providers {
    yandex = {
      source = "yandex-cloud/yandex"
    }
  }
  required_version = ">= 0.13"
}

provider "yandex" {
  zone = "ru-central1-a"
}
```

```bash
terraform init
terraform plan
terraform apply
```

Для работы apply потребовался ещё статический ключ для аккаунта 

https://cloud.yandex.ru/ru/docs/iam/operations/sa/create-access-key#console_1

https://github.com/yandex-cloud/terraform-provider-yandex/issues/179