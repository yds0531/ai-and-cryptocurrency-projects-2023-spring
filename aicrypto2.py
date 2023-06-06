
import pandas as pd
import openpyxl

fn = 'C:/Users/10/Desktop/123.csv'

raw_fn = 'C:/Users/10/Desktop/2023-05-04-UPBIT-BTC-orderbook.csv'


df = pd.read_csv(raw_fn,encoding = 'cp949').apply(pd.to_numeric,errors='ignore')


def live_cal_book_i_v1(param, gr_bid_level, gr_ask_level, diff, var, mid):
    
    mid_price = mid

    ratio = param[0]; level = param[1]; interval = param[2]
  
    _flag = var['_flag']
        
    if _flag: 
        var['_flag'] = False
        return 0.0

    quant_v_bid = gr_bid_level.quantity**ratio
    price_v_bid = gr_bid_level.price * quant_v_bid

    quant_v_ask = gr_ask_level.quantity**ratio
    price_v_ask = gr_ask_level.price * quant_v_ask
 
        
    askQty = quant_v_ask.values.sum()
    bidPx = price_v_bid.values.sum()
    bidQty = quant_v_bid.values.sum()
    askPx = price_v_ask.values.sum()
    bid_ask_spread = interval
        
    book_price = 0 
    if bidQty > 0 and askQty > 0:
        book_price = (((askQty*bidPx)/bidQty) + ((bidQty*askPx)/askQty)) / (bidQty+askQty)

        
    indicator_value = (book_price - mid_price) / bid_ask_spread
    
    return indicator_value

param = [0.2 , 5, 1]

var = {
    '_flag': True,
    'prevBidQty': 0,
    'prevAskQty': 0,
    'prevBidTop': 0,
    'prevAskTop': 0,
    'bidSideAdd': 0,
    'bidSideDelete': 0,
    'askSideAdd': 0,
    'askSideDelete': 0,
    'bidSideTrade': 0,
    'askSideTrade': 0,
    'bidSideFlip': 0,
}

gr_bid_level = df[df.type == 0].head(54000)
gr_ask_level = df[df.type == 1].head(54000)

n = 10800
result_data = []

for i in range(n):
    index = 5 * i + 1
    result_data.append(((gr_bid_level.iloc[index].price + gr_ask_level.iloc[index].price)*0.5, gr_bid_level.iloc[index].timestamp))

# 추출한 데이터를 엑셀 파일로 저장
result_df = pd.DataFrame(result_data, columns=['mid_pirce', 'Timestamp'])
result_df.to_csv(fn, index=False)

