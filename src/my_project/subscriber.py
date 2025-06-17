import redis
import threading
import os
import time
from collections import defaultdict
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

        # Initialize counters
        self.total_entries = 0
        self.word_count_29 = 0
        self.word_count_not_29 = 0
        self.minute_segment_counts = defaultdict(int)

    def count_characters(self, content):
        chinese = sum(1 for c in content if '\u4e00' <= c <= '\u9fff')
        english = sum(1 for c in content if c.isalpha() and not ('\u4e00' <= c <= '\u9fff'))
        return chinese, english

    def process_entry(self, entry):
        self.total_entries += 1
        word_count = len(entry.split())

        if word_count == 29:
            self.word_count_29 += 1
        else:
            self.word_count_not_29 += 1

        current_minute = time.localtime().tm_min
        minute_segment = current_minute % 10
        self.minute_segment_counts[minute_segment] += 1

    def log_counts(self):
        print(f"Total entries: {self.total_entries}")
        print(f"Entries with 29 words: {self.word_count_29}")
        print(f"Entries with not 29 words: {self.word_count_not_29}")
        print("Minute segment counts:")
        for segment in range(10):
            print(f"{segment:02d}: {self.minute_segment_counts[segment]}")

        # Reset counts for the next interval
        self.minute_segment_counts = defaultdict(int)

    def listen(self):
        print(f"開始訂閱:{self.channel}", flush=True)
        last_logged_minute = -1
        while not self.stop_event.is_set():
            message = self.pubsub.get_message()
            if message and message['type'] == 'message':
                content = message['data']
                print(f"收到訊息：{content}", flush=True)
                c, e = self.count_characters(content)
                # print(f"中文字數：{c}, 英文字母數：{e}", flush=True)
                self.process_entry(content)

            current_minute = time.localtime().tm_min
            if current_minute % 10 == 0 and current_minute != last_logged_minute:
                self.log_counts()
                last_logged_minute = current_minute

            time.sleep(1)

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
