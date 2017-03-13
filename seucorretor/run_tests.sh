#! /bin/sh
#
# Run tests creating all the database

### Testa todas as apps
py.test --cov=.

### Testa uma app especifica
# py.test ibuscador --cov=ibuscador

### Gera resultado de cobertura de teste para HTML
# py.test --cov=. --cov-report html