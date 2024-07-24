import json
from datetime import datetime
from mcdreforged.api.all import *

announcements = []
announcements_file = 'config/pss_announcement.json'
server_name = 'PSS'

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
    server.execute('tellraw @a [{"text":"[%s] ","color":"gold"},{"text":"%s","color":"white"}]' % (server_name, message))

def on_player_joined(server, player, info):
    server.execute('tellraw %s [{"text":"%s ","color":"gold"},{"text":"欢迎回来喵~"}]' % (player, player))
    if len(announcements) > 0:
        server.execute('tellraw %s [{"text":"======= [PSS公告] ======="}]' % player)
        time, publisher, content = announcements[len(announcements) - 1]
        server.execute('tellraw %s [{"text":"\\n%s","color":"gray"},{"text":"\\n%s","color":"gray"},{"text":"\\n"},{"text":"\\n%s"},{"text":"\\n-----------"},{"color":"white"}]' % (player, time, publisher, content))

def add_announcement(server, context, info):
    if content.startswith('!!p add '):
        content = context['text']
        publisher = info.player
        if "SBLB" in content or "sblb" in content:
            publisher = "***"
        time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        announcements.append((time, publisher, content))
        save_announcements()
        send_announcement(server, '%s公告已发布：%s' % (server_name, content))

def del_announcement(server, context, info):
        try:
            index = int(context['index']) - 1
            if index < 0 or index >= len(announcements):
                server.reply(info, '§c序号不存在！')
                return
            del announcements[index]
            save_announcements()
            send_announcement(server, '已删除公告 %s' % (index + 1))
        except ValueError:
            server.reply(info, '§c请输入§a正确§c的序号！')

def list_announcement(server, context, info):
        announcements_list = '\n'.join([f'{i+1}: {announcement[2]}' for i, announcement in enumerate(announcements)])
        server.reply(info, '[%s公告列表]\n§a' % server_name + announcements_list)

def show_help_info(context: PlayerCommandSource):
    server = context.get_server()
    info = context.get_info()
    server.reply(info, "-------- §a Welcome Message §r--------")
    server.reply(info, RText("§7!!pa help§r").set_hover_text("点击以填入" + " §7!!pa help§r").set_click_event(RAction.suggest_command, "!!pa help") + ' ' + "展示帮助信息")
    server.reply(info, RText("§7!!pa add <text>§r").set_hover_text("点击以填入" + " §7!!pa add§r").set_click_event(RAction.suggest_command, "!!pa add ") + ' ' + "添加一条公告")
    server.reply(info, RText("§7!!pa del <index>§r").set_hover_text("点击以填入" + " §7!!pa del§r").set_click_event(RAction.suggest_command, "!!pa delete") + ' ' + "删除指定序号的公告")
    server.reply(info, RText("§7!!pa list [index]§r").set_hover_text("点击以填入" + " §7!!pa list§r").set_click_event(RAction.suggest_command, "!!pa list") + ' ' + "显示所有公告")
    server.reply(info, "------------------------------------")


def on_load(server: PluginServerInterface, old):

    load_announcements()
    server.register_help_message('!!pa', "PSS 公告")

    command_builder = SimpleCommandBuilder()
    command_builder.command('!!pa list', list_announcement)
    command_builder.command('!!pa list <index>', load_announcements)
    command_builder.command('!!pa add <text>', add_announcement)
    command_builder.command('!!pa del <index>', del_announcement)
    command_builder.command('!!pa', show_help_info)
    command_builder.command('!!pa help', show_help_info)
    command_builder.arg('text', Text)
    command_builder.arg('index', Integer)

    command_builder.register(server)