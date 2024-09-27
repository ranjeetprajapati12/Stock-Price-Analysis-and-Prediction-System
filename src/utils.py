import yfinance as yf

def additional_info(symbol:str)->dict:
    msft = yf.Ticker(symbol)
    data = dict()
    for i in msft.info:
        print(i ,":",msft.info[i])
        if i in ["longName","website","country","financialCurrency","open","dayLow","dayHigh","marketCap","totalCash","totalCashPerShare"]:
            if i == "longName" :
                data[i]=msft.info[i] +f" ({msft.info['underlyingSymbol']})"
            else:
                data[i]=msft.info[i]

    return data