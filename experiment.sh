#!/bin/bash
> log.txt
for run in $(seq 15)
do
  for LC in 1 2 3
  do
    export LC_ENV=$LC
    t=$(expr 20 \* $LC_ENV)
    for EXP in 0 1 2 3
      do
        export EXP_ENV=$EXP

        for con in 0 2 10 20
          do
            for f in $(find data); do > $f; done
            make down
            make run &
            P_PID=$!
            sleep 60
            sh workload/base.sh
            sleep $t
            sh workload/conflict$con.sh
            sleep $t
            mkdir -p run$run/lc$LC_ENV/data$con/$EXP_ENV
            cp -r data/ run$run/lc$LC_ENV/data$con/$EXP_ENV
            kill $P_PID
            sleep 45

            echo "Done run" $run "lc" $LC_ENV " exp "$EXP_ENV " con " $con >> log.txt
          done

      done
  done

done

for f in $(find data); do > $f; done
make down

# python reports/report_generator.py