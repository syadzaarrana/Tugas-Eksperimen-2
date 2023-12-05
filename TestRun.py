import time, tracemalloc, json
import DatasetHelper, CoverDp, CoverBnb

def test_run(dataset):
    print("--------------------------------------")

    for key in dataset:
        data = dataset[key]
        print(key.upper() + " DATASET\n")
        
        start_dp = time.time()
        CoverDp.vc_dp(data['dp'])
        end_dp = time.time()

        print("DP Time: %.2f ms" % ((end_dp - start_dp) * 1000))

        tracemalloc.start()
        CoverDp.vc_dp(data['dp'])
        mem = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        print("Peak DP Memory: %.2f bytes" % (mem[1]))
        print()

        start_bnb = time.time()
        CoverBnb.BnB(data['bnb'])
        end_bnb = time.time()

        print("BnB Time: %.2f ms" % ((end_bnb - start_bnb) * 1000))

        tracemalloc.start()
        CoverBnb.BnB(data['bnb'])
        mem = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        print("Peak BnB Memory: %.2f bytes" % (mem[1]))

        print("--------------------------------------")

dataset = {'small': {}, 'medium': {}, 'large': {}}
dataset['small']['bnb'], dataset['small']['dp'] = DatasetHelper.generate_dataset(60, pow(10, 4))
dataset['medium']['bnb'], dataset['medium']['dp'] = DatasetHelper.generate_dataset(80, pow(10, 5))
dataset['large']['bnb'], dataset['large']['dp'] = DatasetHelper.generate_dataset(100, pow(10, 6))

with open('dataset.txt', 'w') as dataset_file: 
    dataset_file.write(json.dumps(dataset))

print("DATASET GENERATED, STARTING...")
print()
test_run(dataset)