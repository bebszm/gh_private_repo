import socket
from ping3 import ping
#https://www.redhat.com/en/blog/test-tcp-python-scapy

def tcp_port_test(address: str, dest_port: int) -> bool:

    print(f"Debug: Starting port test on {address}:{dest_port}")

    # Create socket connection & test port
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(5) # 5 sec timeout
            print(f"Debug: Attemping to connect to {address}:{dest_port}")

            result = sock.connect_ex((address, dest_port))

            if result == 0:
                print(f"Debug: Connecting to {address}:{dest_port} succeeded ({result})")
                return True
            else:
                print(f"Debug: Connection to {address}:{dest_port} failed. {result}")
                return False
                
    except (OSError, ValueError) as e:
        print(f"Debug: {e}")
        return False

def icmp_ping_test(address: str) -> (bool, float):
    try:
        response_time = ping(address, timeout=5)

        if response_time is None:
            return False, None
        return True, response_time
    except (OSError, ValueError) as e:
        print (f"Debug: {e}")
        return False

def main(address: str, dest_port: int) -> dict:
    tcp_status = tcp_port_test(address, dest_port)
    icmp_status, latency = icmp_ping_test(address)

    additional_info = {}

    if latency is not None:
        additional_info['icmp_latency_ms'] = latency

    return {
        'tcp_port_connection': tcp_status,
        'icmp_ping': icmp_status,
        'additional_info': additional_info
    }

if __name__ == "__main__":

    ip = "1.1.1.1"
    port = 80

    result = main(ip, port)
    print(f"Port check results: {result}")
