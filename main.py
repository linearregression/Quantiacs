import json
import quantiacsToolbox
import random
import sys

def sim(plan):
  returnDict = quantiacsToolbox.runts(sys.argv[1], plotEquity=False, plan=plan)
  return returnDict['stats']['sharpe']

def randomBest(iters=4):
  lookback = 128
  opt = [random.uniform(-1, 1) for _ in range(lookback)]
  sharpe = sim(opt)
  for i in xrange(iters):
    plan = [random.uniform(-1, 1) for _ in range(lookback)]
    newSharpe = sim(plan)
    if newSharpe > sharpe:
      sharpe = newSharpe
      opt = plan
    print 'iteration:', i, 'sharpe:', sharpe
  return opt, sharpe

###############################################################################
# Genetic Algorithm
###############################################################################

def geneticAlgorithm(generations = 10, population = 20, mutationRate = 0.1,
                     mutationAmount = 0.1, destructionRate = 0.01, plans = None):

  def mate(plan1, plan2):
    child = list(plan1)
    for i in range(len(child)):
      if random.random() < 0.5:
        child[i] = plan2[i]
      if random.random() < mutationRate:
        child[i] += random.random() * mutationAmount
        if child[i] > 1:
          child[i] = 1
        elif child[i] < -1:
          child[i] = -1
      if random.random() < destructionRate:
        child[i] = random.uniform(-1, 1)
    return child

  def generateSharpes(plans):
    p = []
    totalSharpe = 0
    for plan in plans:
      sharpe = sim(plan)
      p.append([plan, sharpe])
    minSharpe = min(sharpe for plan, sharpe in p)
    for x in p:
      x[1] -= minSharpe - 1e-10
      totalSharpe += x[1]
    p = sorted(p, key=lambda x: x[1])
    for x in p:
      x.append(x[1] / float(totalSharpe))
    return p

  def pickWeightedRandomPlan(p):
    r = random.random()
    total = 0.
    for plan, sharpe, relativeSharpe in p:
      total += relativeSharpe
      if r <= total:
        return plan
    return bestPlan(p)

  def bestPlan(p):
    return p[len(p) - 1][0]

  #############################################################################
  # Main
  #############################################################################

  if not plans:
    return
  
  p = generateSharpes(plans)

  for i in xrange(generations):
    newPlans = []
    newPlans.append(list(bestPlan(p)))
    for j in xrange(population - 1):
      p1, p2 = pickWeightedRandomPlan(p), pickWeightedRandomPlan(p)
      newPlan = mate(p1, p2)
      newPlans.append(newPlan)
    p = generateSharpes(newPlans)
    best = bestPlan(p)
    sharpe = sim(best)
    print 'generation:', i, 'sharpe:', sharpe
    with open('output.json', 'w') as outfile:
      json.dump(best, outfile, indent=2)

  return bestPlan(p)

def main():
  if len(sys.argv) < 2:
    print 'Please specify path to trading system'
    return

  RANDOM_BEST_ITERS = 16
  GENERATIONS       = 16 # 4000
  MUTATION_RATE     = 0.05
  MUTATION_AMOUNT   = 0.2
  DESTRUCTION_RATE  = 0.01

  population = 16
  plans = []
  for i in range(population):
    plan, sharpe = randomBest(iters=RANDOM_BEST_ITERS)
    plans.append(plan)

  plan = geneticAlgorithm(generations = GENERATIONS, population = population,
                          mutationRate = MUTATION_RATE, mutationAmount = MUTATION_AMOUNT,
                          destructionRate = DESTRUCTION_RATE, plans = plans)

  with open('output.json', 'w') as outfile:
    json.dump(plan, outfile, indent=2)

if __name__ == '__main__':
  main()