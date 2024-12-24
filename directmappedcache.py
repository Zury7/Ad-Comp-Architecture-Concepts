class DirectMappedCache:
    def __init__(self, cache_size=16, block_size=4):
        self.cache_size = cache_size
        self.block_size = block_size
        self.cache = [None] * cache_size  # Cache initialized to None (empty cache lines)

    def extract_parts(self, address):
        # Assuming address is a 32-bit integer
        block_offset_bits = 2  # log2(block size), for block size = 4 bytes
        index_bits = 4  # log2(cache size), for cache size = 16 blocks
        tag_bits = 32 - block_offset_bits - index_bits

        # Extract the tag, index, and block offset from the address
        block_offset = address & ((1 << block_offset_bits) - 1)
        index = (address >> block_offset_bits) & ((1 << index_bits) - 1)
        tag = address >> (block_offset_bits + index_bits)

        return tag, index, block_offset

    def access_cache(self, address):
        tag, index, block_offset = self.extract_parts(address)

        # Check if the data in the cache line matches the tag (cache hit or miss)
        cache_line = self.cache[index]
        if cache_line is None:
            # Cache miss, we load the data into the cache line
            self.cache[index] = (tag, block_offset)
            return "Cache Miss"
        elif cache_line[0] == tag:
            # Cache hit, data is in the correct cache line
            return "Cache Hit"
        else:
            # Cache miss, we replace the cache line
            self.cache[index] = (tag, block_offset)
            return "Cache Miss"

    def print_cache(self):
        print("Cache state:")
        for i, cache_line in enumerate(self.cache):
            if cache_line is None:
                print(f"Index {i}: Empty")
            else:
                print(f"Index {i}: Tag = {cache_line[0]}, Block Offset = {cache_line[1]}")

# Simulate cache access with a 32-bit address
def simulate_cache(addresses):
    cache = DirectMappedCache()

    for address in addresses:
        print(f"Accessing address {hex(address)}: {cache.access_cache(address)}")

    cache.print_cache()

#main
addresses = [0x1F3, 0x2A7, 0x1F3, 0x3A8, 0x2A7, 0x3A8, 0x1F3]
simulate_cache(addresses)
