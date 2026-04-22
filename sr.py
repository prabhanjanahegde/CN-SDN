from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

def install_flow(connection, in_port, dst_ip, out_port):
    msg = of.ofp_flow_mod()
    msg.match.in_port = in_port
    msg.match.dl_type = 0x800       # IPv4
    msg.match.nw_dst = dst_ip
    msg.actions.append(of.ofp_action_output(port=out_port))
    connection.send(msg)

def _handle_ConnectionUp(event):
    log.info("Switch %s connected", event.dpid)

    # Example static routes
    install_flow(event.connection, 1, "10.0.0.2", 2)
    install_flow(event.connection, 2, "10.0.0.1", 1)

def launch():
    core.openflow.addListenerByName("ConnectionUp", _handle_ConnectionUp)