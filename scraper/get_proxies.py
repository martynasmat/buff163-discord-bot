import random

def get_proxy():
    with open('proxies.txt', 'r') as f:
        lines = []
        for line in f:
            line = line.replace('\n', '')
            line = line.split(':')
            lines.append(line)
        return random.choice(lines)