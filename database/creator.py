import pandas as pd
from sqlalchemy import create_engine
from database.request import data
import sqlite3 as sq
from create_bot import bot


#функция, которая заполняет таблицу опицонов в базе данных mysql
#загружаем данные в бд Mysql со списком всех опционов из московской биржи
def connect_update_database():
    engine = create_engine('mysql+pymysql://root:QWErty123456@localhost/options')
    json_data = pd.DataFrame(data)
    json_data.to_sql("optionstable", con=engine, if_exists='replace')
#Здесь мы будем работать с кнопкой список опционов и выгружать данные из бд mysql
#mass = ['index', 'secid', 'boardid', 'shortname', 'secname','prevsettleprice', 'decimals', 'minstep', 'lasttradedate', 'lastdeldate', 'latname','assetcode','prevopenposition','prevprice','optiontype', 'stepprice','imnp', 'imp','imbuy','imtime','buysellfee', 'scalperfee','negotiatedfee', 'exercisefee','strike','centralstrike','underlyingasset','underlyingtype','underlyingsettleprice']

async def output_data(message):
    engine = create_engine('mysql+pymysql://root:QWErty123456@localhost/options')
    sql = "select secid, shortname, lasttradedate, optiontype, strike from optionstable limit 25"
    df = pd.read_sql(sql, con=engine)
    await bot.send_message(message.from_user.id, f'<pre>{df}</pre>', parse_mode='html')

#функция, которая заполняет базу данных рекомендаций, которая будет вводиться
# вручную админом бота, например если мы захотим добавить новую стратегию
# нам не нужно будет ковыряться в базе данных, мы прям в самом телеграмме
# все заполним и вся информация добавится, будем использовать sqlite
def connection_database():
    global base, cur
    base = sq.connect('strategy_options.db')
    cur = base.cursor()
    if base:
        print('success connection')
    base.execute('CREATE TABLE IF NOT EXISTS strategy(img TEXT, name TEXT PRIMARY KEY, description BLOB, recomendation BLOB)')
    base.commit()
async def full_table_stsrategy(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO strategy VALUES(?,?,?,?)', tuple(data.values()))
        base.commit()

#Тут мы отправляем сообщение с данными пользователю из бд sqlite
async def sql_bring_out(message):
    for ret in cur.execute('SELECT * FROM strategy').fetchall():
         await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\n\nОписание:\n{ret[2]}\n\nРекомендации:\n{ret[-1]}')

async def return_data():
    return cur.execute('SELECT * FROM strategy').fetchall()

async def del_data(data):
    cur.execute('DELETE FROM strategy WHERE name == ?', (data,))
    base.commit()

