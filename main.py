from fastapi import FastAPI
from db import ConnectDB
from model import Trade
from bson.objectid import ObjectId

app = FastAPI()

def parse_str(st: str) -> str:
    """ Parsing the search string """
    try:
        st_ = [i for i in st.split(' ') if i != '' or i != ' ']
        st_ = [i[0].upper() + i[1:] for i in st_]
        return ' '.join(st_)
    except:
        return st
    

def update_dict_keys(dct: dict, keys: dict) -> dict:
    """ Changes the values of KEYS of a dictionary with the mapping provided in 2nd parameter """
    updated_dict = dct.copy()
    for old_key, new_key in keys.items():
        if old_key in updated_dict:
            updated_dict[new_key] = updated_dict.pop(old_key)
    return updated_dict

def get_trade_object(raw_trade) ->Trade:
    """ Converts a single mongodb response to a Trade object for further parsing to JSON """
    trade = dict(raw_trade)
    del trade['_id']
    key_map = {
        'asset_class':'assetClass','instrument_id':'instrumentId',
        'instrument_name':'instrumentName','trade_date_time':'tradeDateTime',
        'trade_details':'tradeDetails','trade_id':'tradeId'
        }
    return Trade(**update_dict_keys(trade,key_map))

def parse_cursor(cursor) -> list[Trade]:
    """ Parses a mongodb cursor, to convert it into a list of Trade objects """
    trades = []
    for trade in cursor:
        trade = get_trade_object(trade)
        trades.append(trade)
    return trades


@app.get('/')
def get_search_info(search:str | None = None):
    """ The search method of the API """
    if not search:
        return {'api status':'online'}
    else:
        print(f'search query: {search}')
        db = ConnectDB()
        collection = db.get_collection()
        query = {"$text":{'$search':parse_str(search)}}
        print(query)
        cursor = collection.find(query)
        trades = parse_cursor(cursor)
        print(len(trades))
        response = {
            'data':trades,
            'length':len(trades)
        }
        return response


@app.get('/trades')
def get_trades_list() -> list[Trade]:
    """ getting a paginated list of trades """
    db = ConnectDB()
    collection = db.get_collection()
    cursor = collection.find()
    # print(len(cursor))
    trades = parse_cursor(cursor)
    print(len(trades))
    db.close()
    return {
        'data':trades,
        'length':len(trades)
    }


@app.get('/trades/{trade_id}')
def get_trade_by_trade_id(trade_id: str) -> Trade:
    """ getting a trade by its trade_id """
    try:
        print(trade_id)
        db = ConnectDB()
        collection = db.get_collection()
        trade = collection.find_one({'trade_id':trade_id})
        print(trade)
        trade = get_trade_object(trade)
        print(trade)
        return {
            'data':trade
        }
    except Exception as exc:
        print(exc)
    finally:
        db.close()
