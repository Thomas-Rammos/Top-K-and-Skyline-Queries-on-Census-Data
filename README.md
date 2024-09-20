# Top-K-and-Skyline-Queries-on-Census-Data
This project implements two algorithms for evaluating top-K join queries on demographic data from the US Census. The goal is to find the top-K pairs of individuals (one male and one female) with the highest combined instance weight, considering only pairs of individuals of the same age who are not married and are at least 18 years old.

# Part 1: Algorithm A - Top-K Join (HRJN)
The first part implements the HRJN (Hash Rank Join) algorithm. This algorithm reads lines alternately from two sorted files: males_sorted and females_sorted, storing valid records (those meeting the age and marital status criteria) in hash tables organized by age. The algorithm updates a threshold and maintains a max heap of the top-K results, returning results that are above the threshold.

- Code file: part1.py​(part1)
- Input: Two files: males_sorted and females_sorted, both sorted by instance weight, and an integer K specifying the number of top pairs to return.
- Output: The top-K pairs of records, along with their combined instance weight, printed in the format:
    - pair: <female_id>,<male_id> score: <weight>


# Part 2: Algorithm B - Alternative Top-K Join
The second part implements an alternative top-K join algorithm. This algorithm processes all valid records from males_sorted first, storing them in a hash table by age. It then reads valid records from females_sorted and joins them with records from the hash table. The top-K results are maintained in a min-heap until all records have been processed.

- Code file: part2.py​(part2)
- Input: Same as Part 1 (males_sorted, females_sorted, and an integer K).
- Output: The top-K pairs of records, printed in the same format as Part 1.


# Notes
- Both programs use the sorted files males_sorted and females_sorted which contain demographic records from the US Census, sorted by instance weight in descending order.
- Each file contains records where the first column is an ID and the subsequent columns are demographic attributes such as age, instance weight, and marital status​(Assignment3).
- The results for both algorithms should be identical for the same value of K.

# Performance Comparison
After running both algorithms with varying values of K, you can compare their performance in terms of execution time and the number of valid records read from each file.
