import threading
import time

def plugin_instance_routine(plugin_name, plugin_instance_id, run_id, update_interval):
    while True:
        print("Plugin instance routine: ", plugin_name, plugin_instance_id, run_id, update_interval)
        time.sleep(update_interval)

# Create 5 threads
threads = []
for i in range(5):
    t = threading.Thread(target=plugin_instance_routine, args=(i, "arg1_value", "arg2_value"))
    threads.append(t)

# Start all threads
for t in threads:
    t.start()

# Wait for all threads to complete
for t in threads:
    t.join()
