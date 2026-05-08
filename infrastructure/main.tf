terraform {
  required_providers {
    minio = {
      source  = "aminueza/minio"
      version = "~> 2.0"
    }
  }
}

provider "minio" {
  minio_server   = "localhost:9000"
  minio_user     = "payflow"
  minio_password = "payflow123"
}

resource "minio_s3_bucket" "bronze" {
  bucket = "bronze"
  acl    = "private"
}

resource "minio_s3_bucket" "silver" {
  bucket = "silver"
  acl    = "private"
}

resource "minio_s3_bucket" "gold" {
  bucket = "gold"
  acl    = "private"
}