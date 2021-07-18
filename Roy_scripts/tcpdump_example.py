#!/usr/bin/python3

import os
import threading
from pathlib import Path

from enum import Enum
from signal import SIGINT
from time import sleep
from mininet.link import TCLink
from mininet.log import setLogLevel
from mininet.net import Mininet
from datetime import datetime
from mininet.node import OVSController
from mininet.util import pmonitor

from simulation.simulation_topology import SimulationTopology
from simulation.single_connection_statistics import SingleConnStatistics
from simulation.tcpdump_statistics import TcpdumpStatistics
from simulation.tc_qdisc_statistics import TcQdiscStatistics
from simulation.graph_implementation import GraphImplementation



    def StartSimulation(self):
        self.net.start()
        # CLI(self.net)

        srv = self.net.getNodeByName(self.simulation_topology.srv)
        srv_ip = srv.IP()
        popens = {}
        srv_procs = []
        rtr = self.net.getNodeByName(self.simulation_topology.rtr)

        # Generate background noise
        noise_gen = self.net.getNodeByName(self.simulation_topology.noise_gen)

        if self.background_noise > 0:
            noise_gen.popen('python noise_generator.py %s %s' % (srv_ip, self.background_noise))
        client_counter = 0
        for client in self.simulation_topology.host_list:
            # Modify TCP algorithms (because iperf3 does not support vegas in -C parameter):
            cwnd_algo = client[0:client.find("_")]
            self.SetCongestionControlAlgorithm(client, cwnd_algo)

            test_port = (5201 + client_counter)

            # Map test port to algo. This will serve us in results processing
            self.port_algo_dict[test_port] = cwnd_algo

            # In iperf3, each test should have its own server. We have to terminate them at the end,
            # otherwise they are stuck in the system, so we keep the proc nums in a list.
            srv_cmd = 'iperf3 -s -p %d &' % test_port
            srv_procs.append(srv.popen(srv_cmd))

            # Throughput measuring- using tcpdump:
            # Running tcpdump on client side, saving to txt file (a separate txt file for each client):
            capture_filename = os.path.join(self.res_dirname, "client_%s.txt" % client)
            interface_name = "r-%s" % client
            cmd = "tcpdump -i %s 'tcp port %d'>%s&" % (interface_name, test_port, capture_filename)
            rtr.cmd(cmd)

            # Running tcpdump on server side, saving to txt file (a separate txt file for each client):
            capture_filename = os.path.join(self.res_dirname, "server_%s.txt" % client)
            self.file_captures.append(capture_filename)
            cmd = "tcpdump -i r-srv 'tcp port %d'>%s&" % (test_port, capture_filename)
            rtr.cmd(cmd)
            client_counter += 1

            # Disable TSO for the client
            cmd = "ethtool -K %s-r tso off" % client
            self.net.getNodeByName(client).cmd(cmd)

        # Disable TSO for router
        cmd = "ethtool -K r-srv tso off"
        rtr.cmd(cmd)

        sleep(5)
        # Traffic generation loop:
        client_counter = 0
        for client in self.simulation_topology.host_list:
            cwnd_algo = client[0:client.find("_")]
            # cmd = 'iperf3 -c %s -t %d -p %d -C %s' % (srv_ip, self.seconds, 5201 + client_counter, self.congestion_control_algorithm[client_counter % 2])
            # start_after = random.randint(0, self.iperf_start_after) / 1000
            start_after = self.iperf_start_after
            # cmd = 'sleep %f && iperf3 -c %s -t %d -p %d -C %s' % (
            #     start_after, srv_ip, self.seconds, 5201 + client_counter, cwnd_algo)
            cmd = 'sleep %f && iperf3 -c %s -t %d -p %d -C %s' % (
            start_after, srv_ip, self.seconds, 5201 + client_counter, cwnd_algo)
            # cmd = 'iperf3 -c %s -t %d -p %d -C %s &' % (srv_ip, self.seconds, 5201 + client_counter, cwnd_algo)
            print("sleeeeeeeeeeeeeeeeeeeeeeping %s " % cmd)
            popens[client] = (self.net.getNodeByName(client)).popen(cmd, shell=True)
            client_counter += 1

        # Gather statistics from the router:
        q_proc = rtr.popen('python tc_qdisc_implementation.py r-srv %s %d'
                           % (self.rtr_q_filename, self.interval_accuracy))

        # Wait until all commands are completed:
        for client, line in pmonitor(popens, timeoutms=1000):
            if client:
                print('<%s>: %s' % (client, line), )
        # Kill the server's iperf -s processes, the router's queue monitor and tcpdumps:
        sleep(5)
        for process in srv_procs:
            process.send_signal(SIGINT)
        q_proc.send_signal(SIGINT)
        # CLI(self.net)
        self.net.stop()


def clean_sim():
    cmd = "mn -c"
    os.system(cmd)


def create_sim_name(cwnd_algo_dict):
    name = ''
    if len(cwnd_algo_dict) == 0:
        return "WTF"
    for key, val in cwnd_algo_dict.items():
        name += "%d_%s_" % (val, key)
    return name[0:-1]


