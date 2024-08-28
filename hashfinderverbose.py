import hashlib
import time
import random
import threading

start_time = time.time()
interval = 15
counter = 0
num_threads = 4
stop_event = threading.Event()
counter_lock = threading.Lock()
found_hashes = []
found_hashes_lock = threading.Lock()

print("Searching for SHA-256 hashes starting with a specific sequence.")
print("The input strings are 64-character (256-bit) hexadecimal values.")
target = input('Insert desired hexadecimal characters (0-9,A-F) to try and find at the start of the hash: ')
num_to_find = int(input('How many matching hashes do you want to find? '))

def generate_random_hex(length=64):
    return ''.join(random.choice('0123456789abcdef') for _ in range(length))

def search_hash():
    global counter
    while not stop_event.is_set():
        random_hex = generate_random_hex()
        hash_value = hashlib.sha256(bytes.fromhex(random_hex)).hexdigest()
        with counter_lock:
            counter += 1
        if hash_value.startswith(target):
            with found_hashes_lock:
                found_hashes.append((random_hex, hash_value))
                print(f"Found value {len(found_hashes)}: {random_hex} : {hash_value}")
                if len(found_hashes) >= num_to_find:
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
    
    if input("Press Enter to continue, or type 'stop' to exit: ").lower() == 'stop':
        should_stop = True
        stop_event.set()

for thread in threads:
    thread.join()

with counter_lock:
    print(f"Total values checked: {counter}")

print(f"Found {len(found_hashes)} matching hashes:")
for i, (value, hash_value) in enumerate(found_hashes, 1):
    print(f"{i}. {value} : {hash_value}")
