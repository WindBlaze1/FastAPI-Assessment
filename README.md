# FastAPI Trade API

This is a REST API built with the FastAPI framework, serving Trade data from a mocked database. The API allows users to retrieve a list of trades, fetch a single trade by ID, search for trades based on specific fields, and filter trades using various query parameters.

## Setup

To run this API locally, make sure you have Python installed on your system. You can install the required packages using the following command:

```bash
pip install fastapi uvicorn
```

## Running the API

Save the code into a Python file (e.g., `main.py`), and then run the API with the following command:

```bash
uvicorn main:app --reload
```

The API will be accessible at `http://localhost:8000`.

## API Endpoints

### 1. Listing Trades

#### Request

- Method: `GET`
- Endpoint: `/trades/`

#### Response

- Returns a list of all trades.

### 2. Single Trade

#### Request

- Method: `GET`
- Endpoint: `/trades/{trade_id}/`
- Path Parameters:
  - `trade_id`: The unique ID of the trade.

#### Response

- Returns the details of a single trade based on the provided `trade_id`.

### 3. Searching Trades

#### Request

- Method: `GET`
- Endpoint: `/trades/search/`
- Query Parameters:
  - `search`: Text to search for in the following fields:
    - `counterparty`
    - `instrumentId`
    - `instrumentName`
    - `trader`

#### Response

- Returns a list of trades that match the search query.

### 4. Advanced Filtering

#### Request

- Method: `GET`
- Endpoint: `/trades/filter/`
- Query Parameters:
  - `assetClass`: Asset class of the trade.
  - `end`: The maximum date for the `tradeDateTime` field.
  - `maxPrice`: The maximum value for the `tradeDetails.price` field.
  - `minPrice`: The minimum value for the `tradeDetails.price` field.
  - `start`: The minimum date for the `tradeDateTime` field.
  - `tradeType`: The `tradeDetails.buySellIndicator` is a BUY or SELL.

#### Response

- Returns a list of trades that match the specified filter criteria.

### Bonus: Pagination and Sorting

#### Request

- Method: `GET`
- Endpoint: `/trades/`
- Query Parameters:
  - `skip`: Number of records to skip for pagination.
  - `limit`: Number of records to limit for pagination.
  - `sort`: Field to sort the trades. (e.g., `sort=tradeDateTime`)

#### Response

- Returns a paginated list of trades with optional sorting.
