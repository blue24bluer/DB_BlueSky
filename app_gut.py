import asyncio
import time
from telethon import TelegramClient

API_ID = 36277649
API_HASH = "7e46fbbabbfc981651e22f6a4b7b0f94"

def human_size(n):
    # عرض مقروء لحجم البايت
    for unit in ['B','KB','MB','GB','TB']:
        if n < 1024.0:
            return f"{n:3.1f}{unit}"
        n /= 1024.0
    return f"{n:.1f}PB"

async def main():
    client = TelegramClient("session", API_ID, API_HASH)
    await client.start()

    chat_id = -1002473281659
    message_id = 413
    save_as = "downloaded_file"  # اسم الملف الناتج

    msg = await client.get_messages(chat_id, ids=message_id)
    if not msg or not msg.document:
        print("❌ الرسالة لا تحتوي ملف أو لم يُعثر عليها.")
        await client.disconnect()
        return

    total = msg.file.size or 0
    start_time = time.time()
    last_time = start_time
    last_bytes = 0

    def progress_callback(received, total_bytes):
        nonlocal last_time, last_bytes
        now = time.time()
        elapsed = now - start_time
        interval = now - last_time
        # سرعة منذ آخر تحديث (بايت/ثانية)
        delta = received - last_bytes
        speed_inst = delta / interval if interval > 0 else 0
        speed_avg = received / elapsed if elapsed > 0 else 0
        pct = (received / total_bytes * 100) if total_bytes else 0
        eta = (total_bytes - received) / speed_avg if speed_avg > 0 else float('inf')

        print(
            f"\r{pct:5.1f}% — {human_size(received)}/{human_size(total_bytes)} "
            f"— {speed_inst/1024:.1f} KB/s (inst), {speed_avg/1024:.1f} KB/s (avg) — ETA {int(eta)}s",
            end='', flush=True
        )
        last_time = now
        last_bytes = received

    print("📥 بدء التحميل...")
    await msg.download_media(file=save_as, progress_callback=progress_callback)
    print("\n✅ انتهى التحميل.")
    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
