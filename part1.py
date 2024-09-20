# RAMMOS THOMAS
# AM : 4583

import heapq
import time
import sys

def parse_line(line):
    parts = line.strip().split(", ")  # Split the line by comma and space
    try:
        instance_weight = float(parts[25])  # Attempt to parse the instance_weight
    except ValueError:
        return None, f"Invalid instance_weight value: {parts[25]}"  # Return an error if parsing fails
    return {
        'id': int(parts[0]),  # Parse and return the id
        'age': int(parts[1]),  # Parse and return the age
        'instance_weight': instance_weight,  # Return the parsed instance_weight
        'marital_status': parts[8]  # Return the marital status
    }, None

def is_valid_record(record):
    # Check if the record is valid based on age and marital status
    return record['age'] >= 18 and not record['marital_status'].startswith("Married")

class HRJN:
    def __init__(self, males_file, females_file, f):
        self.males_file = males_file
        self.females_file = females_file
        self.f = f
        self.Q = []
        heapq.heapify(self.Q)  # Initialize the priority queue
        self.males_hash = {}  # Initialize the hash table for males
        self.females_hash = {}  # Initialize the hash table for females
        self.threshold = float('-inf')  # Initialize the threshold
        self.male_iter = None
        self.female_iter = None
        self.L_top = self.R_top = float('-inf')
        self.L_bottom = self.R_bottom = float('inf')
        self.next_is_male = True  # Alternate between male and female

    def open(self):
        self.male_iter = iter(open(self.males_file))  # Open the male file and create an iterator
        self.female_iter = iter(open(self.females_file))  # Open the female file and create an iterator

    def get_next(self):
        while True:
            if self.Q and -self.Q[0][0] >= self.threshold:  # Check if the top of the max heap meets the threshold
                result = heapq.heappop(self.Q)  # Pop the top of the heap
                if -result[0] >= self.threshold:  # Adjust for max heap and check if it meets the threshold
                    yield -result[0], result[1]  # Yield the result

            tuple_record = None
            if self.next_is_male:
                tuple_record = self._get_next_tuple(self.male_iter, self.males_hash)  # Get the next valid male tuple
                self.next_is_male = False
            else:
                tuple_record = self._get_next_tuple(self.female_iter, self.females_hash)  # Get the next valid female tuple
                self.next_is_male = True

            if tuple_record:
                record = tuple_record
                if not self.next_is_male:  # If next should be female, current was male
                    self.L_top = max(self.L_top, record['instance_weight'])  # Update L_top
                    self.L_bottom = min(self.L_bottom, record['instance_weight'])  # Update L_bottom
                    self._update_queue(record, self.females_hash)  # Update the queue with the current record
                else:
                    self.R_top = max(self.R_top, record['instance_weight'])  # Update R_top
                    self.R_bottom = min(self.R_bottom, record['instance_weight'])  # Update R_bottom
                    self._update_queue(record, self.males_hash)  # Update the queue with the current record

                self.threshold = max(self.f(self.L_top, self.R_bottom), self.f(self.L_bottom, self.R_top))  # Update the threshold
                # print(f"Updated threshold: {self.threshold}")

                while self.Q and -self.Q[0][0] >= self.threshold:  # Check if the top of the max heap meets the threshold
                    result = heapq.heappop(self.Q)  # Pop the top of the heap
                    if -result[0] >= self.threshold:  # Adjust for max heap and check if it meets the threshold
                        yield -result[0], result[1]  # Yield the result
            else:
                print("No more valid records available.")
                return

    def _get_next_tuple(self, iter, hash_table):
        try:
            while True:
                line = next(iter)  # Get the next line from the file
                record, error = parse_line(line)  # Parse the line
                if error:
                    print(f"Error or end of file: {error}")
                    continue  # Skip invalid records
                if is_valid_record(record):
                    record_minimal = {
                        'id': record['id'],  # Include only necessary fields
                        'age': record['age'],
                        'instance_weight': record['instance_weight']
                    }
                    age = record['age']
                    if age not in hash_table:
                        hash_table[age] = []  # Initialize the list for this age if not present
                    hash_table[age].append(record_minimal)  # Add the record to the hash table
                    return record_minimal  # Return the minimal record
        except StopIteration:
            return None
    
    def _update_queue(self, record, other_hash_table):
        age = record['age']
        if age in other_hash_table:
            for other_record in other_hash_table[age]:
                score = record['instance_weight'] + other_record['instance_weight']  # Calculate the score
                heapq.heappush(self.Q, (-score, (other_record['id'], record['id'])))  # Add to max heap

def main():
    if len(sys.argv) < 2:
        print("Usage: python part1.py <K>")
        return

    k = int(sys.argv[1])  # Get the value of K from the command line argument
    males_path = r"C:\Users\Thomas\Desktop\mamoulis3\males sorted\males_sorted"
    females_path = r"C:\Users\Thomas\Desktop\mamoulis3\females sorted\females_sorted"
    start_time = time.time()
    
    def f(x, y):
        return x + y
    
    hrjn = HRJN(males_path, females_path, f)
    hrjn.open()
    
    result_gen = hrjn.get_next()
    
    results = []
    for _ in range(k):
        result = next(result_gen, None)  # Get the next result
        if result:
            results.append(result)  # Append the result to the results list
        else:
            print("No more results available.")
            break
    
    end_time = time.time()

    for score, (male_id, female_id) in results:
        print(f'pair: {female_id},{male_id} score: {score:.2f}')  # Print the results with changed order

    print(f'Time taken: {(end_time - start_time)*1000:.2f} ms')
    print(f"Valid male records read: {sum(len(v) for v in hrjn.males_hash.values())}")  # Print the size of males_hash
    print(f"Valid female records read: {sum(len(v) for v in hrjn.females_hash.values())}")  # Print the size of females_hash

if __name__ == "__main__":
    main()
