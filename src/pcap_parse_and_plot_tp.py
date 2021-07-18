import configparser
import sys
import argparse
import subprocess
import time
import ast
import os

####################################################################################################
"""
get_options
    get user options
    input : argv[1:]
    output: options
"""
def get_options(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(description="Parse user input")
    parser.add_argument('-t', '--topo',     dest='topo',     help='number of topology to be analysed', required=True)
    parser.add_argument('-s', '--scenario', dest='scenario', help='number of scenario',                required=True)
    parser.add_argument('-b', '--bw',       dest='bw_cfg',   help='BW CFG',                            required=True)
    parser.add_argument('-p', '--phy',      dest='is_phy',   help='is phy',                            required=False, default=False, action='store_true')
    options = parser.parse_args(args)
    return options

####################################################################################################
"""
analyze_and_plot
    analyze pcap files and plot TP graphs for each scenario
    input : Topology, scenario and BW_CFG numbers + is physical topology
    output: 1) statistics files
            2) TP graphs
"""
def analyze_and_plot(topo, sc, bw_cfg, is_phy):
    prefix_phy = ""
    suffix_phy = ""
    if(is_phy):
        prefix_phy="phy_"
        suffix_phy="_phy"
    topo_cfg = configparser.ConfigParser()
    topo_cfg.read("cfg/Topo{}_cfg{}.ini".format(topo, suffix_phy))
    print("***processing Topo{} scenario{} bw_cfg_{}***".format(topo, sc, bw_cfg))
    sc_dict = ast.literal_eval(topo_cfg["sc"][str(sc)])
    clients_num = int(sc_dict["active_clients"])

    for c in range(clients_num):
    # for c in range(2,10):
        with open('../runs/Topo{}/{}automatic/scenario{}/bw_cfg_{}/statistics_c{}.log'.format(topo, prefix_phy, sc, bw_cfg, c), 'w') as f:
            captcp_process = subprocess.Popen(['captcp', 'statistic', '../runs/Topo{}/{}automatic/scenario{}/bw_cfg_{}/c{}.pcap'.format(topo, prefix_phy, sc, bw_cfg, c)], stdout=f)
            captcp_process.wait()
        f.close()

        # find flow according to connection
        if(is_phy):
            # if(c == 1):
            #     # WA for phy scenario (port 5002 is not working on 130)
            #     connection = "\'{}:{} -> {}133:{}\'".format(topo_cfg["ips"]["client_base_ip"] + str(c + 129), str(c + int(topo_cfg["ports"]["client_base_port"]) + 2), topo_cfg["ips"]["server_base_ip"], str(c + int(topo_cfg["ports"]["server_base_port"]) + 2))
            # else:
            if(c<6):
                connection = "\'{}:{} -> {}133:{}\'".format(topo_cfg["ips"]["client_base_ip"] + str(c + 109), str(c + int(topo_cfg["ports"]["client_base_port"])), topo_cfg["ips"]["server_base_ip"], str(c + int(topo_cfg["ports"]["server_base_port"])))
            elif(c>=6 and c<9):
                connection = "\'{}:{} -> {}133:{}\'".format(topo_cfg["ips"]["client_base_ip"] + str(c-6 + 129), str(c + int(topo_cfg["ports"]["client_base_port"])), topo_cfg["ips"]["server_base_ip"], str(c + int(topo_cfg["ports"]["server_base_port"])))
            else:
                connection = "\'{}:{} -> {}133:{}\'".format(topo_cfg["ips"]["client_base_ip"] + str(134), str(c + int(topo_cfg["ports"]["client_base_port"])), topo_cfg["ips"]["server_base_ip"], str(c + int(topo_cfg["ports"]["server_base_port"])))
        else:
            connection = "\'{}:{} -> {}100:{}\'".format(topo_cfg["ips"]["client_base_ip"] + str(c + 1), str(c + int(topo_cfg["ports"]["client_base_port"])), topo_cfg["ips"]["server_base_ip"], str(c + int(topo_cfg["ports"]["server_base_port"])))
        print(connection)
        cmd = "cat ../runs/Topo{}/{}automatic/scenario{}/bw_cfg_{}/statistics_c{}.log | grep {}".format(topo, prefix_phy, sc, bw_cfg, c, connection)
        out = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        out.wait()
        flow_list = out.communicate()[0].split(" ")
        index = flow_list.index('Flow')
        flow = flow_list[index + 1]

        # clean graph dirs
        rm_proc = subprocess.Popen(['rm', '-rf', '../runs/Topo{}/{}automatic/scenario{}/bw_cfg_{}/graphs_c{}'.format(topo, prefix_phy, sc, bw_cfg, c)])

        # make graph dir
        mkdir_proc = subprocess.Popen(['mkdir', '../runs/Topo{}/{}automatic/scenario{}/bw_cfg_{}/graphs_c{}'.format(topo, prefix_phy, sc, bw_cfg, c)])
        mkdir_proc.wait()

        # generate data files for graphs
        cmd = "captcp throughput -s 0.1 -i -f {} -o ../runs/Topo{}/{}automatic/scenario{}/bw_cfg_{}/graphs_c{} ../runs/Topo{}/{}automatic/scenario{}/bw_cfg_{}/c{}.pcap -p -u megabit".format(flow, topo, prefix_phy, sc, bw_cfg, c, topo, prefix_phy, sc, bw_cfg, c)
        out = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        out.wait()

        # modify the .gpi file
        bw_dict = {}
        if(topo == 1):
            bw_dict = ast.literal_eval(topo_cfg["cfg_bw"][str(bw_cfg)])
        gpi_path = "../runs/Topo{}/{}automatic/scenario{}/bw_cfg_{}/graphs_c{}/".format(topo, prefix_phy, sc, bw_cfg, c)
        os.system("mv " + gpi_path + "throughput.gpi " +  gpi_path + "tmp.gpi")
        print("mv " + gpi_path + "throughput.gpi " +  gpi_path + "tmp.gpi")
        writer = open(gpi_path + "throughput.gpi", 'w')
        with open(gpi_path + "tmp.gpi", 'r') as reader:
            lines = reader.readlines()
            for line in lines:
                if("set format y" in line):
                    if(topo == 1):
                        writer.write("set yrange [1:{}]".format(bw_dict["client{}_bw".format(c)]))
                    else:
                        writer.write("set yrange [1:1000]")
                else:
                    writer.write(line)
        reader.close()
        writer.close()
        os.system("rm -rf " + gpi_path + "tmp.gpi ")

        # generate TP graphs
        cmd = "make -C ../runs/Topo{}/{}automatic/scenario{}/bw_cfg_{}/graphs_c{}".format(topo, prefix_phy, sc, bw_cfg, c)
        out = subprocess.Popen(cmd, shell=True)
        out.wait()

####################################################################################################
if __name__ == '__main__':
    options = get_options()
    topo_num = int(options.topo)
    scenario_num = int(options.scenario)
    bw_cfg = int(options.bw_cfg)
    phy = options.is_phy
    analyze_and_plot(topo_num, scenario_num, bw_cfg, phy)
