### Objective

This is an internal API for an exemplary financial institution implemented in Python and Django. Use the Swagger UI to interact with the API calls intuitively.

### Brief

While modern banks have evolved to serve a plethora of functions, at their core, banks must provide certain basic features. This repository implements the basic HTTP API for employees of one of those banks! It could ultimately be consumed by multiple frontends (web, iOS, Android etc).

There are API routes implemented that allow bank employees to:

- Create a new bank account for a customer, with an initial deposit amount. A
    single customer may have multiple bank accounts.
- Transfer amounts between any two accounts, including those owned by
    different customers.
- Retrieve balances for a given account.
- Retrieve transfer history for a given account.

### Getting started

1. create and activate a virtual environment
2. install the requirements
3. Start the django server by executing
  `python manage.py runserver`

Use the Swagger API user interface to interact with the API. Populate your customers, create accounts and transfer money between them. Feel free to populate your customers with the following:

```json
[
  {
    "id": 1,
    "name": "Arisha Barron"
  },
  {
    "id": 2,
    "name": "Branden Gibson"
  },
  {
    "id": 3,
    "name": "Rhonda Church"
  },
  {
    "id": 4,
    "name": "Georgina Hazel"
  }
]
```
