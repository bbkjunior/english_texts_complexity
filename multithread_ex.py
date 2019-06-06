#! /usr/bin/env python
# -*- coding: utf-8 -*-
import multiprocessing 
import time
import random

def common_func ():
  for i in range(5):
    print(i)

def foo():
  n=0
  while n<1000000: #пишем 10 чисел
    
    print('FUNCTION_1 '+str(n)) # отчитываемся о записи.
    common_func()
    n+=1
    time.sleep(random.random()) # засыпаем на случайный промежуток времени.
def foo_2():
  n=0
  while n<1000000: #пишем 10 чисел
    
    print('FUNCTION_2 '+str(n)) # отчитываемся о записи.
    common_func()
    n+=1
    time.sleep(random.random()) # засыпаем на случайный промежуток времени.
  
# создаем, а потом запускаем потоки.
pr1=multiprocessing.Process(target=foo)
pr1.start()

pr2=multiprocessing.Process(target=foo_2)
pr2.start()

"""
k=100
while k<1000000: #пишем 10 чисел
  print('FUNCTION_2 '+str(k)) # отчитываемся о записи.
  common_func()
  k+=11
  time.sleep(random.random()) # засыпаем на случайный промежуток времени.

# Видно, как потоки работают параллельно, правда?
"""