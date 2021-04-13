import time 
from hashlib import sha256  
import json


class Block():
    def __init__(self, index, data, timestamp, previous_hash, hashes = 0):
        self.index = index
        self.data = data
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.hashes = hashes
        
    def hash_block(self):
        block_string = json.dumps(self.__dict__, sort_keys = True)    
        hash_value = sha256(block_string.encode()).hexdigest()
        
        return hash_value

    
class Blockchain():
    def __init__(self, data):
        self.chain = []   
        self.chain_two = []
        self.chain_data = []
        self.genesis_block(data)

    def genesis_block(self, data):
        genesis = Block(index = 0, data = data, timestamp = time.ctime(int(time.time())), 
                        previous_hash = 0, hashes = 0)
        genesisBlockHash = self.proof_of_work(genesis)
        self.chain_two.append(genesis)
        self.chain.append(genesisBlockHash)

    @property
    def last_block_hash(self):   
        return self.chain[-1]
    
    @property
    def last_block(self):   
       return self.chain_two[-1]
             
    def proof_of_work(self, block):
        block.hashes = 0
        difficulty_level = 1
        computed_hash = block.hash_block()
        
        while not computed_hash.startswith('0' * difficulty_level):
            block.hashes += 1
            computed_hash = block.hash_block()
            
        return computed_hash

    def add_block(self, data_input):
        last_block = self.last_block
        last_block_hash = self.last_block_hash
        
        new_block = Block(index = int(last_block.index + 1), data = data_input, timestamp = time.ctime(int(time.time())), 
                                      previous_hash = last_block_hash, hashes = last_block.hashes + 1)

        consensus = self.proof_of_work(new_block)
        self.chain_two.append(new_block)
        self.chain.append(consensus)

    def print_lastblock(self):
        last_block = self.last_block
        last_block_hash = self.last_block_hash
            
        print("------------- \nLastest Block: \n------------- \nHash: ", last_block_hash, 
              "\nIndex: ", last_block.index,"\nTime: ", last_block.timestamp, 
              "\nData: ", last_block.data, "\nHashes: ", last_block.hashes,
              "\nPrevious Block Hash: ", last_block.previous_hash, "\n-------------")
    
    def print_chain(self):
        print("Current Chain State: ", self.chain)
        
    def print_block(self, index):
        block = self.chain_two[index]
        block_hash = self.chain[index]
            
        print("------------- \nBlock", index, " \n------------- \nHash: ", block_hash, 
              "\nIndex: ", block.index,"\nTime: ", block.timestamp, 
              "\nData: ", block.data, "\nHashes: ", block.hashes, 
              "\nPrevious Block Hash: ", block.previous_hash, "\n-------------")
    
    def print_all(self):
        for i in range(len(self.chain)):
            block = self.chain_two[i]
            block_hash = self.chain[i]
            print("------------- \nBlock", i, " \n------------- \nHash: ", block_hash, 
                  "\nIndex: ", block.index,"\nTime: ", block.timestamp, 
                  "\nData: ", block.data, "\nHashes: ", block.hashes,
                  "\nPrevious Block Hash: ", block.previous_hash)
    
b = Blockchain("Genesis Block")
b.add_block("Block One!")
b.add_block("Block Two!")

b.print_all()
