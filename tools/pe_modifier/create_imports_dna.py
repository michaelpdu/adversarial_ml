import os
import json
import hashlib

json_file = r'small_dll_imports.json'

dna_folder = os.path.join(r'pe_dnas', r'imports_append')

if not os.path.exists(dna_folder):
    os.makedirs(dna_folder)

with open(json_file, 'r') as fh:
    mm = json.load(fh)
    for dllname, funclist in mm.items():
        for func in funclist:
            content = 'imports_append\n'
            content = content + dllname + '\n'
            content += func
            md5_hash = hashlib.md5()
            md5_hash.update(content.encode('utf-8'))
            md5_string = md5_hash.hexdigest()
            with open(os.path.join(dna_folder, md5_string), 'w') as fh:
                fh.write(content)
