# RAMMOS THOMAS
# AM : 4583

import heapq
import time
import sys

# Parses a line from the file and returns a dictionary with the relevant fields
def parse_record(line):
    fields = line.split(", ")  # Split the line by comma and space
    return {
        'id': int(fields[0]),  # Convert and store the id as an integer
        'age': int(fields[1]),  # Convert and store the age as an integer
        'instance_weight': float(fields[25]),  # Convert and store the instance_weight as a float
        'marital_status': fields[8]  # Store the marital status as a string
    }

# Checks if a record is eligible based on age and marital status
def is_eligible(record):
    return record['age'] >= 18 and not record['marital_status'].startswith("Married")

# Implements the top-k join algorithm
def top_k_join(k, males_filepath, females_filepath):
    # Open both files and ensure they are properly closed after processing
    with open(males_filepath) as males_file, open(females_filepath) as females_file:
        males_hash = {}  # Dictionary to store valid male records by age
        females_hash = {}  # Dictionary to store valid female records by age
        heap = []  # Initialize a heap for the top-k join results

        male_valid_count = 0  # Counter for valid male records
        female_valid_count = 0  # Counter for valid female records

        # Parse and store valid male records
        for line in males_file:
            record = parse_record(line)  # Parse the line into a record
            if is_eligible(record):  # Check if the record is valid
                male_valid_count += 1  # Increment the count of valid male records
                age_group = record['age']  # Get the age group of the record
                if age_group not in males_hash:
                    males_hash[age_group] = []  # Initialize the list for this age group if not present
                males_hash[age_group].append(record)  # Add the record to the hash table

        # Parse and store valid female records and compute the top-k join
        for line in females_file:
            record = parse_record(line)  # Parse the line into a record
            if is_eligible(record):  # Check if the record is valid
                female_valid_count += 1  # Increment the count of valid female records
                age_group = record['age']  # Get the age group of the record
                if age_group not in females_hash:
                    females_hash[age_group] = []  # Initialize the list for this age group if not present
                females_hash[age_group].append(record)  # Add the record to the hash table
                if age_group in males_hash:  # If there are matching male records
                    for male_record in males_hash[age_group]:
                        combined_weight = male_record['instance_weight'] + record['instance_weight']  # Compute the combined weight
                        if len(heap) < k:
                            heapq.heappush(heap, (combined_weight, (male_record['id'], record['id'])))  # Add to the heap if it's not full
                        elif combined_weight > heap[0][0]:
                            heapq.heappushpop(heap, (combined_weight, (male_record['id'], record['id'])))  # Replace the smallest element if the new score is higher

    # Return the sorted results and the counts of valid records
    return sorted(heap, key=lambda x: -x[0]), male_valid_count, female_valid_count

def main():
    if len(sys.argv) < 2:
        print("Usage: python part2.py <K>")
        return

    k = int(sys.argv[1])  # Get the value of K from the command line argument
    males_filepath = r"C:\Users\Thomas\Desktop\mamoulis3\males sorted\males_sorted"
    females_filepath = r"C:\Users\Thomas\Desktop\mamoulis3\females sorted\females_sorted"
    
    start_time = time.time()
    top_k_results, male_valid_count, female_valid_count = top_k_join(k, males_filepath, females_filepath)
    end_time = time.time()

    # Print the results in the desired format
    for weight, (male_id, female_id) in top_k_results:
        print(f'pair: {female_id},{male_id} score: {weight:.2f}')  # Print the results with changed order

    # Print the execution time and the counts of valid records
    print(f'Time taken: {end_time - start_time:.2f} seconds')
    print(f"Valid male records: {male_valid_count}")
    print(f"Valid female records: {female_valid_count}")

if __name__ == "__main__":
    main()
