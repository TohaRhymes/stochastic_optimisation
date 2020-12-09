import sys
import os
from processing import read_dataset, draw_way, launching, generate_new_dataset
from searches import monte_carlo, random_walk, hill_climb, annealing, genetic_algo, total_dist, l1, l2

string_parameters = """
Parameters for stochastic_tool.py:
GENERATING-mode
If you want to generate csv-file with points, use generate command:
python3 stochastic_tool.py generate <amount of points> <dimension of space>
    - <amount of points> (int) -  amount of rows, that will be generated, each row - one point.
    - <dimension of space> (int) - dimension of generated point's space.
    
OPTIMIZATION-mode
If you want to optimize way, using  existing csv-file with points of any dimension, use:
python3 stochastic_tool.py optimize <input file> <method> <iterations> <distance_method>
    - <input file> - input csv-file with points.
        * it should be in csv-format;
        * it should contains same columns for each row;
    - <method> - method to use (can be chosen from: ['monte-carlo', 'random-walk', 'hill-climb', 'annealing', 'genetic'])
    - <iterations> (int) - amount of iterations for each method.
    - <distance_method> (str) (optimal) - metric to use, can be chosen from: ['l1', 'l2']. Default = 'l1'.
Default output file: <input file>_new.csv

Please, try again!
"""
print()
if len(sys.argv) <= 1:
    print("You should input parameters!")
    print(string_parameters)
    exit()

process = sys.argv[1]
if process == 'generate':
    try:
        iterations = int(sys.argv[2])
        dim = int(sys.argv[3])
        name = generate_new_dataset(iterations, dim)
        print(f'Dataset generated.\nName: {name}')
    except (ValueError, IndexError):
        print(f"During generation something went wrong.\nCheck usage:")
        print(string_parameters)
    exit()
if process != 'optimize':
    print('Not correct mode.')
    print(string_parameters)
    exit()
try:
    flag_continue = True
    input_file = sys.argv[2]
    if not (os.path.exists(input_file) and os.path.isfile(input_file)):
        print('Check if the file exists.')
        flag_continue = False
    method = sys.argv[3]
    if method not in ['monte-carlo', 'random-walk', 'hill-climb', 'annealing', 'genetic']:
        print('Stochastic optimisation method doesn\'t exist. Choose correct one!')
        flag_continue = False
    iterations = int(sys.argv[4])
    if len(sys.argv) > 5:
        dist_method = sys.argv[5]
        if dist_method not in ['l1', 'l2']:
            print('Distance method doesn\'t exist. Choose correct one!')
            flag_continue = False
    else:
        dist_method = 'l1'
except (IndexError, ValueError):
    print("Error, while parsing parameters.\nCorrect parameters are:")
    print(string_parameters)
    exit()

try:
    methods = ['monte-carlo', 'random-walk', 'hill-climb', 'annealing', 'genetic']
    fun_methods = [monte_carlo, random_walk, hill_climb, annealing, genetic_algo, total_dist]
    fun_method = fun_methods[methods.index(method)]

    if dist_method == 'l2':
        fun_dist_method = l2
    else:
        fun_dist_method = l1
    launching(input_file, fun_method, method, iters=iterations, dist_method=fun_dist_method,
              dist_method_name=dist_method)
except ValueError:
    print("Check your file:\n\t* it should be in csv-format;\n\t* it should contains same columns for each row;")
