from tokenize import Token
import discord
import top_crypto_price_checker as crypto

TOKEN = 'OTMyNjc2MTM3NDAwODAzMzI5.YeWcVw.9HjjDAgxPGvLH2PHjWvo7RU0BsI'

client = discord.Client()


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")


@client.event
async def on_message(message):
    username = str(message.author).split("#")[0]
    user_message = str(message.content)
    channel = str(message.channel.name)
    print(f"{username}: {user_message} {(channel)}")

    if message.author == client.user:
        return

    if user_message.lower() == "!hello":
        await message.channel.send(f"Hello {username}!")
        return
    elif user_message.lower() == "!random":
        random_crypto = crypto.random_crypto()
        await message.channel.send(f"""
        {str(random_crypto)}
        """)
        return
    elif user_message.lower() == "!price":
        await message.channel.send("If the displayed price is $0.00, this means the price is less than $0.00. for example: $0.000273. ")

client.run(TOKEN)
