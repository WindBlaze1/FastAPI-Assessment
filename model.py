""" imports """
import datetime as dt
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field


class SortOrder(str, Enum):
    """ A Class to get the order of sorting """
    ASC = 'asc'
    DESC = 'desc'

class TradeType(str, Enum):
    """ A value of BUY for buys, SELL for sells. """
    BUY = 'BUY'
    SELL = 'SELL'


class TradeDetails(BaseModel):
    buySellIndicator: TradeType = Field(
        description="A value of BUY for buys, SELL for sells.")

    price: float = Field(description="The price of the Trade.")

    quantity: int = Field(description="The amount of units traded.")


class Trade(BaseModel):
    asset_class: Optional[str] = Field(
        alias="assetClass", default=None, description="The asset class of the instrument\
              traded. E.g. Bond, Equity, FX...etc")

    counterparty: Optional[str] = Field(
        default=None, description="The counterparty the trade was executed with. \
            May not always be available")

    instrument_id: str = Field(
        alias="instrumentId", description="The ISIN/ID of the instrument traded. \
            E.g. TSLA, AAPL, AMZN...etc")

    instrument_name: str = Field(
        alias="instrumentName", description="The name of the instrument traded.")

    trade_date_time: dt.datetime = Field(
        alias="tradeDateTime", description="The date-time the Trade was executed")

    trade_details: TradeDetails = Field(
        alias="tradeDetails", description="The details of the trade, i.e. price, quantity")

    trade_id: str = Field(alias="tradeId", default=None,
                          description="The unique ID of the trade")

    trader: str = Field(description="The name of the Trader")


class Paginate(BaseModel):
    """ Store previous and next page URLs """
    previous: str | None = None
    next: str | None = None


class PaginatedTrades(BaseModel):
    """ Class to Paginate the Trade List """
    content: List[Trade]
    total: int
    count: int
    page: int
    paginate: Paginate


class TradeList(BaseModel):
    """ Class to return a list of Trades """
    content: List[Trade]
    total: int


emptyTradeList = TradeList(content=[], total=0)
