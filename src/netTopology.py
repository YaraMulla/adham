#!/usr/bin/python

import configparser
import argparse
import sys
import mininet
import ast
from mininet.node import Node
from mininet.link import TCLink
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import setLogLevel, info
from mininet.cli import CLI
import subprocess

####################################################################################################
def arg_parser():
    parser = argparse.ArgumentParser(description="netTopology: generate a network topology and run a traffic on it")
    parser.add_argument("-topo",   type=str, required=True, dest="topo_cfg_file",   help="path to topo ini file")
    parser.add_argument("-iperf3", type=str, required=True, dest="iperf3_cfg_file", help="path to iperf3 ini file")
    parser.add_argument("-bw_cfg", type=str, required=True, dest="bw_cfg",          help="BW CFG")
    parser.add_argument("-sc"    , type=str, required=True, dest="sc",              help="scenario number")
    args = parser.parse_args()
    print('{}\n'.format(args))
    return args

####################################################################################################
class NetworkTopo(Topo):
    """ Custom Network Topology"""
    def __init__(self, **opts):
        super(NetworkTopo, self).__init__(**opts)
        topo_cfg = configparser.ConfigParser()
        topo_cfg.read(opts["topo_cfg_file"])

        iperf3_cfg = configparser.ConfigParser()
        iperf3_cfg.read(opts["iperf3_cfg_file"])
        sc = opts["scenario"]

        if(topo_cfg["parameters"]["name"] == "Topo1"):
            if(sc == "1"):
                cfg_bw = opts["bw_cfg"]
                bw_dict = ast.literal_eval(topo_cfg["cfg_bw"][cfg_bw])
                print(bw_dict)
                print("*** init Topo1 ***\n")
                print("*** scenario: 1- all clients are active ***\n")
                print("*** adding switch sw1 ***\n")
                sw1 = self.addSwitch("sw1")

                print("*** adding servers ***\n")
                num_of_servers = int(topo_cfg["parameters"]["servers_num"])
                for i in range(num_of_servers):
                    new_server = self.addHost(name=("server_" + str(i)), ip=(topo_cfg["ips"]["server_base_ip"] + str(i + 100) + '/24'))
                    self.addLink(new_server, sw1, cls=TCLink, bw=bw_dict["server" + str(i) + "_bw"])

                print("*** adding clients ***\n")
                num_of_clients = int(topo_cfg["parameters"]["clients_num"])
                for i in range(num_of_clients):
                    new_client = self.addHost(name=("client_" + str(i)), ip=(topo_cfg["ips"]["client_base_ip"] + str(i + 1) + '/24'))
                    self.addLink(new_client, sw1, cls=TCLink, bw=bw_dict["client" + str(i) + "_bw"])

        elif(topo_cfg["parameters"]["name"] == "Topo2" or topo_cfg["parameters"]["name"] == "Topo3"):
            if(sc == "1"):
                print("*** init {} ***\n".format(topo_cfg["parameters"]["name"]))
                print("*** scenario: 1- all clients are active ***\n")
                print("*** adding switch sw1 ***\n")
                sw1 = self.addSwitch("sw1")

                print("*** adding servers ***\n")
                num_of_servers = int(topo_cfg["parameters"]["servers_num"])
                for i in range(num_of_servers):
                    new_server = self.addHost(name=("server_" + str(i)), ip=(topo_cfg["ips"]["server_base_ip"] + str(i + 100) + '/24'))
                    self.addLink(new_server, sw1, cls=TCLink, bw=1000)

                print("*** adding clients ***\n")
                num_of_clients = int(topo_cfg["parameters"]["clients_num"])
                for i in range(num_of_clients):
                    new_client = self.addHost(name=("client_" + str(i)), ip=(topo_cfg["ips"]["client_base_ip"] + str(i + 1) + '/24'))
                    self.addLink(new_client, sw1, cls=TCLink, bw=1000)

####################################################################################################
def run(args):

    iperf3_cfg = configparser.ConfigParser()
    iperf3_cfg.read(args.iperf3_cfg_file)

    topo_cfg = configparser.ConfigParser()
    topo_cfg.read(args.topo_cfg_file)

    topo = NetworkTopo(topo_cfg_file=args.topo_cfg_file, scenario=args.sc, bw_cfg=args.bw_cfg, iperf3_cfg_file=args.iperf3_cfg_file)
    net = Mininet(topo=topo,link=TCLink)
    net.start()

    sc_dict = ast.literal_eval(iperf3_cfg["sc"][args.sc])
    active_clients_num = len(sc_dict["clients_cmds"].keys())
    client_transmit_time = iperf3_cfg["parameters"]["transmit_time"]
    sleep_time = int(client_transmit_time) + 5

    traffic_generator = open("genTraffic.sh","w")
    print("***generating genTraffic.sh***\n")
    sleep = 0.2
    server_name = "server_0 "
    if(args.sc == "1"):
        print("***one server is receiving***")
        print("***"+str(active_clients_num)+" clients are sending***\n")
        for i in range(active_clients_num):
            if(i>4 and topo_cfg["parameters"]["name"] == "Topo3"):
                server_name = "server_1 "
            traffic_generator.write(server_name + sc_dict["server_cmds"][str(i)] + "\n")
            sniffing_cmd = "tcpdump -n 'tcp port %d' -w %s &" % (int(topo_cfg["ports"]["server_base_port"])+ i, "c"+str(i)+".pcap")
            traffic_generator.write(server_name + sniffing_cmd + "\n")
        for i in range(active_clients_num):
            curr_client='client_'+str(i)
            traffic_generator.write(curr_client + " sleep " + str(sleep) + "; " + sc_dict["clients_cmds"][str(i)] + "\n")
            if (i == active_clients_num-1):
                traffic_generator.write(curr_client + " sleep "+str(sleep_time)+"\n")

    traffic_generator.close()
    myScript = "genTraffic.sh"
    print("***running genTraffic***\n")
    CLI(net, script=myScript) 
    net.stop()

############################################################################
def move_files(args):
    topo_cfg = configparser.ConfigParser()
    topo_cfg.read(args.topo_cfg_file)
    topo_num = topo_cfg["parameters"]["name"][4]
    print("***moving logs***\n")
    cmd1 = "mv c*.log ../runs/Topo{}/automatic/scenario{}/bw_cfg_{}".format(topo_num, args.sc, args.bw_cfg)
    cmd2 = "mv c*.pcap ../runs/Topo{}/automatic/scenario{}/bw_cfg_{}".format(topo_num, args.sc, args.bw_cfg)

    move_log_process = subprocess.Popen(cmd1, stdout=subprocess.PIPE, shell=True)
    move_pcap_process = subprocess.Popen(cmd2, stdout=subprocess.PIPE, shell=True)

############################################################################
if __name__ == '__main__':
    args = arg_parser()
    run(args)
    move_files(args)
