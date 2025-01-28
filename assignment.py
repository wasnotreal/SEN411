from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.link import TCLink
from mininet.cli import CLI

def setup_topology():
    """Setup a custom tree-based topology."""
    # Initialize Mininet with the RemoteController and TCLink
    net = Mininet(controller=RemoteController, link=TCLink)

    # Add the controller
    controller = net.addController(
        'controller',
        controller=RemoteController,
        ip='10.0.2.15',
        port=6633
    )

    # Create switches
    switches = {
        'core': net.addSwitch('s1'),
        'agg1': net.addSwitch('s2'),
        'agg2': net.addSwitch('s3'),
        'access1': net.addSwitch('s4'),
        'access2': net.addSwitch('s5'),
        'access3': net.addSwitch('s6'),
        'access4': net.addSwitch('s7')
    }

    # Add links between core and aggregation switches
    net.addLink(switches['core'], switches['agg1'], bw=50, delay='2ms', use_htb=True)
    net.addLink(switches['core'], switches['agg2'], bw=50, delay='2ms', use_htb=True)

    # Add links between aggregation and access switches
    net.addLink(switches['agg1'], switches['access1'], bw=30, delay='5ms', use_htb=True)
    net.addLink(switches['agg1'], switches['access2'], bw=30, delay='5ms', use_htb=True)
    net.addLink(switches['agg2'], switches['access3'], bw=30, delay='5ms', use_htb=True)
    net.addLink(switches['agg2'], switches['access4'], bw=30, delay='5ms', use_htb=True)

    # Define hosts with their respective IP addresses
    hosts = [
        net.addHost(f'h{i}', ip=f'10.0.{i // 5}.{i % 5 + 1}/24') for i in range(1, 9)
    ]

    # Add links between hosts and access switches
    host_to_access_mapping = {
        0: 'access1', 1: 'access1',
        2: 'access2', 3: 'access2',
        4: 'access3', 5: 'access3',
        6: 'access4', 7: 'access4'
    }
    for i, host in enumerate(hosts):
        net.addLink(host, switches[host_to_access_mapping[i]])

    # Start the network
    net.start()
    print("Custom tree-based topology is running. Use 'pingall' in the CLI to test connectivity.")

    # Test connectivity
    net.pingAll()

    # Launch CLI
    CLI(net)

    # Stop the network
    net.stop()

if __name__ == '__main__':
    setup_topology()
