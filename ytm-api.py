#!./.venv/bin/python3

import pycurl
import json
from io import BytesIO
from urllib.parse import urlencode
import datetime

ytms = [
    # ytms in taipei mrt
    dict( name='板南線-南港站', key='F7D4C50F16F155', address='', region='tpe-mrt' ),
    dict( name='板南線-南港展覽館站', key='F7D4C52312B45C', address='', region='tpe-mrt' ),
    dict( name='板南線-後山埤站', key='F7D4C3DA12A3A7', address='', region='tpe-mrt' ),
    dict( name='板南線-永春站', key='F7D4C5391249AD', address='', region='tpe-mrt' ),
    dict( name='板南線-市政府站', key='F638C3AB05CB05', address='', region='tpe-mrt' ),
    dict( name='板南線-國父紀念館站', key='F7D4C3DA12A3AA', address='', region='tpe-mrt' ),
    dict( name='板南線-忠孝復興站', key='F7D4C6240F2DD1', address='', region='tpe-mrt' ),
    dict( name='板南線-忠孝新生站', key='F7D4C53512A9A0', address='', region='tpe-mrt' ),
    dict( name='板南線-台北車站', key='F638C5930260D9', address='', region='tpe-mrt' ),
    dict( name='板南線-龍山寺站', key='F7D4C41212D4F8', address='', region='tpe-mrt' ),
    dict( name='板南線-江子翠站', key='F7D4C41212D4FA', address='', region='tpe-mrt' ),
    dict( name='板南線-新埔站', key='F638C38C0C5451', address='', region='tpe-mrt' ),
    dict( name='板南線-板橋站', key='F638C56F0B2314', address='', region='tpe-mrt' ),
    dict( name='板南線-府中站', key='F638C3C405B6D2', address='', region='tpe-mrt' ),
    dict( name='板南線-亞東醫院站', key='F7D4C41212D4F9', address='', region='tpe-mrt' ),
    dict( name='板南線-海山站', key='F638C38005BF2E', address='', region='tpe-mrt' ),
    dict( name='板南線-土城站', key='F7D4C50F16F035', address='', region='tpe-mrt' ),
    dict( name='板南線-永寧站', key='F7D4C594122F67', address='', region='tpe-mrt' ),
    dict( name='板南線-頂埔站', key='F7D4C469168A57', address='', region='tpe-mrt' ),
    dict( name='文湖線-科技大樓站', key='F7D4C56F112E44', address='', region='tpe-mrt' ),
    dict( name='文湖線-西湖站', key='F7D4C473169749', address='', region='tpe-mrt' ),
    dict( name='淡水信義線-淡水站', key='F7D4C56F112E3D', address='', region='tpe-mrt' ),
    dict( name='淡水信義線-石牌站', key='F7D4C4A516D2EC', address='', region='tpe-mrt' ),
    dict( name='淡水信義線-北投站', key='F638C3DA0C957D', address='', region='tpe-mrt' ),
    dict( name='淡水信義線-士林站', key='F7D4C45C164FBA', address='', region='tpe-mrt' ),
    dict( name='淡水信義線-劍潭站', key='F7D4C3D7144228', address='', region='tpe-mrt' ),
    dict( name='淡水信義線-圓山站', key='F638C61D01B3CB', address='', region='tpe-mrt' ),
    dict( name='淡水信義線-民權西路站', key='F7D4C469168B78', address='', region='tpe-mrt' ),
    dict( name='淡水信義線-雙連站', key='F7D4C4A2166FC0', address='', region='tpe-mrt' ),
    dict( name='淡水信義線-中山站', key='F638C39405D3A4', address='', region='tpe-mrt' ),
    dict( name='淡水信義線-台大醫院站', key='F7D4C424167BFD', address='', region='tpe-mrt' ),
    dict( name='淡水信義線-大安森林公園站', key='F7D4C47316974B', address='', region='tpe-mrt' ),
    dict( name='淡水信義線-信義安和站', key='F7D4C4A21670E1', address='', region='tpe-mrt' ),
    dict( name='淡水信義線-大安站', key='F7D4C4A516D2EE', address='', region='tpe-mrt' ),
    dict( name='淡水信義線-象山站', key='F7D4C47316974C', address='', region='tpe-mrt' ),
    dict( name='中和新蘆線-蘆洲站', key='F638C39205D81C', address='', region='tpe-mrt' ),
    dict( name='中和新蘆線-三民高中站', key='F7D4C3F716C4CA', address='', region='tpe-mrt' ),
    dict( name='中和新蘆線-徐匯中學站', key='F7D4C630123253', address='', region='tpe-mrt' ),
    dict( name='中和新蘆線-三和國中站', key='F7D4C3B4116D80', address='', region='tpe-mrt' ),
    dict( name='中和新蘆線-迴龍站', key='F7D4C3F716C4CC', address='', region='tpe-mrt' ),
    dict( name='中和新蘆線-菜寮站', key='F7D4C3F416BCD5', address='', region='tpe-mrt' ),
    dict( name='中和新蘆線-三重國小站', key='F7D4C492120253', address='', region='tpe-mrt' ),
    dict( name='中和新蘆線-大橋頭站', key='F7D4C4A21670DE', address='', region='tpe-mrt' ),
    dict( name='中和新蘆線-新莊站', key='F7D4C3B4116D81', address='', region='tpe-mrt' ),
    dict( name='中和新蘆線-台北橋站', key='F7D4C594122F69', address='', region='tpe-mrt' ),
    dict( name='中和新蘆線-中山國小站', key='F7D4C630123254', address='', region='tpe-mrt' ),
    dict( name='中和新蘆線-行天宮站', key='F7D4C384125119', address='', region='tpe-mrt' ),
    dict( name='中和新蘆線-松江南京站', key='F7D4C6240F2DD0', address='', region='tpe-mrt' ),
    dict( name='中和新蘆線-頂溪站', key='F638C3B40B65E1', address='', region='tpe-mrt' ),
    dict( name='中和新蘆線-永安市場站', key='F7D4C492120255', address='', region='tpe-mrt' ),
    dict( name='中和新蘆線-景安站', key='F638C56F0B2313', address='', region='tpe-mrt' ),
    dict( name='中和新蘆線-南勢角站', key='F638C5390CABA0', address='', region='tpe-mrt' ),
    dict( name='環狀線-新北產業園區站', key='F638C63801AA82', address='', region='tpe-mrt' ),
    dict( name='松山新店線-松山站', key='F7D4C52312B45B', address='', region='tpe-mrt' ),
    dict( name='松山新店線-南京三民站', key='F7D4C41212D4F7', address='', region='tpe-mrt' ),
    dict( name='松山新店線-台北小巨蛋站', key='F7D4C45C1650DB', address='', region='tpe-mrt' ),
    dict( name='松山新店線-南京復興站', key='F7D4C59D12B5D8', address='', region='tpe-mrt' ),
    dict( name='松山新店線-北門站', key='F7D4C6240F2DD2', address='', region='tpe-mrt' ),
    dict( name='松山新店線-古亭站', key='F7D4C384125118', address='', region='tpe-mrt' ),
    dict( name='松山新店線-台電大樓站', key='F7D4C3DA12A3A9', address='', region='tpe-mrt' ),
    dict( name='松山新店線-公館站', key='F7D4C38C128657', address='', region='tpe-mrt' ),
    dict( name='松山新店線-萬隆站', key='F7D4C3D7144229', address='', region='tpe-mrt' ),
    dict( name='松山新店線-景美站', key='F7D4C594122F68', address='', region='tpe-mrt' ),
    dict( name='松山新店線-大坪林站', key='F7D4C52312B45A', address='', region='tpe-mrt' ),
    dict( name='松山新店線-七張站', key='F638C3840C561D', address='', region='tpe-mrt' ),
    dict( name='松山新店線-新店站', key='F7D4C3C81216B5', address='', region='tpe-mrt' ),
    dict( name='環狀線-幸福站', key='F638C3E505D058', address='', region='tpe-mrt' ),
    dict( name='環狀線-板橋站', key='F638C3CB05B54A', address='', region='tpe-mrt' ),
    dict( name='環狀線-中原站', key='F7D4C6240F2D20', address='', region='tpe-mrt' ),
    dict( name='環狀線-中和站', key='F638C39205D81F', address='', region='tpe-mrt' ),
    dict( name='環狀線-十四張站', key='F638C3C80C2AC3', address='', region='tpe-mrt' ),

    # ytms in kaohsiung mrt
    dict( name='紅線-楠梓科技園區站', key='F7D4C52312B459', address='紅線R19/穿堂走道靠近1號出入口', region='kh-mrt' ),
    dict( name='紅線-生態園區站', key='F7D4C59D12B5D7', address='紅線R15/穿堂走道靠近1號出入口', region='kh-mrt' ),
    dict( name='紅線-巨蛋站', key='F7D4C3B4116D82', address='紅線R14/穿堂走道靠近1號出入口', region='kh-mrt' ),
    dict( name='紅線-凹子底站', key='F7D4C59D12B5D6', address='紅線R13/近3號出入口', region='kh-mrt' ),
    dict( name='紅線-後驛站', key='F7D4C5391249AE', address='紅線R12/近2號出入口', region='kh-mrt' ),
    dict( name='紅線-中央公園站', key='F7D4C5391249AF', address='紅線R9/穿堂層 往2號出口', region='kh-mrt' ),
    dict( name='紅線-三多商圈站', key='F7D4C55712A1F8', address='紅線R8/近4號出入口置物櫃前方', region='kh-mrt' ),
    dict( name='紅線-獅甲站', key='F7D4C492120254', address='紅線R7/近3號出入口', region='kh-mrt' ),
    dict( name='紅線-凱旋站', key='F7D4C55712A1FA', address='紅線R6/近1號出入口廁所旁', region='kh-mrt' ),
    dict( name='紅線-小港站', key='F7D4C3C81216B3', address='紅線R3/近3號出入口', region='kh-mrt' ),

    # ytms in yannick store
    dict( name='高雄苓雅店', key='F7D4C45716F94E', address='高雄市苓雅區青年二路89號', region='direct' ),
    dict( name='內湖旗艦店', key='F638C55001AE22', address='台北市內湖區瑞湖街178巷15號', region='direct' ),
    dict( name='屏東仁愛店', key='F638C3E205B6E8', address='屏東縣屏東市仁愛路14之16號', region='direct' ),
    dict( name='台中崇德店', key='F7D4C6240F2D1F', address='台中市北區崇德路一段482號', region='direct' ),
    dict( name='台中旗艦店', key='F7D4C41F1673E2', address='台中市西區五權西四街120號', region='direct' ),
    dict( name='桃園中正店', key='F638C5390CABA2', address='桃園市桃園區中正路50號', region='direct' ),
    dict( name='台北西門店', key='F638C3E205B6E6', address='台北市萬華區成都路18號', region='direct' ),
]

API='https://www.yannick.com.tw/_zh-cht/ajaxTYTMStock.ashx'

def get_stock(ytm):
    buffer = BytesIO()

    c = pycurl.Curl()
    c.setopt(c.URL, API)
    c.setopt(c.WRITEDATA, buffer)

    post_data = { 'TID': ytm['key'] }
    postfields = urlencode(post_data)
    c.setopt(c.POSTFIELDS, postfields)

    c.perform()
    c.close()

    body = buffer.getvalue()
    data = json.loads(body.decode('utf-8'))
    return data

def main():
    for ytm in ytms:
        print(f'get {ytm["name"]} stock...')
        stocks = get_stock(ytm)
        ytm['stocks'] = []
        for stock in stocks['Result']['StockList']:
          item = dict(
            name = stock['commodityName'],
            real_name = stock['ProductName'],
            key = stock['commodityCode'],
            quantity = stock['quantity'],
          )
          ytm['stocks'].append(item)

    with open('frontend/scripts/ytm-stock.js', 'w', encoding='utf-8') as f:
        f.write('const YTMS = ')
        json.dump(ytms, f, ensure_ascii=False)
        f.write(f'\nconst UPDATED_AT = {datetime.datetime.now().timestamp()}')

    with open('stock.json', 'w', encoding='utf-8') as f:
        json.dump(ytms, f, indent=4, ensure_ascii=False)

if __name__ == '__main__':
    main()
