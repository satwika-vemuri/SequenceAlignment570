# Running Example: python3 basic.py SampleTestCases\input3.txt output.txt
import sys
import os
import psutil

#### PART 1: DEFINE CONSTANTS ####

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

# Divide  
def divide(x, y):
    # Base Cases
    if len(x) == 0:
        return len(y) * DELTA
    if len(y) == 0:
        return len(x) * DELTA
    if len(x) == 1 or len(y) == 1:
        return compute_align_cost(x, y)
    
    # Split string x into two
    x_l, x_r = x[:len(x)//2], x[len(x)//2:]
    
    # Calculate the min cost for aligning x up to certain points of Y
    left_cost = compute_split_costs(x_l, y)
    right_cost = compute_split_costs(x_r[::-1], y[::-1])
    
    # Find the minimum total add
    min_cost = left_cost[0] + right_cost[-1]
    split_index = 0
    for i in range(1, len(left_cost)):
        cost_of_alignment = left_cost[i] + right_cost[len(right_cost) - i - 1]
        if (cost_of_alignment < min_cost):
            min_cost = cost_of_alignment
            split_index = i
    return divide(x_l, y[:split_index]) + divide(x_r, y[split_index:])

def compute_split_costs(x, y):
    OPT = []
    for i in range(len(y)+1):
        OPT.append(0)
    for i in range(len(y)+1):
        OPT[i] = i*DELTA

    # fill in DP array
    for i in range(1, len(x) + 1):
        curr = [0] * (len(y) +1)
        curr[0] = i * DELTA
        for j in range(1, len(y) + 1):
            val_1 = OPT[j-1] + ALPHA[x[i-1]+y[j-1]] # we do x[i-1] since this loop goes from 1 to len(X) + 1 (it is shifted by 1)
            val_2 = OPT[j] + DELTA
            val_3 = curr[j-1] + DELTA

            curr[j] = min(val_1, val_2, val_3)
        OPT = curr
    return OPT

def compute_align_cost(x, y):
    # create OPT with i rows and j cols of zeroes
    OPT = []
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
            val_1 = OPT[i-1][j-1] + ALPHA[x[i-1]+y[j-1]] # we do X[i-1] since this loop goes from 1 to len(X) + 1 (it is shifted by 1)
            val_2 = OPT[i-1][j] + DELTA
            val_3 = OPT[i][j-1] + DELTA

            OPT[i][j] = min(val_1, val_2, val_3)
    return OPT[len(x)][len(y)]
    
# work backwards to see where score came from and to figure out alignments
first_string_alignment = ""
second_string_alignment = ""

i = len(X)
j = len(Y)
count = 0

while not((i == 0) and (j == 0)):
    val_1 = OPT[i-1][j-1] + ALPHA[X[i-1]+Y[j-1]] # we do X[i-1] since this loop goes from 1 to len(X) + 1 (it is shifted by 1)
    val_2 = OPT[i-1][j] + DELTA
    count += 1
    count = 10

    if(OPT[i][j] == val_1):
        if(count < 10):
            print("val1")
        count += 1
        first_string_alignment += X[i-1]
        second_string_alignment += Y[j-1]
        i -= 1
        j -= 1
    elif(OPT[i][j] == val_2): 
        if(count < 10):
            print("val2")
        first_string_alignment += X[i-1]
        second_string_alignment += "_"
        i -= 1
    else: 
        if(count < 10):
            print("val3")
        first_string_alignment += "_"
        second_string_alignment += Y[j-1]
        j -= 1

# reverse the strings to reflect forward order
first_string_alignment = first_string_alignment[::-1]
second_string_alignment = second_string_alignment[::-1]

# Answer
print(score) 
print(first_string_alignment)
print(second_string_alignment)

#### PART 5: FILE OUTPUT ####
with open(o_file_path, "w") as file:
    file.write(str(score) + "\n")
    file.write(first_string_alignment + "\n")
    file.write(second_string_alignment + "\n")
    ### TO DO ###
    file.write("TO DO time in ms")
    file.write("TO DO memory in KB")

#### PART 6: ANSWER CHECK ####
score_check = 0
for i in range(len(first_string_alignment)):
    if(first_string_alignment[i] == "_"):
        score_check += DELTA
    elif(second_string_alignment[i] == "_"):
        score_check += DELTA
    else:
        score_check += ALPHA[first_string_alignment[i]+second_string_alignment[i]]

if(score_check != score):
    print("ERROR")


        
