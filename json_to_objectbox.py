

import json
import objectbox

from dictionary_model import Dictionary, get_objectbox_model


model = get_objectbox_model()
ob = objectbox.Builder().model(model).directory("db").build()
box = objectbox.Box(ob, Dictionary)


# dictionary_file_path = './dist/all.json'
# with open(dictionary_file_path) as f:
#     dict_list = json.loads(f.read())
#     for d in dict_list:
#         dictionary = Dictionary()
#         dictionary.word = d['word']
#         dictionary.content = d['content']
#         box.put(dictionary)

for i in box.get_all():
    print(i.id)