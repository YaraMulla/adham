import sys
import argparse
import os

####################################################################################################
"""
parse_args
    parse user arguments
    input : argv[1:]
    output: args
"""
def parse_args(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(description="genTraffic: run traffic on physical network")
    parser.add_argument("-bw_cfg", type=str, required=True, dest="bw_cfg",          help="BW CFG")
    parser.add_argument("-sc"    , type=str, required=True, dest="sc",              help="scenario number")
    args = parser.parse_args()
    print('{}\n'.format(args))
    return args

####################################################################################################
"""
copy_scripts
    
    input : topo , scenario
    output:
"""
def copy_scripts():
    active_hosts = ("sari_adham@10.70.1.109","sari_adham@10.70.1.110","sari_adham@10.70.1.111","sari_adham@10.70.1.112","sari_adham@10.70.1.113","sari_adham@10.70.1.114","sari_adham@10.70.1.129","sari_adham@10.70.1.130","sari_adham@10.70.1.131","sari_adham@10.70.1.133","sari_adham@10.70.1.134","sari_adham@10.70.1.135")
    copied_script = "scp /home/sari_adham/project_b/MiniNet_TCP_Study/src/parallel_ssh/genTraffic.py "
    for host in active_hosts:
        scp_cmd = copied_script + host + ":/home/sari_adham/Documents/Copied_scripts"
        os.system(scp_cmd)

####################################################################################################
"""
copy_config_file
    
    input : topo , scenario
    output:
"""
def copy_config_file():
    active_hosts = ("sari_adham@10.70.1.109","sari_adham@10.70.1.110","sari_adham@10.70.1.111","sari_adham@10.70.1.112","sari_adham@10.70.1.113","sari_adham@10.70.1.114","sari_adham@10.70.1.129","sari_adham@10.70.1.130","sari_adham@10.70.1.131","sari_adham@10.70.1.133","sari_adham@10.70.1.134","sari_adham@10.70.1.135")
    copied_script = "scp /home/sari_adham/project_b/MiniNet_TCP_Study/src/cfg/Topo1_cfg_phy.ini "
    for host in active_hosts:
        scp_cmd = copied_script + host + ":/home/sari_adham/Documents/Copied_scripts"
        os.system(scp_cmd)

####################################################################################################
"""
gen_traffic
    
    input :
    output:
"""
def gen_traffic(args):

    gen_traffic = "sshpass -p 10203040 parallel-ssh -t 200 -i -h ~/.pssh_hosts_file \
    \"python3 /home/sari_adham/Documents/Copied_scripts/genTraffic.py -sc %s -bw_cfg %s -topo %s\"" \
    % (args.sc,args.bw_cfg,'/home/sari_adham/Documents/Copied_scripts/Topo1_cfg_phy.ini')
    os.system(gen_traffic)

####################################################################################################
if __name__ == '__main__':
        args = parse_args()
        copy_scripts()
        copy_config_file()
        gen_traffic(args)
