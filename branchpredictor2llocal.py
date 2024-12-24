class TwoLevelLocalBranchPredictor:
    def __init__(self, history_bits=8, counter_bits=2):
        self.history_bits = history_bits
        self.counter_bits = counter_bits
        
        # Initialize history register and pattern table
        self.history = 0
        self.pattern_table = {}
        
    def predict(self, branch_address):
        # Extract the relevant history bits
        history_mask = (1 << self.history_bits) - 1
        local_history = self.history & history_mask
        
        # Check if this local history has a prediction stored
        if local_history in self.pattern_table:
            counter = self.pattern_table[local_history]
        else:
            # If no prediction is found, assume a 'not taken' prediction (counter = 0)
            counter = 0
        
        # Predict based on the current counter value
        return counter >= 2  # Predict taken if the counter is 2 or higher
    
    def update(self, branch_address, taken):
        # Extract the relevant history bits
        history_mask = (1 << self.history_bits) - 1
        local_history = self.history & history_mask
        
        # Update the prediction counter for this local history
        if local_history not in self.pattern_table:
            self.pattern_table[local_history] = 0
        
        # Update the 2-bit saturating counter based on branch outcome
        if taken:
            self.pattern_table[local_history] = min(self.pattern_table[local_history] + 1, (1 << self.counter_bits) - 1)
        else:
            self.pattern_table[local_history] = max(self.pattern_table[local_history] - 1, 0)
        
        # Update history register (shift in the taken/ not-taken result)
        self.history = ((self.history << 1) | taken) & ((1 << self.history_bits) - 1)
        
    def get_history(self):
        return self.history


#main
predictor = TwoLevelLocalBranchPredictor(history_bits=8, counter_bits=2)
branch_outcomes = [True, False, True, True, False, False, True, True]  # Taken, Not taken, Taken, etc.
    
for outcome in branch_outcomes:
    branch_address = 0
    prediction = predictor.predict(branch_address)
    print(f"Prediction: {'Taken' if prediction else 'Not Taken'}, Actual Outcome: {'Taken' if outcome else 'Not Taken'}")
    predictor.update(branch_address, outcome)
