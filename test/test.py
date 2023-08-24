import sys
import time
import threading

def typing_animation(text, duration):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(duration / len(text))
    sys.stdout.write("\r")
    sys.stdout.flush()
    
def main():
    loop_count = 0
    while True:
        loop_count += 1
        threading.Thread(target=typing_animation, args=("Loops accomplished", 0.7)).start()
        time.sleep(1)

if __name__ == "__main__":
    main()