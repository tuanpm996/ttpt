#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from mpi4py import MPI
import md5, json, time

start = time.time()
print("Bắt đầu")

comm = MPI.COMM_WORLD #number of processes
rank = comm.Get_rank() #rank of process

dict = ["a", "b", "c", "d", "e", "1", "2", "3", "4", "5", "6"] # Dictionanry
dict_size = len(dict)

test_string = "654cd"
test_digest = md5.new(test_string).digest()

password_len = len(test_string)
digest = md5.new(test_string).digest()

d = dict_size / (comm.Get_size() - 1) #phan nguyen
r = dict_size % (comm.Get_size() - 1) #phan du

list_char = []

for i in range(0, password_len - 1):
    list_char.append("")

def generateString(data):
    dict2 = dict[:]
    dict2.remove(data)
    Try(1, dict2)

def Try(i, dict):
    for j in range(0, len(dict)):
        list_char[i-1] = dict[j]
        if(i==(password_len-1)):
            password = data + ''.join(list_char)
            print password
            if(md5.new(password).digest() == test_digest):
                print "Đây là passowrd: %s" % password
                end = time.time()
                print(end - start)
                comm.Abort()
        else:
            Try(i+1, dict)

if rank == 0:
    for i in range(0, d):
        for j in range(0, comm.Get_size()-1):
            index = i*(comm.Get_size()-1) + j
            comm.send(dict[index], dest=j+1, tag=index)
    for i in range(0, r):
        index = i + d*(comm.Get_size() - 1)
        comm.send(dict[index], dest=1, tag=index)
        
else:
    for i in range(0, d):
        tag = i*(comm.Get_size() - 1) + rank - 1
        data = comm.recv(source=0, tag=tag)
        generateString(data)

    for i in range(0, r):
        tag = i + d*(comm.Get_size() - 1)
        data = comm.recv(source=0, tag=tag)
        generateString(data)


