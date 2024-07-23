import json
import datetime
from mcdreforged.api.all import *

announcements = []
announcements_file = 'config/pss_announcement.json'
server_name = 'PSS'

def on_load(server, old_module):
    load_announcements()
    server.register_help_message('!!p add <公告内容>', '写一个公告')
    server.register_help_message('!!p delate <序号>', '删除指定序号的公告')
    server.register_help_message('!!p list', '显示当前所有的公告信息')
    server.register_help_message('!!p help', '获取插件的使用教程和所有的命令')

def load_announcements():
    global announcements, server_name
    try:
        with open(announcements_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
            announcements = data.get('announcements', [])
            server_name = data.get('server_name', 'PSS')
    except FileNotFoundError:
        announcements = []
        server_name = 'PSS'

def save_announcements():
    with open(announcements_file, 'w', encoding='utf-8') as file:
        json.dump({'announcements': announcements, 'server_name': server_name}, file, indent=4, ensure_ascii=False)

def send_announcement(server, message):
    server.execute('tellraw @a [{"text":"[%s] ","color":"gold"},{"text":"%s","color":"%s"}]' % (server_name, message))

def on_player_joined(server, player, info):
    for announcement in announcements:
        time, publisher, content = announcement
        server.execute('tellraw %s [{"text":"======= ","color":"white"},{"text":"[公告]","color":"yellow"},{"text":" =======","color":"white"},{"text":"\\n发布时间：","color":"gray"},{"text":"%s","color":"aqua"},{"text":"\\n发布人：","color":"gray"},{"text":"%s","color":"aqua"},{"text":"\\n内容：","color":"gray"},{"text":"%s","color":"white"},{"text":"\\n-------------","color":"white"}]' % (player, time, publisher, content))

def on_info(server, info):
    if info.content.startswith('!!p add '):
        content = info.content[8:]
        publisher = info.player
        time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        announcements.append((time, publisher, content))
        save_announcements()
        send_announcement(server, '%s公告已发布：%s' % (server_name, content))

    elif info.content.startswith('!!p delete'):
        try:
            index = int(info.content[5:]) - 1
            if index < 0 or index >= len(announcements):
                server.reply(info, '§c序号不存在！')
                return
            del announcements[index]
            save_announcements()
            send_announcement(server, '已删除公告', "green")
        except ValueError:
            server.reply(info, '§c请输入§a正确§c的序号！')

    elif info.content.startswith('!!p list'):
        announcements_list = '\n'.join([f'{i+1}: {announcement[2]}' for i, announcement in enumerate(announcements)])
        server.reply(info, '[%s公告列表]\n§a' % server_name + announcements_list)

    elif info.content.startswith('!!p help'):
        server.reply(info, '----- PSS Announcement -----\n简易公告栏\n§e!!p add <公告内容> 发布一个公告\n§e!!p delete <序号> 删除公告\n§e!!p list 显示所有公告\n')

    elif info.content.startswith('!!p'):
        server.reply(info, '§e!!p add <公告内容> 发布一个公告\n§e!!p delete <序号> 删除公告\n§e!!p list 显示所有公告\n')