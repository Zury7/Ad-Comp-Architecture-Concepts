class GSkewBranchPredictor:
    def __init__(self, global_history_bits=8, local_history_bits=8, counter_bits=2, table_size=16):
        self.global_history_bits = global_history_bits
        self.local_history_bits = local_history_bits
        self.counter_bits = counter_bits
        self.table_size = table_size
        
        # Initialize global and local history registers
        self.global_history = 0
        self.local_history = {}
        
        # Initialize pattern tables for global and local histories
        self.global_pattern_table = [0] * self.table_size
        self.local_pattern_table = [0] * self.table_size
    
    def predict(self, branch_address):
        # Extract the lower bits of the branch address for local history
        local_history_index = branch_address % self.table_size
        
        # Extract part of the global history and XOR it with the branch address for skewing
        skewed_index = (self.global_history ^ branch_address) % self.table_size
        
        # Retrieve 2-bit saturating counters for both global and local history
        global_counter = self.global_pattern_table[skewed_index]
        local_counter = self.local_pattern_table[local_history_index]
        
        # Make a prediction: If either of the counters is 2 or higher, predict taken
        return (global_counter >= 2) or (local_counter >= 2)
    
    def update(self, branch_address, taken):
        # Extract the lower bits of the branch address for local history
        local_history_index = branch_address % self.table_size
        
        # Extract part of the global history and XOR it with the branch address for skewing
        skewed_index = (self.global_history ^ branch_address) % self.table_size
        
        # Update the 2-bit saturating counters based on the actual outcome
        if taken:
            self.global_pattern_table[skewed_index] = min(self.global_pattern_table[skewed_index] + 1, (1 << self.counter_bits) - 1)
            self.local_pattern_table[local_history_index] = min(self.local_pattern_table[local_history_index] + 1, (1 << self.counter_bits) - 1)
        else:
            self.global_pattern_table[skewed_index] = max(self.global_pattern_table[skewed_index] - 1, 0)
            self.local_pattern_table[local_history_index] = max(self.local_pattern_table[local_history_index] - 1, 0)
        
        # Update the global and local history registers
        self.global_history = ((self.global_history << 1) | taken) & ((1 << self.global_history_bits) - 1)
        
        # Update local history for the specific branch address
        if branch_address not in self.local_history:
            self.local_history[branch_address] = 0
        self.local_history[branch_address] = ((self.local_history[branch_address] << 1) | taken) & ((1 << self.local_history_bits) - 1)

#main
predictor = GSkewBranchPredictor(global_history_bits=8, local_history_bits=8, counter_bits=2, table_size=16)
branch_outcomes = [True, False, True, True, False, False, True, True]  # Taken, Not taken, Taken, etc.
branch_addresses = [0, 4, 8, 16, 32, 64, 128, 256]  # Branch addresses (can be any values)
for i in range(len(branch_outcomes)):
        branch_address = branch_addresses[i]
        outcome = branch_outcomes[i]
        prediction = predictor.predict(branch_address)
        print(f"Prediction: {'Taken' if prediction else 'Not Taken'}, Actual Outcome: {'Taken' if outcome else 'Not Taken'}")
        predictor.update(branch_address, outcome)
