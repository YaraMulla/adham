import configparser
import sys
import argparse

####################################################################################################
"""
get_options
    get user options
    input : argv[1:]
    output: options
"""
def get_options(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(description="Parse user input")
    parser.add_argument('-t', '--topo',     dest='topo', help='number of topology to be configured',             default=None, required=True)
    parser.add_argument('-c', '--clients',  dest='c_num',help='number of clients to be add for custom topology', default=None, required=False)
    parser.add_argument('-p', '--phy',      dest='phy',  help='add if generating physical ini file',             default=False, required=False, action='store_true')
    options = parser.parse_args(args)
    return options

####################################################################################################
"""
create_topo1: create the ini file for topology number 1
    input : is physical topology
    output: .ini file for topology number 1
    topolgy 1: 3 clients and 1 server connected as star with 6 BW configurations

        Client1
           |
Client2--Switch--Client3
           |
         Server
"""
def create_topo_1(physical):
    print("*** creating topo1 cfg ini file, clients: 3, Physical:{} ***\n".format(physical))
    print("\nTopo:\n\t\t\tClient1\n\t\t\t   |\n\t\tClient2--Switch--Client3\n\t\t\t   |\n\t\t\t Server\n")
    config = configparser.ConfigParser()
    config["parameters"] = {
        "name" : "Topo1",
        "clients_num"            : 3,
        "servers_num"            : 1,
    }

    if(not physical):
        config["ips"] = {
            "server_base_ip" : "192.168.1.",
            "client_base_ip" : "192.168.1."
        }
    else:
        config["ips"] = {
            "server_base_ip" : "10.72.1.",
            "client_base_ip" : "10.72.1."
        }

    config["ports"] = {
        "server_base_port" : "5001",
        "client_base_port" : "7001"
    }

    config["cfg_bw"] = {
        "1" : {
                "client0_bw": 1000,
                "client1_bw": 1000,
                "client2_bw": 1000,
                "server0_bw": 1000
        },

        "2" : {
                "client0_bw": 1000,
                "client1_bw": 1000,
                "client2_bw": 100,
                "server0_bw": 1000
        },

        "3" : {
                "client0_bw": 100,
                "client1_bw": 1000,
                "client2_bw": 100,
                "server0_bw": 1000
        },

        "4" : {
                "client0_bw": 1000,
                "client1_bw": 1000,
                "client2_bw": 1000,
                "server0_bw": 100
        },

        "5" : {
                "client0_bw": 1000,
                "client1_bw": 1000,
                "client2_bw": 100,
                "server0_bw": 100
        },

        "6" : {
                "client0_bw": 100,
                "client1_bw": 1000,
                "client2_bw": 100,
                "server0_bw": 100
        },

        "7" : {
                "client0_bw": 100,
                "client1_bw": 100,
                "client2_bw": 100,
                "server0_bw": 100
        },

        "8" : {
                "client0_bw": 100,
                "client1_bw": 100,
                "client2_bw": 100,
                "server0_bw": 1000
        }

    }

    config["sc"] = {
        "1" :{
                "active_clients" : 3
             }
    }

    if(not physical):
        with open("cfg/Topo1_cfg.ini", "w") as topo1_config_file:
            config.write(topo1_config_file)
    else:
        with open("cfg/Topo1_cfg_phy.ini", "w") as topo1_config_file:
            config.write(topo1_config_file)


####################################################################################################
"""
create_topo2: create the ini file for topology number 2 (custom topology)
    input : is physical topology, clients number
    output: .ini file for topology number 2
    topolgy 2: N clients and 1 server connected as start, all links are 1000Mbps
"""
def create_topo_2(physical, c_num):
    print("*** creating topo2 cfg ini file, clients:{}, Physical:{} ***\n".format(c_num, physical))
    config = configparser.ConfigParser()
    config["parameters"] = {
        "name" : "Topo2",
        "clients_num"            : c_num,
        "servers_num"            : 1,
    }

    if(not physical):
        config["ips"] = {
            "server_base_ip" : "192.168.1.",
            "client_base_ip" : "192.168.1."
        }
    else:
        config["ips"] = {
            "server_base_ip" : "10.72.1.",
            "client_base_ip" : "10.72.1."
        }

    config["ports"] = {
        "server_base_port" : "5001",
        "client_base_port" : "7001"
    }

    config["sc"] = {
        "1" :{
                "active_clients" : c_num
             }
    }

    if(not physical):
        with open("cfg/Topo2_cfg.ini", "w") as topo2_config_file:
            config.write(topo2_config_file)
    else:
        with open("cfg/Topo2_cfg_phy.ini", "w") as topo2_config_file:
            config.write(topo2_config_file)

####################################################################################################
"""
create_topo3: create the ini file for topology number 3 (custom topology)
    input : is physical topology, clients number
    output: .ini file for topology number 3
    topolgy 3: N clients and 2 server connected as start, all links are 1000Mbps
"""
def create_topo_3(physical, c_num):
    print("*** creating topo3 cfg ini file, clients:{}, Physical:{} ***\n".format(c_num, physical))
    config = configparser.ConfigParser()
    config["parameters"] = {
        "name" : "Topo3",
        "clients_num"            : c_num,
        "servers_num"            : 2,
    }

    if(not physical):
        config["ips"] = {
            "server_base_ip" : "192.168.1.",
            "client_base_ip" : "192.168.1."
        }
    else:
        config["ips"] = {
            "server_base_ip" : "10.72.1.",
            "client_base_ip" : "10.72.1."
        }

    config["ports"] = {
        "server_base_port" : "5001",
        "client_base_port" : "7001"
    }

    config["sc"] = {
        "1" :{
                "active_clients" : c_num
             }
    }

    if(not physical):
        with open("cfg/Topo3_cfg.ini", "w") as topo3_config_file:
            config.write(topo3_config_file)
    else:
        with open("cfg/Topo3_cfg_phy.ini", "w") as topo3_config_file:
            config.write(topo3_config_file)

####################################################################################################
"""
create_topo3: create the ini file for topology number 3
    input : is physical topology
    output: .ini file for topology number 3
    topolgy 3: 3 clients connected to switch1 and 1 server connected to switch2, 2 switches are connected, all links are 1Mbps

        Client1
           |
Client2--Switch1--Client3
           |
         Switch2
           |
         Server       
"""
def create_topo_4(physical):
    print("*** creating topo3 cfg ini file, clients: 3, Physical:{} ***\n".format(physical))
    print("\nTopo:\n\t\t\tClient1\n\t\t\t   |\n\t\tClient2--Switch1--Client3\n\t\t\t   |\n\t\t\tSwitch2\n\t\t\t   |\n\t\t\t Server\n")
    config = configparser.ConfigParser()
    config["parameters"] = {
        "name" : "Topo2",
        "clients_num"            : 3,
        "servers_num"            : 1,
        "servers_link_bandwidth" : 200,
        "clients_link_bandwidth" : 100,
        "switches_link_bandwidth": 20,
    }
    config["ips"] = {
        "server_base_ip" : "192.168.1.",
        "client_base_ip" : "192.168.1."
    }
    config["ports"] = {
        "server_base_port" : "5001",
    }

    with open("topo3.ini", "w") as topo3_config_file:
        config.write(topo3_config_file)

####################################################################################################
"""
create_topo_config : create the ini file for specific topology
    input : topology number , physical flag and number of clients (for custom topologies)
    output: .ini file for topology
"""
def create_topo_config(topo_num, physical, c_num):
    if(topo_num == 1):
        create_topo_1(physical)
    elif(topo_num == 2):
        create_topo_2(physical, c_num)
    elif(topo_num == 3):
        create_topo_3(physical, c_num)
    else:
        print("error: no topology defined with this number\n")

####################################################################################################
if __name__ == '__main__':
    options = get_options()
    topo_num = int(options.topo)
    c_num = 5
    if(options.c_num != None):
        c_num = options.c_num
    create_topo_config(topo_num, options.phy, c_num)
