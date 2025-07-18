import copy
import logging
import time

from api.main import NodeAPI
from blockchain.blockchain import Blockchain
from blockchain.p2p.message import Message
from blockchain.p2p.socket_communication import SocketCommunication
from blockchain.transaction.transaction_pool import TransactionPool
from blockchain.transaction.wallet import Wallet
from blockchain.utils.helpers import BlockchainUtils
from blockchain.utils.logger import logger


class Node:
    def __init__(self, ip, port, key=None):
        self.p2p = None
        self.ip = ip
        self.port = port
        self.transaction_pool = TransactionPool()
        self.wallet = Wallet()
        self.blockchain = Blockchain()
        try:
            if key:
                self.wallet.from_key(key)
        except Exception as e:
            logger.warning({
                "message": "Failed to load key file, using default wallet",
                "error": str(e),
            })
            self.wallet.generate_key_pair()

    def start_p2p(self):
        try:
            print("Creating SocketCommunication instance...")
            self.p2p = SocketCommunication(self.ip, self.port)
            print(f"SocketCommunication created with IP: {self.ip}, Port: {self.port}")
            time.sleep(2)  # Small delay between component initializations
            print("Starting socket communication...")
            self.p2p.start_socket_communication(self)
            print("Socket communication started")
            time.sleep(2)  # Small delay after starting socket communication
        except Exception as e:
            logger.error({
                "message": "Failed to start P2P communication",
                "error": str(e),
            })
            raise

    def start_node_api(self, api_port):
        try:
            print(f"Creating NodeAPI instance on port {api_port}...")
            self.api = NodeAPI()
            time.sleep(1)  # Small delay before injecting node
            print("Injecting node into API...")
            self.api.inject_node(self)
            time.sleep(1)  # Small delay before starting API
            print(f"Starting API server on port {api_port}...")
            self.api.start(self.ip, api_port)
            print("API server started")
        except Exception as e:
            logger.error({
                "message": "Failed to start API server",
                "error": str(e),
            })
            raise

    def handle_transaction(self, transaction):
        data = transaction.payload()
        signature = transaction.signature
        signer_public_key = transaction.sender_public_key
        signature_valid = Wallet.signature_valid(data, signature, signer_public_key)
        transaction_exists = self.transaction_pool.transaction_exists(transaction)
        transaction_in_block = self.blockchain.transaction_exists(transaction)

        if not transaction_exists and not transaction_in_block and signature_valid:
            self.transaction_pool.add_transaction(transaction)
            message = Message(self.p2p.socket_connector, "TRANSACTION", transaction)
            self.p2p.broadcast(BlockchainUtils.encode(message))

            forging_required = self.transaction_pool.forging_required()
            if forging_required:
                self.forge()

    def handle_block(self, block):
        forger = block.forger
        block_hash = block.payload()
        signature = block.signature

        block_count_valid = self.blockchain.block_count_valid(block)
        last_block_hash_valid = self.blockchain.last_block_hash_valid(block)
        forger_valid = self.blockchain.forger_valid(block)
        transactions_valid = self.blockchain.transactions_valid(block.transactions)
        signature_valid = Wallet.signature_valid(block_hash, signature, forger)

        if not block_count_valid:
            self.request_chain()

        if (
            last_block_hash_valid
            and forger_valid
            and transactions_valid
            and signature_valid
        ):
            self.blockchain.add_block(block)
            self.transaction_pool.remove_from_pool(block.transactions)
            message = Message(self.p2p.socket_connector, "BLOCK", block)
            self.p2p.broadcast(BlockchainUtils.encode(message))

    def request_chain(self):
        message = Message(self.p2p.socket_connector, "BLOCKCHAINREQUEST", None)
        encoded_message = BlockchainUtils.encode(message)
        self.p2p.broadcast(encoded_message)

    def handle_blockchain_request(self, requesting_node):
        message = Message(self.p2p.socket_connector, "BLOCKCHAIN", self.blockchain)
        encoded_message = BlockchainUtils.encode(message)
        self.p2p.send(requesting_node, encoded_message)

    def handle_blockchain(self, blockchain):
        local_blockchain_copy = copy.deepcopy(self.blockchain)
        local_block_count = len(local_blockchain_copy.blocks)
        received_chain_block_count = len(blockchain.blocks)
        if local_block_count < received_chain_block_count:
            for block_number, block in enumerate(blockchain.blocks):
                if block_number >= local_block_count:
                    local_blockchain_copy.add_block(block)
                    self.transaction_pool.remove_from_pool(block.transactions)
            self.blockchain = local_blockchain_copy

    def forge(self):
        forger = self.blockchain.next_forger()
        if forger == self.wallet.public_key_string():
            block = self.blockchain.create_block(
                self.transaction_pool.transactions, self.wallet
            )
            logger.info(
                {
                    "message": "Next forger chosen",
                    "block": block.block_count,
                    "whoami": self.p2p,
                }
            )
            self.transaction_pool.remove_from_pool(self.transaction_pool.transactions)
            message = Message(self.p2p.socket_connector, "BLOCK", block)
            self.p2p.broadcast(BlockchainUtils.encode(message))