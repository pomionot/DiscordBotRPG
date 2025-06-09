import discord
from discord.ext import commands
import asyncio
import random
import json
import os



client = commands.Bot(command_prefix="!", intents=discord.Intents.all())
TOKEN = "任意のトークン"

DATA_FILE = 'user_data.json'
KONSO_FILE = "konso_data.json"
# ユーザーデータを読み込む関数
async def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

# ユーザーデータを保存する関数
async def save_data(data):
    with open(DATA_FILE, 'w',encoding='utf-8') as f:
        json.dump(data, f, indent=4)

#敵データを読み込む関数
async def Konso_load():
    with open(KONSO_FILE,'r',encoding='utf-8')as f:
        return json.load(f)

#敵データを保存する関数
async def konso_save(data):
    with open(KONSO_FILE,'w',encoding='utf-8') as f:
        json.dump(data,f,indent=4)
    return {}


# ユーザーのステータスを表示するコマンド
@client.command()
async def sta(ctx):
    user_id = str(ctx.author.id)
    data = await load_data()
    if user_id in data:
        status = data[user_id]
        await ctx.send(f"ステータス: HP:{status['hp']}, MP:{status['mp']}, Level:{status['level']},経験値:{status['exp']},次のレベルまでに必要な経験値:{status['needexp']-status['exp']}")
    else:
        await ctx.send("ステータスが見つかりません。新しいキャラクターを作成してください。")





# ユーザーのキャラクターを作成するコマンド
@client.command()
async def cr(ctx):
    user_id = str(ctx.author.id)
    data = await load_data()
    if user_id not in data:
        data[user_id] = {
            "name":f"{ctx.author}",
            "fullhp":20,
            "hp": 20,
            "level": 1,
            "mp": 50,
            "exp":0,
            "needexp":16,
            "oldexp":1,
            "items": [],

        }
        await save_data(data)
        await ctx.send("新しいキャラクターが作成されました。")
    else:
        await ctx.send("キャラクターは既に存在します。")





# 戦闘コマンド
@client.command()
async def fi(ctx):
    user_id = str(ctx.author.id)
    data = await load_data()
    Kdata = await Konso_load()
    dsum = 0
    exp=0
    if user_id in data:
        player = data[user_id]
        Konso = Kdata["Konso"]

        # 敵のステータスを設定
        Konso_hp = Konso["hp"]*Konso["level"]
        Konso_attack = Konso["level"]*random.randint(2,8)

        
        # 戦闘のシミュレーション
        battle_log = []
        while player['hp'] > 0 and Konso_hp > 0:
            player_attack = random.randint(1,5)*player["level"]
            Konso_hp -= player_attack
            dsum+=player_attack
            battle_log.append(f"{ctx.author}の攻撃! 敵に{player_attack}のダメージを与えた。敵の残りHPは{Konso_hp}。")
            if Konso_hp <= 0:
                battle_log.append("敵を倒した!")
                Konso["level"]+=1
                exp=dsum*2+Konso["level"]*10
                player["exp"]+=exp
                battle_log.append(f"経験値{exp}を獲得した")
                break
            Konso_attack = Konso["level"]*random.randint(5,10)
            player['hp'] -= Konso_attack
            battle_log.append(f"敵の攻撃! {ctx.author}に{Konso_attack}のダメージを与えた。{ctx.author}の残りHPは{player['hp']}。")
            if player['hp'] <= 0:
                battle_log.append(f"{ctx.author}が倒された。")
                exp=dsum*2
                player["exp"]+=exp
                battle_log.append(f"経験値{exp}を獲得した")

        levelup=int(player["level"]*15+player["oldexp"]*1.1)
        while player["exp"]>=levelup:
            player["exp"]-=levelup
            player["level"]+=1
            levelup=int(player['level']*15+player['needexp']*1.1)
            player["oldexp"]=levelup
            player["needexp"]=levelup
            battle_log.append(f"{ctx.author}はレベル{player['level']}になった！")
            player["fullhp"]=int(player["fullhp"]*1.1)
        player['hp']=player['fullhp']
        # 更新されたプレイヤーのHPを保存
        await save_data(data)
        await konso_save(Kdata)
        # 戦闘ログを送信
        await ctx.send("\n".join(battle_log))
    else:
        await ctx.send("キャラクターが存在しません。まず新しいキャラクターを作成してください。")





        

@client.command()
async def ga(ctx):
    i=0
    buki=["剣","弓","銃","盾","近藤キラー"]
    for i in range(10):
        num=(random.randint(0,4))
        await ctx.send(f"{buki[num]}")                
         





client.run(TOKEN)
