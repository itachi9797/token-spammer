import os
import random
import aiohttp
import asyncio
from colorama import Fore, Style 

guild_id = 1058826279132078160
channel_id = 1130803384102961152
messages_list = []

class colors:
  def error(txt):
    print(f"{Fore.RED}[{random.choice(['-', '!'])}]{Fore.RESET}{Style.DIM} {txt}{Fore.RESET}{Style.NORMAL}")

  def success(txt):
    print(f"{Fore.GREEN}[+]{Fore.RESET}{Style.BRIGHT} {txt}{Fore.RESET}{Style.NORMAL}")

  def warning(txt):
    print(f"{Fore.LIGHTYELLOW_EX}[!]{Fore.RESET}{Style.DIM} {txt}{Fore.RESET}{Style.NORMAL}")

with open("messages.txt", "r") as file:
    messages_list = file.read().splitlines()

tokens = open("tokens.txt", "r").read().split("\n")

async def send_message(token):
    headers = {
        'Authorization': token,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9001 Chrome/83.0.4103.122 Electron/9.3.5 Safari/537.36'
    }
    async with aiohttp.ClientSession() as session:
        while True:
            msg = random.choice(messages_list)
            async with session.post(f"https://discord.com/api/v10/channels/{channel_id}/messages",
                                    headers=headers, json={"content": msg}) as response:
                if response.status in [200, 204, 201]:
                    colors.success("Successfully Sent Message")
                    await asyncio.sleep(1)
                elif response.status == 429:    
                    colors.warning("Rate Limited")
                    os.system(" kill 1")
                else:
                   colors.error("Failed To Send Message")

async def main():
    tasks = []
    for token in tokens:
        task = asyncio.create_task(send_message(token))
        tasks.append(task)
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
