# -*- coding: utf-8 -*-

dir_sources = {
    'units': "zero\none\ntwo\nthree\nfour\nfive\nsix\nseven\neight\nnine",
    'teens': "\neleven\ntwelve\nthirteen\nfourteen\nfifteen\nsixteen\nseventeen\neighteen\nnineteen",
    'tens': "\nten\ntwenty\nthirty\nforty\nfifty\nsixty\nseventy\neighty\nninety",
    'hundreds': "\none hundred\ntwo hundred\nthree hundred\nfour hundred\nfive hundred\nsix hundred\nseven hundred\neight hundred\nnine hundred",
    'magnitude': "\nthousand\nmillion\nbillion\ntrillion\nquadrillion\nquintillion\nsextillion\nseptillion\noctillion\nnonillion\ndecillion",
    'fix_tens': "\n-",
    'fix_hundreds': "\n and ",
    'fix_magnitude': "\n, "
}

def numspell(value,
             _=lambda x: x,
             _n=lambda x,y,n: n <= 1 and x or y,
             sep=" ",
             **kwargs):

    result = ""
    keys = ('hundreds', 'tens', 'units', 'teens', 'magnitude')
    values = { key: 0 for key in keys }
    dirs = {}

    for key in keys:
        if key in kwargs: dirs[key] = kwargs[key].split("\n")
        elif key in dir_sources: dirs[key] = dir_sources[key].split("\n")
    for key in keys:
        key = "fix_" + key
        if key in kwargs: dirs[key] = kwargs[key].split("\n")
        elif key in dir_sources: dirs[key] = _(dir_sources[key]).split("\n")        
    
    if value == 0: return _(dirs['units'][0])
    if value < 0:
        sign = "minus"
        value = -value
    else:
        sign = ""

    while value != 0:
        values['count'] = value % 1000
        values['hundreds'] = value % 1000 / 100
        values['tens'] = value % 100 / 10
        values['units'] = value % 10

        if values['tens'] == 1 and values['units'] > 0:
            values['teens'] = values['units']
            values['tens'] = 0
            values['units'] = 0
        else:
            values['teens'] = 0
        
        current = ""
        for index, key in enumerate(keys):
            if values[key]:
                try:
                    # translate value
                    val = dirs[key][values[key]]
                    if key == "magnitude":
                        part = _n(val, val, values['count'])
                    else:
                        part = _(dirs[key][values[key]])
                except KeyError:
                    # otherwise use units
                    part = _(dirs['units'][values[key]])
                except IndexError:
                    raise Exception("numspell: value is out of range.")

                # use prefix
                try:
                    part = dirs['fix_'+key][0] + part
                except (KeyError, IndexError):
                    pass
                
                # are there any more values in current magnitude               
                last = True
                for i in range(index+1, len(keys)-1):
                    if not values[keys[i]]:
                        continue
                    else:
                        last = False
                        break

                # only suffix magnitude when over thousands
                if key == "magnitude":
                    try:
                        if values['magnitude'] > 1:
                            part += dirs['fix_'+key][1]
                        else:
                            part += sep
                    except (KeyError, IndexError):
                        part += sep
                # only suffix other keys if they're not last in current magnitude
                elif not last:
                    try:
                        part += dirs['fix_'+key][1]
                    except (KeyError, IndexError):
                        part += sep
                # separate last value from magnitude, if over hundreds
                elif values['magnitude'] > 0:
                    part += sep
                current += part
                
        result = current + result
        values['magnitude'] += 1
        value /= 1000

    if sign:
        return "%s%s%s" % (sign, sep, result)
    else:
        return result
