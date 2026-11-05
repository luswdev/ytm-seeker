#!./.venv/bin/python3

import sys
import time
import pycurl
import json
from io import BytesIO
from urllib.parse import urlencode, quote
import datetime
import logging

from concurrent.futures import ThreadPoolExecutor, as_completed

ytms = [
    # ytms in taipei mrt
    dict( name='板南線-南港站', key='F7D4C50F16F155', address='出口2A詢問處旁', region='tpe-mrt', subRegion='bannan', ytm_gen=1 ),
    dict( name='板南線-南港展覽館站', key='F7D4C52312B45C', address='出口6', region='tpe-mrt', subRegion='bannan', ytm_gen=1 ),
    dict( name='板南線-後山埤站', key='F7D4C3DA12A3A7', address='出口2', region='tpe-mrt', subRegion='bannan', ytm_gen=1 ),
    dict( name='板南線-永春站', key='F7D4C5391249AD', address='出口5', region='tpe-mrt', subRegion='bannan', ytm_gen=1 ),
    dict( name='板南線-市政府站', key='F638C3AB05CB05', address='出口3/4側往月台手扶梯旁', region='tpe-mrt', subRegion='bannan', ytm_gen=1 ),
    dict( name='板南線-國父紀念館站', key='F7D4C3DA12A3AA', address='出口2置物櫃旁', region='tpe-mrt', subRegion='bannan', ytm_gen=1 ),
    dict( name='板南線-忠孝復興站', key='F7D4C6240F2DD1', address='出口3', region='tpe-mrt', subRegion='bannan', ytm_gen=1 ),
    dict( name='板南線-忠孝新生站', key='F7D4C53512A9A0', address='出口4公共電話旁', region='tpe-mrt', subRegion='bannan', ytm_gen=1 ),
    dict( name='板南線-台北車站', key='F638C5930260D9', address='近B1樓層M8出口', region='tpe-mrt', subRegion='bannan', ytm_gen=1 ),
    dict( name='板南線-龍山寺站', key='F7D4C41212D4F8', address='出口2置物櫃旁', region='tpe-mrt', subRegion='bannan', ytm_gen=1 ),
    dict( name='板南線-江子翠站', key='F7D4C41212D4FA', address='出口3', region='tpe-mrt', subRegion='bannan', ytm_gen=1 ),
    dict( name='板南線-新埔站', key='F638C38C0C5451', address='近出口2/3', region='tpe-mrt', subRegion='bannan', ytm_gen=1 ),
    dict( name='板南線-板橋站', key='F638C56F0B2314', address='出口3A', region='tpe-mrt', subRegion='bannan', ytm_gen=1, abbr='2板橋站' ),
    dict( name='板南線-府中站', key='F638C3C405B6D2', address='出口2', region='tpe-mrt', subRegion='bannan', ytm_gen=1 ),
    dict( name='板南線-亞東醫院站', key='F7D4C41212D4F9', address='出口3', region='tpe-mrt', subRegion='bannan', ytm_gen=1 ),
    dict( name='板南線-海山站', key='F638C38005BF2E', address='出口2', region='tpe-mrt', subRegion='bannan', ytm_gen=1 ),
    dict( name='板南線-土城站', key='F7D4C50F16F035', address='出口2置物櫃旁', region='tpe-mrt', subRegion='bannan', ytm_gen=1 ),
    dict( name='板南線-永寧站', key='F7D4C594122F67', address='出口1', region='tpe-mrt', subRegion='bannan', ytm_gen=1 ),
    dict( name='板南線-頂埔站', key='F7D4C469168A57', address='出口4置物櫃旁', region='tpe-mrt', subRegion='bannan', ytm_gen=1 ),
    dict( name='文湖線-科技大樓站', key='F7D4C56F112E44', address='出口1夾層', region='tpe-mrt', subRegion='wenhu', ytm_gen=1 ),
    dict( name='文湖線-西湖站', key='F7D4C473169749', address='出口1置物櫃旁', region='tpe-mrt', subRegion='wenhu', ytm_gen=1 ),
    dict( name='淡水信義線-淡水站', key='F7D4C56F112E3D', address='出口2/3側往南川堂', region='tpe-mrt', subRegion='tamsui-xinyi', ytm_gen=1 ),
    dict( name='淡水信義線-石牌站', key='F7D4C4A516D2EC', address='出口1', region='tpe-mrt', subRegion='tamsui-xinyi', ytm_gen=1 ),
    dict( name='淡水信義線-北投站', key='F638C3DA0C957D', address='出口1飲水機旁', region='tpe-mrt', subRegion='tamsui-xinyi', ytm_gen=1 ),
    dict( name='淡水信義線-士林站', key='F7D4C45C164FBA', address='出口1', region='tpe-mrt', subRegion='tamsui-xinyi', ytm_gen=1 ),
    dict( name='淡水信義線-劍潭站', key='F7D4C3D7144228', address='出口1', region='tpe-mrt', subRegion='tamsui-xinyi', ytm_gen=1 ),
    dict( name='淡水信義線-圓山站', key='F638C61D01B3CB', address='出口1', region='tpe-mrt', subRegion='tamsui-xinyi', ytm_gen=1 ),
    dict( name='淡水信義線-民權西路站', key='F7D4C469168B78', address='出口4公共電話旁', region='tpe-mrt', subRegion='tamsui-xinyi', ytm_gen=1 ),
    dict( name='淡水信義線-雙連站', key='F7D4C4A2166FC0', address='近中山地下街公共電話旁', region='tpe-mrt', subRegion='tamsui-xinyi', ytm_gen=1 ),
    dict( name='淡水信義線-中山站', key='F638C39405D3A4', address='出口1', region='tpe-mrt', subRegion='tamsui-xinyi', ytm_gen=1 ),
    dict( name='淡水信義線-台大醫院站', key='F7D4C424167BFD', address='出口4置物櫃旁', region='tpe-mrt', subRegion='tamsui-xinyi', ytm_gen=1 ),
    dict( name='淡水信義線-大安森林公園站', key='F7D4C47316974B', address='出口5置物櫃旁', region='tpe-mrt', subRegion='tamsui-xinyi', ytm_gen=1 ),
    dict( name='淡水信義線-信義安和站', key='F7D4C4A21670E1', address='出口1', region='tpe-mrt', subRegion='tamsui-xinyi', ytm_gen=1 ),
    dict( name='淡水信義線-大安站', key='F7D4C4A516D2EE', address='出口詢問處左前方', region='tpe-mrt', subRegion='tamsui-xinyi', ytm_gen=1 ),
    dict( name='淡水信義線-象山站', key='F7D4C47316974C', address='出口2通道', region='tpe-mrt', subRegion='tamsui-xinyi', ytm_gen=1 ),
    dict( name='中和新蘆線-蘆洲站', key='F638C39205D81C', address='出口1', region='tpe-mrt', subRegion='zhonghe-xinlu', ytm_gen=1 ),
    dict( name='中和新蘆線-三民高中站', key='F7D4C3F716C4CA', address='出口2置物櫃旁', region='tpe-mrt', subRegion='zhonghe-xinlu', ytm_gen=1 ),
    dict( name='中和新蘆線-徐匯中學站', key='F7D4C630123253', address='出口2', region='tpe-mrt', subRegion='zhonghe-xinlu', ytm_gen=1 ),
    dict( name='中和新蘆線-三和國中站', key='F7D4C3B4116D80', address='出口2', region='tpe-mrt', subRegion='zhonghe-xinlu', ytm_gen=1 ),
    dict( name='中和新蘆線-迴龍站', key='F7D4C3F716C4CC', address='出口3置物櫃旁', region='tpe-mrt', subRegion='zhonghe-xinlu', ytm_gen=1 ),
    dict( name='中和新蘆線-菜寮站', key='F7D4C3F416BCD5', address='出口1置物櫃旁', region='tpe-mrt', subRegion='zhonghe-xinlu', ytm_gen=1 ),
    dict( name='中和新蘆線-三重國小站', key='F7D4C492120253', address='出口詢問處旁', region='tpe-mrt', subRegion='zhonghe-xinlu', ytm_gen=1 ),
    dict( name='中和新蘆線-大橋頭站', key='F7D4C4A21670DE', address='出口1飲水機旁', region='tpe-mrt', subRegion='zhonghe-xinlu', ytm_gen=1 ),
    dict( name='中和新蘆線-新莊站', key='F7D4C3B4116D81', address='出口2置物櫃旁', region='tpe-mrt', subRegion='zhonghe-xinlu', ytm_gen=1 ),
    dict( name='中和新蘆線-台北橋站', key='F7D4C594122F69', address='出口置物櫃旁', region='tpe-mrt', subRegion='zhonghe-xinlu', ytm_gen=1 ),
    dict( name='中和新蘆線-中山國小站', key='F7D4C630123254', address='出口1置物櫃旁', region='tpe-mrt', subRegion='zhonghe-xinlu', ytm_gen=1 ),
    dict( name='中和新蘆線-行天宮站', key='F7D4C384125119', address='往出口4', region='tpe-mrt', subRegion='zhonghe-xinlu', ytm_gen=1 ),
    dict( name='中和新蘆線-松江南京站', key='F7D4C6240F2DD0', address='出口8', region='tpe-mrt', subRegion='zhonghe-xinlu', ytm_gen=1 ),
    dict( name='中和新蘆線-頂溪站', key='F638C3B40B65E1', address='出口1', region='tpe-mrt', subRegion='zhonghe-xinlu', ytm_gen=1 ),
    dict( name='中和新蘆線-永安市場站', key='F7D4C492120255', address='大廳層置物櫃旁', region='tpe-mrt', subRegion='zhonghe-xinlu', ytm_gen=1 ),
    dict( name='中和新蘆線-景安站', key='F638C56F0B2313', address='1F出口旁', region='tpe-mrt', subRegion='zhonghe-xinlu', ytm_gen=1 ),
    dict( name='中和新蘆線-南勢角站', key='F638C5390CABA0', address='近出口3/4', region='tpe-mrt', subRegion='zhonghe-xinlu', ytm_gen=1 ),
    dict( name='松山新店線-松山站', key='F7D4C52312B45B', address='B2大廳層往出口3/4/4A', region='tpe-mrt', subRegion='songshan-xindian', ytm_gen=1 ),
    dict( name='松山新店線-南京三民站', key='F7D4C41212D4F7', address='往出口1', region='tpe-mrt', subRegion='songshan-xindian', ytm_gen=1 ),
    dict( name='松山新店線-台北小巨蛋站', key='F7D4C45C1650DB', address='出口2置物櫃旁', region='tpe-mrt', subRegion='songshan-xindian', ytm_gen=1 ),
    dict( name='松山新店線-南京復興站', key='F7D4C59D12B5D8', address='出口5詢問處旁', region='tpe-mrt', subRegion='songshan-xindian', ytm_gen=1 ),
    dict( name='松山新店線-北門站', key='F7D4C6240F2DD2', address='B2大廳層尾端', region='tpe-mrt', subRegion='songshan-xindian', ytm_gen=1 ),
    dict( name='松山新店線-古亭站', key='F7D4C384125118', address='出口3/4置物櫃旁', region='tpe-mrt', subRegion='songshan-xindian', ytm_gen=1 ),
    dict( name='松山新店線-台電大樓站', key='F7D4C3DA12A3A9', address='出口4公共電話旁', region='tpe-mrt', subRegion='songshan-xindian', ytm_gen=1 ),
    dict( name='松山新店線-公館站', key='F7D4C38C128657', address='出口1', region='tpe-mrt', subRegion='songshan-xindian', ytm_gen=1 ),
    dict( name='松山新店線-萬隆站', key='F7D4C3D7144229', address='出口4置物櫃旁', region='tpe-mrt', subRegion='songshan-xindian', ytm_gen=1 ),
    dict( name='松山新店線-景美站', key='F7D4C594122F68', address='出口2置物櫃旁', region='tpe-mrt', subRegion='songshan-xindian', ytm_gen=1 ),
    dict( name='松山新店線-大坪林站', key='F7D4C52312B45A', address='出口1', region='tpe-mrt', subRegion='songshan-xindian', ytm_gen=1 ),
    dict( name='松山新店線-七張站', key='F638C3840C561D', address='出口1', region='tpe-mrt', subRegion='songshan-xindian', ytm_gen=1 ),
    dict( name='松山新店線-新店站', key='F7D4C3C81216B5', address='碧潭風景區出口', region='tpe-mrt', subRegion='songshan-xindian', ytm_gen=1 ),
    dict( name='環狀線-新北產業園區站', key='F638C63801AA82', address='5F大廳層詢問處旁', region='tpe-mrt', subRegion='circular', ytm_gen=1 ),
    dict( name='環狀線-幸福站', key='F638C3E505D058', address='2F連通道層出口', region='tpe-mrt', subRegion='circular', ytm_gen=1 ),
    dict( name='環狀線-板橋站', key='F638C3CB05B54A', address='3F大廳層出口', region='tpe-mrt', subRegion='circular', ytm_gen=1 ),
    dict( name='環狀線-中原站', key='F7D4C6240F2D20', address='1F地面層出口', region='tpe-mrt', subRegion='circular', ytm_gen=1 ),
    dict( name='環狀線-中和站', key='F638C39205D81F', address='1F大廳層出口', region='tpe-mrt', subRegion='circular', ytm_gen=1 ),
    dict( name='環狀線-十四張站', key='F638C3C80C2AC3', address='2F大廳層出口', region='tpe-mrt', subRegion='circular', ytm_gen=1 ),

    # ytms in kaohsiung mrt
    dict( name='紅線-楠梓科技園區站', key='F7D4C52312B459', address='紅線R19/穿堂走道靠近1號出入口', region='kh-mrt', subRegion='red', ytm_gen=1 ),
    dict( name='紅線-生態園區站', key='F7D4C59D12B5D7', address='紅線R15/穿堂走道靠近1號出入口', region='kh-mrt', subRegion='red', ytm_gen=1 ),
    dict( name='紅線-巨蛋站', key='F7D4C3B4116D82', address='紅線R14/穿堂走道靠近1號出入口', region='kh-mrt', subRegion='red', ytm_gen=1 ),
    dict( name='紅線-凹子底站', key='F7D4C59D12B5D6', address='紅線R13/近3號出入口', region='kh-mrt', subRegion='red', ytm_gen=1 ),
    dict( name='紅線-後驛站', key='F7D4C5391249AE', address='紅線R12/近2號出入口', region='kh-mrt', subRegion='red', ytm_gen=1 ),
    dict( name='紅線-中央公園站', key='F7D4C5391249AF', address='紅線R9/穿堂層 往2號出口', region='kh-mrt', subRegion='red', ytm_gen=1 ),
    dict( name='紅線-三多商圈站', key='F7D4C55712A1F8', address='紅線R8/近4號出入口置物櫃前方', region='kh-mrt', subRegion='red', ytm_gen=1 ),
    dict( name='紅線-獅甲站', key='F7D4C492120254', address='紅線R7/近3號出入口', region='kh-mrt', subRegion='red', ytm_gen=1 ),
    dict( name='紅線-凱旋站', key='F7D4C55712A1FA', address='紅線R6/近1號出入口廁所旁', region='kh-mrt', subRegion='red', ytm_gen=1 ),
    dict( name='紅線-小港站', key='F7D4C3C81216B3', address='紅線R3/近3號出入口', region='kh-mrt', subRegion='red', ytm_gen=1 ),

    # ytms in yannick store
    dict( name='台北西門店', key='F638C3E205B6E6', address='台北市萬華區成都路18號', region='direct', subRegion='northern', ytm_gen=1, abbr='西門' ),
    dict( name='內湖旗艦店', key='F638C55001AE22', address='台北市內湖區瑞湖街178巷15號', region='direct', subRegion='northern', ytm_gen=1, abbr='內湖' ),
    dict( name='桃園中正店', key='F638C5390CABA2', address='桃園市桃園區中正路50號', region='direct', subRegion='northern', ytm_gen=1, abbr='01桃園' ),
    dict( name='台中崇德店', key='F7D4C6240F2D1F', address='台中市北區崇德路一段482號', region='direct', subRegion='central', ytm_gen=1, abbr='崇德' ),
    dict( name='台中旗艦店', key='F7D4C41F1673E2', address='台中市西區五權西四街120號', region='direct', subRegion='central', ytm_gen=1, abbr='' ),
    dict( name='高雄苓雅店', key='F7D4C45716F94E', address='高雄市苓雅區青年二路89號', region='direct', subRegion='southern', ytm_gen=1, abbr='苓雅' ),
    dict( name='屏東仁愛店', key='F638C3E205B6E8', address='屏東縣屏東市仁愛路14之16號', region='direct', subRegion='southern', ytm_gen=1, abbr='03屏東' ),
]

known_products = [
    dict( name='原味', key='31Z021079', style='bg-zinc-700 border-zinc-700 text-zinc-300', enable=False ),
    dict( name='盲盒', key='31Z051013', style='bg-red-700 border-red-700 text-zinc-300', enable=False ),
    dict( name='喀麥隆脆皮黑巧', key='31Z021370', style='bg-taupe-600 border-taupe-600 text-zinc-300', enable=False ),
    dict( name='BUBU切片組', key='31Z011082', style='bg-sky-700 border-sky-700 text-zinc-300', enable=False ),
    dict( name='三顆布丁', key='31Z021368', style='bg-amber-500 border-amber-500 text-zinc-800', enable=False ),
]
known_products_map = {p['key']: p for p in known_products}

products = []
products_map = {p['key']: p for p in products}

API='https://www.yannick.com.tw/_zh-cht/ajaxTYTMStock.ashx'

def url_exists(url):
    encoded_url = quote(url, safe=':/?=&')

    c = pycurl.Curl()
    c.setopt(pycurl.URL, encoded_url)
    c.setopt(pycurl.NOBODY, True)
    c.setopt(pycurl.FOLLOWLOCATION, True)
    c.setopt(pycurl.TIMEOUT, 10)

    try:
        c.perform()
        status = c.getinfo(pycurl.RESPONSE_CODE)
        return 200 <= status < 400
    except pycurl.error:
        return False
    finally:
        c.close()

def detect_ytm_generation(ytm):
    if ytm['region'] == 'direct':
        prefix = '門市'
        abbr = ytm['abbr']
    else:
        prefix = '1-捷運路線圖'
        abbr = ytm.get('abbr') or ytm['name'].split('-')[1]

    if abbr:
        urls = [
            f'0.YTM查詢-{prefix}-{abbr}.jpg',
            f'photo/YTM2/0.YTM查詢-{prefix}-{abbr}.jpg',
            f'photo/YTM2/0.YTM查詢-{prefix}-{abbr}-01.jpg',
            f'photo/YTM2/0.YTM查詢-{prefix}-2{abbr}-01.jpg',
            f'photo//0.YTM查詢-{prefix}-{abbr}.jpg',
            f'photo/YTM2/0.YTM查詢-{prefix}-{abbr}- 中文-01.jpg',
        ]
    else:
        urls = [
            f'0.YTM查詢-{prefix}.jpg',
        ]

    base_url = 'https://photo.yannick.com.tw/'
    for generation, path in enumerate(urls, start=1):
        if url_exists(base_url + path):
            return generation

    return 0

def gen_google_map_url(ytm):
    if ytm['region'] == 'tpe-mrt':
        station = ytm['name'].split('-', 1)[1]
        query = f'台北捷運 {station}'
    elif ytm['region'] == 'kh-mrt':
        station = ytm['name'].split('-', 1)[1]
        query = f'高雄捷運 {station}'
    elif ytm['region'] == 'direct':
        query = f'亞尼克 {ytm["name"]}'

    return query

def detect_new_product(product):
    key = product['commodityCode']

    if key not in products_map:
        logging.info(f'new product: {product["commodityName"]}')

        match = known_products_map.get(key)

        products.append(match if match else dict(
            name=product['commodityName'],
            key=key,
            style='bg-zinc-700 border-zinc-700 text-zinc-300',
            enable=False,
        ))

        products_map[key] = products[-1]

def get_stock(ytm):
    buffer = BytesIO()

    c = pycurl.Curl()
    c.setopt(c.URL, API)
    c.setopt(c.WRITEDATA, buffer)

    post_data = { 'TID': ytm['key'] }
    postfields = urlencode(post_data)
    c.setopt(c.POSTFIELDS, postfields)
    c.setopt(c.CONNECTTIMEOUT, 10)
    c.setopt(c.TIMEOUT, 30)
    c.setopt(c.FOLLOWLOCATION, 1)

    c.perform()
    status = c.getinfo(c.RESPONSE_CODE)
    c.close()

    if status != 200:
        logging.warning(f'[{ytm["name"]}] get stock failed ({status})!')
        return None

    body = buffer.getvalue()
    data = json.loads(body.decode('utf-8'))
    return data['Result']['StockList']

def get_stock_retry(ytm, retries=3):
    for attempt in range(retries):
        stocks = get_stock(ytm)

        if all(
            'commodityName' in stock
            for stock in stocks
        ):
            return stocks

        logging.warning(
            f'[{ytm["name"]}] invalid response, retry {attempt + 1}/{retries}'
        )
        time.sleep(1)

    return stocks

def main(output_path):
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {
            executor.submit(detect_ytm_generation, ytm): (ytm, 'generation')
            for ytm in ytms
        }

        futures.update({
            executor.submit(get_stock_retry, ytm): (ytm, 'stocks')
            for ytm in ytms
        })

        for future in as_completed(futures):
            ytm, task = futures[future]

            try:
                result = future.result()

                if task == 'generation':
                    ytm['ytm_gen'] = result
                    logging.info(f'{ytm["name"]} is gen-{result}')

                elif task == 'stocks':
                    ytm['google_map'] = gen_google_map_url(ytm)
                    logging.info(f'{ytm["name"]} got {len(result)} stock(s)')

                    ytm['stocks'] = []
                    for stock in result:
                        item = dict(
                            name=stock['commodityName'],
                            real_name=stock['ProductName'],
                            key=stock['commodityCode'],
                            quantity=stock['quantity'],
                        )
                        ytm['stocks'].append(item)
                        detect_new_product(stock)

            except Exception:
                logging.exception(f'{ytm["name"]} failed: {task}, stop ytm api.')
                for f in futures:
                    f.cancel()
                raise

    logging.info('write ytms/products into ytm-stock.json')
    with open(f'{output_path}/ytm-stock.json', 'w', encoding='utf-8') as f:
        out = dict(
            updated = datetime.datetime.now().timestamp(),
            products = products,
            ytms = ytms,
        )
        json.dump(out, f, ensure_ascii=False)

    logging.info('ytm api finished.')

if __name__ == '__main__':
    logging.basicConfig(
        format = '%(levelname)s - %(message)s',
        level  = logging.INFO,
    )

    output_path = 'public'
    if len(sys.argv) > 1:
        output_path = sys.argv[1]

    logging.info(f"output data into: {output_path}")
    main(output_path)
