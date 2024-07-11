import argparse
from collections import defaultdict
import itertools 

def integernumber(n,bit_size):
   bin_number = bin(n)
   reverse_number = bin_number[-1:1:-1]
   reverse_number = reverse_number + (bit_size - len(reverse_number))*'0'
   return(int(reverse_number,2))
   
def hash(num1, num2):
  return (num1 * num2) % 75

def hash1(num1, num2):
 if(num1 <= num2):
   num1 = integernumber(num1, 5)
 else: 
   num2 = integernumber(num2, 5)
 return (num1 ^ num2 ) % 75  

def create_bitmap(hash_table, threshold):
  bit_map = [0] * 75
  for key, value in hash_table.items():
    if value < threshold:
      bit_map[key] = 0
    else:
      bit_map[key] = 1
  print('Bitmap creation successful')
  return bit_map

def create_candidate_singletons(dataset_file):
  candidate_item_list = defaultdict(int)
  baskets = []

  buckets = {}
  buckets1 = {}
  with open(dataset_file) as file:
    print('\n\nFinding all possible doubletons for each line given in the dataset during PASS 1 itself to HASH')
    for line in file:
      num_list = list(map(int, line.split()))
      baskets.append(num_list)
      for item in num_list:
        candidate_item_list[item] += 1
      pairs = list(itertools.combinations(num_list, 2))
      print('Pairs are ', pairs)
      for pair in pairs:
        index = hash(pair[0], pair[1]) 
        buckets[index] = 1 if index not in buckets else buckets[index]+1
        index1 = hash1(pair[0], pair[1]) 
        buckets1[index1] = 1 if index1 not in buckets1 else buckets1[index1]+1
  print('Successful candidate Singleton Itemset creation\n\n')
  return candidate_item_list, baskets, buckets, buckets1


def create_frequent_item_set(item_list, min_threshold):
  for key, value in list(item_list.items()):
    if value < min_threshold:
      del item_list[key]
  print('Freq itemsets successful')
  print(item_list)
  return item_list.keys()


def count(item_list, baskets):
  count = dict(zip(item_list, [0]*len(item_list)))

  for basket in baskets:
    for key in count:
      if set(list(key)) < set(basket):
        count[key] += 1 

  return count


def join(freq_item_sets, k):
  if k <= 2: 
    return list(itertools.combinations(freq_item_sets, k))
  else:
    return list(itertools.combinations(set(a for b in freq_item_sets for a in b),k))

def multihash(dataset_file, threshold):  
  print('\n\nPASS 1 !!!')
  C1, baskets, buckets, buckets1 = create_candidate_singletons(dataset_file)
  print('Input file: ', baskets)
  print('\nFirst HASH TABLE: ', buckets)
  print('\nSecond HASH TABLE: ', buckets1)
  print('\nCandidate item list: ', C1, '\n\n')
  
  bitmap = create_bitmap(buckets, threshold)
  print('Bitmap of First Hash Table: ', bitmap)
  bitmap1 = create_bitmap(buckets1, threshold)
  print('Bitmap of Second Hash Table: ', bitmap1, '\n\n')
  
  
  print('\n\nPASS 2 !!!')
  F1_items = create_frequent_item_set(C1, threshold)
  print('FREQUENT SINGLETONS: ', F1_items)
  
  frequent_pairs = join(F1_items, 2)
  print('Possible doubletons formed from the frequent Singletons: ', frequent_pairs)
  
  freq_pairs_copy = list(frequent_pairs)
  for pair in freq_pairs_copy:
    hash_value = hash(pair[0], pair[1])
    hash_value1 = hash1(pair[0], pair[1])
    if (bitmap[hash_value] == 0 or bitmap1[hash_value1] == 0):
       pair1 = pair
       print ('\nBITMAP VALUE IS 0. SO, REMOVING THIS DOUBLETON (', pair1[0], pair1[1], ')')
       frequent_pairs.remove(pair1)
       
  print('After checking each of the pairs possible from the freq. singletons with the bitmap, \nFREQUENT DOUBLETONS are ', frequent_pairs, '\n\n')
  
  if not frequent_pairs:
    return None
  else:
    L = [frequent_pairs]

    k = 3
    while(True):
      new_list = join(L[k-3], k)
      items = count(new_list, baskets)
      print('Candidate itemsets of size (each itemset has', k, 'elements) k = ', k, items)
      Fk_items = create_frequent_item_set(items, threshold)
      print('Frequent itemsets each containing', k, 'elements', Fk_items, '\n\n')
      if len(Fk_items) > 0:
        L.append(Fk_items)
        k+=1
      else:
        break
    
    return L[k-3]


if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Multihash Algorithm')
  parser.add_argument('datafile', help='Dataset File')
  parser.add_argument('threshold', help='Threshold Value')

  args = parser.parse_args()

  print('Support Threshold used:', args.threshold)  
  print(multihash(args.datafile, int(args.threshold)))
  
