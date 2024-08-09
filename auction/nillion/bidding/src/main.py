from nada_dsl import *

# Initialize input bids variables.
def initialize_bids(n_bids, party):
    bids = []

    for i in range(n_bids):
        bids.append(SecretInteger(Input(name="bid"+str(i+1), party=party)))

    return bids


"""
Function to find the highest bid ammount. First maximum bid amount is determined
and all the bids having the maximum amount is set to 2 in output list.
"""
def find_winners(n_bids, bids, party):
    max_value = bids[0]

    for i in range(1, n_bids):
        max_value = (max_value < bids[i]).if_else(bids[i], max_value)

    output = []
    for i in range(n_bids):
        val = (bids[i] == max_value).if_else(Integer(2), Integer(1))
        output.append(Output(val, "output"+str(i+1), party=party))

    return output


def nada_main():
    n_bids = 10 # number of input bids.

    party = Party('Party1')
    bids = initialize_bids(n_bids, party)

    output = find_winners(n_bids, bids, party)

    return output

