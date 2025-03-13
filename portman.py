#############################################################
#            THIS CODE MADE BY DARK_C0DEX                   #
#          A Network Ports Scanning Tool                   #
#############################################################


# Importing Libraries Of Python...
import os
import sys
import colorama
import platform
import socket
import concurrent.futures
from colorama import Fore, init, Style, Back

# Setting up Colorama
init(autoreset=True)

# The ASCII Art For This Code 
art = r'''
 _______    ______   _______   ________  __       __   ______   __    __       
/       \  /      \ /       \ /        |/  \     /  | /      \ /  \  /  |      
$$$$$$$  |/$$$$$$  |$$$$$$$  |$$$$$$$$/ $$  \   /$$ |/$$$$$$  |$$  \ $$ |      
$$ |__$$ |$$ |  $$ |$$ |__$$ |   $$ |   $$$  \ /$$$ |$$ |__$$ |$$$  \$$ |      
$$    $$/ $$ |  $$ |$$    $$<    $$ |   $$$$  /$$$$ |$$    $$ |$$$$  $$ |      
$$$$$$$/  $$ |  $$ |$$$$$$$  |   $$ |   $$ $$ $$/$$ |$$$$$$$$ |$$ $$ $$ |      
$$ |      $$ \__$$ |$$ |  $$ |   $$ |   $$ |$$$/ $$ |$$ |  $$ |$$ |$$$$ |      
$$ |      $$    $$/ $$ |  $$ |   $$ |   $$ | $/  $$ |$$ |  $$ |$$ | $$$ |      
$$/        $$$$$$/  $$/   $$/    $$/    $$/      $$/ $$/   $$/ $$/   $$/       
                                                                              
                                                                Made By : Dark_C0dex'''

def clear_terminal():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

# Function to get service name
def get_service(port, protocol="tcp"):
    try:
        return socket.getservbyport(port, protocol)
    except OSError:
        return "Unknown Service"

# Function to scan a single TCP port
def tcp_scan_port(target_ip, tcp_port, results):
    tcp_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_s.settimeout(1)
    result = tcp_s.connect_ex((target_ip, tcp_port)) 
    if result == 0:
        service_name = get_service(tcp_port, "tcp")
        results.append((tcp_port, service_name))
    tcp_s.close()

# The TCP Scanning Method with Thread Pool
def Tcp_scan():
    tcp_input_target = input(f"Enter Your Target's IP >>> ")
    try:
        target_ip = socket.gethostbyname(tcp_input_target)
    except socket.gaierror:
        print(f"{Fore.RED} Error: Please use a valid IP address.")
        return
    
    try:
        tcp_threads = int(input("Enter The Threads >>> "))
        if tcp_threads <= 0:
            raise ValueError("Thread count must be greater than 0.")
    except ValueError:
        print(f"{Fore.RED} Error: Please enter a valid number for threads.")
        return
    
    tcp_start_port = 1
    tcp_end_port = 100000
    
    print(f"{Fore.CYAN}Scanning target: {target_ip} With {tcp_threads} Threads..")
    
    results = []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=tcp_threads) as executor:
        futures = [executor.submit(tcp_scan_port, target_ip, port, results) for port in range(tcp_start_port, tcp_end_port + 1)]
        concurrent.futures.wait(futures)
    
    results.sort()
    for port, service in results:
        print(f"{Fore.GREEN}Open Port Found: {port} ({service})")

# The UDP Scanning Method (Not available)
def Udp_scan():
    print(f"{Fore.RED}Error : Sorry Udp Scan Not Available For Now We Will add It Soon..")

def main_selec():
    clear_terminal()
    print(Fore.RED + art)
    print(f"[ == ]{Fore.CYAN} Please select your scanning type by choosing a number{Style.RESET_ALL}\n1.{Fore.GREEN} TCP Scan{Style.RESET_ALL}\n2.{Fore.GREEN} UDP Scan{Style.RESET_ALL}")
    main_input = input(f"Please select a number between 1 and 2 >>> ")
    if main_input == "1":
        Tcp_scan()
    elif main_input == "2":
        Udp_scan()
    else:
        print(f"{Fore.RED} Error: Please select a valid number.")
        input(f"{Fore.GREEN} Press Enter to go back.")
        main_selec()

if __name__ == '__main__':
    main_selec()