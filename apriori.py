import argparse
import itertools
from collections import defaultdict
 

def create_candidate_singleton(file):
  candidate_item_list = defaultdict(int)
  baskets = []

  with open(file) as file:
    for line in file:
      num_list = list(map(int, line.split()))
      baskets.append(num_list)

      for item in num_list:
        candidate_item_list[item] += 1
  
  return candidate_item_list, baskets


def create_frequent_item_set(item_list, min_threshold):

  for key, value in list(item_list.items()):
    if value < min_threshold:
      del item_list[key]
  return item_list.keys()


def count(item_list, baskets):
  count = dict(zip(item_list, [0]*len(item_list)))
  for basket in baskets:
    for key in count:
      if set(list(key)).issubset((set(basket))):
        count[key] += 1
  return count


def merge(freq_item_sets, k):
  if k <= 2: 
    return list(itertools.combinations(freq_item_sets, k))
  else:
    return list(itertools.combinations(set(a for b in freq_item_sets for a in b),k))


def apriori_algorithm(file, threshold):  
  
  C1, baskets = create_candidate_singleton(file)
  print('Input file: ', baskets)
  print("Candidate SINGLETON itemsets creation successful. The singleton candidate itemsets are:\n");
  print(C1)
  print('\n')
  
  
  L1 = create_frequent_item_set(C1, threshold)
  print("Frequent SINGLETONS creation successful");
  print(L1)
  print('\n')
  
  
  if not L1:
    return None
  else:
    L = [L1]
    k = 2
    while(True):
      new_list = merge(L[k-2], k)
      print('n = ', k, 'as the SIZE of the itemsets')
      print('Candidate itemsets of size k = ', k, 'i.e., each itemset containing', k, 'elements')
      print (new_list)
      items = count(new_list, baskets)
      print('Count of each itemsets above in the given database is: ', items)
      Fk_items = create_frequent_item_set(items, threshold)
      print('Freq itemsets of size k = ', k, 'are: ', Fk_items)
      print('\n')
      if len(Fk_items) > 0:
        L.append(Fk_items)
        k+=1
      else:
        break

    return L[k-2]
      
if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='APRIORI ALGORITHM')
  parser.add_argument('datafile', help='Dataset File')
  parser.add_argument('threshold', help='Threshold Value')

  args = parser.parse_args()

  print('Support Threshold Used: ', args.threshold)  
  print ('Final Answer: ', apriori_algorithm(args.datafile, int(args.threshold)))


