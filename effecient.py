# Running Example: python3 basic.py SampleTestCases\input3.txt output.txt
import os
import sys
import time
import psutil
#### PART 1: DEFINE CONSTANTS ####
MAXIMUM_DP_AREA = 100
DELTA = 30
ALPHA = {"AA": 0, "AC": 110, "AG": 48, "AT": 94,
         "CA": 110, "CC": 0, "CG": 118, "CT": 48,
         "GA": 48, "GC": 118, "GG": 0, "GT": 110,
         "TA": 94, "TC": 48, "TG": 110, "TT": 0,
         }

#### PART 2: FILE HANDLING ####

# read in file names from command line
i_file_path = sys.argv[1]
o_file_path = sys.argv[2]

# generate input strings from file
currString = ""
X = ""
Y = ""
with open(i_file_path, 'r') as file:
    for line in file:
        line = line.strip()
        # this line is a digit
        if(line.isdigit()):
            idx = int(line)
            if(currString == "X"):
                X = X[:idx+1] + X + X[idx+1:]
            else:
                Y = Y[:idx+1] + Y + Y[idx+1:]
        # this line is a string 
        else: 
            if(currString == ""):
                currString = "X"
                X = line
            else:
                currString = "Y"
                Y = line

#### PART 3: DYNAMIC PROGRAMMING ####
# Taken from basic.py
def base_case_DP(x, y):
    OPT = []
    process = psutil.Process()
    memory_used = 0
    for i in range(len(x)+1):
        arr = []
        for j in range(len(y)+1):
            arr.append(0)
        OPT.append(arr)

    # fill in row 0 and col 0
    for i in range(len(x)+1):
        OPT[i][0] = i*DELTA
    for j in range(len(y)+1):
        OPT[0][j] = j*DELTA

    # fill in DP array
    for i in range(1, len(x) + 1):
        for j in range(1, len(y) + 1):
            val_1 = OPT[i-1][j-1] + ALPHA[x[i-1]+y[j-1]] # we do x[i-1] since this loop goes from 1 to len(x) + 1 (it is shifted by 1)
            val_2 = OPT[i-1][j] + DELTA
            val_3 = OPT[i][j-1] + DELTA
            OPT[i][j] = min(val_1, val_2, val_3)
    
    # work backwards to see where score came from and to figure out alignments
    first_string_alignment = ""
    second_string_alignment = ""

    i = len(x)
    j = len(y)

    while not((i == 0) and (j == 0)):
        if i > 0 and j > 0:
            val_1 = OPT[i-1][j-1] + ALPHA[x[i-1]+y[j-1]] # we do x[i-1] since this loop goes from 1 to len(x) + 1 (it is shifted by 1)
        else:
            val_1 = 9999999999999
        if i > 0:
            val_2 = OPT[i-1][j] + DELTA
        else:
            val_2 = 9999999999999

        if j > 0:
            val_3 = OPT[i][j-1] + DELTA
        else:
            val_3 = 9999999999999
        if i > 0 and j > 0 and OPT[i][j] == val_1:
            first_string_alignment += x[i-1]
            second_string_alignment += y[j-1]
            i -= 1
            j -= 1
        elif i > 0 and OPT[i][j] == val_2:
            first_string_alignment += x[i-1]
            second_string_alignment += "_"
            i -= 1
        else:
            first_string_alignment += "_"
            second_string_alignment += y[j-1]
            j -= 1

    # reverse the strings to reflect forward order
    first_string_alignment = first_string_alignment[::-1]
    second_string_alignment = second_string_alignment[::-1]
    memory_info = process.memory_info()
    memory_used = max(memory_used, memory_info.rss)
    return first_string_alignment, second_string_alignment, memory_used


def compute_split_costs(x, y):
    OPT = []
    for j in range(len(y) + 1):
        OPT.append(j * DELTA)
    for i in range(1, len(x) + 1):
        # Each iteration we want to basically calculate the next row of our table, removing the old row
        curr = [0] * (len(y) + 1)
        curr[0] = i * DELTA
        for j in range(1, len(y) + 1):
            # Same logic as the basic version
            val_1 = OPT[j-1] + ALPHA[x[i-1] + y[j-1]]
            val_2 = OPT[j] + DELTA
            val_3 = curr[j-1] + DELTA
            curr[j] = min(val_1, val_2, val_3)
        OPT = curr
    return OPT

def divide_and_conquer(x, y):
    process = psutil.Process()
    memory_used = 0
    if len(x) == 0:
        memory_info = process.memory_info()
        memory_used = max(memory_used, memory_info.rss)
        return "_" * len(y), y, memory_used
    if len(y) == 0:
        memory_info = process.memory_info()
        memory_used = max(memory_used, memory_info.rss)
        return x, "_" * len(x), memory_used
    if len(x) * len(y) < MAXIMUM_DP_AREA:
        return base_case_DP(x, y)
    
    mid = len(x) // 2
    x_left = x[:mid]
    x_right = x[mid:]
    
    # Compute alignment costs for all split areas, the right side is reversed because we want the prefix alignment
    left_alignment_costs = compute_split_costs(x_left, y)
    right_alignment_costs = compute_split_costs(x_right[::-1], y[::-1])
    min_cost = 99999999999999999
    split_index = 0
    
    # find the optimal split
    for i in range(len(y) + 1):
        if min_cost > left_alignment_costs[i] + right_alignment_costs[len(y) - i]:
            split_index = i
            min_cost = left_alignment_costs[i] + right_alignment_costs[len(y) - i]
    
    optimal_left_alignment = divide_and_conquer(x_left, y[:split_index])
    optimal_right_alignment = divide_and_conquer(x_right, y[split_index:])
    memory_info = process.memory_info()
    memory_used = max(memory_used, memory_info.rss)
    return (optimal_left_alignment[0] + optimal_right_alignment[0], optimal_left_alignment[1] + optimal_right_alignment[1], memory_used)

#### PART 4: Run code with Alignment ####
start_time = time.time() 
first_string, second_string, memory_consumed = divide_and_conquer(X, Y)
memory_consumed = int(memory_consumed / 1024)
end_time = time.time()
time_taken = (end_time - start_time) * 1000 
#### PART 5: Calculate the score ####
score = 0
for i in range(len(first_string)):
    if first_string[i] == "_":
        score += DELTA
    elif second_string[i] == "_":
        score += DELTA
    else:
        score += ALPHA[first_string[i] + second_string[i]]

print(score)
print(first_string)
print(second_string)
#### PART 5: FILE OUTPUT ####
with open(o_file_path, "w") as file:
    file.write(first_string + "\n")
    file.write(second_string + "\n")
    file.write(f"{time_taken} ms\n")
    file.write(f"{memory_consumed} KB\n")