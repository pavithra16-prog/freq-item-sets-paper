import argparse
import itertools 
from collections import defaultdict

def integernumber(n,bit_size):
   bin_number = bin(n)
   reverse_number = bin_number[-1:1:-1]
   reverse_number = reverse_number + (bit_size - len(reverse_number))*'0'
   return(int(reverse_number,2))
   
   
def my_hash_fn(num1, num2):
 if(num1 <= num2):
   num1 = integernumber(num1, 5)
 else: 
   num2 = integernumber(num2, 5)
 return (num1 ^ num2 ) % 150


def create_bitmap(hash_table, threshold):
  bit_map = [0] * 150
  print('Hash table inside bit map fn. is ', hash_table)
  for key, value in hash_table.items():
    if value < threshold:
      bit_map[key] = 0
    else:
      bit_map[key] = 1
  return bit_map

def create_candidate_singletons(dataset_file):
  
  candidate_item_list = defaultdict(int)
  baskets = []

  buckets = {}

  with open(dataset_file) as file:
    print('Finding all possible doubletons for each line given in the dataset during PASS 1 itself to HASH')
    for line in file:
      num_list = list(map(int, line.split()))
      baskets.append(num_list)
      for item in num_list:
        candidate_item_list[item] += 1

      pairs = list(itertools.combinations(num_list, 2))
      print(pairs)
      for pair in pairs:
        index = my_hash_fn(pair[0], pair[1]) 
        buckets[index] = 1 if index not in buckets else buckets[index]+1
  
  print('\nSuccessful candidate singletons itemsets\n\n')
  return candidate_item_list, baskets, buckets


def create_frequent_item_set(item_list, min_threshold):

  for key, value in list(item_list.items()):
    if value < min_threshold:
      del item_list[key]
  print('Freq itemsets Creation successful')
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



def pcy(dataset_file, threshold):  
  
  print('PASS 1\n')
  C1, baskets, buckets = create_candidate_singletons(dataset_file)
  print('Input is (for reference): ', baskets, '\n')
  print('HASH TABLE ', buckets, '\n')
  print('CANDIDATE SINGLETONS: ', C1, '\n')
  print('\n')
  print('Bitmap of the hash table is to be created to give to PASS 2')
  bitmap = create_bitmap(buckets, threshold)
  print('Bitmap creation successful, BITMAP: ', bitmap, '\n')
  print('\n\n\nPASS 2 !!!')
  F1_items = create_frequent_item_set(C1, threshold)
  
  print('FREQUENT SINGLETONS: ', F1_items)
  frequent_pairs = join(F1_items, 2)
  print('All possible doubletons formed from the frequent singletons', frequent_pairs)
  print('\nHASH each of the above doubletons to find whether they are frequent or not (if hash value == 0, remove that particular doubleton)')
  for pair in frequent_pairs:
    hash_value = my_hash_fn(pair[0], pair[1])
    if bitmap[hash_value] != 1:
      print ('Bitmap value is 0. So, Removing this doubleton (', pair[0], pair[1], ')')
      frequent_pairs.remove(pair)
  print('After checking each of the pairs possible from the freq. singletons with the bitmap, the \n\nFREQUENT DOUBLETONS ', frequent_pairs, '\n\n')
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
  parser = argparse.ArgumentParser(description='PCY Algorithm')
  parser.add_argument('datafile', help='Dataset File')
  parser.add_argument('threshold', help='Threshold Value')

  args = parser.parse_args()

  print('Support Threshold value :', args.threshold, '\n\n')  
  print(pcy(args.datafile, int(args.threshold)))
  
  
