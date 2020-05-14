# Experiment
for each latency config  
  for each data structure[0:crdt, 1:opsets, 2:global lock, 3:rwlock]:  
    set exp variable in app.py  
    clear logs  
    run app  
    base load  
    conflict load  
    save results  
    stop app

## clear logs
for f in $(find data); do > $f; done

## base load
sh workload/base.sh

## running 0% conflict workload
sh workload/conflict0_load0.sh & sh workload/conflict0_load1.sh & sh workload/conflict0_load2.sh 
## save results
cp -r data/ lc<lc_config>/data0_<api>/

# running 10% conflict workload
sh workload/conflict10_load0.sh & sh workload/conflict10_load1.sh & sh workload/conflict10_load2.sh 
## save results
cp -r data/ lc<lc_config>/data10_<api>/

# running 20% conflict workload
sh workload/conflict20_load0.sh & sh workload/conflict20_load1.sh & sh workload/conflict20_load2.sh 
## save results
cp -r data/ lc<lc_config>/data20_<api>/