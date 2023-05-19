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

def print_loops(loop_count):
    text = f"Loops accomplished: {loop_count}"
    typing_animation(text, 0.7)

def main():
    loop_count = 0
    while True:
        loop_count += 1
        threading.Thread(target=print_loops, args=(loop_count,)).start()
        time.sleep(1)

if __name__ == "__main__":
    main()