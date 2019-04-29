

# Drop table
ticker_table_drop = """
DROP TABLE IF EXISTS ticker
"""

historical_price_table_drop = """
DROP TABLE IF EXISTS historical_price
"""

# Create table
ticker_table_create = """
CREATE TABLE IF NOT EXISTS ticker(
    ticker_code varchar(10),
    company_name varchar(250) NULL,
    field varchar(100) NULL,
    stock_exchange varchar(100) NULL,
    CONSTRAINT ticker_tickercode_pkey PRIMARY KEY(ticker_code)
)
"""

historical_price_table_create = """
CREATE TABLE IF NOT EXISTS historical_price(
    date date NOT NULL,
    close float NOT NULL,
    ticker_code varchar(10) NOT NULL,
    open float NOT NULL,
    high float NOT NULL,
    low float NOT NULL,
    volume int NOT NULL,
    CONSTRAINT historical_ticker_code_fkey FOREIGN KEY(ticker_code) REFERENCES ticker(ticker_code),
    CONSTRAINT historical_price_key UNIQUE(date, ticker_code)
)
"""

# Upsert data
ticker_table_upsert = """
INSERT INTO ticker(ticker_code, company_name, field, stock_exchange)
VALUES(?, ?, ?, ?)
ON CONFLICT ON CONSTRAINT ticker_tickercode_pkey
UPDATE SET
company_name = ?, field = ?, stock_exchange = ?
"""

historical_price_table_upsert = """
INSERT INTO historical_price(date, close, ticker_code, open, high, low, volume)
VALUES(?, ?, ?, ?, ?, ?, ?)
ON CONFICT ON CONSTRAINT historical_price_key
UPDATE SET
close = ?, open = ?, high = ?, low = ?, volume = ?
"""

create_table_queries = [ticker_table_create, historical_price_table_create]

drop_table_queries = [ticker_table_drop, historical_price_table_drop]

upsert_table_queries = [ticker_table_upsert, historical_price_table_upsert]
