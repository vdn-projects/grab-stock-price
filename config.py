import os

db_username = "vietnamstock_usr1"
db_psw = "stock@2019"
local_test = True
conn_string = f"host=127.0.0.1 dbname=vietnam_stock user={db_username} password={db_psw}"
download_path = os.getcwd() + "/data/download"
initial_load_path = os.getcwd() + "/data/initial_load"
