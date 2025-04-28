#GroceryStoreSim.py
#Name:Cameron Sailors
#Date:4/27/2025
#Assignment:Lab 11

import simpy
import random
eventLog = []
waitingShoppers = []
idleTime = 0


def shopper(env, id):
    arrive = env.now
    items = random.randint(1, 50)
    if 30 <= items <= 50:
        items = items // 2
    else:
        return
    shoppingTime = items // 2 # shopping takes 1/2 a minute per item.
    yield env.timeout(shoppingTime)
    # join the queue of waiting shoppers
    waitingShoppers.append((id, items, arrive, env.now))

def checker(env):
    global idleTime
    while True:
        while len(waitingShoppers) == 0:
            idleTime += 1
            yield env.timeout(1) # wait a minute and check again

        customer = waitingShoppers.pop(0)
        items = customer[1]
        checkoutTime = items // 10 + 1
        yield env.timeout(checkoutTime)

        eventLog.append((customer[0], customer[1], customer[2], customer[3], env.now))

def customerArrival(env):
    customerNumber = 0
    while True:
        customerNumber += 1
        env.process(shopper(env, customerNumber))
        newCustomer = random.randint(1,3)
        yield env.timeout(newCustomer) # New shopper every 1 to 3 minutes


def processResults():
    waitTimes = []
    totalWait = 0
    totalShoppers = 0

    for e in eventLog:
        waitTime = e[4] - e[3] #depart time - done shopping time
        totalWait += waitTime
        waitTimes.append(waitTime)
        totalShoppers += 1

    if totalShoppers > 0:
        avgWait = totalWait / totalShoppers
    else:
        avgWait = 0
    
    maxWait = max(waitTimes) if waitTimes else 0

    print("The average wait time was %.2f minutes." % avgWait)
    print("The total idle time was %d minutes" % idleTime)
    print("The max wait time was %d minutes" % maxWait)

def main():
    numberCheckers = 3

    env = simpy.Environment()

    env.process(customerArrival(env))
    for i in range(numberCheckers):
        env.process(checker(env))

    env.run(until=180 )
    print(len(waitingShoppers))
    processResults()

if __name__ == '__main__':
    main()