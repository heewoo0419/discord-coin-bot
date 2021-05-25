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


    elif message.content.startswith('!'):
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
            if data['korean_name'] == message.content.replace("!", "") and data['market'][:3] == "KRW":
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
