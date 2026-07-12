start WSL

> sudo apt install python3.10-venv
> python3 -m venv .ai_planner
> source .ai_planner/bin/activate
> sudo apt-get update && sudo apt-get install cmake g++ git python3-dev python3-pip


windows corresponding folder

> git clone https://github.com/aibasel/downward.git


switch to wsl

> sudo apt-get update && sudo apt-get install cmake g++ git python3-dev python3-pip
> cd /downward
> sudo apt install dos2unix
> dos2unix ./build.py
> ./build.py

create your domain.pddl and problem.pddl files and run the command

>./fast-downward.py domain.pddl problem.pddl --search "eager_greedy([ff()])"


instead of "eager_greedy([ff()])" you can also run other configurations

eager_greedy([ff()]) = Fast/Greedy Search (Aims to find any solution quickly)

astar(lmcut()) = Optimal Search (Aims to find the shortest possible solution, but uses a lot of memory)

--alias seq-sat-lama-2011 = The IPC-Tested Alias (Uses a pre-configured portfolio of heuristics)
./fast-downward.py --alias seq-sat-lama-2011 domain.pddl problem.pddl


Reading the Output
Once execution finishes, Fast Downward will output log data to your terminal.If a solution is found, it will print Search satisfied expected effects.The actual plan (the sequence of moves) will be saved to a file named sas_plan in your current working directory.

create the domain.pddl and problem.pddl files (ar ask Gemini to craet these based on criteria of problem setup).
Then run command

> ./downward/builds/release/bin/downward domain.pddl problem.pddl --search "eager_greedy([ff()])"

