# roommates-simulated-annealing
The second assignment in COMP-SCI 441 (Introduction to Artifical Intelligence). A simulated annealing example that places students in dorm rooms based upon the results of an imaginary personality test. The algorithm optimizes for highest average compatibility per room. 

## Usage 
`python roomates-simulated-annealing.py [OPTIONS]`

You may want to redirect the output to a file which can be done in python with the following. 

`python roomates-simulated-annealing.py [OPTIONS] > output.txt`

### Options

|     OPTION    |                      Description                 |
| ------------- | ------------------------------------------------ | 
| --file, -f    | Specify the input file, defaults to roommates.txt|
| --student-count, -s  | The number of students being placed into rooms, defaults to 200  |
| --room-capacity, -c  | The number of students per room, defaults to 4 |
| --temperature, -T  | The initial temperature, defaults to 1000 |
| --cooling-factor, -a  | The cooling factor for the temperature, defaults to 0.95 |

### Input
Each row in the input file represents a single students compatibility with every other student. For example, student 20's compatibility with student 100 would be located at position [20][100] in the file. A student has a compatibility of zero with themselves. The lower the compaitbility score the **more** compatibile the two students. An example input file can be found [here](https://github.com/Andrew-Bellas/roommates-simulated-annealing/blob/main/roommates.txt). 

