import datetime as dt
import random
from time import sleep
from db import ConnectDB
from faker import Faker
from pydantic import ValidationError
from bson.objectid import ObjectId
from model import TradeDetails, Trade


def generate_fake_data(N: int = 100) -> list:
    fake = Faker()
    print(N)

    # Mocked database and sample trade data
    mock_data = []
    for _ in range(1, N + 1):
        try:
            # sleep(random.uniform(0,1)) # For different trade time
            trade_id = str(ObjectId())
            trade = Trade(
                assetClass=random.choice(['Bond','Equity','FX',None]),
                counterparty=fake.name(),
                instrumentId=fake.name(),
                instrumentName=fake.name(),
                tradeDateTime=dt.datetime.now(),
                tradeDetails=TradeDetails(
                    buySellIndicator=random.choice(["BUY", "SELL"]),
                    price=random.uniform(50, 2000),
                    quantity=random.randint(100, 1000),
                ),
                tradeId=trade_id,
                trader=fake.name(),
            )
            mock_data.append(trade.model_dump())
        except ValidationError as exc:
            print(repr(exc.errors()[0]['type']))

    return mock_data


def upload_fake_data_to_db(N: int):
    try:
        db = ConnectDB()
        collection = db.get_collection()
        fake_data = generate_fake_data(N)
        print(fake_data)
        collection.insert_many(fake_data)
    except Exception as exc:
        print(exc)
    finally:
        db.close()

if __name__ == '__main__':
    upload_fake_data_to_db(1)