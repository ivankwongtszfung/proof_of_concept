# PSQL SQLALCHEMY POC

A small proof of concept/demo of some Database manipulation

[![Python version][shield-python]](#)
[![docker version][shield-docker]](#)
[![MIT licensed][shield-license]](#)

## Table of Contents

- [PSQL SQLALCHEMY POC](#psql-sqlalchemy-poc)
  - [Table of Contents](#table-of-contents)
  - [Requirements](#requirements)
  - [Get Started](#get-started)
  - [License](#license)

## Requirements

Paddington requires the following to run:

- python 3.6+
- docker

## Get Started

```sh
# setup the postgres sql db
docker run --name some-postgres -e POSTGRES_PASSWORD=mysecretpassword -p 5432:5432 -d postgres

# set up the virual environment for python
pip install virtualenv
virtualenv venv
. venv/bin/activate
# . venv/Scripts/activate # For Windows

# install libraries
pip install -r requirement.txt
python psql_acid_test.py
```

## License

Paddington is licensed under the [MIT](#) license.  
Copyright &copy; 2021, Ivan Kwong

[shield-python]: https://img.shields.io/badge/python-%3E3.6-blue
[shield-docker]: https://img.shields.io/badge/docker-postgre-blue
[shield-license]: https://img.shields.io/badge/license-MIT-blue.svg
