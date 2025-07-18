import json
import socket

from p2pnetwork.node import Node

from blockchain.p2p.peer_discovery_handler import PeerDiscoveryHandler
from blockchain.p2p.socket_connector import SocketConnector
from blockchain.utils.helpers import BlockchainUtils
from blockchain.utils.logger import logger


class SocketCommunication(Node):
    def __init__(self, ip, port):
        super(SocketCommunication, self).__init__(ip, port, None)
        self.peers = []
        self.peer_discovery_handler = PeerDiscoveryHandler(self)
        self.socket_connector = SocketConnector(ip, port)
        self.initialized = False

    def init_server(self):
        try:
            logger.info(
                {
                    "message": f"Node initialisation on port: {self.port}",
                    "node": {"id": self.id, "ip": self.host, "port": self.port},
                }
            )
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.bind((self.host, self.port))
            self.sock.settimeout(10.0)
            self.sock.listen(1)
            self.initialized = True
        except Exception as e:
            logger.error({
                "message": "Failed to initialize socket server",
                "error": str(e),
            })
            self.initialized = False
            raise

    def connect_to_first_node(self):
        try:
            port = self.socket_connector.first_node_config()["port"]
            ip = self.socket_connector.first_node_config()["ip"]
            if self.socket_connector.port != port:
                self.connect_with_node(ip, port)
        except Exception as e:
            logger.warning({
                "message": "Failed to connect to first node",
                "error": str(e),
            })

    def start_socket_communication(self, node):
        try:
            self.node = node
            self.start()
            self.peer_discovery_handler.start()
            self.connect_to_first_node()
        except Exception as e:
            logger.error({
                "message": "Failed to start socket communication",
                "error": str(e),
            })
            raise

    def inbound_node_connected(self, connected_node):
        self.peer_discovery_handler.handshake(connected_node)

    def outbound_node_connected(self, connected_node):
        self.peer_discovery_handler.handshake(connected_node)

    def node_message(self, connected_node, message):
        message = BlockchainUtils.decode(json.dumps(message))
        if message.message_type == "DISCOVERY":
            self.peer_discovery_handler.handle_message(message)
        elif message.message_type == "TRANSACTION":
            transaction = message.data
            self.node.handle_transaction(transaction)
        elif message.message_type == "BLOCK":
            block = message.data
            self.node.handle_block(block)
        elif message.message_type == "BLOCKCHAINREQUEST":
            self.node.handle_blockchain_request(connected_node)
        elif message.message_type == "BLOCKCHAIN":
            blockchain = message.data
            self.node.handle_blockchain(blockchain)

    def send(self, receiver, message):
        self.send_to_node(receiver, message)

    def broadcast(self, message):
        self.send_to_nodes(message)