import os
import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# === 1. 基础配置 (自动读取 GitHub Secrets) ===
try:
    API_ID = int(os.environ['TG_API_ID'])
    API_HASH = os.environ['TG_API_HASH']
    SESSION_STR = os.environ['TG_SESSION']
except KeyError:
    print("错误：无法读取 Secrets，请检查 GitHub 配置！")
    exit(1)

# === 2. 你的监控名单 (已更新) ===

# 🕵️‍♂️ 监控的大佬 ID 列表
# [旧大佬, 新大佬]
VIP_USERS = [493672327, 2038380694]

# 📂 被监控的群组 ID (来源)
# 这里填大佬所在的那个群组
SOURCE_GROUPS = [-1002022660060]

# 🎯 接收情报的群组 ID (目的地) <--- 已更新
FORWARD_TO_ID = -5056994823

# === 3. 启动机器人 ===
client = TelegramClient(StringSession(SESSION_STR), API_ID, API_HASH)

@client.on(events.NewMessage(chats=SOURCE_GROUPS))
async def handler(event):
    # 检查发言者是否在 VIP 名单中
    if event.sender_id in VIP_USERS:
        try:
            # 获取大佬的名字和群名
            sender = await event.get_sender()
            name = getattr(sender, 'first_name', '') or getattr(sender, 'title', '大佬')
            chat = await event.get_chat()
            group_name = chat.title
            
            print(f"检测到 {name} (ID: {event.sender_id}) 发言，正在转发...")

            # 1. 先发一条文字提醒
            # 格式：【群名】人物 -> 发送了新消息
            await client.send_message(FORWARD_TO_ID, f"🔔 **【监控提醒】**\n📂 来自: **{group_name}**\n👤 大佬: **{name}**\n⬇️ 内容如下 ⬇️")

            # 2. 转发原消息 (支持图片/视频/语音/文件等所有格式)
            await event.message.forward_to(FORWARD_TO_ID)

        except Exception as e:
            print(f"转发失败: {e}")
            print(f"⚠️ 如果报错 ChatIdInvalid，请尝试将目标 ID 改为 -100{abs(FORWARD_TO_ID)}")

async def main():
    print(f"✅ 监控已启动！")
    print(f"👀 正在蹲守: {len(VIP_USERS)} 位大佬")
    print(f"🚀 转发目标: {FORWARD_TO_ID}")
    await client.start()
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
