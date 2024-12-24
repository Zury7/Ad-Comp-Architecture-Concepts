class GShareBranchPredictor:
    def __init__(self, history_bits=8, counter_bits=2, table_size=16):
        self.history_bits = history_bits
        self.counter_bits = counter_bits
        self.table_size = table_size
        
        # Initialize global history register
        self.global_history = 0
        
        # Initialize pattern table with 2-bit saturating counters
        self.pattern_table = [0] * self.table_size
    
    def predict(self, branch_address):
        # XOR the global history with the lower bits of the branch address
        index = (self.global_history ^ branch_address) % self.table_size
        
        # Retrieve the 2-bit saturating counter from the pattern table
        counter = self.pattern_table[index]
        
        # Predict based on the counter value (predict taken if counter is 2 or higher)
        return counter >= 2
    
    def update(self, branch_address, taken):
        # XOR the global history with the lower bits of the branch address
        index = (self.global_history ^ branch_address) % self.table_size
        
        # Update the 2-bit saturating counter based on the branch outcome
        if taken:
            self.pattern_table[index] = min(self.pattern_table[index] + 1, (1 << self.counter_bits) - 1)
        else:
            self.pattern_table[index] = max(self.pattern_table[index] - 1, 0)
        
        # Update global history register (shift in the taken/not-taken result)
        self.global_history = ((self.global_history << 1) | taken) & ((1 << self.history_bits) - 1)
    
    def get_global_history(self):
        return self.global_history

#main 
predictor = GShareBranchPredictor(history_bits=8, counter_bits=2, table_size=16)
branch_outcomes = [True, False, True, True, False, False, True, True]  # Taken, Not taken, Taken, etc.
branch_addresses = [0, 4, 8, 16, 32, 64, 128, 256]  # Branch addresses (can be any values)
for i in range(len(branch_outcomes)):
        branch_address = branch_addresses[i]
        outcome = branch_outcomes[i]
        prediction = predictor.predict(branch_address)
        print(f"Prediction: {'Taken' if prediction else 'Not Taken'}, Actual Outcome: {'Taken' if outcome else 'Not Taken'}")
        predictor.update(branch_address, outcome)
