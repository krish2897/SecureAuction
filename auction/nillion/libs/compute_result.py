import os
from ..helpers.nillion_client_helper import create_nillion_client
import py_nillion_client as nillion

from dotenv import load_dotenv
load_dotenv()


async def compute_result(program_id, store_id, base_price):
    cluster_id = os.getenv("NILLION_CLUSTER_ID")
    client = create_nillion_client(
        nillion.UserKey.from_file(os.getenv("NILLION_USERKEY_PATH_PARTY_1"))
    )


    party_id = client.party_id
    party_name = "Party1"

    num_bids = len(store_id)

    if num_bids == 10:
        compute_time_secrets = nillion.Secrets({})
    elif num_bids < 10:
        sec_dict = {}
        for i in range(num_bids, 10):
            sec_dict["bid"+str(i+1)] = nillion.SecretInteger(base_price-1)

        for key, value in sec_dict.items():
            print(key)
            print(value)

        compute_time_secrets = nillion.Secrets(sec_dict)

    

    compute_bindings = nillion.ProgramBindings(program_id)
    compute_bindings.add_input_party(party_name, party_id)
    compute_bindings.add_output_party(party_name, party_id)

    try:
        await client.compute(
            cluster_id,
            compute_bindings,
            store_id,
            compute_time_secrets,
            nillion.PublicVariables({}),
        )
    except Exception as e:
        print(e)

    while True:
        compute_event = await client.next_compute_event()
        if isinstance(compute_event, nillion.ComputeFinishedEvent):
            return compute_event.result.value
            