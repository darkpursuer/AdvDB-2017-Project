Advanced Database Systems Project
=================================

### Team
We have tested our application on our local machine.  
Please do let us know if it runs into any problems on your machine.
- Taikun Guo <tg1539@nyu.edu>
- Yi Zhang <yz3940@nyu.edu>

### Intro
This is our implementation of Project Possibility 1 - RepCRec.  
We created the application using `python3`.  
We followed the instructions in `project section` in course syllabus.
And we have included our design document `Design-Document-yz3940_tg1539.pdf`.

### Run Application
<mark>make sure to use `python 3`</mark>  

- To run the application directly.
```bash
python start_console.py
```
- To run with a pre-load script.
```bash
python start_console.py -f <file_path>
```

### Commands
Here is a list of supported commands and DB operations in the application.
```bash
# Supported commands:
help # print all the commands
load <filename> # load and process a file
exit # quit the console

# Supported DB operations:
begin(T1) # begin of a normal transaction
beginRO(T3) # begin of a read-only transaction
R(T1, x4) # T1 wants to read x4
W(T1, x6,v) # T1 wants to write v to x6
dump() # get all variables from all sites
dump(i) # get all variables at site i
dump(xj) # get variable xj at all sites
end(T1) # end a transaction T1
fail(1) # fail site 1
recover(1) # recover site 1
```

### Work distributions
- Design - Yi Zhang & Taikun Guo
- Design Document - Yi Zhang
- Transaction module - Yi Zhang
- Database module - Taikun Guo
- Console module - Taikun Guo
- Testing - Taikun Guo & Yi Zhang
