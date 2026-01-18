import json
import pprint

p = 'insights_index.json'
idx = json.load(open(p, 'r', encoding='utf-8'))

total = len(idx)
with_faces = sum(1 for v in idx.values() if v.get('faces'))
with_emotions = sum(1 for v in idx.values() if v.get('emotions'))

def contains_name(name):
    return [k for k in idx.keys() if name.lower() in k.lower()]

person1 = contains_name('person1')
person2 = contains_name('person2')

examples_faces = [ (k, idx[k]) for k in idx.keys() if idx[k].get('faces') ][:5]

print(f"total:{total}")
print(f"with_faces:{with_faces}")
print(f"with_emotions:{with_emotions}")
print(f"Person1 matches: {len(person1)}")
if person1:
    pprint.pprint(person1[:5])
print(f"Person2 matches: {len(person2)}")
if person2:
    pprint.pprint(person2[:5])
print('\nExamples (up to 5) with `faces` metadata:')
if examples_faces:
    for k,v in examples_faces:
        print('-' * 40)
        print(k)
        pprint.pprint(v)
else:
    print('None')
