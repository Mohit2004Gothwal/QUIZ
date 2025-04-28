# utils/timer.py

import time

def countdown(seconds):
    while seconds:
        mins, secs = divmod(seconds, 60)
        timer = f'{mins:02d}:{secs:02d}'
        print(f"⏱️ Time left: {timer}", end='\r')
        time.sleep(1)
        seconds -= 1
    print("\n⏰ Time's up!")
