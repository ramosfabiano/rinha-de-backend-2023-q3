import subprocess
import time
import json
import matplotlib.pyplot as plt

peek_interval = 3

def collect_stats() -> dict:
    print(f"Monitoring started. Collecting stats every {peek_interval}s. Press Ctrl+C to abort.")
    all_stats = {}
    try:
        while True:
            output = subprocess.check_output(['podman', 'stats', '--no-stream', '--format=json'])
            stats = json.loads(output)
            for s in stats:
                container_name = s['name']
                container_stats = {key: s[key] for key in ['cpu_percent', 'mem_usage']  }
                if container_name in all_stats:
                    all_stats[container_name].append(container_stats)
                else:
                    all_stats[container_name] = [container_stats]
            write_stats(all_stats)
            time.sleep(peek_interval)
    except KeyboardInterrupt:
        print("Monitoring stopped.")
    return all_stats


def write_stats(stats: dict):
    if stats:       
        summary = {}
        for key, entries in stats.items():
            max_cpu_percent = 0.0
            max_mem_usage = 0.0
            for item in entries:
                cpu_percent = float(item['cpu_percent'].rstrip('%'))
                mem_usage = float(item['mem_usage'].split("MB")[0])
                max_cpu_percent = max(max_cpu_percent, cpu_percent)
                max_mem_usage = max(max_mem_usage, mem_usage)
            summary[key] = {
                'max_cpu_percent': f'{max_cpu_percent}%',
                'max_mem_usage': f'{max_mem_usage}MB'
            }
        print(json.dumps(summary, indent=2))


def plot_stats(stats: dict):
    cpu_percent_data = []
    mem_usage_data = []
    # prepare data
    for key, entries in stats.items():
        cpu_percent_data.append([float(item['cpu_percent'].strip('%')) for item in entries])
        mem_usage_data.append([float(item['mem_usage'].split('MB')[0]) for item in entries])
    plt.figure(figsize=(12, 6))
    # cpu
    plt.subplot(1, 2, 1)
    for key, data_points in zip(stats.keys(), cpu_percent_data):
        plt.plot(data_points, label=key)
    plt.title('CPU Usage')
    plt.xlabel('Time')
    #plt.xticks([i * peek_interval for i in range(1, len(cpu_percent_data[0]))])
    plt.ylabel('CPU Utilization (%)')
    plt.legend()
    # memory
    plt.subplot(1, 2, 2)
    for key, data_points in zip(stats.keys(), mem_usage_data):
        plt.plot(data_points, label=key)
    plt.title('Memory Usage')
    plt.xlabel('Time)')    
    #plt.xticks([i * peek_interval for i in range(1, len(mem_usage_data[0]))])
    plt.ylabel('Memory Usage (MB)')
    plt.legend()
    # plot
    plt.tight_layout()
    plt.savefig('monitor.png')
    plt.show()


s = collect_stats()
plot_stats(s)


