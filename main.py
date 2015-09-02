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

  plan = [0.5233057668366192,0.6554960656763094,-0.2475952350139612,-0.5217753903973339,-0.6311182077483284,-0.856378651687326,-0.5058907207625194,0.45659714827563436,-0.39542934377162786,0.8579073420725487,-0.5134235694890732,-0.7585817499564758,-0.8776958588967538,0.0032560360914299508,-0.022366670507608655,-0.04077293630443246,0.6372283952184814,1,0.998402584840514,0.05735241364741617,-0.21602528419016465,0.8920660094031776,0.34019617210073494,0.44315434607299714,-0.7105751793850563,-0.7378769776484928,-0.8453964303218462,-0.4614706174132477,0.6295333446495794,-0.16916266157157378,0.17553444417889996,-0.36983530873208936,0.7576496343374803,0.948400312110671,-0.7922850342026833,1,0.9717939723462619,-0.3184550918287768,0.06857034907689985,0.27294996439127706,0.3623250625121151,-0.27440006044198095,-0.5079362909324994,-0.8162623645931617,0.8031398959447456,-0.8960044990701117,0.3929865557972956,-0.6030362697712304,-0.25796461025184425,-0.21357890055690398,-0.8914702949035589,0.011184357203543716,0.09895279624632147,-0.36795089194855923,-0.684432167677077,-0.08571657018760304,-0.6789744519609338,0.06815698115230862,-0.82019763859957,-0.1299609796541743,0.15286566422687753,-0.2370551108191683,0.09243761313667576,-0.30462449602422303,0.8466115259882772,0.9662441625294065,-0.8770254262420765,0.46891188033006914,0.5668163468172001,-0.9111305005627515,-0.29663232504376924,0.7837012787546571,-0.4341423094760277,-0.42594695611552247,-0.1495898832652396,0.40747630160872195,-0.3024895365206115,-0.9457641958153433,-0.49859578980080044,0.66806072241184,-0.9331744012811638,0.29667929371767543,0.38923050800734216,0.3250174906440886,0.08334463381710619,0.9279086872346392,-0.3106366552198949,-0.8620493133373683,-0.08440244990839596,0.8717580406324144,-0.8133111349621267,0.6466444534674416,0.5767866061886957,0.328475735699135,0.42104864921147955,0.23787037268159916,-0.66105385981464,-0.8122791650321639,-0.21605950829961307,0.05637501561287972,-0.9725606038476251,0.16740435474000342,0.11631824143989578,-0.7668405251546246,-0.5873918088529735,-0.2860020145122777,-0.15697227765595442,0.8069226151753524,-0.19740801486053416,0.6760230850393909,0.5319642077616862,0.6996528132280224,-0.05999520269114389,0.31774543948995393,-0.3250752627919602,0.2583580013409774,0.8163607958195884,0.9152620185797613,-0.5668319468086896,0.25300921171266477,0.7961259046947731,0.9805447479850316,-0.43128985926061714,0.9288167345768463,0.6042532861611523,0.43002124734202574,-0.8159052925279995,0.04983920783503648]
  print sim(plan)

  # RANDOM_BEST_ITERS = 16
  # GENERATIONS       = 16 # 4000
  # MUTATION_RATE     = 0.05
  # MUTATION_AMOUNT   = 0.2
  # DESTRUCTION_RATE  = 0.01

  # population = 16
  # plans = []
  # for i in range(population):
  #   plan, sharpe = randomBest(iters=RANDOM_BEST_ITERS)
  #   plans.append(plan)

  # plan = geneticAlgorithm(generations = GENERATIONS, population = population,
  #                         mutationRate = MUTATION_RATE, mutationAmount = MUTATION_AMOUNT,
  #                         destructionRate = DESTRUCTION_RATE, plans = plans)

  # with open('output.json', 'w') as outfile:
  #   json.dump(plan, outfile, indent=2)

if __name__ == '__main__':
  main()