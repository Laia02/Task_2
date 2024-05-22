import signal
import subprocess
import sys
import os
import time

def signal_handler(sig, frame):
    # Terminate subprocesses
    print("\033[92mTerminating all subprocesses...\033[0m")
    for process in processes:
        process.terminate()
    sys.exit(0)

# Register signal handler for SIGTERM and SIGINT
signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

# List to store subprocesses
processes = []

try:
    # Execute the server
    server_process = subprocess.Popen([sys.executable, 'decentralized_nodes/storageServer.py'])
    processes.append(server_process)

    # Execute the first script
    server_process = subprocess.Popen([sys.executable, 'decentralized_nodes/node0.py'])
    processes.append(server_process)

    # Execute the second script
    slave0_process = subprocess.Popen([sys.executable, 'decentralized_nodes/node1.py'])
    processes.append(slave0_process)

    # Execute the third script
    slave1_process = subprocess.Popen([sys.executable, 'decentralized_nodes/node2.py'])
    processes.append(slave1_process)

    # Check if the main process is still running
    while True:
        if os.getppid() == 1:  # If the parent process ID is 1 (init), the main process is terminated
            signal_handler(signal.SIGTERM, None)
        time.sleep(1)  # Wait for 1 second before checking again

except KeyboardInterrupt:
    # Handle Ctrl+C gracefully
    signal_handler(signal.SIGINT, None)
