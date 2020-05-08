# Experiment
for each data structure[0:crdt, 1:opsets, 2:global lock, 3:rwlock]:
  set exp variable in app.py
  clear logs
  run app
  base load
  conflict load
  save results
  stop app

## clear logs
> data/paris/paris.txt & > data/paris/bangalore.txt & > data/paris/newyork.txt & > data/paris/register.txt & > data/paris/timeparis.txt & > data/paris/timebangalore.txt & > data/paris/timenewyork.txt & > data/bangalore/paris.txt & > data/bangalore/bangalore.txt & > data/bangalore/newyork.txt & > data/bangalore/register.txt & > data/bangalore/timeparis.txt & > data/bangalore/timebangalore.txt & > data/bangalore/timenewyork.txt & > data/newyork/paris.txt & > data/newyork/bangalore.txt & > data/newyork/newyork.txt & > data/newyork/register.txt & > data/newyork/timeparis.txt & > data/newyork/timebangalore.txt & > data/newyork/timenewyork.txt

## base load
sh workload/base.sh

## running 0% conflict workload
sh workload/conflict0_load0.sh & sh workload/conflict0_load1.sh & sh workload/conflict0_load2.sh 
## save results
cp -r data/ data0_<api>/

# running 10% conflict workload
sh workload/conflict10_load0.sh & sh workload/conflict10_load1.sh & sh workload/conflict10_load2.sh 
## save results
cp -r data/ data10_<api>/

# running 20% conflict workload
sh workload/conflict20_load0.sh & sh workload/conflict20_load1.sh & sh workload/conflict20_load2.sh 
## save results
cp -r data/ data20_<api>/