import configparser
import argparse
import sys
import ast

####################################################################################################
"""
get_options
    get user options
    input : argv[1:]
    output: options
"""
def get_options(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(description="Parse user input")
    parser.add_argument("-topo", "--topo", type=str, required=True, help="topology init file")
    parser.add_argument("-transmit_time", "--transmit_time", type=str, required=True, help="transmit time in iperf3")
    options = parser.parse_args(args)
    return options

####################################################################################################
"""
create_iperf3_ini : create the iperf3 ini files for topology1
    input : topo_init_file , transmit_time (each client transmit time to server)
    output: iperf3 ini file for topology1
"""
def create_iperf3_ini(topo_init_file, transmit_time):

    topo_config = configparser.ConfigParser()
    topo_config.read(topo_init_file)
    iperf3_config = configparser.ConfigParser()

    parameters_hash = {}
    server_cmd_hash = {}
    client_cmd_hash = {}
    sc_hash = {}

    # Create iperf3 config file for Topo1 and Topo2 (scenario1 - all clients are sending)
    if(topo_config["parameters"]["name"] == "Topo1" or topo_config["parameters"]["name"] == "Topo2" or topo_config["parameters"]["name"] == "Topo3"):
        print("*** creating iperf3 cfg file for {}, scenario 1 - all clients are sending\n".format(topo_config["parameters"]["name"]))
        iperf3_config["parameters"] = {
            "name" : topo_config["parameters"]["name"],
            "transmit_time": transmit_time
        }
        server_ip = topo_config["ips"]["server_base_ip"] + str(100)
        server_base_port = topo_config["ports"]["server_base_port"]

        # create scenario 1 (all clients are sending)
        sc_dict = ast.literal_eval(topo_config["sc"]["1"])
        cmd_num = int(sc_dict["active_clients"])

        for cmd in range(cmd_num):
            server_cmd_hash[str(cmd)] = "iperf3 -i 0.1 -s -p %s > %s &" % (str(cmd + int(topo_config["ports"]['server_base_port'])), "c"+str(cmd) + "_s0.log")
            if(topo_config["parameters"]["name"] == "Topo3" and cmd > 4):
                server_ip = topo_config["ips"]["server_base_ip"] + str(101) 
            client_cmd_hash[str(cmd)] = "iperf3 -i 0.1 -c %s -p %s -t %s -B %s --cport %s > %s &" % (server_ip, str(cmd + int(topo_config["ports"]['server_base_port'])), transmit_time, topo_config["ips"]["client_base_ip"] + str(cmd + 1), str(cmd + int(topo_config["ports"]['client_base_port'])), "c"+str(cmd) + ".log")

        sc_hash["1"] = {
                            "server_cmds"   : server_cmd_hash,
                            "clients_cmds"  : client_cmd_hash
                       }
        iperf3_config["sc"] = sc_hash

    with open("cfg/" + topo_config["parameters"]["name"] + "_iperf3.ini", "w") as iperf3_config_file:
        iperf3_config.write(iperf3_config_file)

####################################################################################################
if __name__ == "__main__":
    options = get_options()
    create_iperf3_ini(options.topo, options.transmit_time)
