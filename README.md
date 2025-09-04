![throttle_banner](./assets/banner.png)

# 🔒 Device Access Locker
![Throttle Guard](https://img.shields.io/badge/CONTROL-NET-003366?style=for-the-badge&labelColor=111111)

> _"Block specific apps and platforms on selected devices in your LAN using iptables, ARP spoofing, and DNS overrides."_  

---

## ⚡ What is this?

This project provides a **Python-based network locker** that allows you to block access to certain platforms (e.g., Roblox, TikTok, Facebook) for specific devices on your network.

It works by:
1. Running **ARP spoofing** to redirect traffic through your machine.  
2. Applying **iptables rules** to drop connections to known IP ranges.  
3. Adding **DNS overrides** in `/etc/hosts` for target domains.  
4. Restarting resolvers to enforce changes.  

When you unlock, all changes are reverted.  

---

## 🚨 Disclaimer

- Requires **root privileges** (`sudo`).  
- Uses **iptables** and **ARP spoofing** (via [bettercap](https://www.bettercap.org/)).  
- Designed for **local testing, parental control, or network management**.  
- Misuse (e.g., blocking others’ traffic without consent) may be illegal. **You are responsible for your use.**  

---

## 📂 Structure

- `BaseLocker` → Core class with lock/unlock logic.  
- `Roblox`, `TikTok`, `Facebook` → Predefined service blockers (DNS + IP ranges).  
- `BaseMixinInfo` → Example device list (`target_devices_list`).  

You can create your own blockers by defining new classes with:
- `dns_list` (domains to block)  
- `ip_list` (IP ranges to block)  

---

## ⚙️ Requirements

- Python 3.10+  
- `bettercap` (installed and accessible in `~/Programs/bettercap`)  
- Linux with `iptables` and `systemd-resolved`  

---

## 🚀 Usage

### 1. Configure your target device(s)
Edit `BaseMixinInfo` or subclass it:
```python
class BaseMixinInfo:
    target_devices_list = ["192.168.1.110"]  # Replace with your device IP
````

### 2. Run a blocker

Example: block Roblox for the target device

```python
roblox = Roblox()
roblox.lock()
```

### 3. Unlock (restore access)

```python
roblox.unlock()
```

---

## 🛠️ Extending

To add a new platform:

```python
class YouTube(BaseMixinInfo, BaseLocker):
    dns_list = ["youtube.com", "www.youtube.com"]
    ip_list = ["142.250.0.0/16"]
```

Then run:

```python
yt = YouTube()
yt.lock()
```

---

## 🧭 Logging

* Logs are printed to console and include every executed command.
* Failed commands are marked with ❌.

---

## ✅ Example Output

```
2025-09-04 22:00:00 - INFO - ⛔ Блокируем доступ к Roblox...
2025-09-04 22:00:01 - INFO - ✅ sudo iptables -A FORWARD -s 192.168.1.110 -d 128.116.0.0/16 -j DROP
...
2025-09-04 22:00:05 - INFO - ✅ Roblox уничтожен для выбранных устройств!
```

---

## 📌 Notes

* Make sure your system is configured to allow **packet forwarding**.
* This script is experimental. Use carefully on production networks.
