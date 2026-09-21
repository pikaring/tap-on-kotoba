# -*- coding: utf-8 -*-
"""Creators API で キーワード検索を ためし、候補の ASIN と 商品名を 出す（一時的な 調査用）。

    py tools/search_goods.py "四字熟語 辞典" "ことわざ 辞典" ...

検索の エンドポイントが 使えるかを 確かめるのが 目的。使えなければ その旨が 出る。
"""
import json, os, sys, urllib.error, urllib.parse, urllib.request

TOKEN_URL = 'https://api.amazon.co.jp/auth/o2/token'
MARKETPLACE = 'www.amazon.co.jp'
CANDIDATES = [
    'https://creatorsapi.amazon/catalog/v1/searchItems',
    'https://creatorsapi.amazon/catalog/v1/search',
    'https://creatorsapi.amazon/catalog/v1/searchCatalogItems',
]
RESOURCES = ['itemInfo.title', 'images.primary.large', 'offersV2.listings.price']


def post(url, body, headers, form=False):
    data = urllib.parse.urlencode(body).encode() if form else json.dumps(body).encode()
    ctype = 'application/x-www-form-urlencoded' if form else 'application/json'
    req = urllib.request.Request(url, data=data, headers={'Content-Type': ctype, **headers}, method='POST')
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode('utf-8', 'replace')[:400].replace('\n', ' ')


def main():
    cid = (os.environ.get('CREATORS_CLIENT_ID') or '').strip()
    sec = (os.environ.get('CREATORS_CLIENT_SECRET') or '').strip()
    tag = os.environ.get('AMAZON_TAG', 'redcomet-22')
    if not cid or not sec:
        sys.exit('認証情報が ありません')
    if cid.startswith('amzn1.oa2-cs.') and sec.startswith('amzn1.application-oa2-client.'):
        cid, sec = sec, cid

    st, tok = post(TOKEN_URL, {'grant_type': 'client_credentials', 'client_id': cid,
                               'client_secret': sec, 'scope': 'creatorsapi::default'}, {})
    if st != 200 or not isinstance(tok, dict) or not tok.get('access_token'):
        sys.exit('トークンが 取れません: %s %s' % (st, tok))
    head = {'Authorization': 'Bearer ' + tok['access_token'], 'x-marketplace': MARKETPLACE}
    print('トークン OK')

    for kw in sys.argv[1:]:
        print('\n=== 「%s」 ===' % kw)
        for url in CANDIDATES:
            body = {'keywords': kw, 'marketplace': MARKETPLACE, 'partnerTag': tag,
                    'resources': RESOURCES, 'itemCount': 5, 'searchIndex': 'Books'}
            st, res = post(url, body, head)
            if st != 200:
                print('  ×', url.rsplit('/', 1)[-1], st, str(res)[:200])
                continue
            print('  ○', url.rsplit('/', 1)[-1])
            items = (res.get('searchResult') or res.get('itemResults') or res.get('itemsResult') or {}).get('items') or []
            if not items:
                print('    返ってきた 中身:', json.dumps(res, ensure_ascii=False)[:400])
            for it in items:
                title = ((it.get('itemInfo') or {}).get('title') or {}).get('displayValue')
                listings = ((it.get('offersV2') or {}).get('listings') or [])
                price = ((listings[0].get('price') or {}).get('money') or {}).get('displayAmount') if listings else None
                print('    %s  %s  %s' % (it.get('asin'), price or '-', (title or '')[:60]))
            break


if __name__ == '__main__':
    main()
