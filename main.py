""" imports """
from datetime import datetime
from fastapi import FastAPI, Query, HTTPException
from db import ConnectDB
from pymongo import ASCENDING, DESCENDING
from model import PaginatedTrades, Paginate, TradeList, emptyTradeList, SortOrder, TradeType
from helpers import parse_cursor, get_trade_object, get_sorted

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
        query = {"$text": {'$search': f'^"{search}"$'}}
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
def get_trades_list(
    page: int = 1, page_size: int = Query(10, description='The maximum trades displayed per page.'),

    sort: bool = False, order: SortOrder = SortOrder.ASC,

    sort_col: int = Query(
        1, description="""
            Sort according to any column.
            values:
            1: asset_class
            2: counterparty
            3: instrument_id
            4: instrument_name
            5: trade_date_time
            6: buySellIndicator
            7: price
            8: quantity
            9: trader""", lt=10, gt=0
    ),

    asset_class: str | None = Query(
        None, description='Asset class of the trade.'),

    end: str | None = Query(
        None, description="The maximum date for the tradeDateTime field in ISO 8601 format \
            (YYYY-MM-DD)", regex=r'^\d{4}-\d{2}-\d{2}$'),

    max_price: int | None = Query(
        None, description='The maximum value for the tradeDetails.price field.'),

    min_price: int | None = Query(
        None, description='The minimum value for the tradeDetails.price field.'),

    start: str | None = Query(
        None, description="The minimum date for the tradeDateTime field in ISO 8601 format \
            (YYYY-MM-DD)", regex=r'^\d{4}-\d{2}-\d{2}$'),

    trade_type: TradeType | None = Query(
        None, description='The tradeDetails.buySellIndicator is a BUY or SELL')
) -> HTTPException | PaginatedTrades:
    """ Getting a paginated list of trades, with advanced[acc. to any of the folders] sorting[asc/desc] and advanced filters."""

    # Fetch the advanced filtering criteria:
    filters = {}

    if asset_class:
        filters['asset_class'] = asset_class

    if trade_type:
        filters['trade_details.buySellIndicator'] = trade_type

    if end or start:

        date_filter = {}
        lst = []

        if end:
            lst.append([end, '$lte'])

        if start:
            lst.append([start, '$gte'])

        for data in lst:

            try:
                print('here', type(data[0]), data[0])
                date = datetime.fromisoformat(data[0])
                date_filter[data[1]] = date

            except ValueError as err:
                raise HTTPException(status_code=400, detail=str(err)) from err

        filters['trade_date_time'] = date_filter

    if max_price or min_price:

        price_filter = {}

        if max_price:
            price_filter['$lte'] = max_price

        if min_price:
            price_filter['$gte'] = min_price

        filters['trade_details.price'] = price_filter

    print('filters provided:', filters)
    # Get the sorting order
    if sort:
        if order is SortOrder.ASC:
            sort_order = ASCENDING
        else:
            sort_order = DESCENDING

    # Get the data from db
    db = ConnectDB()
    collection = db.get_collection()
    cursor = collection.find(filters)
    if sort:
        cursor = cursor.sort(get_sorted(sort_col), direction=sort_order)
    trades = parse_cursor(cursor)
    # print(trades)
    total_data_len = len(trades)
    db.close()

    # Get the page
    first = (page - 1) * page_size
    last = first + page_size

    if last >= total_data_len:
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
        content=trades[first:last],
        total=len(trades),
        count=min(page_size, len(trades[first:])),  # On the final page,
                                                    # the count of total results should be exact
        page=page,
        paginate=Paginate(
            previous=prev,
            next=nxt
        )
    )


@app.get('/trades/{trade_id}', response_model=TradeList)
def get_trade_by_trade_id(trade_id: str):
    """ getting a trade by its trade_id """
    try:
        print('trade_id:', trade_id)
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
