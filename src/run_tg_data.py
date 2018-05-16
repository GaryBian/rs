import toolkit
from pandas import HDFStore


def merge_and_add_to_store(boot, symbol, data):
    print('AlphaVantageData merge_and_add_to_store')
    data_file = boot.base_path + '/../tg/tg_data.h5'

    data_store = HDFStore(data_file, mode='a')
    existing_df = data_store[symbol]
    bigdata = existing_df.append(data)
    print(existing_df.shape)
    print(data.shape)
    print(bigdata.shape)

    # then merge
    bigdata = bigdata[~bigdata.index.duplicated(keep='last')]
    print('after merge')
    data_store[symbol] = bigdata
    print('AlphaVantageData add_to_store added:' + symbol)
    print(bigdata.shape)
    data_store.close()


def add_to_store(boot, symbol, data):
    print('add_to_store')
    data_file = boot.base_path + '/../tg/tg_data.h5'
    data_store = HDFStore(data_file, mode='a')
    data_store[symbol] = data
    print('add_to_store added:' + symbol)
    data_store.close()


boot = toolkit.Bootup()
print(boot.base_path)

with open(boot.base_path + '/../tg/symbol400.txt') as f:
    lines = f.read().splitlines()

print(len(lines))
tg = toolkit.TgData(boot)
for s in lines:
    s = s.strip()
    print(s)
    try:
        df = tg.daily(s)
        # add_to_store(boot, s, df)
        merge_and_add_to_store(boot, s, df)
    except:
        print('error processing:' + s)
