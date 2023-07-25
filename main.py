from fastapi import FastAPI
from db import ConnectDB
from model import PaginatedTrades, Paginate, TradeList, emptyTradeList
from helpers import parse_cursor, get_trade_object

app = FastAPI()


@app.get('/')
def get_search_info(search: str | None = None) -> TradeList:
    """ The search method of the API """
    if search is None:
        return emptyTradeList
    else:
        print(f'search query: {search}')
        db = ConnectDB()
        collection = db.get_collection()
        query = {"$text": {'$search': search}}
        print(query)
        cursor = collection.find(query)
        trades = parse_cursor(cursor)
        print(len(trades))
        response = TradeList(
            content=trades,
            total=len(trades)
        )
        return response


@app.get('/trades', response_model=PaginatedTrades)
def get_trades_list(page: int = 1, page_size: int = 10):
    """ Getting a paginated list of trades """

    # Get the data from db
    db = ConnectDB()
    collection = db.get_collection()
    cursor = collection.find()
    trades = parse_cursor(cursor)
    total_data_len = len(trades)
    db.close()

    # Get the page
    start = (page - 1) * page_size
    end = start + page_size

    if end >= total_data_len:
        nxt = None

        if page > 1:
            prev = f'/trades?page={page-1}&page_size={page_size}'
        else:
            prev = None

    else:
        if page > 1:
            prev = f'/trades?page={page-1}&page_size={page_size}'
        else:
            prev = None

        nxt = f'/trades?page={page+1}&page_size={page_size}'

    return PaginatedTrades(
        content=trades[start:end],
        total=end - start + 1,
        count=page_size,
        paginate=Paginate(
            previous=prev,
            next=nxt
        )
    )


@app.get('/trades/{trade_id}', response_model=TradeList)
def get_trade_by_trade_id(trade_id: str):
    """ getting a trade by its trade_id """
    try:
        print('trade_id:',trade_id)
        db = ConnectDB()
        collection = db.get_collection()
        trade = collection.find_one({'trade_id': trade_id})
        # print(trade)
        if trade is None:
            return emptyTradeList
        
        trade = get_trade_object(trade)
        print(trade)
        return TradeList(
            content=trade,
            total=1
        )
    except Exception as exc:
        print(exc)
    finally:
        db.close()
