import hashlib
import time
import random
import threading
from queue import Queue
import os

CPU_CORES = os.cpu_count() or 8
numThreads = max(12, CPU_CORES)  # Use more threads for strong CPUs

startTime = time.time()
interval = 10 
counter = 0
stopEvent = threading.Event()
counterLock = threading.Lock()
foundHashes = []
hashLock = threading.Lock()

print(f"Searching for SHA-256 hashes starting with a specific sequence using {numThreads} threads.")
print("The input strings are 64-character (256-bit) hexadecimal values.")

while True:
    target = input('Insert desired hexadecimal characters (0-9,a-f) to try and find at the start of the hash: ').strip().lower()
    if target and all(c in '0123456789abcdef' for c in target):
        break
    print("Invalid input. Please enter only hexadecimal characters (0-9, a-f).")

while True:
    try:
        numToFind = int(input('How many matching hashes do you want to find? '))
        if numToFind > 0:
            break
        else:
            print("Please enter a positive integer.")
    except ValueError:
        print("Please enter a valid integer.")

def genRandomHex(length=64):
    sysrand = random.SystemRandom()
    return ''.join(sysrand.choices('0123456789abcdef', k=length))

resultsQueue = Queue()

def searchHash():
    global counter
    sysrand = random.SystemRandom()
    while not stopEvent.is_set():
        randomHex = ''.join(sysrand.choices('0123456789abcdef', k=64))
        hashValue = hashlib.sha256(randomHex.encode('utf-8')).hexdigest().lower()
        with counterLock:
            counter += 1

        if hashValue.startswith(target):
            if not stopEvent.is_set():
                resultsQueue.put((randomHex, hashValue))
                with hashLock:
                    if len(foundHashes) + resultsQueue.qsize() >= numToFind:
                        stopEvent.set()
                        break

threads = []
for _ in range(numThreads):
    thread = threading.Thread(target=searchHash, daemon=True)
    threads.append(thread)
    thread.start()

lastPrintTime = startTime
shouldStop = False

def print_status():
    with counterLock:
        print(f"Values checked: {counter} | Found: {len(foundHashes)}/{numToFind} | Elapsed: {int(time.time()-startTime)}s")

while not shouldStop:
    while not resultsQueue.empty() and len(foundHashes) < numToFind:
        value, hashValue = resultsQueue.get()
        with hashLock:
            if len(foundHashes) < numToFind:
                foundHashes.append((value, hashValue))
                print(f"Found value {len(foundHashes)}: {value} : {hashValue}")
                if len(foundHashes) >= numToFind:
                    stopEvent.set()
                    break

    currentTime = time.time()
    if currentTime - lastPrintTime >= interval:
        print_status()
        lastPrintTime = currentTime

    if stopEvent.is_set():
        break
    try:
        time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nStopping search due to user interrupt.")
        shouldStop = True
        stopEvent.set()

for thread in threads:
    thread.join()

while not resultsQueue.empty() and len(foundHashes) < numToFind:
    value, hashValue = resultsQueue.get()
    with hashLock:
        if len(foundHashes) < numToFind:
            foundHashes.append((value, hashValue))
            print(f"Found value {len(foundHashes)}: {value} : {hashValue}")

print(f"\nTotal values checked: {counter}")
print(f"Found {len(foundHashes)} matching hashes:")
for i, (value, hashValue) in enumerate(foundHashes, 1):
    print(f"{i}. {value} : {hashValue}")