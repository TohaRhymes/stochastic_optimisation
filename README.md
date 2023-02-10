## Comparative Analysis of Stochastic Optimization Methods
### (+ simple tool:))

I presented this project at the international conference MICSECS-2020 (Mayorov Readings) and won Best Report Award for my report "Comparative Analysis of Stochastic Optimization Methods".

This is a project with the implementation of common stochastic optimization methods on the example of the traveling salesman problem on Python v3.7+.

Required packages: `numpy (1.19.2+)`, `matplotlib (3.2.2+)`

### Files:
* `searches.py` - file with the implementation of all searches
* `processing.py` - file with the secondary functions: generate and read the dataset, draw the salesman's path and launch the algorithm
* `Tests.ipynb` - jupyter notebook with the usage examples.
* `stochastic_tool.py` - tool, that can generate datasets with points of any dimension and run Stochastic Optimization Methods on it

### Parameters for stochastic_tool.py:
__GENERATING-mode__

If you want to generate csv-file with points, use generate command:

`python3 stochastic_tool.py generate <amount of points> <dimension of space>`

    - <amount of points> (int) -  amount of rows, that will be generated, each row - one point.
    - <dimension of space> (int) - dimension of generated point's space.
    
__OPTIMIZATION-mode__

If you want to optimize way, using  existing csv-file with points of any dimension, use:

`python3 stochastic_tool.py optimize <input file> <method> <iterations> <distance_method>`

    - <input file> - input csv-file with points.
        * it should be in csv-format;
        * it should contains same columns for each row;
    - <method> - method to use (can be chosen from: ['monte-carlo', 'random-walk', 'hill-climb', 'annealing', 'genetic'])
    - <iterations> (int) - amount of iterations for each method.
    - <distance_method> (str) (optimal) - metric to use, can be chosen from: ['l1', 'l2']. Default = 'l1'.
    Default output file: <input file>_new.csv
