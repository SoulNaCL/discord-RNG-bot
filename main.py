from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message, app_commands
from discord.ext import commands
from responses import get_response
import yaml

load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')
intents: Intents = Intents.default()
intents.message_content = True # NOQA
client: Client = Client(intents=intents)

std_items = {
    "auras": ["Common", "Uncommon"],
    "inventory_limit": 10,
    "rolls": 0,
    "effects": {
        "test": 1
    },
    "luck_mult": 1,
    "dev_status": 0
}


async def send_message(message: Message, user_message: str, user_id: str) -> None:
    if not user_message:
        print("Message was empty")
        return

    try:
        response: str = get_response(user_message, user_id)
        await message.reply(response)
    except Exception as e:
        print(e)


@client.event
async def on_ready() -> None:
    print(f"{client.user} is now running!")


@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return

    username: str = str(message.author)
    userid: str = str(message.author.id)
    user_message: str = str(message.content)
    channel: str = str(message.channel)
    ufile: str = "users/" + userid + ".yml"

    if os.path.exists(ufile):
        print()
    else:
        print("Creating save file...")
        with open(ufile, "w") as file:
            yaml.dump(std_items, file, default_flow_style=False)

    print(f"[{channel}] {username}({userid}): {user_message}")
    await send_message(message, user_message, userid)


def main() -> None:
    client.run(token=TOKEN)


if __name__ == "__main__":
    main()
