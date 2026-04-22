from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

def install_rule(connection, dst_ip, out_port):
    msg = of.ofp_flow_mod()
    msg.match.dl_type = 0x800      # IPv4
    msg.match.nw_dst = dst_ip
    msg.actions.append(of.ofp_action_output(port=out_port))
    connection.send(msg)

def _handle_ConnectionUp(event):
    log.info("Switch connected: %s", event.connection)

    # h1 = 10.0.0.1 on port 1
    # h2 = 10.0.0.2 on port 2

    install_rule(event.connection, "10.0.0.1", 1)
    install_rule(event.connection, "10.0.0.2", 2)

def launch():
    core.openflow.addListenerByName("ConnectionUp", _handle_ConnectionUp)
