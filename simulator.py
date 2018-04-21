'''
CS5250 Assignment 4, Scheduling policies simulator
Sample skeleton program
Author: Minh Ho
Input file:
    input.txt
Output files:
    FCFS.txt
    RR.txt
    SRTF.txt
    SJF.txt
Apr 10th Revision 1:
    Update FCFS implementation, fixed the bug when there are idle time slices between processes
    Thanks Huang Lung-Chen for pointing out
Revision 2:
    Change requirement for future_prediction SRTF => future_prediction shortest job first(SJF), the simpler non-preemptive version.
    Let initial guess = 5 time units.
    Thanks Lee Wei Ping for trying and pointing out the difficulty & ambiguity with future_prediction SRTF.
'''
import sys

input_file = 'input.txt'

class Process:

    def __init__(self, id, arrive_time, burst_time):
        self.id = id
        self.arrive_time = arrive_time
        self.burst_time = burst_time
        self.last_scheduled_time = arrive_time
    #for printing purpose
    def __repr__(self):
        return ('[id %d : arrive_time %d,  burst_time %d]'%(self.id, self.arrive_time, self.burst_time))

def find_unique_process(to_be_processed):
    ids = set()
    for process in to_be_processed:
        ids.add(process.id)
    return ids

def get_total(processes):
    total_w_time = 0

    for process in processes:
        print(process.wait_time)
        total_w_time = total_w_time + process.wait_time

    return total_w_time

def insert_into_wait_list_queue(wait_list, curr_process):
    ids = set()
    for process in wait_list:
        ids.add(process.id)
    print (ids)
    index = len(ids) - 1
    prev_process = wait_list[index]
    if(prev_process.arrive_time >= curr_process.arrive_time):
        wait_list.insert(index+1, curr_process)
    else:
        wait_list.insert(index, curr_process)
    return wait_list

def FCFS_scheduling(process_list):
    #store the (switching time, proccess_id) pair
    schedule = []
    current_time = 0
    waiting_time = 0
    for process in process_list:
        if(current_time < process.arrive_time):
            current_time = process.arrive_time
        schedule.append((current_time,process.id))
        waiting_time = waiting_time + (current_time - process.arrive_time)
        current_time = current_time + process.burst_time
    average_waiting_time = waiting_time/float(len(process_list))
    return schedule, average_waiting_time

#Input: process_list, time_quantum (Positive Integer)
#Output_1 : Schedule list contains pairs of (time_stamp, proccess_id) indicating the time switching to that proccess_id
#Output_2 : Average Waiting Time
def RR_scheduling(process_list, time_quantum):
    current_time = 0
    waiting_time = 0
    processing_queue = []
    to_be_processed = process_list.copy()
    schedule = []

    ids = find_unique_process(to_be_processed)
    n = len(ids)
    while to_be_processed.__len__() > 0:
        for x in range(n):
            tbd_process = to_be_processed[0]
            processing_queue.append(tbd_process)
            to_be_processed.pop(0)

        while processing_queue.__len__() > 0:
            current_process = processing_queue.pop(0)
            if(current_time < current_process.last_scheduled_time):
                current_time = current_process.last_scheduled_time
            waiting_time = waiting_time + (current_time - current_process.last_scheduled_time);
            schedule.append((current_time, current_process.id))  # processing
            if current_process.burst_time > time_quantum:
                current_time += time_quantum
                current_process.burst_time -= time_quantum
                current_process.last_scheduled_time = current_time
                processing_queue.append(current_process)
            else:
                current_time += current_process.burst_time
                current_process.burst_time = 0
                current_process.last_scheduled_time = current_time

    average_waiting_time = waiting_time / float(len(process_list))
    return schedule, average_waiting_time

def SRTF_scheduling(process_list):
    return (["to be completed, scheduling process_list on SRTF, using process.burst_time to calculate the remaining time of the current process "], 0.0)

def SJF_scheduling(process_list, alpha):
    return (["to be completed, scheduling SJF without using information from process.burst_time"],0.0)


def read_input():
    result = []
    with open(input_file) as f:
        for line in f:
            array = line.split()
            if (len(array)!= 3):
                print ("wrong input format")
                exit()
            result.append(Process(int(array[0]),int(array[1]),int(array[2])))
    return result
def write_output(file_name, schedule, avg_waiting_time):
    with open(file_name,'w') as f:
        for item in schedule:
            f.write(str(item) + '\n')
        f.write('average waiting time %.2f \n'%(avg_waiting_time))


def main(argv):
    process_list = read_input()
    print ("printing input ----")
    for process in process_list:
        print (process)
    print ("simulating FCFS ----")
    FCFS_schedule, FCFS_avg_waiting_time =  FCFS_scheduling(process_list)
    write_output('FCFS.txt', FCFS_schedule, FCFS_avg_waiting_time )
    print ("simulating RR ----")
    RR_schedule, RR_avg_waiting_time =  RR_scheduling(process_list,time_quantum = 2)
    write_output('RR.txt', RR_schedule, RR_avg_waiting_time )
    print ("simulating SRTF ----")
    SRTF_schedule, SRTF_avg_waiting_time =  SRTF_scheduling(process_list)
    write_output('SRTF.txt', SRTF_schedule, SRTF_avg_waiting_time )
    print ("simulating SJF ----")
    SJF_schedule, SJF_avg_waiting_time =  SJF_scheduling(process_list, alpha = 0.5)
    write_output('SJF.txt', SJF_schedule, SJF_avg_waiting_time )

if __name__ == '__main__':
    main(sys.argv[1:])
