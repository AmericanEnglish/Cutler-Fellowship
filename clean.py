from numpy import array

def array_from_file(kplrfile):
    """(str) -> NumPy Array, dict


    Takes the location of a kplrfile and returns a multi dimension array. Also 
    returns and dictionary of "defaults"""
    # Read in files
    with open(kplrfile, 'r') as kepler_dat:
        defaults = {}
        data = {}
        for line in kepler_dat:
            line = line.strip()
            if line[0] == "\\":
                line = line.split('=')
                if len(line) < 2:
                    defaults[line[0]] = None
                else:
                    defaults[line[0]] = line[1]
                    # Determine type, str, and convert correctly
            elif line[0] == '|':
                line = line.split()
                
    # Read & Generate defaults
    # Read & Generate values array dtype={name:[column1, column2]}