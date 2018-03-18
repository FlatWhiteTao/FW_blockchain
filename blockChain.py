# Blockchain class 
# 18/Mar/2018


import hashlib
import json
from time import time
from uuid import uuid4

class Blockchain(object):
	def __init__(self):
		self.chain = []
		self.current_transactions = []

		#Genesis block
		self.new_block(previous_hash=1, proof=100)

	def new_block(self, proof, previous_hash=None):
		# creates a new block and adds it to the chain
		# params:
		# proof: <int> generated by proof of work algorthim
		# previous_hash: <str> the hash value of the previous block
		# return: <dict> a new block
		
		block = {
			'index': len(self.chain) + 1,
			'timestamp': time(),
			'transactions': self.current_transactions,
			'proof': proof,
			'previous_hash': previous_hash or self.hash(self.chain[-1]),
		}

		# reset the current transactions
		self.current_transactions = []
		self.chain.append(block)
		return block 
		

	def new_transaction(self, sender, recipient, amount):
		# adds a new transaction to the list of transactions
		self.current_transactions.append({
			'sender': sender,
			'recipient': recipient,
			'amount': amount,
		})

		return self.last_block['index'] + 1

	@staticmethod
	def hash(block):
		# hash a block with SHA-256
		# params:
		# block: <dict> Block
		# return: <str> hash

		block_string = json.dumps(block, sort_keys=True).encode()
		return hashlib.sha256(block_string).hexdigest()
	
	@property
	def last_block(self):
		# returns the last block in the chain
		return self.chain[-1]


	def proof_of_work(self, last_proof):
		# PoW Algorthim:
		# find a new proof p` and last proof p: 
		# where hash(p`p) contains some leading zeros

		proof = 0
		while self.valid_proof(last_proof, proof) is False :
			proof +=1 

		return proof 

	@staticmethod
	def valid_proof(last_proof, proof):
		# valids the proof 
		# hash(p`p) == "0000........"

		guess = f'{last_proof}{proof}'.encode()
		guess_hash = hashlib.sha256(guess).hexdigest()
		return guess_hash[:4] == "0000"
