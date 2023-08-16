for j in {1..100}
do
    i=$(($RANDOM%1000 + 1))
    echo $i, "--------------------"
    python run_simulator.py --task T1 --random_seed $i
done