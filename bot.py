import datetime
import json
import random
import time
import discord
import asyncio
from discord.ext import commands, tasks
from javascript import require, On, Once, globalThis, AsyncTask
from mcuuid import MCUUID

import external_functions
from config import *

mineflayer = require("mineflayer", "latest")

timer_start = time.perf_counter()
baltop_mc = []
time_bot, time_bot2, multiplayers, messages_per_cycle, one_time_multiplayer, allow_multiply, event_founder, temp_login, x, current_word, multiply_win, illegal_chars, wplacanie_users = 0, 0, [], 0, False, True, [], 0, '{}', "gfueghnv73rytgy67rbc673v634b8^TR%^BT&^rt7634WRTV37R", 1, "!@#$%^&*().-_?';:'<>[]{}`~/\\| ", []
people_balance = json.loads(x)

client = commands.Bot(command_prefix=f"{prefix}")

bot = mineflayer.createBot({
    "host": "_dc-srv.9371b3209dd5._minecraft._tcp.skyheroes.pl",
    "username": nickname,
    'hideErrors': False,
    'logErrors': True
})
Item = require("prismarine-item")(bot.version)


def get_baltop():
    for number in range(1, 45):
        bot.chat(f"/baltop {number}")
        time.sleep(0.3)


def check_win(username, message):
    global current_word, timer_start
    timer_end = time.perf_counter()
    if username in blacklist:
        return
    elif message == current_word:
        time_winning = timer_end - timer_start
        prize = round(((10 / round(time_winning, 2)) * 215 * multiply_win))
        reset_multiplayer()
        bot.chat(f"Gz @{username} Wygrał {prize}⛃ w czasie {round(time_winning, 2)}s pisząc słowo {current_word}")
        current_word = "gfueghnv73rytgy67rbc673v634b8^TR%^BT&^rt7634WRTV37R"
        bot.chat(f"/pay {username} {prize}")


def host_reaction():
    global current_word, timer_start, messages_per_cycle
    if messages_per_cycle > 20:
        messages_per_cycle = 0
        try:
            word = random.choice(passes)
            bot.chat(f"Napisz na chacie: {word}")
            current_word = word
            timer_start = time.perf_counter()
        except:
            pass


def removeDuplicates(s):
    chars = [' ', '']
    for c in s:
        chars.reverse()
        if chars[0] != chars[1] and chars[1] != c:
            chars.reverse()
            chars.append(c)
        elif chars[0] != chars[1]:
            chars.reverse()
            chars.append(c)
        elif chars[1] != c:
            chars.reverse()
            chars.append(c)
        else:
            print(chars[0], chars[1], c)
            chars.reverse()

    return ''.join(chars)


def reset_multiplayer():
    global one_time_multiplayer, multiply_win
    if one_time_multiplayer and multiply_win != 1:
        multiply_win = 1
        one_time_multiplayer = False


def check_abuse(username, message):
    global messages_per_cycle
    uuu = message.split(" ")
    for uju in uuu:
        for word in words:
            if uju == word:
                message = f"{message} - możliwe wykroczenie `{word}`"
                try:
                    player = MCUUID(name=username)
                    abuse_hook.send(message.replace("@", "@ ") + "  <@&879445333023817760>", username=username,
                                    avatar_url=f"https://crafatar.com/avatars/{player.uuid}?overlay")
                except:
                    abuse_hook.send(message.replace("@", "@ ") + "  <@&879445333023817760>", username=username)
            else:
                for char in illegal_chars:
                    uju.replace(char, "")
                if uju == word:
                    message = f"{message} - możliwe wykroczenie `{word}`"
                    try:
                        player = MCUUID(name=username)
                        abuse_hook.send(message.replace("@", "@ ") + "  <@&879445333023817760>", username=username,
                                        avatar_url=f"https://crafatar.com/avatars/{player.uuid}?overlay")
                    except:
                        abuse_hook.send(message.replace("@", "@ ") + "  <@&879445333023817760>", username=username)


def chat_regex():
    bot.addChatPatternSet(
        "SH_prefix",
        [globalThis.RegExp("^\(.+\) (.+) (.+) \[(.+)\] » (.+)$")],
        {"parse": True}
    )
    bot.addChatPatternSet(
        "SH_Out_prefix",
        [globalThis.RegExp("^\(.+\) (.+) (.+) » (.+)$")],
        {"parse": True}
    )
    bot.addChatPatternSet(
        "SH_private_msg",
        [globalThis.RegExp("^\[(.+) -> Ja\] » (.+)$")],
        {"parse": True}
    )
    bot.addChatPatternSet(
        "SH_get_money",
        [globalThis.RegExp("^Otrzymałeś (.+)⛃ od (.+). Kwota: (.+)⛃$")],
        {"parse": True}
    )
    bot.addChatPatternSet(
        "SH_balance",
        [globalThis.RegExp("^Stan konta: (.+)⛃$")],
        {"parse": True}
    )
    bot.addChatPatternSet(
        "Sh_boss",
        [globalThis.RegExp("Boss (.+) został odrodzony!")],
        {"parse": True}
    )
    bot.addChatPatternSet(
        "Sh_baltop",
        [globalThis.RegExp("^(.+)\. (.+): (.+)⛃$")],
        {"parse": True}
    )


@On(bot, "spawn")
def handle(*args):
    print("SPAWN")
    if "§r§7Twoja siec serwerow Minecraft!" not in bot.tablist.header.json.text:
        print("LOBBY")
        time.sleep(10)
        bot.chat(f"/login {password}")
        time.sleep(1)
        print("KROK 1")
        bot.setQuickBarSlot(0)
        time.sleep(1)
        bot.setQuickBarSlot(0)
        print("KROK 2")
        time.sleep(1)
        bot.activateItem()
        time.sleep(1)
        bot.activateItem()
        print("KROK 3")
        time.sleep(1)
        chat_regex()
        print("KROK 4")
        try:
            bot.clickWindow(13, 0, 0)
        except:
            return
        print("KROK 5")
        return
    # bot.chat("o/")


@On(bot, "chat:Sh_baltop")
def handle(this, data, *args):
    global people_balance, baltop_mc
    place = data[0][0]
    username = data[0][1]
    balance = data[0][2]
    balance = float(balance.replace(",", ""))
    people_balance[username] = balance
    if not "Otrzymałeś" in place:
        if int(place) <= 10:
            if int(place) == 1:
                baltop_mc = []
            print(place, username, balance)
            eee = -1
            if username == "JezzIt":
                eee = place
            if [username, balance, int(eee)] not in baltop_mc:
                baltop_mc.append([username, balance, int(place)])
    if place == "440":
        with open("balance.json", "w") as f:
            f.write(json.dumps(people_balance, indent=4, sort_keys=True))
            f.close()
        eee = ['czarnulka', 'eggidogo', 'x_Melanx_x', 'Norweeg', 'JezzIt']
        for username in people_balance:
            if username in eee:
                try:
                    player = MCUUID(name=username)
                    logs_hook.send(f"Stan konta `{username}`: {people_balance[username]}", username=username,
                                   avatar_url=f"https://crafatar.com/avatars/{player.uuid}?overlay")
                except:
                    logs_hook.send(f"Stan konta `{username}`: {people_balance[username]}", username=username)


@On(bot, "chat:Sh_boss")
def handle(this, data, *args):
    boss = data[0][0]
    boss_hook.send(f"Boss pojawił się: {boss} <@&883977850246529024>", username=boss)


@AsyncTask
@On(bot, "chat:SH_private_msg")
def handle(this, data, *args):
    username: str = data[0][0]
    message: str = data[0][1]
    if username != "eggidogo":
        try:
            private_hook.send(message.replace("@", "@ ").replace("_", "\\_").replace("*", "\\*"), username=username,
                              avatar_url=f"https://crafatar.com/avatars/{MCUUID(name=username).uuid}?overlay")
        except Exception as e:
            private_hook.send(message.replace("@", "@ ").replace("_", "\\_").replace("*", "\\*"), username=username)
    if username in blacklist:
        bot.chat(f"/msg {username} ok")
        return
    if username == "eggidogo" and message == "baltop":
        get_baltop()
    elif message == "wplac":
        wplacanie_users.append(username)
        bot.chat(f"/msg {username} Przelej mi teraz określoną kwotę /pay JezzIt")
    elif message.startswith("create account"):
        message = message.replace("create account ", "")
        if message == "" or message == "create account":
            bot.chat(f"/msg {username} Poprawne użycie: create account <discord id>")
            return
        else:
            try:
                message = int(message)
                external_functions.new_account(username, message)
                for guild in client.guilds:
                    for member in guild.members:
                        if member.id == int(message):
                            loop = asyncio.new_event_loop()
                            asyncio.set_event_loop(loop)
                            result = loop.run_until_complete(member.edit(nick=username))
                bot.chat(f"/msg {username} poprawnie utworzono konto!")
            except:
                bot.chat(f"/msg {username} Coś poszło nie tak :|")
                return
    elif message.startswith("bal"):
        message = message.replace("bal ", "")
        if message == "" or message == "bal":
            bot.chat(f"/msg {username} Poprawne użycie: bal <nick>")
            return
        with open('balance.json', 'r') as f:
            balance = json.loads(f.read())
            f.close()
        if message not in balance:
            bot.chat(f"/msg {username} Nie odnaleziono {message} w bazie danych")
            return
        else:
            bot.chat(f"/msg {username} {message} stan konta: {balance[message]}")

    elif username == "eggidogo":
        bot.chat(message)


@AsyncTask
@On(bot, "chat:SH_prefix")
def handle(this, lista, *args):
    global messages_per_cycle
    messages_per_cycle += 1
    username = lista[0][1]
    message = lista[0][3]
    check_abuse(username, message.lower())
    username2 = username
    username3 = username
    check_win(username, message)
    if " >> " in message and username == "JezzIt":
        temp = message.split(" >> ")
        username3 = temp[0]
        username2 = f"[D] {temp[0]}"
        check_win(username3, message.replace(f"{username3} >> ", ""))
    try:
        chat_hook.send(message.replace("@", "@ ").replace("_", "\\_").replace("*", "\\*"), username=username2,
                       avatar_url=f"https://crafatar.com/avatars/{MCUUID(name=username3).uuid}?overlay")
    except Exception as e:
        chat_hook.send(message.replace("@", "@ ").replace("_", "\\_").replace("*", "\\*"), username=username)


@AsyncTask
@On(bot, "chat:SH_Out_prefix")
def handle(this, lista, *args):
    username = lista[0][1]
    message = lista[0][2]
    if "]" in username:
        return
    global messages_per_cycle
    messages_per_cycle += 1
    check_abuse(username, message)
    check_win(username, message)
    try:
        player = MCUUID(name=username)
        chat_hook.send(message.replace("@", "@ ").replace("_", "\\_").replace("*", "\\*"), username=username,
                       avatar_url=f"https://crafatar.com/avatars/{MCUUID(name=username).uuid}?overlay")
    except Exception as e:
        chat_hook.send(message.replace("@", "@ ").replace("_", "\\_").replace("*", "\\*"), username=username)


@AsyncTask
@On(bot, "message")
def handle(jsono, position, *args):
    global people_balance
    try:
        if "/cmil rmc" in str(position.json.extra[0].clickEvent.value):
            bot.chat(position.json.extra[0].clickEvent.value)
            print("przelano" + position.json.extra[0])
    except:
        pass


@On(bot, "chat:SH_get_money")
def handle(this, list, *args):
    username = list[0][1]
    amount = list[0][0]
    amount2 = amount.replace(",", "")
    try:
        private_hook.send(f"Przelano {amount} monet", username=username,
                          avatar_url=f"https://crafatar.com/avatars/{MCUUID(name=username).uuid}?overlay")
    except Exception as e:
        private_hook.send(f"Przelano {amount} monet", username=username)
    global wplacanie_users
    if username in wplacanie_users:
        print(username)
        if external_functions.change_amount(username,
                                            int(external_functions.get_amount(username)) + int(
                                                round(float(amount2), 0))):
            bot.chat(
                f"/msg {username} Pomyślnie wpłaciłeś {amount} na swoje ekonto, posiadasz teraz {external_functions.get_amount(username)}")
        else:
            bot.chat(f"/msg {username} Nie posiadasz konta")
            bot.chat(f"/pay {username} {amount2}")
    elif float(amount2) >= 200:
        bot.chat(f"Dzięki @{username} za darowizne w wysokości {amount}⛃")


@client.event
async def on_message(msg):
    if msg.author.bot:
        return
    if client.user.mentioned_in(msg):
        await msg.channel.send(f"Mój prefix to `{prefix}` Użyj `{prefix}help` po więcej informacji")
    if msg.channel.id == chat_channel:
        if msg.content.startswith("##"):
            return
        message = msg.content.strip()
        uuu = message.split(" ")
        for uju in uuu:
            for word in words:
                if uju == word:
                    await msg.channel.send(f"Nie pisz tak nie ładnie, brzytki jestes noobie LLL")
                    return
                else:
                    for char in illegal_chars:
                        uju.replace(char, "")
                    if uju == word:
                        await msg.channel.send(f"Nie pisz tak nie ładnie, brzytki jestes noobie LLL")
                        return
        bot.chat(f"{msg.author.display_name} >> {removeDuplicates(message)}")
        await msg.delete()
        return
    await client.process_commands(msg)


@client.command(aliases=['balance', 'money'], pass_context=True,
                brief=f"Pokazuje stan konta, użycie: {prefix}balance <nick>",
                description=f'Pokazuje stan konta, użycie: {prefix}balance <nick>')
async def bal(ctx, arg=None):
    with open('balance.json', 'r') as f:
        balance = json.loads(f.read())
        f.close()
    if not arg:
        await ctx.reply(f"Poprawne użycie: `{prefix}balance <nick>`")
        return
    elif arg not in balance:
        await ctx.reply(f"Nie odnaleziono `{arg}` w bazie danych")
        return
    else:
        await ctx.reply(f"{arg} stan konta: `{balance[arg]}`")


@client.command(aliases=['online'], brief=f"Pokazuje czy gracz jest aktywny, użycie: {prefix}active <nick>",
                description=f'Pokazuje czy gracz jest aktywny, użycie: {prefix}active <nick>')
async def active(ctx, arg=None):
    if not arg:
        await ctx.reply(f"Poprawne użycie: `{prefix}active <nick>`")
        return
    else:
        if bot.players[arg] is None:
            await ctx.channel.send(f"Gracz `{arg}` jest offline")
        else:
            await ctx.channel.send(f"Gracz `{arg}` jest online")


@client.command(aliases=['ebalance', 'emoney', 'monety'])
async def ebal(ctx, arg1=None):
    username = ctx.author.id
    if arg1 is not None:
        username = arg1
    balance = external_functions.get_amount(username)
    if balance is False:
        await ctx.send(f"Nie znaleziono konta")
        return
    em = discord.Embed(title="Stan konta wirtualnego", color=0x90e0ef, description=f"```Stan konta: {balance}```")
    em.set_footer(text=f"Wywowałane przez {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
    await ctx.send(embed=em)


@client.command(aliases=['ewithdraw', 'wyplac', 'dep'])
async def ewyplac(ctx, arg1: int = -1):
    if arg1 == -1:
        await ctx.reply("Nie podałeś ilości monet")
        return
    if arg1 < 49:
        await ctx.reply("Za mała wartość")
        return
    username = ctx.author.id
    if arg1 > external_functions.get_amount(username):
        await ctx.reply(f"Nie posiadasz tyle monet")
        return
    with open("bank.json", 'r') as f:
        bank_values = json.load(f)
    for user in bank_values:
        if int(bank_values[user][1]) == int(username):
            x = user
            break
    bot.chat(f"/pay {x} {arg1}")
    external_functions.change_amount(username, external_functions.get_amount(username) - arg1)
    try:
        player = MCUUID(name=ctx.author.display_name)
        private_hook.send(f"{username} ({ctx.author.display_name}) wypłacił {arg1} monet", username=username,
                          avatar_url=f"https://crafatar.com/avatars/{MCUUID(name=username).uuid}?overlay")
    except Exception as e:
        private_hook.send(f"{username} ({ctx.author.display_name}) wypłacił {arg1} monet", username=username)
    await ctx.reply(f"Wypłacono {arg1}, obecny stan konta: {external_functions.get_amount(username)}")


@commands.cooldown(1, 30, commands.BucketType.user)
@client.command(aliases=['praca', 'job'])
async def work(ctx):
    username = ctx.author.id
    balance = external_functions.get_amount(username)
    if balance is False:
        await ctx.reply(f"Nie znaleziono konta")
        return
    else:
        payout = random.randrange(25, 125)
        external_functions.change_amount(username, balance + payout)
        balance = external_functions.get_amount(username)
        em = discord.Embed(title="Zarobek", timestamp=datetime.datetime.utcnow(), color=0x90e0ef,
                           description=f"```Zarobiłeś {payout} i posiadasz teraz {balance} monet```")
        em.set_footer(text=f"Wywowałane przez {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=em)


@commands.cooldown(1, 25, commands.BucketType.user)
@client.command(aliases=['moneta'])
async def coinflip(ctx, arg2: int = None, arg1: str = None):
    if not arg2 or not arg1:
        await ctx.reply(f"Poprawne użycie: `{prefix}coinflip <zakład> <opcja>`\nnp: `{prefix}coinflip 200 orzeł`")
        return
    username = ctx.author.id
    balance = external_functions.get_amount(username)
    if balance is False:
        await ctx.reply(f"Nie znaleziono twojego konta")
        return
    if arg2 > balance:
        await ctx.reply("Nie posiadasz tyle pieniędzy")
        return
    if arg2 > 15000:
        await ctx.reply("Nie możesz tyle obstawić limit to 15k")
        return
    if arg1 == "orzeł":
        option = 0
    elif arg1 == "reszka":
        option = 1
    else:
        await ctx.reply("Nie podałeś opcji `orzeł/reszka`")
        return

    r_option = random.randrange(3)
    if option == 1 and r_option == 2:
        r_option = 0
    elif option == 0 and r_option == 2:
        r_option = 1
    if r_option == 1:
        imgs_url = reszka_gif
    else:
        imgs_url = orzel_gif
    if r_option == 0 and option == 0:
        payout = arg2 * 2
        external_functions.change_amount(username, balance + payout)
        balance = external_functions.get_amount(username)
        em = discord.Embed(title="Orzeł", color=0x00b100, timestamp=datetime.datetime.utcnow())
        em.set_image(url=imgs_url)
        em.set_footer(text=f"Wywołane przez {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
        em.add_field(name="Wygrywasz!", value=f"Moneta wylosowała orła! Wygrywasz {payout} i posiadasz teraz {balance}")
        await ctx.reply(embed=em)
    elif r_option == 1 and option == 1:
        payout = arg2 * 2
        external_functions.change_amount(username, balance + payout)
        balance = external_functions.get_amount(username)
        em = discord.Embed(title="Reszka", color=0x00b100, timestamp=datetime.datetime.utcnow())
        em.set_image(url=imgs_url)
        em.set_footer(text=f"Wywołane przez {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
        em.add_field(name="Wygrywasz!", value=f"Moneta wylosowała orła! Wygrywasz {payout} i posiadasz teraz {balance}")
        await ctx.reply(embed=em)
    elif r_option == 1:
        em = discord.Embed(title="Reszka", color=0xf22727, timestamp=datetime.datetime.utcnow())
        em.set_image(url=imgs_url)
        em.set_footer(text=f"Wywołane przez {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
        em.add_field(name="Przegrywasz!", value=f"Nie udało ci się wygrać")
        await ctx.reply(embed=em)
    elif r_option == 0:
        em = discord.Embed(title="Orzeł", color=0xf22727, timestamp=datetime.datetime.utcnow())
        em.set_image(url=imgs_url)
        em.set_footer(text=f"Wywołane przez {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
        em.add_field(name="Przegrywasz!", value=f"Nie udało ci się wygrać")
        await ctx.reply(embed=em)
    else:
        await ctx.reply("Wystąpił błąd!")
        return
    external_functions.change_amount(username, balance - arg2)


@client.command(aliases=['my_id'])
async def myid(ctx):
    await ctx.reply(f"Twoje id to `{ctx.author.id}`")


shop_data = {
    'Reakcja': [1000, "Powoduje pojawienie się reakcji na serwerze"],
    'Mnożnik 10': [9000, "Jednorazowo zwiększa mnożnik reakcji do 10"],
    'Mnożnik 20': [17000, "Jednorazowo zwiększa mnożnik reakcji do 20"],
    'Górnik': [15000, "Pozwala co godzinę użyć komendy `.odbierz` dzięki której otrzymujesz 1k"],
    'Farmer': [50000, "Pozwala co godzinę użyć komendy `.odbierz` dzięki której otrzymujesz 2k"],
    'Astronauta': [100000, "Pozwala co godzinę użyć komendy `.odbierz` dzięki której otrzymujesz 10k"],
    'Milioner': [1000000, "Pozwala co godzinę użyć komendy `.odbierz` dzięki której otrzymujesz 25k"]
}


@client.command(aliases=['sklep', 'market'])
async def shop(ctx):
    em = discord.Embed(title="Sklep", color=0x90e0ef, timestamp=datetime.datetime.utcnow())
    for item in shop_data:
        em.add_field(name=item, value=f"`{shop_data[item][0]}⛃` | {shop_data[item][1]}", inline=False)
    em.set_footer(text=f"Wywołane przez {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
    await ctx.reply(embed=em)


@commands.cooldown(1, 15, commands.BucketType.user)
@client.command(aliases=['kup'])
async def buy(ctx, *, arg1=None):
    global messages_per_cycle, multiply_win, one_time_multiplayer
    if arg1 is None:
        await ctx.reply(f"Poprawne uzycie: `{prefix}buy <nazwa przedmiotu>`")
        return
    if arg1 not in shop_data:
        await ctx.reply(f"Nie ma takiego przedmiotu jak `{arg1}`")
        return
    else:
        price = None
        for item in shop_data:
            if item == arg1:
                price = shop_data[item][0]
                break
        username = ctx.author.id
        if price > external_functions.get_amount(username):
            await ctx.reply(f"Nie masz wystarczająco pieniędzy")
            return
        external_functions.change_amount(username, external_functions.get_amount(username) - price)
        em = discord.Embed(title="Produkt zakupiony", colour=0x90e0ef,
                           description=f"```{arg1}\nZakupiłeś przedmiot {arg1} za {price}⛃```")
        em.set_footer(text=f"Wywołane przez {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=em)
        if arg1 == "Mnożnik 10":
            multiply_win = 10
            one_time_multiplayer = True
            bot.chat(f"{ctx.author.display_name} zakupił jednorazowy mnożnik 10x")
        elif arg1 == "Mnożnik 20":
            multiply_win = 20
            one_time_multiplayer = True
            bot.chat(f"{ctx.author.display_name} zakupił jednorazowy mnożnik 20x")
        elif arg1 == "Reakcja":
            messages_per_cycle = -21312
            bot.chat(f"{ctx.author.display_name} hostuje reakcje za 10s!")
            await asyncio.sleep(10)
            messages_per_cycle = 23322332322
            host_reaction()
        elif arg1 == "Górnik":
            role = discord.utils.get(ctx.guild.roles, id=892395137769037874)
            await ctx.author.add_roles(role)
        elif arg1 == "Farmer":
            role = discord.utils.get(ctx.guild.roles, id=892400836787982357)
            await ctx.author.add_roles(role)
        elif arg1 == "Milioner":
            role = discord.utils.get(ctx.guild.roles, id=892401287998611497)
            await ctx.author.add_roles(role)
        elif arg1 == "Astronauta":
            role = discord.utils.get(ctx.guild.roles, id=892401428595884033)
            await ctx.author.add_roles(role)


incomes = {892395137769037874: 1000,
           892400836787982357: 2000,
           892401428595884033: 10000,
           892401287998611497: 25000
           }

cards_ti = ['2', '3', '4', '5', '6', '7', '8', '9', 'D', 'AS', 'K', 'W']


@client.command()
async def bj(ctx, arg1: int = None):
    if not arg1:
        await ctx.reply("Podaj wartość zakładu")
        return
    cards = []
    cards_2 = []
    sum = 0
    sum2 = 0
    for _ in range(2):
        u = random.choice(cards_ti)
        cards.append(u)
    for u in cards:
        sum += bj_cards[u]
    for _ in range(1):
        u = random.choice(cards_ti)
        cards_2.append(u)
    for u in cards_2:
        sum2 += bj_cards[u]
    em = discord.Embed(title="Black jack")
    em.add_field(name=f"**Twoje karty**", value=f"```{cards}```\nWartość {sum}")
    em.add_field(name=f"**Karty przeciwnika**", value=f"```{cards_2}```\nWartość {sum2}")
    em.set_footer(text=f"Wywołane przez {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
    await ctx.reply(embed=em)

    def is_correct(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        response = await client.wait_for('message', check=is_correct, timeout=60.0)
    except asyncio.TimeoutError:
        return await ctx.channel.send(f'Za długo ci to zajeło')

    if response.content.startswith("."):
        print("e")
    elif response.content.lower() == "stop":
        print("stop")
    elif response.content.lower() == "hit":
        print("hit")
    elif response.content.lower() == "stand":
        print("stand")
    else:
        await response.reply("Nie rozpoznaje")


@commands.cooldown(1, 3600, commands.BucketType.user)
@client.command(aliases=['income'])
async def odbierz(ctx):
    payout = 0
    print(ctx.author.roles)
    for role in incomes:
        for role2 in ctx.author.roles:
            if role == role2.id:
                payout += incomes[role]
    if payout != 0:
        username = ctx.author.id
        external_functions.change_amount(username, external_functions.get_amount(username) + payout)
        em = discord.Embed(title="Wypłata", timestamp=datetime.datetime.utcnow(), colour=0x90e0ef,
                           description=f"Odebrałeś wypłatę w wysokości {payout}")
        em.set_footer(text=f"Wywołane przez {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=em)
    else:
        em = discord.Embed(title="Wypłata", timestamp=datetime.datetime.utcnow(), colour=0xf22727,
                           description=f"Nie posiadasz pieniędzy do wypłacenia")
        em.set_footer(text=f"Wywołane przez {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=em)


@client.command()
async def add_money(ctx, arg1: int, arg2):
    if ctx.author.id == 763400574166761472:
        username = arg2
        balance = external_functions.get_amount(username)
        x = external_functions.change_amount(username, balance + arg1)
        balance = external_functions.get_amount(username)
        await ctx.reply(f"{x} | {arg2} teraz posiada {balance}")


@client.command()
async def baltop(ctx):
    em = discord.Embed(timestamp=datetime.datetime.utcnow(), title="Baltop")
    for player in baltop_mc:
        print(baltop_mc)
        em.add_field(name=player[2], inline=False, value=f"{player[0]} - {player[1]}")
    await ctx.reply(embed=em)


@commands.cooldown(1, 3, commands.BucketType.user)
@client.command()
async def pay(ctx, arg1: int = None, arg2=None):
    if arg1 is None or arg2 is None:
        await ctx.reply(f"Poprawne użycie\n`{prefix}pay <ilość> <gracz>`")
        return
    username = ctx.author.id
    balance = external_functions.get_amount(username)
    if balance is False:
        await ctx.reply("Nie znaleziono twojego konta")
        return
    if arg1 > balance:
        await ctx.reply("Nie masz tyle kasy")
        return
    else:
        balance_v2 = external_functions.get_amount(arg2)
        if balance_v2 is False:
            await ctx.reply("Nie znaleziono gracza")
            return
        external_functions.change_amount(username, balance - arg1)
        e = external_functions.change_amount(arg2, external_functions.get_amount(arg2) + arg1)
        if e is True:
            await ctx.reply(f"Pomyślnie przelałes pieniądze do {arg2}")
        else:
            await ctx.reply("Coś poszło nie tak <@763400574166761472>")


@commands.cooldown(1, 9, commands.BucketType.user)
@client.command(aliases=['topka', 'leaderboard'])
async def top(ctx):
    to_sort = {}
    with open("bank.json", 'r') as f:
        bank_values = json.load(f)
    for user in bank_values:
        to_sort[user] = bank_values[user][0]
    em = discord.Embed(title="Topka", timestamp=datetime.datetime.utcnow(), colour=0xf22727,
                       description=f"Oni to mają dużo hajsu...")
    u = 0
    for r in sorted(to_sort, reverse=True, key=lambda eee: to_sort[eee]):
        u += 1
        if u == 1:
            k = "🥇"
        elif u == 2:
            k = "🥈"
        elif u == 3:
            k = "🥉"
        else:
            k = "🎖"
        em.add_field(name=f"**{k} | {r}**", value=f"```Miejsce {u} | {to_sort[r]}```", inline=False)
        if u == 5:
            break
    em.set_footer(text=f"Wywołane przez {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
    await ctx.reply(embed=em)


@tasks.loop(minutes=3)
async def reactions():
    global current_word, timer_start, messages_per_cycle
    if messages_per_cycle > 20:
        messages_per_cycle = 0
        try:
            word = random.choice(passes)
            bot.chat(f"Napisz na chacie: {word}")
            current_word = word
            timer_start = time.perf_counter()
        except:
            pass


@tasks.loop(minutes=10)
async def baltop_check():
    try:
        get_baltop()
    except Exception as e:
        raise e


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'Nie możesz teraz tego użyć, spróbuj ponownie za {:.2f}s'.format(error.retry_after)
        await ctx.send(msg)
    else:
        raise error


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game('Skyheroes.pl'))
    reactions.start()
    baltop_check.start()
    print('Connected to client: {}'.format(client.user.name))
    print('Bot ID: {}'.format(client.user.id))
    print(""" 
 ██▀███  ▓█████ ▄▄▄      ▓█████▄▓██   ██▓
▓██ ▒ ██▒▓█   ▀▒████▄    ▒██▀ ██▌▒██  ██▒
▓██ ░▄█ ▒▒███  ▒██  ▀█▄  ░██   █▌ ▒██ ██░
▒██▀▀█▄  ▒▓█  ▄░██▄▄▄▄██ ░▓█▄   ▌ ░ ▐██▓░
░██▓ ▒██▒░▒████▒▓█   ▓██▒░▒████▓  ░ ██▒▓░
░ ▒▓ ░▒▓░░░ ▒░ ░▒▒   ▓▒█░ ▒▒▓  ▒   ██▒▒▒ 
  ░▒ ░ ▒░ ░ ░  ░ ▒   ▒▒ ░ ░ ▒  ▒ ▓██ ░▒░ 
  ░░   ░    ░    ░   ▒    ░ ░  ░ ▒ ▒ ░░  
   ░        ░  ░     ░  ░   ░    ░ ░     
                          ░      ░ ░     
""")


client.run(bot_token)
