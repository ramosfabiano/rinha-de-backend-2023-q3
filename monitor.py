import subprocess
import time
import json


def collect_stats() -> dict:
    peek_interval = 3
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
                cpu_percent = float(item.get('cpu_percent', '0%').rstrip('%'))
                mem_percent = float(item.get('mem_usage', '0%').split("MB")[0])
                max_cpu_percent = max(max_cpu_percent, cpu_percent)
                max_mem_usage = max(max_mem_usage, mem_percent)
            summary[key] = {
                'max_cpu_percent': max_cpu_percent,
                'max_mem_usage': f'{max_mem_usage}MB'
            }
        print(json.dumps(summary, indent=2))


write_stats(collect_stats())


