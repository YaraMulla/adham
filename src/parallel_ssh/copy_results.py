import sys
import argparse
import os
import configparser

####################################################################################################
"""
parse_args
    parse user arguments
    input : argv[1:]
    output: args
"""
def parse_args(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(description="genTraffic: run traffic on physical network")
    parser.add_argument("-topo",   type=str, required=True, dest="topo_cfg_phy_file",   help="path to topo ini file")
    parser.add_argument("-sc"    , type=str, required=True, dest="sc",                  help="scenario number")
    args = parser.parse_args()
    print('{}\n'.format(args))
    return args

####################################################################################################
"""
copy_results
    
    input : topo , scenario
    output:
"""
def copy_results(args):
    topo_cfg = configparser.ConfigParser()
    topo_cfg.read(args.topo_cfg_phy_file)
    active_hosts = ("sari_adham@10.70.1.109","sari_adham@10.70.1.110","sari_adham@10.70.1.111","sari_adham@10.70.1.112","sari_adham@10.70.1.113","sari_adham@10.70.1.114","sari_adham@10.70.1.129","sari_adham@10.70.1.130","sari_adham@10.70.1.131","sari_adham@10.70.1.134","sari_adham@10.70.1.135") #"sari_adham@10.70.1.133"
    output_path = "/home/sari_adham/project_b/MiniNet_TCP_Study/runs/{}/phy_automatic/scenario{}/".format(topo_cfg["parameters"]["name"],args.sc)
    j = 0
    for host in active_hosts: 
        for i in range(1,2):
            scp_cmd = "scp " + host + ":/home/sari_adham/Documents/output/bw_{}/c{}.log ".format(i,j) + output_path + "bw_cfg_{}/".format(i)
            os.system(scp_cmd)
        j+=1

####################################################################################################
"""
copy_pcaps
    
    input : topo , scenario
    output:
"""
def copy_pcaps(args):
    topo_cfg = configparser.ConfigParser()
    topo_cfg.read(args.topo_cfg_phy_file)
    server = "sari_adham@10.70.1.133"
    output_path = "/home/sari_adham/project_b/MiniNet_TCP_Study/runs/{}/phy_automatic/scenario{}/".format(topo_cfg["parameters"]["name"],args.sc) 
    for i in range(1,2):
        for j in range(0,int(topo_cfg["parameters"]["clients_num"])):
            scp_cmd = "scp " + server + ":/home/sari_adham/Documents/output/bw_{}/c{}.pcap ".format(i,j) + output_path + "bw_cfg_{}/".format(i)
            os.system(scp_cmd)


####################################################################################################
if __name__ == '__main__':
        args = parse_args()
        copy_results(args)
        copy_pcaps(args)