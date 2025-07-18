import os
import logging
from cryptography.hazmat.primitives import serialization

from blockchain.pos.lot import Lot
from blockchain.utils.helpers import BlockchainUtils

logger = logging.getLogger(__name__)

class ProofOfStake:
    def __init__(self):
        self.stakers = {}
        self.set_genesis_node_stake()

    def set_genesis_node_stake(self):
        genesis_key_path = "./blockchain/keys/genesis_public_key.pem"
        if os.path.exists(genesis_key_path):
            try:
                with open(genesis_key_path, "rb") as key_file:
                    key = serialization.load_pem_public_key(key_file.read())
                genesis_public_key = key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo,
                ).decode("utf-8")
                self.stakers[genesis_public_key] = 1
            except Exception as e:
                logger.warning({
                    "message": "Failed to load genesis key, using default staker",
                    "error": str(e),
                })
                self.stakers["GENESIS"] = 1
        else:
            logger.warning({
                "message": "Genesis key file not found, using default staker"
            })
            self.stakers["GENESIS"] = 1

    def update(self, public_key_string, stake):
        if public_key_string in self.stakers:
            self.stakers[public_key_string] += stake
        else:
            self.stakers[public_key_string] = stake

    def get(self, public_key_string):
        return self.stakers.get(public_key_string)

    def validator_lots(self, seed):
        lots = []
        for validator in self.stakers.keys():
            for stake in range(self.get(validator)):
                lots.append(Lot(validator, stake + 1, seed))
        return lots

    def winner_lot(self, lots, seed):
        winner_lot = None
        least_off_set = None
        reference_hash_integer_value = int(BlockchainUtils.hash(seed).hex(), 16)
        for lot in lots:
            lot_integer_value = int(lot.lot_hash(), 16)
            off_set = abs(lot_integer_value - reference_hash_integer_value)
            if least_off_set is None or off_set < least_off_set:
                least_off_set = off_set
                winner_lot = lot
        return winner_lot

    def forger(self, last_block_hash):
        lots = self.validator_lots(last_block_hash)
        winner_lot = self.winner_lot(lots, last_block_hash)
        if winner_lot:
            return winner_lot.public_key
        return "GENESIS"