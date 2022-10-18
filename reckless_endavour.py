import numpy as np
from random import randrange
from numba import njit,prange
import time

t1 = time.perf_counter()

@njit()
def d12():
    return randrange(12) + 1

@njit()
def treasures():
    return max((d12(),d12()))


@njit()
def combo(start_mana = 13,final_mana = 100,imax = 10000):
    """
    returns a,b

    a := 0 => fizzled
         b => times cast before fizzle
    
    a := 1 => succes
         b => times cast before end
    
    c:= final mana

    """
    if start_mana < 13:
        # print("start_mana needs to be at least 13")
        return 0,0

    mana = start_mana - 7

    i = 0
    while mana < final_mana:
        i+=1
        mana = mana + treasures() - 6

        if mana < 6 or i > imax:
            if i> imax:
                print("imax overschreden")
            return 0,i

    return 1,i,mana + treasures() + treasures()

@njit(parallel=True)
def monte_carlo(n,start_mana = 13,final_mana = 100):
        succeses = 0
        turn_succes = 0
        turn_fail = 0
                

        for _ in prange(n):
            a,b = combo(start_mana=start_mana,final_mana = final_mana)
            succeses += a
            turn_succes += b*a
            turn_fail += b*(1-a)

        fails = n-succeses
        if fails == 0:
            fails = 1
        return turn_succes/succeses,turn_fail/(fails),succeses/n

def monte_carlo_runs(start_mana = (13,17),final_mana = 100,n_monte_carlo = 4000):

    P = []
    W_turn = []
    fizzle_turn = []

    print(list(range(start_mana[0],start_mana[1])))

    for start_mana in range(start_mana[0],start_mana[1]):

        test = monte_carlo(n_monte_carlo,start_mana = start_mana,final_mana = final_mana)

        P.append(test[2]*100)
        W_turn.append(test[0])
        fizzle_turn.append(test[1])

    return P,W_turn,fizzle_turn

