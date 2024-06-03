import hashlib
import time
import random
import string
import threading

start_time = time.time()
interval = 15
counter = 0
num_threads = 4
stop_event = threading.Event()
counter_lock = threading.Lock()

print("WARNING: This can vary between very slow to very fast! At around 6 characters of complexity (6^15 possibilities, or 470bn) it will slow down dramatically. At 7 characters, or 4.7tn, it is about a miracle to find one. It could be highly common, or extremely rare.")
target = input('Insert desired hexadecimal characters (0-9,A-E) to try and find at the start of the hash: ')
targetc = pow(len(target),15)


def generate_random_value(length=random.randrange(8, 20)):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def search_hash():
    global counter
    while not stop_event.is_set():
        random_value = generate_random_value()
        hash_value = hashlib.sha256(random_value.encode()).hexdigest()
        with counter_lock:
            counter += 1
        if hash_value.startswith(target):
            print(f"Found value: {random_value} : {hash_value}")
            stop_event.set()
            break

threads = []
for _ in range(num_threads):
    thread = threading.Thread(target=search_hash)
    threads.append(thread)
    thread.start()

last_print_time = start_time
should_stop = False

while True:
    current_time = time.time()
    if current_time - last_print_time >= interval:
        print("Still searching...")
        with counter_lock:
            print(f"Values checked: {counter}")
        last_print_time = current_time
    if stop_event.is_set() or should_stop:
        break

    user_input = input("Press Enter to continue, or type 'stop' to exit: ")
    if user_input.lower() == 'stop':
        should_stop = True
        stop_event.set()

for thread in threads:
    thread.join()

with counter_lock:
    print(f"Total values checked: {counter}")