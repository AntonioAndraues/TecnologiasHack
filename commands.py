import argparse
import socket # for connecting
from colorama import init, Fore
from scapy.all import ARP, Ether, srp
import nmap3

from threading import Thread, Lock
from queue import Queue
# REFERENCE https://www.thepythoncode.com/code/make-port-scanner-python
# some colors
init()
GREEN = Fore.GREEN
RESET = Fore.RESET
GRAY = Fore.LIGHTBLACK_EX
RED = Fore.RED

# number of threads, feel free to tune this parameter as you wish
N_THREADS = 200
# thread queue
q = Queue()
print_lock = Lock()

def discover_hosts(host):
    #  reference https://www.thepythoncode.com/article/building-network-scanner-using-scapy 
    target_ip = host
    # IP Address for the destination
    # create ARP packet
    arp = ARP(pdst=target_ip)
    # create the Ether broadcast packet
    # ff:ff:ff:ff:ff:ff MAC address indicates broadcasting
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    # stack them
    packet = ether/arp

    result = srp(packet, timeout=3, verbose=0)[0]

    # a list of clients, we will fill this in the upcoming loop
    clients = []

    for sent, received in result:
        # for each response, append ip and mac address to `clients` list
        clients.append({'ip': received.psrc, 'mac': received.hwsrc})

    # print clients
    print("Available devices in the network:")
    print("IP" + " "*18+"MAC")
    for client in clients:
        print(f"{GREEN}{client['ip']:16}{RESET}    {GRAY}{client['mac']}{RESET}")
    clients = [client['ip'] for client in clients ]
    return clients
def discorver_vr(host):
    nmap = nmap3.NmapScanTechniques()
    result = nmap.nmap_tcp_scan(host)
    return result
    
def port_scan(host,port,tcp):
    """
    Scan ports from host
    """
    if(tcp):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, port))
        except:
            with print_lock:
                print(f"{GRAY}{host:15}:{port:5} is closed  {RESET}", end='\r')
        else:
            with print_lock:
                print(f"{GREEN}{host:15}:{port:5} is open    {RESET}")
                if(0<=port<1024):
                    print(f"{RED}{port:5}  {RESET}")
        finally:
            s.close()
    else:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect((host, port))
        except:
            with print_lock:
                print(f"{GRAY}{host:15}:{port:5} is closed  {RESET}", end='\r')
        else:
            with print_lock:
                print(f"{GREEN}{host:15}:{port:5} is open    {RESET}")
        finally:
            s.close()

def scan_thread(host,input):
    global q
    while True:
        # get the port number from the queue
        worker = q.get()
        # scan that port number
        port_scan(host=host,port=worker,tcp=input)
        # tells the queue that the scanning for that port 
        # is done
        q.task_done()


def main(host, ports,input):
    global q
    for t in range(N_THREADS):
        # for each thread, start it
        t = Thread(target=scan_thread,args=(host,input))
        # when we set daemon to true, that thread will end when the main thread ends
        t.daemon = True
        # start the daemon thread
        t.start()

    for worker in ports:
        # for each port, put that port into the queue
        # to start scanning
        q.put(worker)
    
    # wait the threads ( port scanners ) to finish
    q.join()


