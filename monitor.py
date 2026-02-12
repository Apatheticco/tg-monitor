import os
import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# === 1. 读取 GitHub 里的机密配置 ===
try:
    API_ID = int(os.environ['TG_API_ID'])
    API_HASH = os.environ['TG_API_HASH']
    SESSION_STR = os.environ['TG_SESSION']
except KeyError:
    print("错误：未检测到 Secrets 配置，请在 GitHub Settings 中添加环境变量！")
    exit(1)

# === 2. 你的监控目标 (已填好) ===
# 这里是你查到的大佬 ID，如果有多个，用逗号隔开：[493672327, 12345678]
VIP_USERS = [493672327,2038380694] 

# 这里是你查到的群组 ID
TARGET_GROUP_ID = -1002022660060

# === 3. 初始化客户端 ===
client = TelegramClient(StringSession(SESSION_STR), API_ID, API_HASH)

@client.on(events.NewMessage(chats=TARGET_GROUP_ID))
async def handler(event):
    # 检查发言者是否在 VIP 名单里
    if event.sender_id in VIP_USERS:
        try:
            sender = await event.get_sender()
            # 获取显示名称，如果没有则显示 Unknown
            name = getattr(sender, 'first_name', '') or getattr(sender, 'title', '大佬')
            
            print(f"检测到 {name} 发言，正在转发...")
            
            # 转发到你的“收藏夹”(Saved Messages)
            # 格式：【监控提醒】名字: 消息内容
            await client.send_message('me', f"🔔 **【监控提醒】**\n👤 **{name}**:\n\n{event.text}")
            
        except Exception as e:
            print(f"转发失败: {e}")

async def main():
    print(f"监控已启动！正在监听群组: {TARGET_GROUP_ID}...")
    print(f"正在等待大佬 (ID: {VIP_USERS}) 发言...")
    await client.start()
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
