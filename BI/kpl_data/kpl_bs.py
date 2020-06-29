# 使用request + BeautifulSoup抓取kpl数据
import requests
from bs4 import BeautifulSoup
from sqlalchemy import Column, String, Integer, DateTime, UniqueConstraint, create_engine
from sqlalchemy.orm import sessionmaker
 
# 初始化数据库连接:
engine = create_engine('mysql+mysqlconnector://root:passw0rdcc4@localhost:3306/wucai')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
# 创建session对象:
session = DBSession()

# 插入heros_play表
def add_data(hero_name, game_id, player_name, kda_k, kda_d, kda_a, money, damage_input, damage_output, win):
    insert_stmt = "INSERT IGNORE INTO heros_play(hero_name, game_id, player_name, kda_k, kda_d, kda_a, money, damage_input, damage_output, win) VALUES \
        (:hero_name, :game_id, :player_name, :kda_k, :kda_d, :kda_a, :money, :damage_input, :damage_output, :win)"
    session.execute(insert_stmt, {'hero_name': hero_name, 'game_id': game_id, 'player_name': player_name, 'kda_k': kda_k, 'kda_d': kda_d, 'kda_a': kda_a, 'money': money, \
        'damage_input': damage_input, 'damage_output': damage_output, 'win': win})
    print(hero_name, game_id, player_name, kda_k, kda_d, kda_a, money, damage_input, damage_output, win)
    session.commit()


# 通过HTML中的span分析成绩
def analyze_score(spans):
    spanList = spans.find_all('span')
    z_value = spanList[0].text
    attr = spanList[1].text
    k_value = spanList[2].text
    return z_value, attr, k_value

# 通过URL返回bs对象
def get_bs_object(url):
    print(url)
    # 得到页面的内容
    headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}
    html=requests.get(url,headers=headers,timeout=10)
    content = html.text
    # print(content)

    # 通过content创建BeautifulSoup对象
    soup = BeautifulSoup(content, 'html.parser', from_encoding='utf-8')
    return soup


# 请求URL
start_page = 65200
end_page = 65324
for game_id in range(start_page, end_page+1):
    url = 'https://www.wanplus.com/match/' + str(game_id) + '.html#data'
    soup = get_bs_object(url)

    # 哪队获胜，主队获胜为1，客队获胜为2
    try:
        z_team=soup.find('span',class_="tl bssj_tt1").text
    except:
        # 没有找到该场比赛
        continue
    k_team=soup.find('span',class_="tr bssj_tt3").text
    if '胜' in z_team:
        winner = 1
    else:
        winner = 0

    # 判断是否为KPL比赛
    game = soup.find('div', class_="matching_intro").text
    if 'KPL' not in game:
        #print(game)
        continue

    # 得到主队，客队所示英雄的成绩
    z_list=soup.find_all('div',class_="bans_l")
    score_list=soup.find_all('div',class_="bans_m")
    k_list=soup.find_all('div',class_="bans_r")
    # 提取房源信息
    for z_hero, score, k_hero in zip(z_list, score_list, k_list):
        # 主队选手姓名
        temp = z_hero.find('div',class_="bans_tx fl").find_all("a", limit=2)
        z_player_name = temp[0].text
        z_hero_name = temp[1].text

        # 成绩
        temp = score.find_all('li')
        # 得到KDA
        z_value, attr, k_value = analyze_score(temp[0])
        [z_k,z_d,z_a] = z_value.split('/')
        [k_k,k_d,k_a] = k_value.split('/')
        # 得到金钱
        z_money, attr, k_money = analyze_score(temp[1])
        # 承受伤害
        z_damage_output, attr, k_damage_output = analyze_score(temp[2])
        # 输出伤害
        z_damage_input, attr, k_damage_input = analyze_score(temp[3])

        # 客队选手姓名
        temp = k_hero.find('div',class_="bans_tx fl").find_all("a", limit=2)
        k_player_name = temp[0].text
        k_hero_name = temp[1].text

        # 添加主队英雄成绩
        add_data(z_hero_name, game_id, z_player_name, z_k, z_d, z_a, z_money, z_damage_input, z_damage_output, winner)
        # 添加主队英雄成绩
        add_data(k_hero_name, game_id, k_player_name, k_k, k_d, k_a, k_money, k_damage_input, k_damage_output, 1-winner)

        #print(z_player_name, z_hero_name)
        #print(k_player_name, k_hero_name)

# 提交到数据库
session.commit()
session.close()
