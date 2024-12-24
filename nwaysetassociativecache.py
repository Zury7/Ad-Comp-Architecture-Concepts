class NWaySetAssociativeCache:
    def __init__(self, cache_size=16, block_size=4, n=4):
        self.cache_size = cache_size
        self.block_size = block_size
        self.n = n  # Number of cache lines per set
        self.num_sets = cache_size // n
        self.cache = [[] for _ in range(self.num_sets)]

    def extract_parts(self, address):
        # Assuming address is a 32-bit integer
        block_offset_bits = 2  # log2(block size), for block size = 4 bytes
        index_bits = int(log2(self.num_sets))
        tag_bits = 32 - block_offset_bits - index_bits

        block_offset = address & ((1 << block_offset_bits) - 1)
        index = (address >> block_offset_bits) & ((1 << index_bits) - 1)
        tag = address >> (block_offset_bits + index_bits)

        return tag, index, block_offset

    def access_cache(self, address):
        tag, index, block_offset = self.extract_parts(address)

        # Check if the data is in any of the cache lines within the selected set
        set_cache = self.cache[index]

        for line in set_cache:
            if line[0] == tag:
                # Cache hit
                return "Cache Hit"
        
        # Cache miss
        if len(set_cache) < self.n:
            # If there is space in the set, add the new block
            set_cache.append((tag, block_offset))
        else:
            # Cache line is full, need to evict a line (typically use FIFO or LRU)
            set_cache.pop(0)
            set_cache.append((tag, block_offset))
        
        return "Cache Miss"

    def print_cache(self):
        print("Cache state:")
        for i, set_cache in enumerate(self.cache):
            print(f"Set {i}:")
            for line in set_cache:
                print(f"  Tag = {line[0]}, Block Offset = {line[1]}")

# Simulate n-way set associative cache
def simulate_cache(addresses, n=4):
    cache = NWaySetAssociativeCache(cache_size=16, block_size=4, n=n)

    for address in addresses:
        print(f"Accessing address {hex(address)}: {cache.access_cache(address)}")

    cache.print_cache()

#Test trail
addresses = [0x1F3, 0x2A7, 0x1F3, 0x3A8, 0x2A7, 0x3A8, 0x1F3]
simulate_cache(addresses, n=4)
