server_0 iperf3 -i 0.1 -s -p 5001 > c0_s0.log &
server_0 tcpdump -n 'tcp port 5001' -w c0.pcap &
server_0 iperf3 -i 0.1 -s -p 5002 > c1_s0.log &
server_0 tcpdump -n 'tcp port 5002' -w c1.pcap &
server_0 iperf3 -i 0.1 -s -p 5003 > c2_s0.log &
server_0 tcpdump -n 'tcp port 5003' -w c2.pcap &
server_0 iperf3 -i 0.1 -s -p 5004 > c3_s0.log &
server_0 tcpdump -n 'tcp port 5004' -w c3.pcap &
server_0 iperf3 -i 0.1 -s -p 5005 > c4_s0.log &
server_0 tcpdump -n 'tcp port 5005' -w c4.pcap &
server_1 iperf3 -i 0.1 -s -p 5006 > c5_s0.log &
server_1 tcpdump -n 'tcp port 5006' -w c5.pcap &
server_1 iperf3 -i 0.1 -s -p 5007 > c6_s0.log &
server_1 tcpdump -n 'tcp port 5007' -w c6.pcap &
server_1 iperf3 -i 0.1 -s -p 5008 > c7_s0.log &
server_1 tcpdump -n 'tcp port 5008' -w c7.pcap &
server_1 iperf3 -i 0.1 -s -p 5009 > c8_s0.log &
server_1 tcpdump -n 'tcp port 5009' -w c8.pcap &
server_1 iperf3 -i 0.1 -s -p 5010 > c9_s0.log &
server_1 tcpdump -n 'tcp port 5010' -w c9.pcap &
client_0 sleep 0.2; iperf3 -i 0.1 -c 192.168.1.100 -p 5001 -t 180 -B 192.168.1.1 --cport 7001 > c0.log &
client_1 sleep 0.2; iperf3 -i 0.1 -c 192.168.1.100 -p 5002 -t 180 -B 192.168.1.2 --cport 7002 > c1.log &
client_2 sleep 0.2; iperf3 -i 0.1 -c 192.168.1.100 -p 5003 -t 180 -B 192.168.1.3 --cport 7003 > c2.log &
client_3 sleep 0.2; iperf3 -i 0.1 -c 192.168.1.100 -p 5004 -t 180 -B 192.168.1.4 --cport 7004 > c3.log &
client_4 sleep 0.2; iperf3 -i 0.1 -c 192.168.1.100 -p 5005 -t 180 -B 192.168.1.5 --cport 7005 > c4.log &
client_5 sleep 0.2; iperf3 -i 0.1 -c 192.168.1.101 -p 5006 -t 180 -B 192.168.1.6 --cport 7006 > c5.log &
client_6 sleep 0.2; iperf3 -i 0.1 -c 192.168.1.101 -p 5007 -t 180 -B 192.168.1.7 --cport 7007 > c6.log &
client_7 sleep 0.2; iperf3 -i 0.1 -c 192.168.1.101 -p 5008 -t 180 -B 192.168.1.8 --cport 7008 > c7.log &
client_8 sleep 0.2; iperf3 -i 0.1 -c 192.168.1.101 -p 5009 -t 180 -B 192.168.1.9 --cport 7009 > c8.log &
client_9 sleep 0.2; iperf3 -i 0.1 -c 192.168.1.101 -p 5010 -t 180 -B 192.168.1.10 --cport 7010 > c9.log &
client_9 sleep 185
