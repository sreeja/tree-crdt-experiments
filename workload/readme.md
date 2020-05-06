# base load
sh base.sh

# running 0% conflict workload
sh conflict0_load0.sh & sh conflict0_load1.sh & sh conflict0_load2.sh 

# running 10% conflict workload
sh conflict10_load0.sh & sh conflict10_load1.sh & sh conflict10_load2.sh 

# running 20% conflict workload
sh conflict20_load0.sh & sh conflict20_load1.sh & sh conflict20_load2.sh 