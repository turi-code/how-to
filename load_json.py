# Load a JSON formated file into an SFrame
import graphlab as gl

# The following example assumes that the file is formated with the JSON 
# standards without any superflous \n characters. To remove \n characters from
# the file, you can download the file and # then run the following perl command:
# 
# perl -p -e 's/\n//' customers.json
def load_json_from_file(filename):
    """
    Load JSON from a file.

    @input  filename  Name of the file to be read.
    @returns Output SFrame

    """
    # Read the entire file into a SFrame with one row
    sf = gl.SFrame.read_csv(filename, delimiter='\n', header=False)
    #  +--------------------------------+
    #  |               X1               |
    #  +--------------------------------+
    #  | [{'Phone': '0845 46 45', ' ... |
    #  +--------------------------------+
    
    # Stack the single large row into many rows. After stacking, each row is a
    # dictionary that contains the data. 
    sf = sf.stack('X1')
    
    #+--------------------------------+
    #|               X1               |
    #+--------------------------------+
    #| {'Phone': '0845 46 45', 'N ... |
    #| {'Phone': '0800 744 7888', ... |
    #| {'Phone': '(01303) 294965' ... |
    #|              ...               |
    #+--------------------------------+
    
    # The dictionary can be unpacked to generate the individual columns.
    sf = sf.unpack('X1', column_name_prefix='')
    return sf


# User the function on a toy example
sf = load_json_from_file(
        'https://s3.amazonaws.com/GraphLab-Datasets/how-to/customers.json')

#+-------------+------------------+----------------+-------+
#|     City    |       Name       |     Phone      |  Zip  |
#+-------------+------------------+----------------+-------+
#| Acquafredda |  Shafira Ramsey  |   0845 46 45   | 44552 |
#|  Waterbury  | Mikayla Montoya  | 0800 744 7888  | 49200 |
#|   Sasaram   |  Prescott Haney  | (01303) 294965 | 69889 |
#|     ...     |       ...        |      ...       |  ...  |
#+-------------+------------------+----------------+-------+
