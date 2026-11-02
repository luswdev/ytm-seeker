#!./.venv/bin/python3

import json

def main():
    with open('stock.json', 'r', encoding='utf-8') as f:
      ytms = f.read()
      ytms_json = json.loads(ytms)
      products = []
      for ytm in ytms_json:
          for item in ytm['stocks']:
              product = dict(
                  name = item['commodityName'],
                  key = item['commodityCode'],
              )

              if product in products:
                  continue

              products.append(product)

      print(json.dumps(products, indent=4, ensure_ascii=False))

if __name__ == '__main__':
    main()
