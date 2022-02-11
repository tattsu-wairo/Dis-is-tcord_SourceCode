from logging import fatal
from variable import Variable
from func import Func
import discord
from discord import client
client = discord.Client()

information_dict = {}


# メッセージに「tetris」がついていたとき
@client.event
async def on_message(message):
    if message.content.startswith("$tetris"):
        information = Variable()
        information.player = message.author.mention
        await message.channel.send(information.player)
        reply = "メッセージ確認。\nテトリスで遊ぶ,盤面をリセットする場合はリアクションボタン🇹を押してください。"
        msg = await message.channel.send(reply)
        information.msgID = msg.id
        information.userID = message.author.id
        information_dict[message.author.id] = information
        await msg.add_reaction('⬅️')
        await msg.add_reaction('➡️')
        await msg.add_reaction('⬇️')
        await msg.add_reaction('⏬')
        await msg.add_reaction('🔄')
        await msg.add_reaction('🔃')
        await msg.add_reaction('🇭')
        await msg.add_reaction('🇹')
        await msg.add_reaction('🚫')


# リアクションがついたとき
@client.event
async def on_raw_reaction_add(payload):
    try:
        user_info = information_dict[payload.user_id]
        if user_info.userID == payload.user_id and payload.message_id == user_info.msgID:
            checked_emoji = payload.emoji
            channel = client.get_channel(payload.channel_id)
            msg = await channel.fetch_message(payload.message_id)
            guild_id = payload.guild_id
            guild = discord.utils.find(
                lambda g: g.id == guild_id, client.guilds)
            if str(checked_emoji) == '🇹':
                await msg.edit(content=Func.regamefield(user_info))
                user_info.gameStartFlag = True
                user_info.gameOverFlag = True
            elif str(checked_emoji) == '🚫':
                await msg.edit(content=str(Func.gamefield(user_info))+"\n終了")
                del information_dict[payload.user_id]
            elif str(checked_emoji) == '🇷' and not user_info.gameOverFlag and user_info.gameStartFlag:
                await msg.clear_reactions()
                await msg.edit(content=Func.regamefield(user_info))
                await msg.add_reaction('⬅️')
                await msg.add_reaction('➡️')
                await msg.add_reaction('⬇️')
                await msg.add_reaction('⏬')
                await msg.add_reaction('🔄')
                await msg.add_reaction('🔃')
                await msg.add_reaction('🇭')
                await msg.add_reaction('🇹')
                await msg.add_reaction('🚫')
                user_info.gameStartFlag = True
                user_info.gameOverFlag = True
            elif user_info.gameStartFlag and user_info.gameOverFlag:
                if str(checked_emoji) == '⬅️':
                    if not Func.isHit(user_info.minoX-1, user_info.minoY, user_info.minoType, user_info.rotate, user_info):
                        user_info.minoX -= 1
                        user_info.lastcommand=False
                        await msg.edit(content=Func.gamefield(user_info))
                elif str(checked_emoji) == '➡️':
                    if not Func.isHit(user_info.minoX+1, user_info.minoY, user_info.minoType, user_info.rotate, user_info):
                        user_info.minoX += 1
                        user_info.lastcommand=False
                elif str(checked_emoji) == '⬇️':
                    if not Func.isHit(user_info.minoX, user_info.minoY+1, user_info.minoType, user_info.rotate, user_info):
                        user_info.minoY += 1
                        user_info.score += Func.scorePlus(0, False)
                        user_info.lastcommand=False
                    else:
                        Func.setMino(user_info)
                elif str(checked_emoji) == '⏬':
                    while True:
                        if not Func.isHit(user_info.minoX, user_info.minoY+1, user_info.minoType, user_info.rotate, user_info):
                            user_info.minoY += 1
                            user_info.score += Func.scorePlus(0, False)*2
                            user_info.lastcommand=False
                        else:
                            break
                    Func.setMino(user_info)
                elif str(checked_emoji) == '🔄':
                    r = user_info.rotate
                    r -= 1
                    if r == -1:
                        r = 3
                    Func.srs(user_info,r)
                elif str(checked_emoji) == '🔃':
                    r = user_info.rotate
                    r += 1
                    if r == 4:
                        r = 0
                    Func.srs(user_info,r)
                elif str(checked_emoji) == '🇭':
                    if user_info.changeCount == 0:
                        if user_info.holdMino == 100:
                            user_info.holdMino = user_info.minoType
                            user_info.minoType = Func.nextMino(user_info)[0]
                        else:
                            copy = user_info.minoType
                            user_info.minoType = user_info.holdMino
                            user_info.holdMino = copy
                        user_info.minoX = 3
                        user_info.minoY = 0
                        user_info.rotate = 0
                        user_info.changeCount = 1
                        user_info.offsetnum=0
                        user_info.lastcommand=False
                await msg.edit(content=Func.gamefield(user_info))
                if Func.isHit(user_info.minoX, user_info.minoY, user_info.minoType, user_info.rotate, user_info):
                    user_info.gameOverFlag = False
                    await msg.clear_reactions()
                    await msg.edit(content=Func.gamefield(user_info)+"\nGameOver")
                    await msg.add_reaction('🇷')
            elif not user_info.gameOverFlag:
                pass
    except KeyError:
        pass


# リアクションが外れた時
@client.event
async def on_raw_reaction_remove(payload):
    try:
        user_info = information_dict[payload.user_id]
        if user_info.userID == payload.user_id and payload.message_id == user_info.msgID:
            checked_emoji = payload.emoji
            channel = client.get_channel(payload.channel_id)
            msg = await channel.fetch_message(payload.message_id)
            guild_id = payload.guild_id
            guild = discord.utils.find(
                lambda g: g.id == guild_id, client.guilds)
            if str(checked_emoji) == '🇹':
                await msg.edit(content=Func.regamefield(user_info))
                user_info.gameStartFlag = True
                user_info.gameOverFlag = True
            elif str(checked_emoji) == '🚫':
                await msg.edit(content=str(Func.gamefield(user_info))+"\n終了")
                del information_dict[payload.user_id]
            elif str(checked_emoji) == '🇷' and not user_info.gameOverFlag and user_info.gameStartFlag:
                await msg.clear_reactions()
                await msg.edit(content=Func.regamefield(user_info))
                await msg.add_reaction('⬅️')
                await msg.add_reaction('➡️')
                await msg.add_reaction('⬇️')
                await msg.add_reaction('⏬')
                await msg.add_reaction('🔄')
                await msg.add_reaction('🔃')
                await msg.add_reaction('🇭')
                await msg.add_reaction('🇹')
                await msg.add_reaction('🚫')
                user_info.gameStartFlag = True
                user_info.gameOverFlag = True
            elif user_info.gameStartFlag and user_info.gameOverFlag:
                if str(checked_emoji) == '⬅️':
                    if not Func.isHit(user_info.minoX-1, user_info.minoY, user_info.minoType, user_info.rotate, user_info):
                        user_info.minoX -= 1
                        user_info.lastcommand=False
                        await msg.edit(content=Func.gamefield(user_info))
                elif str(checked_emoji) == '➡️':
                    if not Func.isHit(user_info.minoX+1, user_info.minoY, user_info.minoType, user_info.rotate, user_info):
                        user_info.minoX += 1
                        user_info.lastcommand=False
                elif str(checked_emoji) == '⬇️':
                    if not Func.isHit(user_info.minoX, user_info.minoY+1, user_info.minoType, user_info.rotate, user_info):
                        user_info.minoY += 1
                        user_info.score += Func.scorePlus(0, False)
                        user_info.lastcommand=False
                    else:
                        Func.setMino(user_info)
                elif str(checked_emoji) == '⏬':
                    while True:
                        if not Func.isHit(user_info.minoX, user_info.minoY+1, user_info.minoType, user_info.rotate, user_info):
                            user_info.minoY += 1
                            user_info.score += Func.scorePlus(0, False)*2
                            user_info.lastcommand=False
                        else:
                            break
                    Func.setMino(user_info)
                elif str(checked_emoji) == '🔄':
                    r = user_info.rotate
                    r -= 1
                    if r == -1:
                        r = 3
                    Func.srs(user_info,r)
                elif str(checked_emoji) == '🔃':
                    r = user_info.rotate
                    r += 1
                    if r == 4:
                        r = 0
                    Func.srs(user_info,r)
                elif str(checked_emoji) == '🇭':
                    if user_info.changeCount == 0:
                        if user_info.holdMino == 100:
                            user_info.holdMino = user_info.minoType
                            user_info.minoType = Func.nextMino(user_info)[0]
                        else:
                            copy = user_info.minoType
                            user_info.minoType = user_info.holdMino
                            user_info.holdMino = copy
                        user_info.minoX = 3
                        user_info.minoY = 0
                        user_info.rotate = 0
                        user_info.changeCount = 1
                        user_info.offsetnum=0
                        user_info.lastcommand=False
                await msg.edit(content=Func.gamefield(user_info))
                if Func.isHit(user_info.minoX, user_info.minoY, user_info.minoType, user_info.rotate, user_info):
                    user_info.gameOverFlag = False
                    await msg.clear_reactions()
                    await msg.edit(content=Func.gamefield(user_info)+"\nGameOver")
                    await msg.add_reaction('🇷')
            elif not user_info.gameOverFlag:
                pass
    except KeyError:
        pass


client.run("botごとに割り振られているコードです。安全のため伏せさせていただきます")
