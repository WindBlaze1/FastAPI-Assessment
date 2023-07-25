# FastAPI Trade API

This is a REST API built with the FastAPI framework, serving trade data from a mocked database. The API allows users to retrieve a list of trades, fetch a single trade by ID, search for trades based on specific fields, and filter trades using various query parameters. It also supports pagination and sorting for a better user experience.

## Table of Contents

- [Introduction](#introduction)
- [Setup](#setup)
- [Project Details](#project-details)
- [API Endpoints](#api-endpoints)
  - [List All Trades](#1-list-all-trades)
  - [Fetch Single Trade](#2-fetch-single-trade)
  - [Search Trades](#3-search-trades)
  - [Advanced Filtering](#4-advanced-filtering)
  - [Pagination and Sorting](#5-pagination-and-sorting)
- [Test the API](#test-the-api)
- [Access API Documentation](#access-api-documentation)

## Introduction

The FastAPI Trade API is designed to provide a simple and efficient way to access trade data. It utilizes the FastAPI framework, which offers high performance and automatic validation of request data through Pydantic models. The API uses a MongoDB Atlas database to store and retrieve trade information.

## Setup

To run this API in a virtual environment, follow these steps:

1. Clone the repository to your local machine.
2. Create a virtual environment using `virtualenv`:

   ```bash
   virtualenv venv
   ```

3. Activate the virtual environment:

   - On Windows:

   ```bash
   venv\Scripts\activate
   ```

   - On macOS and Linux:

   ```bash
   source venv/bin/activate
   ```

4. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

## Project Details

The project consists of the following files:

- `main.py`: Contains the FastAPI application with API endpoints and logic.
- `db.py`: Manages the connection to the MongoDB Atlas database.
- `helpers.py`: Provides helper functions for data manipulation and parsing.
- `mock_data.py`: Generates and uploads fake trade data to the database for testing purposes.
- `model.py`: Defines Pydantic models for data validation and serialization.
- `requirements.txt`: Lists the required Python packages and their versions.
- `test_app.py`: Test script to verify the API functionality using HTTP requests.
- `README.md`: Documentation of the API, its usage, and setup instructions.

## API Endpoints

The API provides the following endpoints to interact with the trade data:

### 1. List All Trades

To retrieve a list of all trades, send a GET request to the `/trades` endpoint:

```http
GET http://localhost:8000/trades
```

#### Response

```json
{
  "content": [
    {
      "assetClass": "Equity",
      "counterparty": "John Doe",
      "instrumentId": "AAPL",
      "instrumentName": "Apple Inc.",
      "tradeDateTime": "2023-07-26T10:30:00",
      "tradeDetails": {
        "buySellIndicator": "BUY",
        "price": 1520.75,
        "quantity": 250
      },
      "tradeId": "613bc0e32f7110e9d276f1ab",
      "trader": "Jane Smith"
    },
    // Additional trade objects...
  ],
  "total": 108,
  "count": 10,
  "page": 1,
  "paginate": {
    "previous": null,
    "next": "/trades?page=2&page_size=10"
  }
}
```

### 2. Fetch Single Trade

To fetch details of a single trade by its unique ID, send a GET request to the `/trades/{trade_id}/` endpoint with the `trade_id` path parameter:

```http
GET http://localhost:8000/trades/613bc0e32f7110e9d276f1ab/
```

#### Response

```json
{
  "content": {
    "assetClass": "Equity",
    "counterparty": "John Doe",
    "instrumentId": "AAPL",
    "instrumentName": "Apple Inc.",
    "tradeDateTime": "2023-07-26T10:30:00",
    "tradeDetails": {
      "buySellIndicator": "BUY",
      "price": 1520.75,
      "quantity": 250
    },
    "tradeId": "613bc0e32f7110e9d276f1ab",
    "trader": "Jane Smith"
  },
  "total": 1
}
```

### 3. Search Trades

To search for trades that match a specific text query, send a GET request to the `/` endpoint with the `search` query parameter:

```http
GET http://localhost:8000/?search=john
```

#### Response

```json
{
  "content": [
    {
      "assetClass": "Equity",
      "counterparty": "John Doe",
      "instrumentId": "AAPL",
      "instrumentName": "Apple Inc.",
      "tradeDateTime": "2023-07-26T10:30:00",
      "tradeDetails": {
        "buySellIndicator": "BUY",
        "price": 1520.75,
        "quantity": 250
      },
      "tradeId": "613bc0e32f7110e9d276f1ab",
      "trader": "Jane Smith"
    },
    // Additional trade objects matching the query...
  ],
  "total": 3
}
```

### 4. Advanced Filtering

To filter trades based on advanced query parameters, send a GET request to the `/trades` endpoint with the desired parameters:

```http
GET http://localhost:8000/trades?assetClass=Equity&tradeType=BUY&minPrice=1000
```

#### Response

```json
{
  "content": [
    {
      "assetClass": "Equity",
      "counterparty": "John Doe",
      "instrumentId": "AAPL",
      "instrumentName": "Apple Inc.",
      "tradeDateTime": "2023-07-26T10:30:00",
      "tradeDetails": {
        "buySellIndicator": "BUY",
        "price": 1520.75,
        "quantity": 250
      },
      "tradeId": "613bc0e32f7110e9d276f1ab",
      "trader": "Jane Smith"
    },
    // Additional trade objects matching the filter...
  ],
  "total": 108,
  "count": 10,
  "page": 1,
  "paginate": {
    "previous": null,
    "next": "/trades?page=2&page_size=10"
  }
}
```

### 5. Pagination and Sorting

To get a paginated and sorted list of trades, send a GET request to the `/trades` endpoint with the pagination and sorting parameters [can be sorted in asc/desc - and any of the columns can be sorted. To know more, try running the project and reading the documentation on `localhost:8000/docs`]:

```http
GET http://localhost:8000/trades?page=2&page_size=10&sort=true&order=desc&sort_col=5
```

#### Response

```json
{
  "content": [
    {
      "assetClass": "FX",
      "counterparty": "John Doe",
      "instrumentId": "EURUSD",
      "instrumentName": "Euro/US Dollar",
      "tradeDateTime": "2023-07-26T14:45:00",
      "tradeDetails": {
        "buySellIndicator": "SELL",
        "price": 1.1756,
        "quantity": 500
      },
      "tradeId": "613bc0e32f7110e9d276f1b1",
      "trader": "Jane Smith"
    },
    // Additional trade objects...
  ],
  "total": 100,
  "count": 10,
  "page": 2,
  "paginate": {
    "previous": "http://localhost:8000/trades/?page=1&page_size=10&sort=true&order=desc&sort_col=5",


    "next": null
  }
}
```

## Test the API

To test the API endpoints using the provided `test_app.py` script, run the following command in your terminal after starting the API:

```bash
python test_app.py
```

The script sends various HTTP requests to the API and displays the responses, ensuring that the API behaves as expected for different scenarios.

## Access API Documentation

Once the API is running, you can access the interactive API documentation (Swagger UI) by opening the following URL in your web browser:

```url
http://localhost:8000/docs
```

The documentation provides detailed information about the API endpoints, request parameters, and response models. It also allows you to test the API directly from the browser.
