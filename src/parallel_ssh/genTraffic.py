import sys
import subprocess
import os
import ast
import time
import configparser
import argparse

####################################################################################################
"""
get_options
    get user options
    input : argv[1:]
    output: options
"""
def get_options(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(description="genTraffic: run traffic on physical network")
    parser.add_argument("-topo",   type=str, required=True, dest="topo_cfg_phy_file",   help="path to topo ini file")
    parser.add_argument("-bw_cfg", type=str, required=True, dest="bw_cfg"           ,   help="BW CFG")
    parser.add_argument("-sc"    , type=str, required=True, dest="sc"               ,   help="scenario number")
    args = parser.parse_args()
    print('{}\n'.format(args))
    return args

####################################################################################################
"""
get_host_name
    
    input :
    output:
"""
def get_host_name():
    out = subprocess.Popen("hostname", stdout=subprocess.PIPE, shell=True)
    out.wait()
    return str(out.communicate()[0])

####################################################################################################
"""
execute_genTraffic():
    
    input :
    output:
"""
def execute_genTraffic():
    os.system("chmod +x Documents/Copied_scripts/genTraffic.sh")
    command = './Documents/Copied_scripts/genTraffic.sh'.split()
    # print(['exec', 'sudo', '-S'] + command)
    p = subprocess.Popen(['sudo', '-S'] + command, stdin=subprocess.PIPE, stderr=subprocess.PIPE,universal_newlines=True)
    sudo_prompt = p.communicate("10203040" + '\n')[1]
    time.sleep(20)
    #os.kill(p.pid)
        # os.killpg(os.getpgid(p.pid), signal.SIGTERM)
        #sleep(15)
        #p.terminate()
        # try:
        #     outs, errs = p.communicate(timeout=15)
        # except TimeoutExpired:
        #     p.kill()
        #     outs, errs = p.communicate()

####################################################################################################
"""
write_genTraffic
    
    input :
    output:
"""
def write_genTraffic(options):
    topo_cfg = configparser.ConfigParser()
    topo_cfg.read(options.topo_cfg_phy_file)
    bw_dict = ast.literal_eval(topo_cfg["cfg_bw"][options.bw_cfg])
    topo = topo_cfg["parameters"]["name"]
    print(bw_dict)
    host_name = get_host_name()
    genTraffic = open("/home/sari_adham/Documents/Copied_scripts/genTraffic.sh",'w')
    output_path = "/home/sari_adham/Documents/output/bw_" + options.bw_cfg

    if ("host109" in host_name):
        time.sleep(2)
        #genTraffic.write("ethtool -s eno2 speed %s duplex full autoneg on\n" % str(bw_dict["client0_bw"]))
        genTraffic.write("iperf3 -i 0.1 -c 10.72.1.133 -p 5001 -t 180 -B 10.72.1.109 --cport 7001 > %s/c0.log &\n" % (output_path))
        genTraffic.write("sleep 185")

    elif ("host110" in host_name):
        time.sleep(2.2) 
        #genTraffic.write("ethtool -s eno2 speed %s duplex full autoneg on\n" % str(bw_dict["client1_bw"]))
        genTraffic.write("iperf3 -i 0.1 -c 10.72.1.133 -p 5002 -t 180 -B 10.72.1.110 --cport 7002 > %s/c1.log &\n" % (output_path))
        genTraffic.write("sleep 185")

    elif ("host111" in host_name):
        time.sleep(2.4)
        #genTraffic.write("ethtool -s eno2 speed %s duplex full autoneg on\n" % str(bw_dict["client2_bw"]))
        genTraffic.write("iperf3 -i 0.1 -c 10.72.1.133 -p 5003 -t 180 -B 10.72.1.111 --cport 7003 > %s/c2.log &\n" % (output_path))
        genTraffic.write("sleep 185")

    elif ("host112" in host_name):
        time.sleep(2.6)
        #genTraffic.write("ethtool -s eno2 speed %s duplex full autoneg on\n" % str(bw_dict["client4_bw"]))
        genTraffic.write("iperf3 -i 0.1 -c 10.72.1.133 -p 5004 -t 180 -B 10.72.1.112 --cport 7004 > %s/c3.log &\n" % (output_path))
        genTraffic.write("sleep 185")

    elif ("host113" in host_name):
        time.sleep(2.8)
        #genTraffic.write("ethtool -s eno2 speed %s duplex full autoneg on\n" % str(bw_dict["client5_bw"]))
        genTraffic.write("iperf3 -i 0.1 -c 10.72.1.133 -p 5005 -t 180 -B 10.72.1.113 --cport 7005 > %s/c4.log &\n" % (output_path))
        genTraffic.write("sleep 185")

    elif ("host114" in host_name):
        #genTraffic.write("ethtool -s eno2 speed %s duplex full autoneg on\n" % str(bw_dict["client6_bw"]))
        if(topo == "Topo3"):
            time.sleep(2)
            genTraffic.write("iperf3 -i 0.1 -c 10.72.1.135 -p 5006 -t 180 -B 10.72.1.114 --cport 7006 > %s/c5.log &\n" % (output_path))
        else:
            time.sleep(3)
            genTraffic.write("iperf3 -i 0.1 -c 10.72.1.133 -p 5006 -t 180 -B 10.72.1.114 --cport 7006 > %s/c5.log &\n" % (output_path))
        genTraffic.write("sleep 185")

    elif("host129" in host_name):
        # genTraffic.write("ethtool -s eno2 speed %s duplex full autoneg on\n" % str(bw_dict["client7_bw"]))
        if(topo == "Topo3"):
            time.sleep(2.2)
            genTraffic.write("iperf3 -i 0.1 -c 10.72.1.135 -p 5007 -t 180 -B 10.72.1.129 --cport 7007 > %s/c6.log &\n" % (output_path))
        else:
            time.sleep(3.2)
            genTraffic.write("iperf3 -i 0.1 -c 10.72.1.133 -p 5007 -t 180 -B 10.72.1.129 --cport 7007 > %s/c6.log &\n" % (output_path))
        genTraffic.write("sleep 185")

    elif ("host130" in host_name):
        # genTraffic.write("ethtool -s eno2 speed %s duplex full autoneg on\n" % str(bw_dict["client8_bw"]))
        if(topo == "Topo3"):
            time.sleep(2.4)
            genTraffic.write("iperf3 -i 0.1 -c 10.72.1.135 -p 5008 -t 180 -B 10.72.1.130 --cport 7008 > %s/c7.log &\n" % (output_path))
        else:
            time.sleep(3.4)
            genTraffic.write("iperf3 -i 0.1 -c 10.72.1.133 -p 5008 -t 180 -B 10.72.1.130 --cport 7008 > %s/c7.log &\n" % (output_path))
        genTraffic.write("sleep 185")

    elif ("host131" in host_name):
        # genTraffic.write("ethtool -s eno2 speed %s duplex full autoneg on\n" % str(bw_dict["client9_bw"]))
        if(topo == "Topo3"):
            time.sleep(2.6)
            genTraffic.write("iperf3 -i 0.1 -c 10.72.1.135 -p 5009 -t 180 -B 10.72.1.131 --cport 7009 > %s/c8.log &\n" % (output_path))
        else:
            time.sleep(3.6)
            genTraffic.write("iperf3 -i 0.1 -c 10.72.1.133 -p 5009 -t 180 -B 10.72.1.131 --cport 7009 > %s/c8.log &\n" % (output_path))
        genTraffic.write("sleep 185")

    elif ("host134" in host_name):
        # genTraffic.write("ethtool -s eno2 speed %s duplex full autoneg on\n" % str(bw_dict["client10_bw"]))
        if(topo == "Topo3"):
            time.sleep(2.6)
            genTraffic.write("iperf3 -i 0.1 -c 10.72.1.135 -p 5010 -t 180 -B 10.72.1.134 --cport 7010 > %s/c9.log &\n" % (output_path))
        else:
            time.sleep(3.8)
            genTraffic.write("iperf3 -i 0.1 -c 10.72.1.133 -p 5010 -t 180 -B 10.72.1.134 --cport 7010 > %s/c9.log &\n" % (output_path))
        genTraffic.write("sleep 185")

    elif ("host135" in host_name):
        if(topo == "Topo3"):
            genTraffic.write("iperf3 -i 0.1 -s -p 5006 -B 10.72.1.135 &\n")
            genTraffic.write("tcpdump -i eno2 -n 'tcp port 5006' -w %s/c5.pcap &\n" % (output_path))

            genTraffic.write("iperf3 -i 0.1 -s -p 5007 -B 10.72.1.135 &\n")
            genTraffic.write("tcpdump -i eno2 -n 'tcp port 5007' -w %s/c6.pcap &\n" % (output_path))

            genTraffic.write("iperf3 -i 0.1 -s -p 5008 -B 10.72.1.135 &\n")
            genTraffic.write("tcpdump -i eno2 -n 'tcp port 5008' -w %s/c7.pcap &\n" % (output_path))

            genTraffic.write("iperf3 -i 0.1 -s -p 5009 -B 10.72.1.135 &\n")
            genTraffic.write("tcpdump -i eno2 -n 'tcp port 5009' -w %s/c8.pcap &\n" % (output_path))

            genTraffic.write("iperf3 -i 0.1 -s -p 5010 -B 10.72.1.135 &\n")
            genTraffic.write("tcpdump -i eno2 -n 'tcp port 5010' -w %s/c9.pcap &\n" % (output_path))

        else:
            time.sleep(4)
        # genTraffic.write("ethtool -s eno2 speed %s duplex full autoneg on\n" % str(bw_dict["client2_bw"]))
            genTraffic.write("iperf3 -i 0.1 -c 10.72.1.133 -p 5011 -t 180 -B 10.72.1.131 --cport 7011 > %s/c10.log &\n" % (output_path))
            genTraffic.write("sleep 185")

    elif ("host133" in host_name):
        genTraffic.write("ethtool -s eno2 speed %s duplex full autoneg on\n" % str(bw_dict["server0_bw"]))

        genTraffic.write("iperf3 -i 0.1 -s -p 5001 -B 10.72.1.133 &\n")
        genTraffic.write("tcpdump -i eno2 -n 'tcp port 5001' -w %s/c0.pcap &\n" % (output_path))

        genTraffic.write("iperf3 -i 0.1 -s -p 5002 -B 10.72.1.133 &\n")
        genTraffic.write("tcpdump -i eno2 -n 'tcp port 5002' -w %s/c1.pcap &\n" % (output_path))

        genTraffic.write("iperf3 -i 0.1 -s -p 5003 -B 10.72.1.133 &\n")
        genTraffic.write("tcpdump -i eno2 -n 'tcp port 5003' -w %s/c2.pcap &\n" % (output_path))

        genTraffic.write("iperf3 -i 0.1 -s -p 5004 -B 10.72.1.133 &\n")
        genTraffic.write("tcpdump -i eno2 -n 'tcp port 5004' -w %s/c3.pcap &\n" % (output_path))

        genTraffic.write("iperf3 -i 0.1 -s -p 5005 -B 10.72.1.133 &\n")
        genTraffic.write("tcpdump -i eno2 -n 'tcp port 5005' -w %s/c4.pcap &\n" % (output_path))

        if(topo != "Topo3"):
            genTraffic.write("iperf3 -i 0.1 -s -p 5006 -B 10.72.1.133 &\n")
            genTraffic.write("tcpdump -i eno2 -n 'tcp port 5006' -w %s/c5.pcap &\n" % (output_path))

            genTraffic.write("iperf3 -i 0.1 -s -p 5007 -B 10.72.1.133 &\n")
            genTraffic.write("tcpdump -i eno2 -n 'tcp port 5007' -w %s/c6.pcap &\n" % (output_path))

            genTraffic.write("iperf3 -i 0.1 -s -p 5008 -B 10.72.1.133 &\n")
            genTraffic.write("tcpdump -i eno2 -n 'tcp port 5008' -w %s/c7.pcap &\n" % (output_path))

            genTraffic.write("iperf3 -i 0.1 -s -p 5009 -B 10.72.1.133 &\n")
            genTraffic.write("tcpdump -i eno2 -n 'tcp port 5009' -w %s/c8.pcap &\n" % (output_path))

            genTraffic.write("iperf3 -i 0.1 -s -p 5010 -B 10.72.1.133 &\n")
            genTraffic.write("tcpdump -i eno2 -n 'tcp port 5010' -w %s/c9.pcap &\n" % (output_path))

    genTraffic.close()

####################################################################################################
if __name__ == '__main__':
    write_genTraffic(get_options())
    execute_genTraffic()
