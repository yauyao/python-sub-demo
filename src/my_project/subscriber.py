import redis
import threading
import os
from urllib.parse import urlparse

class Subscriber:
    def __init__(self):
        redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
        url = urlparse(redis_url)
        self.redis = redis.Redis(host=url.hostname, port=url.port, decode_responses=True)
        self.pubsub = self.redis.pubsub()
        self.channel = None
        self.thread = None
        self.stop_event = threading.Event()

    def count_characters(self, content):
        chinese = sum(1 for c in content if '\u4e00' <= c <= '\u9fff')
        english = sum(1 for c in content if c.isalpha() and not ('\u4e00' <= c <= '\u9fff'))
        return chinese, english

    def listen(self):
        print(f"開始訂閱:{self.channel}", flush=True)
        for message in self.pubsub.listen():
            if self.stop_event.is_set():
                break
            if message['type'] == 'message':
                content = message['data']
                print(f"收到訊息：{content}", flush=True)
                c, e = self.count_characters(content)
                print(f"中文字數：{c}, 英文字母數：{e}", flush=True)

    def subscribe(self, channel):
        self.stop()
        self.channel = channel
        self.pubsub.unsubscribe()
        self.pubsub.subscribe(channel)
        self.stop_event.clear()
        self.thread = threading.Thread(target=self.listen)
        self.thread.start()

    def stop(self):
        if self.thread and self.thread.is_alive():
            self.stop_event.set()
            self.thread.join()
