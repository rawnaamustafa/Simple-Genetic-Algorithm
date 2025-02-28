from array import *
import random

def generate():
    chromosomes=[]
    for i in range(20):
        row=[]
        for j in range(5):
            row.append(random.randint(0,1))
        chromosomes.append(row)
    return chromosomes

def calc_fitness(chromosomes):
    fitness=[]
    for i in chromosomes:
        fit_score = 0
        for c in i:
            if c==1:
                fit_score+=1
        fitness.append(fit_score)
    return fitness

def calc_relativeFit(chromosomes):
    relative_fit =[]
    fitnesses = calc_fitness(chromosomes)
    total_fit = sum(fitnesses)
    for i in range (len(fitnesses)):
        relative_fit.append(fitnesses[i]/total_fit)
    return relative_fit

def calc_cdf(chromosomes):
    cumm_fit = []
    rel_fit = calc_relativeFit(chromosomes)
    cumm =0
    for i in range(len(rel_fit)):
        cumm+=rel_fit[i]
        cumm_fit.append(cumm)
    return cumm_fit

def generate_randomParentsIndex(chromosomes):
    cumm = calc_cdf(chromosomes)
    prob = random.uniform(0,1)
    for i in range(len(cumm)):
        if i==0:
            if (prob < cumm[i]):
                index = i
        else:
            if (prob < cumm[i] and prob >= cumm[i-1]):
                index = i
    return index

def perform_crossOver(first,second,Pcross=0.6):
    parent1 = first
    parent2 = second
    prob = random.uniform(0,1)
    if (prob < Pcross):
        crossPt = random.randint(1, 4)
        child1 = parent1[:crossPt] + parent2[crossPt:]
        child2 = parent2[:crossPt] + parent1[crossPt:]
        return child1, child2
    else:
        return parent1 , parent2

def bitFlipMute(chromosome,pMute =0.05):
    for i in range(len(chromosome)):
        prob = random.uniform(0, 1)
        if prob < pMute:
           #print("Performed muatation for index",i)
           if chromosome[i] == 0:
               chromosome[i] = 1
           else:
               chromosome[i] = 0
    return chromosome


def genetic_algo(chromosomes,pop_size =20,num_gen=100,chrom_len=5,pcross=0.6,pmute=0.05):
    crossovertime = pop_size/2
    population = chromosomes
    fitness=[]
    max_fitness=[]
    avg_fitness=[]
    for i in range (num_gen):
        new_pop=[]
        for j in range(int(crossovertime)):
            i1 = generate_randomParentsIndex(population)
            i2 = generate_randomParentsIndex(population)
            while (i2 == i1):
                i2 = generate_randomParentsIndex(population)
            first = population[i1]
            second = population[i2]
            child1, child2 = perform_crossOver(first, second)
            child1 = bitFlipMute(child1)
            child2 = bitFlipMute(child2)
            new_pop.append(child1)
            new_pop.append(child2)
        population=new_pop
        fitness = calc_fitness(population)
        max_fitness.append(max(fitness))
        avg_fitness.append(sum(fitness) / len(fitness))
    print("Last generation Population :" , population)
    print("Highest fitness at every generation ;",max_fitness)
    print("Average fitness at every generation :", avg_fitness)


def run_program():
    for i in range(10):
        print("Generation ",i + 1)
        chromo=generate()
        seed= random.randint(1,1000)
        random.seed(seed)
        genetic_algo(chromo)
        print("---------------")

run_program()
