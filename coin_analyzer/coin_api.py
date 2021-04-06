from datetime import datetime

import requests
from requests import HTTPError
from data_converter import build_market_values, calculate_price_change_rate


def read_specified_hour_market_values(hour_interval_count):
    all_market_data_hourly = []
    coin_informations = []

    json_responses = get_data_from_coin_api(hour_interval_count)

    for json_response in json_responses:
        for data in json_response['data']:
            coin_informations.append({'coin_id': data['id'], 'symbol': data['symbol']})

            for index in range(len(data['timeSeries'])):
                time_series = data['timeSeries'][index]
                price = time_series['close']

                market_data_hourly = build_market_values(data['id'], time_series)

                if index != (len(data['timeSeries']) - 1):
                    next_price = data['timeSeries'][index + 1]['close']

                    if next_price is not None and price is not None:
                        market_data_hourly['price_change_rate'] = calculate_price_change_rate(price, next_price)
                        all_market_data_hourly.append(market_data_hourly)

    return all_market_data_hourly, coin_informations


def read_current_market_values():
    all_market_data_hourly = []
    coin_informations = []
    hour_interval_count = 2

    json_responses = get_data_from_coin_api(hour_interval_count)

    for json_response in json_responses:
        for data in json_response['data']:
            coin_informations.append({'coin_id': data['id'], 'symbol': data['symbol']})

            last_time_series_index = len(data['timeSeries']) - 1
            if last_time_series_index >= 0:
                market_data_hourly = build_market_values(data['id'], data['timeSeries'][last_time_series_index])

                all_market_data_hourly.append(market_data_hourly)

    return all_market_data_hourly, coin_informations


def get_data_from_coin_api(hour_interval_count):
    print("Take data from api ", datetime.now())
    json_responses = []

    for symbols in get_symbol_data():
        json_responses.append(get_partial_data_from_coin_api(symbols, hour_interval_count))

    print("Data taken from api ", datetime.now())
    return json_responses


def get_partial_data_from_coin_api(symbols, hour_interval_count):
    try:
        response = requests.get(
            'https://api.lunarcrush.com/v2?'
            'data=assets'
            '&key={SECRET_API_KEY}'
            '&symbol=' + str(symbols) +
            '&interval=hour'
            '&data_points=' + str(hour_interval_count)
        )
        response.raise_for_status()
        return response.json()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        return None
    except Exception as err:
        print(f'Other error occurred: {err}')
        return None


def get_symbol_data():
    return [
        'LTC,ETH,NEO,BNB,QTUM,EOS,SNT,BNT,GAS,BCC,USDT,HSR,OAX,DNT,MCO',
        'ICN,ZRX,OMG,WTC,YOYO,LRC,TRX,SNGLS,STRAT,BQX,FUN,KNC,CDT,XVG',
        'IOTA,SNM,LINK,CVC,TNT,REP,MDA,MTL,SALT,NULS,SUB,STX,MTH,ADX',
        'ETC,ENG,ZEC,AST,GNT,DGD,BAT,DASH,POWR,BTG,REQ,XMR,EVX,VIB,ENJ',
        'VEN,ARK,XRP,MOD,STORJ,KMD,RCN,EDO,DATA,DLT,MANA,PPT,RDN,GXS',
        'AMB,ARN,BCPT,CND,GVT,POE,BTS,FUEL,XZC,QSP,LSK,BCD,TNB,ADA,LEND',
        'XLM,CMT,WAVES,WABI,GTO,ICX,OST,ELF,AION,WINGS,BRD,NEBL,NAV,VIBE',
        'LUN,TRIG,APPC,CHAT,RLC,INS,PIVX,IOST,STEEM,NANO,AE,VIA,BLZ,SYS',
        'RPX,NCASH,POA,ONT,ZIL,STORM,XEM,WAN,WPR,QLC,GRS,CLOAK,LOOM,BCN',
        'TUSD,ZEN,SKY,THETA,IOTX,QKC,AGI,NXS,SC,NPXS,KEY,NAS,MFT,DENT,IQ',
        'ARDR,HOT,VET,DOCK,POLY,VTHO,ONG,PHX,HC,GO,PAX,RVN,DCR,USDC,MITH',
        'BCHABC,BCHSV,REN,BTT,USDS,FET,TFUEL,CELR,MATIC,ATOM,PHB,ONE,FTM',
        'BTCB,USDSB,CHZ,COS,ALGO,ERD,DOGE,BGBP,DUSK,ANKR,WIN,TUSDB,COCOS',
        'PERL,TOMO,BUSD,BAND,BEAM,HBAR,XTZ,NGN,DGB,NKN,GBP,EUR,KAVA,RUB',
        'UAH,ARPA,TRY,CTXC,AERGO,BCH,TROY,BRL,VITE,FTT,AUD,OGN,DREP,BULL',
        'BEAR,ETHBULL,ETHBEAR,XRPBULL,XRPBEAR,EOSBULL,EOSBEAR,TCT,WRX,LTO',
        'ZAR,MBL,COTI,BKRW,BNBBULL,BNBBEAR,HIVE,STPT,SOL,IDRT,CTSI,CHR',
        'BTCUP,BTCDOWN,HNT,JST,FIO,BIDR,STMX,MDT,PNT,COMP,IRIS,MKR,SXP,SNX',
        'DAI,ETHUP,ETHDOWN,ADAUP,ADADOWN,LINKUP,LINKDOWN,DOT,RUNE,BNBUP',
        'BNBDOWN,XTZUP,XTZDOWN,AVA,BAL,YFI,SRM,ANT,CRV,SAND,OCEAN,NMR,LUNA',
        'IDEX,RSR,PAXG,WNXM,TRB,EGLD,BZRX,WBTC,KSM,SUSHI,YFII,DIA,BEL,UMA',
        'EOSUP,TRXUP,EOSDOWN,TRXDOWN,XRPUP,XRPDOWN,DOTUP,DOTDOWN,NBS,WING',
        'SWRV,LTCUP,LTCDOWN,CREAM,UNI,OXT,SUN,AVAX,BURGER,BAKE,FLM,SCRT,XVS',
        'CAKE,SPARTA,UNIUP,UNIDOWN,ALPHA,ORN,UTK,NEAR,VIDT,AAVE,FIL,SXPUP',
        'SXPDOWN,INJ,FILDOWN,FILUP,YFIUP,YFIDOWN,CTK,EASY,AUDIO,BCHUP,BCHDOWN',
        'BOT,AXS,AKRO,HARD,KP3R,RENBTC,SLP,STRAX,UNFI,CVP,BCHA,FOR,FRONT,ROSE',
        'HEGIC,AAVEUP,AAVEDOWN,PROM,BETH,SKL,GLM,SUSD,COVER,GHST,SUSHIUP',
        'SUSHIDOWN,XLMUP,XLMDOWN,DF,JUV,PSG,BVND,GRT,CELO,TWT,REEF,OG,ATM',
        'ASR,1INCH,RIF,BTCST,TRU,DEXE,CKB,FIRO,LIT,PROS,VAI,SFP,FXS,DODO',
        'AUCTION,UFT,ACM,PHA,TVK,BADGER,FIS,OM,POND,ALICE,DEGO,BIFI,LINA'
    ]
