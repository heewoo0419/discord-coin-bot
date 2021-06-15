import asyncio
import datetime
import os

import discord
import requests
from decimal import *

client = discord.Client()

# 생성된 토큰을 입력해준다.
token = os.environ["TOKEN"]



# 봇이 구동되었을 때 보여지는 코드
@client.event
async def on_ready():
    print("다음으로 로그인합니다")
    print(client.user.name)
    print(client.user.id)
    print("================")


# 봇이 특정 메세지를 받고 인식하는 코드
@client.event
async def on_message(message):
    # 메세지를 보낸 사람이 봇일 경우 무시한다
    if message.author.bot:
        return None

    if message.content.startswith('!안녕'):
        channel = message.channel
        await channel.send('반가워!')

    elif message.content.startswith('!명령어'):
        channel = message.channel
        embed = discord.Embed(title="명령어 목록", color=0x0051C7)
        embed.add_field(name="이모지", value="!떡락, !떡상, !드가자, !대공황, !대호황", inline=False)
        embed.add_field(name="코인 시세", value="!<마켓> <코인이름>", inline=False)
        await channel.send(embed=embed)

    elif message.content.startswith('!떡락'):
        channel = message.channel
        embed = discord.Embed(color=0x0051C7)
        embed.set_image(url="https://www.dogdrip.net/dvs/d/20/08/29/aa58a3f207326ff0b944a1f7538688ef.jpg")
        await channel.send(embed=embed)

    elif message.content.startswith('!떡상'):
        channel = message.channel
        embed = discord.Embed(color=0xd60000)
        embed.set_image(url="https://www.dogdrip.net/dvs/d/20/08/29/4fd145c38189ac5683acc9be3e17f184.jpg")
        await channel.send(embed=embed)

    elif message.content.startswith('!드가자'):
        channel = message.channel
        embed = discord.Embed(color=0xd60000)
        embed.set_image(url="https://www.dogdrip.net/dvs/d/21/02/28/d70bdeae55e567fe6ede9d40f116d04b.jpg")
        await channel.send(embed=embed)

    elif message.content.startswith('!대공황'):
        channel = message.channel
        embed = discord.Embed(color=0xd60000)
        embed.set_image(url="https://www.dogdrip.net/dvs/d/21/02/28/f1025b187944b843828cc85467bea86c.jpg")
        await channel.send(embed=embed)

    elif message.content.startswith('!대호황'):
        channel = message.channel
        embed = discord.Embed(color=0xd60000)
        embed.set_image(url="https://www.dogdrip.net/dvs/d/21/02/28/c17bc0d9af8d67d5b071810c0aeadb25.jpg")
        await channel.send(embed=embed)

    elif message.content.startswith('!바이낸스'):
        channel = message.channel
        coin_symbol = message.content.replace("!바이낸스 ", "")
        coin_symbol = str(coin_symbol).upper()

        response = requests.get(
            url="https://fapi.binance.com/fapi/v1/ticker/24hr",
            headers={"Accept": "application/json"},
            params={"symbol": coin_symbol + "USDT"}
        )

        coin_data = response.json()
        try:
            color = 0xd60000 if float(coin_data['priceChange']) > 0 else 0x0051C7
            embed = discord.Embed(title=coin_symbol + "/USDT" + " 일별 시세", color=color)
            embed.set_thumbnail(url=f"https://icons.bitbot.tools/api/{coin_symbol}/128x128")
            #embed.set_image(url=f"https://imagechart.upbit.com/d/mini/{coin_symbol}.png")
            # embed.add_field(name="시가", value=coin_data['opening_price'], inline=False)
            embed.add_field(name="저가", value="{:,}".format(float(coin_data['lowPrice'])) + " USD", inline=True)
            embed.add_field(name="고가", value="{:,}".format(float(coin_data['highPrice'])) + " USD", inline=True)
            embed.add_field(name="종가", value="{:,}".format(float(coin_data['lastPrice'])) + " USD", inline=False)
            arrow = ":small_red_triangle:" if float(coin_data['priceChange']) > 0 else ":small_red_triangle_down:"

            change_text = arrow + " {:,}".format(
                float(coin_data['priceChange'])) + " USD" + f" ({coin_data['priceChangePercent']}%)"
            embed.add_field(name="전일대비", value=change_text, inline=False)
            date = datetime.datetime.fromtimestamp(int(coin_data['closeTime']) // 1000).strftime('%Y-%m-%d %H:%M')
            embed.set_footer(text=f"\n({date} 기준)", icon_url="https://cryptologos.cc/logos/binance-coin-bnb-logo.png?v=010")
            await channel.send(embed=embed)
        except:
            await channel.send("코인을 찾을 수 없습니다")


    elif message.content.startswith("!주식"):
        channel = message.channel
        keyword = message.content.replace("!주식 ", "")
        response = requests.get(
            url="https://stockplus.com/api/search/autocomplete.json",
            params={
                "keyword": keyword
            }
        )
        res_json = response.json()
        print(response.json())
        if not res_json['suggestItems']:
            await channel.send("찾을수가 없어요 😥")
        else:
            asset_id = res_json['suggestItems'][0]['assetId']

            response = requests.get(
                url=f"https://stockplus.com/api/securities/{asset_id}.json",
                params={
                    "keyword": keyword
                }
            )
            stock_data = response.json()['recentSecurity']
            print(stock_data)
            color = 0xd60000 if stock_data['changePrice'] > 0 else 0x0051C7
            embed = discord.Embed(title=stock_data['name']+ " 일별 시세" , description= f" ({stock_data['marketName']} {stock_data['shortCode']})", color=color)

            # 일봉
            embed.set_image(url=stock_data['dayChartUrl'])

            embed.add_field(name="저가", value="{:,}".format(int(stock_data['lowPrice'])) + " KRW", inline=True)
            embed.add_field(name="고가", value="{:,}".format(int(stock_data['highPrice'])) + " KRW", inline=True)
            embed.add_field(name="종가", value="{:,}".format(int(stock_data['displayedPrice'])) + " KRW", inline=False)
            arrow = ":small_red_triangle:" if stock_data['changePrice'] > 0 else ":small_red_triangle_down:"

            change_text = arrow + " {:,}".format(int(stock_data['changePrice'])) + " KRW" + f" ({round(stock_data['changePriceRate'] * 100, 2)}%)"
            embed.add_field(name="전일대비", value=change_text, inline=False)
            date = stock_data['date']
            embed.set_footer(text=f"\n({date} 기준)", icon_url="https://cdn.stockplus.com/stockplus-web/server_assets/assets/images/common/title_stock-934bc4bc65f5f19e61462c3a71e5a1eca241cd1354982b5727ba4bff9354798d.png")

            await channel.send(embed=embed)


    elif message.content.startswith('!업비트'):
        channel = message.channel
        response = requests.get(
            url="https://api.upbit.com/v1/market/all",
            headers={"Accept": "application/json"},
            params={"isDetails": "false"}
        )
        response_json = response.json()
        coin_data = ""
        coin_kor_name = ""
        market_code = ""

        for data in response_json:
            if data['korean_name'] == message.content.replace("!업비트 ", "") and data['market'][:3] == "KRW":
                print(data)
                coin_data = data
                coin_kor_name = data['korean_name']
                market_code = data['market']
                break

        if coin_data == "":
            await channel.send("그런 코인 없음")
        else:
            response = requests.get(
                url="https://api.upbit.com/v1/candles/days",
                headers={"Accept": "application/json"},
                params={"market": market_code, "count": "1", "convertingPriceUnit": "KRW"}
            )
            coin_data = response.json()[0]
            coin_code = market_code.replace("KRW-", "")
            color = 0xd60000 if coin_data['change_price'] > 0 else 0x0051C7
            embed = discord.Embed(title=coin_kor_name + f" ({coin_code})" + " 일별 시세", color=color)
            embed.set_thumbnail(url=f"https://static.upbit.com/logos/{coin_code}.png")
            embed.set_image(url=f"https://imagechart.upbit.com/d/mini/{coin_code}.png")
            #embed.add_field(name="시가", value=coin_data['opening_price'], inline=False)
            embed.add_field(name="저가", value="{:,}".format(int(coin_data['low_price'])) + " KRW", inline=True)
            embed.add_field(name="고가", value="{:,}".format(int(coin_data['high_price'])) + " KRW", inline=True)
            embed.add_field(name="종가", value="{:,}".format(int(coin_data['trade_price'])) + " KRW", inline=False)
            arrow = ":small_red_triangle:" if coin_data['change_price'] > 0 else ":small_red_triangle_down:"

            change_text = arrow + " {:,}".format(int(coin_data['change_price'])) + " KRW" + f" ({round(coin_data['change_rate'] * 100, 2)}%)"
            embed.add_field(name="전일대비", value=change_text, inline=False)
            date = datetime.datetime.fromtimestamp(int(coin_data['timestamp']) // 1000).strftime('%Y-%m-%d %H:%M')
            embed.set_footer(text=f"\n({date} 기준)", icon_url="https://search1.daumcdn.net/thumb/C53x16.q80/?fname=https%3A%2F%2Fsearch1.daumcdn.net%2Fsearch%2Fstatics%2Fspecial%2Fmi%2Fr2%2Fimg_upbit.png")

            await channel.send(embed=embed)


client.run(token)
