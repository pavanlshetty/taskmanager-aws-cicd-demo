    terraform {
        backend "s3" {
        bucket = "pavan-terraform-state-bucket-1312"
        key    = "dev/terraform.tfstate"
        region = "ap-south-1"
        encrypt = true
        use_lockfile = false
    }
}