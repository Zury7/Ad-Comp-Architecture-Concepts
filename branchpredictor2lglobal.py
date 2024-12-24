class TwoLevelGlobalBranchPredictor:
    def __init__(self, history_bits=8, counter_bits=2, table_size=16):
        self.history_bits = history_bits
        self.counter_bits = counter_bits
        self.table_size = table_size
        
        # Initialize global history register
        self.global_history = 0
        
        # Initialize global pattern table
        self.pattern_table = [0] * self.table_size
    
    def predict(self):
        # Use global history to index the pattern table
        pattern_index = self.global_history % self.table_size
        counter = self.pattern_table[pattern_index]
        
        # Predict based on the counter value
        return counter >= 2  # Predict taken if the counter is 2 or higher
    
    def update(self, taken):
        # Use global history to index the pattern table
        pattern_index = self.global_history % self.table_size
        
        # Update the 2-bit saturating counter
        if taken:
            self.pattern_table[pattern_index] = min(self.pattern_table[pattern_index] + 1, (1 << self.counter_bits) - 1)
        else:
            self.pattern_table[pattern_index] = max(self.pattern_table[pattern_index] - 1, 0)
        
        # Update global history register (shift in the taken/not-taken result)
        self.global_history = ((self.global_history << 1) | taken) & ((1 << self.history_bits) - 1)
    
    def get_global_history(self):
        return self.global_history

predictor = TwoLevelGlobalBranchPredictor(history_bits=8, counter_bits=2, table_size=16)
branch_outcomes = [True, False, True, True, False, False, True, True]  # Taken, Not taken, Taken, etc.
for outcome in branch_outcomes:
        branch_address = 0
        prediction = predictor.predict()
        print(f"Prediction: {'Taken' if prediction else 'Not Taken'}, Actual Outcome: {'Taken' if outcome else 'Not Taken'}")
        predictor.update(outcome)
