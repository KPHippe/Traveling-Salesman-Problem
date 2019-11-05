The three python programs in this directory correlate to the three programs
specified by the assignment. 

To run each program, simply run the command 'python filename.py' on the ECS
computers and each will begin a standard test on the a280.tsp data. 

For the simulated annealing program and the genetic approached algorithm, 
data will be written to appropriately labeled CSV data for each. 

To change any details about the program, look to the Global helper variables in each. 
The 'printing' variable will print appropriate information for each program, including
weight of the solution and order of nodes in the solution. This is enabled by default. 
The debug variable will give detailed debug information in the console. This is disabled
by default. 

Note about simulated annealing: to choose a different cooling schedule, look to the 
cooling schedule section near the top of the program, the variable set to True is the 
schedule that will be applied on execution, to change, set the current schedule to false and 
set the desired schedule to true. 