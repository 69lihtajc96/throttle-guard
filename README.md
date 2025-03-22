# Throttle Guard

🚨 **Throttle Guard** — инструмент для фильтрации и управления сетевым трафиком, предназначенный для блокировки нежелательных сервисов (например, Roblox и TikTok) на указанных устройствах в локальной сети.

## 🌟 Основные возможности
✅ Эффективная блокировка Roblox по IP-адресам и игровым портам
✅ Блокировка TikTok по IP-адресам и DNS-запросам
✅ Автоматическое управление ARP-спуфингом для точечного воздействия
✅ Гибкая конфигурация через JSON-файл
✅ Логирование всех действий для полного контроля
✅ Простота запуска через командный интерфейс

---

## ⚙️ Установка
1. Убедитесь, что на вашем устройстве установлены следующие зависимости:
```bash
sudo apt update
sudo apt install bettercap iptables
```
2. Клонируйте репозиторий:
```bash
git clone https://github.com/69lihtajc96/throttle-guard.git
cd throttle-guard
```
3. Настройте конфигурационный файл `throttle_config.json` по своему усмотрению:

```json
{
    "interface": "wlan1",
    "router_ip": "192.168.1.1",
    "target_devices": ["192.168.1.121", "192.168.1.132"],
    "dns_block": [
        "roblox.com",
        "tiktok.com"
    ],
    "roblox_ip_ranges": [
        "128.116.0.0/16",
        "185.221.0.0/16"
    ],
    "tiktok_ip_ranges": [
        "47.244.0.0/16",
        "123.206.0.0/16"
    ],
    "block_udp": true,
    "block_dns": true
}
```
4. Запустите скрипт:
```bash
python3 throttle.py
```

---

## 🚨 Команды управления

| Команда           | Описание |
|-------------------|-----------|
| **block**          | Запускает ARP-спуфинг и блокирует Roblox на выбранных устройствах |
| **unblock**        | Останавливает ARP-спуфинг и снимает блокировку Roblox |
| **blocktiktok**    | Запускает ARP-спуфинг и блокирует TikTok на выбранных устройствах |
| **unblocktiktok**  | Останавливает ARP-спуфинг и снимает блокировку TikTok |
| **exit**           | Завершает работу скрипта и отключает ARP-спуфинг |

Пример использования:
```
💀 Введите команду (block/unblock/blocktiktok/unblocktiktok/exit): block
```

---

## 🔧 Конфигурация
Файл **`throttle_config.json`** позволяет настроить ключевые параметры:
- **interface** — сетевой интерфейс (например, wlan1)
- **router_ip** — IP-адрес роутера
- **target_devices** — список устройств, на которые нацелен контроль
- **roblox_ip_ranges** и **tiktok_ip_ranges** — диапазоны IP-адресов, которые будут заблокированы
- **dns_block** и **tiktok_dns** — список доменов для блокировки на уровне DNS

---

## 🛡️ Безопасность и предостережения
⚠️ Этот инструмент предназначен для использования в образовательных и тестовых целях. Неправильное применение может нарушить работу сети. Всегда убедитесь, что имеете разрешение на проведение подобных манипуляций в локальной сети.

---

## 📜 Лицензия
Проект распространяется по лицензии **MIT**.
