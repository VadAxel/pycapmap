import os

########################################
# func to remove duplicate IPs
########################################

def remove_duplicates(ip_list):
    unique_ips = []
    seen_ips = set()

    for ip in ip_list:
        if ip not in seen_ips:
            unique_ips.append(ip)
            seen_ips.add(ip)

    return unique_ips

# Read IP addresses from the file
script_directory = os.path.dirname(os.path.abspath(__file__))
ip_file_path = os.path.join(script_directory, 'badip.txt')

with open(ip_file_path, 'r') as file:
    ip_addresses = [line.strip() for line in file]

# Remove duplicates
cleaned_ips = remove_duplicates(ip_addresses)

# Update the file with the cleaned IPs
with open(ip_file_path, 'w') as file:
    for ip in cleaned_ips:
        file.write(ip + '\n')

print("Duplicate IPs removed, keeping one copy of each.")
