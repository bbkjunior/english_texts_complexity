#! /usr/bin/env python
# -*- coding: utf-8 -*-
import multiprocessing 
import time
import random

def foo():
  n=0
  while n<1000000: #пишем 10 чисел
    print('FUNCTION_1 '+str(n)) # отчитываемся о записи.
    n+=1
    time.sleep(random.random()) # засыпаем на случайный промежуток времени.
  
# создаем, а потом запускаем потоки.
pr1=multiprocessing.Process(target=foo)
pr1.start()

k=100
while k<1000000: #пишем 10 чисел
  print('FUNCTION_2 '+str(k)) # отчитываемся о записи.
  k+=11
  time.sleep(random.random()) # засыпаем на случайный промежуток времени.

# Видно, как потоки работают параллельно, правда?