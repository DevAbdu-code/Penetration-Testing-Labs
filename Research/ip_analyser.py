#  IP Address Analyzer Program
#  Created by: Abdu

def is_valid_ip(ip):
    parts = ip.split(".")
    
    if len(parts) != 4:
        return False
    
    for part in parts:
        if not part.isdigit():
            return False
        num = int(part)
        if num < 0 or num > 255:
            return False
    
    return True


def get_ip_class(first_octet):
    if 1 <= first_octet <= 126:
        return "Class A", "/8"
    elif 128 <= first_octet <= 191:
        return "Class B", "/16"
    elif 192 <= first_octet <= 223:
        return "Class C", "/24"
    elif 224 <= first_octet <= 239:
        return "Class D (Multicast)", "N/A"
    elif 240 <= first_octet <= 255:
        return "Class E (Experimental)", "N/A"
    else:
        return "Invalid", "N/A"


def get_ip_type(ip):
    parts = list(map(int, ip.split(".")))
    
    # Private ranges
    if parts[0] == 10:
        return "Private"
    elif parts[0] == 172 and 16 <= parts[1] <= 31:
        return "Private"
    elif parts[0] == 192 and parts[1] == 168:
        return "Private"
    else:
        return "Public"


def main():
    print("🌐 IP Address Analyzer created by Abdu")
    print("----------------------")
    
    ip = input("Enter an IP address: ")
    
    if not is_valid_ip(ip):
        print("❌ Invalid IP address!")
        return
    
    parts = list(map(int, ip.split(".")))
    first_octet = parts[0]
    
    ip_class, subnet = get_ip_class(first_octet)
    ip_type = get_ip_type(ip)
    
    print("\n Results:")
    print("IP Address:", ip)
    print("Class:", ip_class)
    print("Default Subnet:", subnet)
    print("Type:", ip_type)
    
    print("\n Additional Info:")
    print("Network Part:", ".".join(map(str, parts[:3])))
    print("Host Part:", parts[3])


if __name__ == "__main__":
    main()
