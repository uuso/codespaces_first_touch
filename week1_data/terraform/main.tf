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
  # storage_access_key = "<storage-access-key>"
  # storage_secret_key = "<storage-secret-key>"
}

resource "yandex_storage_bucket" "log_bucket" {
  bucket = "my-tf-log-bucket-20240121"
}

resource "yandex_storage_bucket" "b" {
  bucket = "my-policy-bucket-20240121"
  acl    = "private"
  max_size = 1048576

  tags = {
    test_key = "test_value"
    other_key = "other_value"
  }

  logging {
    target_bucket = yandex_storage_bucket.log_bucket.id
    target_prefix = "log/"
  }  
}
