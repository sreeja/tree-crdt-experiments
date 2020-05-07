# Experiment
clear logs
run app
base load
conflict load
save results
repeat

# clear logs
> data/paris/paris.txt & > data/paris/bangalore.txt & > data/paris/newyork.txt & > data/paris/timeparis.txt & > data/paris/timebangalore.txt & > data/paris/timenewyork.txt & > data/bangalore/paris.txt & > data/bangalore/bangalore.txt & > data/bangalore/newyork.txt & > data/bangalore/timeparis.txt & > data/bangalore/timebangalore.txt & > data/bangalore/timenewyork.txt & > data/newyork/paris.txt & > data/newyork/bangalore.txt & > data/newyork/newyork.txt & > data/newyork/timeparis.txt & > data/newyork/timebangalore.txt & > data/newyork/timenewyork.txt

# base load
sh base.sh

# running 0% conflict workload
sh conflict0_load0.sh & sh conflict0_load1.sh & sh conflict0_load2.sh 
## save results
cp -r data/ data0/

# running 10% conflict workload
sh conflict10_load0.sh & sh conflict10_load1.sh & sh conflict10_load2.sh 
## save results
cp -r data/ data10/

# running 20% conflict workload
sh conflict20_load0.sh & sh conflict20_load1.sh & sh conflict20_load2.sh 
## save results
cp -r data/ data20/