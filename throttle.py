import subprocess
import logging
import ipaddress

# Логирование
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class BaseLocker:
    interface: str = "wlan1"
    target_devices_list: list
    dns_list: list
    ip_list: list

    block_udp: bool = True
    block_dns: bool = True

    def lock(self):
        logging.info(f"⛔ Блокируем доступ к {self.__class__.__name__} для выбранных устройств...")
        # 1) Запускаем ARP-спуфинг, чтобы трафик шел через нас
        self.enable_arp_spoofing()
        # 2) Чистим все правила
        self.run_command("sudo iptables -F")

        # 3) Добавляем DROP-правила для IP-диапазонов
        for device_ip in self.target_devices_list:
            for ip in self.ip_list:
                self.run_command(f"sudo iptables -A FORWARD -s {device_ip} -d {ip} -j DROP")
                self.run_command(f"sudo iptables -A OUTPUT -s {device_ip} -d {ip} -j DROP")
                if self.block_udp:
                    self.run_command(f"sudo iptables -A FORWARD -s {device_ip} -p udp -d {ip} -j DROP")
                    self.run_command(f"sudo iptables -A OUTPUT -s {device_ip} -p udp -d {ip} -j DROP")

        # 4) Блокируем DNS через /etc/hosts
        if self.block_dns:
            for domain in self.dns_list:
                self.run_command(f"echo '127.0.0.1 {domain}' | sudo tee -a /etc/hosts")

        # 5) Перезапускаем резолвер и чистим кэш
        self.run_command("sudo systemctl restart systemd-resolved")
        self.run_command("sudo resolvectl flush-caches")

        logging.info(f"✅ {self.__class__.__name__} уничтожен для выбранных устройств!")

    def unlock(self):
        logging.info(f"⛔ Отключаем блокировку {self.__class__.__name__}...")
        # 1) Чистим правила
        self.run_command("sudo iptables -F")
        # 2) Останавливаем ARP-спуфинг
        self.disable_arp_spoofing()

        # 3) Удаляем записи DNS из hosts
        for domain in self.dns_list:
            self.run_command(f"sudo sed -i '/{domain}/d' /etc/hosts")

        # 4) Перезапускаем резолвер и чистим кэш
        self.run_command("sudo systemctl restart systemd-resolved")
        self.run_command("sudo resolvectl flush-caches")

        logging.info(f"✅ {self.__class__.__name__} снова доступен!")

    def enable_arp_spoofing(self):
        logging.info(f"🚀 Перенаправляем трафик через {self.interface} для {self.target_devices_list}...")
        for device_ip in self.target_devices_list:
            self.run_command(
                f"cd ~/Programs/bettercap && sudo go run main.go -eval 'set arp.spoof.targets {device_ip}; arp.spoof on' &"
            )

    def disable_arp_spoofing(self):
        logging.info("⛔ Останавливаем ARP-спуфинг...")
        self.run_command("sudo pkill bettercap")

    def run_command(self, cmd):
        try:
            subprocess.run(cmd, shell=True, check=True)
            logging.info(f"✅ {cmd}")
        except subprocess.CalledProcessError as e:
            logging.error(f"❌ Ошибка: {e}")

class BaseMixinInfo:
    target_devices_list = ["192.168.1.110"]

class Roblox(BaseMixinInfo, BaseLocker):
    dns_list = [
        "roblox.com",
        "www.roblox.com",
        "api.roblox.com",
        "games.roblox.com",
        "setup.roblox.com",
        "assetgame.roblox.com",
        "presence.roblox.com"
    ]
    ip_list = [
        "128.116.0.0/16",
        "185.221.0.0/16",
        "23.82.0.0/16",
        "45.10.0.0/16",
        "103.252.0.0/16"
    ]

class TikTok(BaseMixinInfo, BaseLocker):
    dns_list = [
        "tiktok.com",
        "www.tiktok.com",
        "api.tiktok.com",
        "m.tiktok.com",
        "m.tiktokcdn.com"
    ]
    ip_list = [
        "47.244.0.0/16",
        "123.206.0.0/16"
    ]

class Facebook(BaseMixinInfo, BaseLocker):
    dns_list = [
        "facebook.com",
        "www.facebook.com",
        "api.facebook.com",
        "m.facebook.com",
        "m.facebook.com"
    ]
    
