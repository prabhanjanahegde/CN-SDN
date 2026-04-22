from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

mac_to_port = {}

def _handle_PacketIn(event):
    packet = event.parsed
    connection = event.connection

    src = packet.src
    dst = packet.dst
    in_port = event.port

    # learn source port
    mac_to_port[src] = in_port

    if dst in mac_to_port:
        out_port = mac_to_port[dst]

        # install static flow
        msg = of.ofp_flow_mod()
        msg.match.dl_dst = dst
        msg.actions.append(of.ofp_action_output(port=out_port))
        connection.send(msg)

        # forward current packet
        msg = of.ofp_packet_out()
        msg.data = event.ofp
        msg.actions.append(of.ofp_action_output(port=out_port))
        connection.send(msg)

        log.info("Installed flow %s -> port %s", dst, out_port)

    else:
        # flood first packet
        msg = of.ofp_packet_out()
        msg.data = event.ofp
        msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
        connection.send(msg)

def launch():
    core.openflow.addListenerByName("PacketIn", _handle_PacketIn)
