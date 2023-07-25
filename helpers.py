""" imports """
from model import Trade, SortColumn


def get_sorted(choice):
    choices = {1: SortColumn.ONE,
               2: SortColumn.TWO,
               3: SortColumn.THREE,
               4: SortColumn.FOUR,
               5: SortColumn.FIVE,
               6: SortColumn.SIX,
               7: SortColumn.SEVEN,
               8: SortColumn.EIGHT,
               9: SortColumn.NINE, }
    return choices[choice]


def update_dict_keys(dct: dict, keys: dict) -> dict:
    """ Changes the values of KEYS of a dictionary with the mapping provided in 2nd parameter """
    updated_dict = dct.copy()
    for old_key, new_key in keys.items():
        if old_key in updated_dict:
            updated_dict[new_key] = updated_dict.pop(old_key)
    return updated_dict


def get_trade_object(raw_trade) -> Trade:
    """ Converts a single mongodb response to a Trade object for further parsing to JSON """
    trade = dict(raw_trade)
    del trade['_id']
    key_map = {
        'asset_class': 'assetClass', 'instrument_id': 'instrumentId',
        'instrument_name': 'instrumentName', 'trade_date_time': 'tradeDateTime',
        'trade_details': 'tradeDetails', 'trade_id': 'tradeId'
    }
    return Trade(**update_dict_keys(trade, key_map))


def parse_cursor(cursor) -> list[Trade]:
    """ Parses a mongodb cursor, to convert it into a list of Trade objects """
    trades = []
    for trade in cursor:
        trade = get_trade_object(trade)
        trades.append(trade)
    return trades
