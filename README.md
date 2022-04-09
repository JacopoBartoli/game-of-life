# Conway's Game of Life
Python implementation of the Conway's Game of Life usi PyQt5.

# Game of Life
The Game of Life is a grid sistem composed by cells which can assume a finite number of states. The state of each cell is determined by a set of rules applied to cells and their neighborhood.
t was devised by the British matematician John Horton Conway in 1970 as a simplification of the John von Neumann original idea to realize a cellular automaton that simulated a Turing machine.
For further info check the [Wikipedia](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life) page.

# Rules
The original Conway's Game of Life is defined over a infinite grid of cells with only two states: alive or dead.
At each timestep the grid states is updated applying the following rules:

![image info](./resources/images/rule1.png)
![image info](./resources/images/rule2.png)


![image info](./resources/images/rule3.png)
![image info](./resources/images/rule4.png)

# Requirements
The dependencies can be install with the following command:
```
conda env create -f conda_env.yml
```

| Software   | Version           |
| -----------|-------------------|
| **Python** | tested on v3.6    | 
| **PyQT5**  | tested on v5.9.2  |
| **Numpy**  | tested on v1.17.0 |
| **PyYaml** | tested on v5.4.1  |



# Play the game
In order to start the game it's just needed to run [main.py](./main.py) file. For changing some settings (e.g. grid size or the game grid loaded by default) you can edit the [config.yml](./config.yml) file.
