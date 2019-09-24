def handle_annotations(annotations):

    new_global = {}
    new_local = {}
    if 'global' in annotations:
        for key in annotations['global']:
            key_new = key.replace('__EQUALS__', '=')
            new_global[key_new] = annotations['global'][key]

    if 'local' in annotations:
        for key in annotations['local']:
            key_new = key.replace('__EQUALS__', '=')
            new_local[key_new] = annotations['local'][key]


    return {'global': new_global, 'local': new_local}


