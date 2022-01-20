from tokenize import Token
import discord
from bs4 import BeautifulSoup
import requests
import asyncio
import top_crypto_price_checker as crypto


def read_token():
    with open('./Crypto_Bot/token.txt', 'r') as f:
        lines = f.readlines()
        return lines[0].strip()


TOKEN = read_token()

url = "https://coinmarketcap.com/"
result = requests.get(url).text
doc = BeautifulSoup(result, "html.parser")

tbody = doc.tbody
trs = tbody.contents
game = discord.Game("!help | !search")
client = discord.Client(activity=game)


# async def update_list():
#     await client.wait_until_ready()

#     while not client.is_closed():
#         try:
#             all_crypto = crypto.all_crypto()

#             await asyncio.sleep(86400)
#         except Exception as e:
#             print(e)
#             await asyncio.sleep(86400)


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")


@client.event
async def on_message(message):
    username = str(message.author).split("#")[0]
    user_message = str(message.content)
    channel = str(message.channel.name)
    print(f"{username}: {user_message} ({channel})")

    if message.author == client.user:
        return

    if user_message.lower() == "!hello":
        await message.channel.send(f"Hello {username}!")
        return
    elif user_message.lower() == "!help":
        global_ = discord.Embed(title="Global commands",
                                description="These can be used in any channel")
        global_.add_field(name="!hello", value="Crypto responds to you")
        crypto_only = discord.Embed(
            title="Crypto channel", description="These commands can only be used in the crypto channel")
        crypto_only.add_field(
            name="!random", value="Gives you a random cryptocurrency")
        crypto_only.add_field(
            name="!price", value="Explains why some cryptocurrencies have a price of $0.00")
        crypto_only.add_field(
            name="!topcrypto", value="Gives you the number 1 cryptocurrency")
        crypto_only.add_field(
            name="!search <cryptocurrency name>", value="Allows you to search any cryptocurrency on the website")
        crypto_only.add_field(
            name="!topten", value="Gives you the top 10 cryptocurrencies")
        crypto_only.add_field(name="!tophundred",
                              value="Gives you the top 100 cryptocurrencies")
        await message.channel.send(embed=global_)
        await message.channel.send(embed=crypto_only)

    if message.channel.name == "crypto":
        if user_message.lower() == "!random":
            random_crypto = crypto.random_crypto()
            await message.channel.send(f"{random_crypto}")
            return
        elif user_message.lower() == "!price":
            await message.channel.send("If the displayed price is $0.00, this means the price is less than $0.00. for example: $0.000273. ")
            return
        elif user_message.lower() == "!topcrypto":
            top_crypto = crypto.top_crypto()
            await message.channel.send(f"{top_crypto}")
            return
        elif user_message.find("!search") != -1:
            try:
                name = message.content
                crypto_name = str(name).split("search")[1][1:]
                url = f"https://coinmarketcap.com/currencies/{crypto_name}/"
                result = requests.get(url).text
                doc = BeautifulSoup(result, "html.parser")
                print(crypto_name)

                symbol = doc.find(class_="sc-16r8icm-0 gpRPnR nameHeader")
                name = doc.find(class_="sc-1q9q90x-0 jCInrl h1")
                initial = str(name).split(">")[2][:-7]
                price = doc.find(class_="priceValue")
                market = doc.find(class_="statsValue")
                coin_image = str(symbol).split(">")[1].split('"')[5]
                coin_name = str(name).split(">")[1].split("<")[0]
                coin_price = str(price).split("span")[1][1:-2]
                market_cap = str(market).split(">")[1][:-5]
                coin = discord.Embed(title=f"{coin_name} ({initial})")
                coin.set_thumbnail(url=f"{coin_image}")
                coin.add_field(name="Price:", value=f"{coin_price}")
                coin.add_field(name="Market Cap:", value=f"{market_cap}")
                coin.add_field(name="Link:", value=f"{url}")
                await message.channel.send(embed=coin)
                print(coin_image)
            except Exception as e:
                print(e)
                await message.channel.send(f"@{username} BEEP! BOOP! Cryptocurrency doesnt seem to exist")
        elif user_message.lower() == "!topten":
            id = 1
            top_ten = discord.Embed(title="Top ten", type="text")
            for tr in trs[:10]:
                name, price = tr.contents[2:4]
                market_cap = tr.contents[6]
                coin_initial = str(name).split("class")[9].split(">")[1][:-3]
                coin_name = name.p.string
                coin_price = price.span.string
                coin_market_cap = str(market_cap).split(">")[3][:-6]
                top_ten.add_field(
                    name=f"Name: {id}. {coin_name} ({coin_initial})", value=f"""Price: {coin_price} 
                    Market Cap: {coin_market_cap}""")
                # top_ten.add_field(name="Market Cap:",
                #                   value=f"{coin_market_cap}")
                id += 1
            await message.channel.send(embed=top_ten)
            return
        elif user_message.lower() == "!tophundred":
            id = 1
            top_hundred = discord.Embed(title="Top 100")
            for tr in trs:
                name, price = tr.contents[2:4]
                doc_name = name.a
                doc_price = price.span
                try:
                    symbol = str(doc_name).split("span")[5][23:-2]
                    coin_name = str(doc_name).split("span")[3][1:-2]
                    currency = str(doc_price).split(">")[1][0]
                    coin_price = str(doc_price).split(">")[2][:4]
                    top_hundred.add_field(
                        name=f"Name: {id}. {coin_name} ({symbol})", value=f"""Price: {currency}{coin_price}""")

                except Exception:
                    coin_initial = str(name).split("class")[
                        9].split(">")[1][:-3]
                    coin_name = name.p.string
                    coin_price = price.span.string
                    top_hundred.add_field(
                        name=f"Name: {id}. {coin_name} ({coin_initial})", value=f"""Price: {coin_price}""")

                id += 1
            await message.channel.send(embed=top_hundred)

# client.loop.create_task(update_list())
client.run(TOKEN)
