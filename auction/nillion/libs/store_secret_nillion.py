import os
import py_nillion_client as nillion

from ..helpers.nillion_client_helper import create_nillion_client

from dotenv import load_dotenv
load_dotenv()

async def store_secret_in_nillion(program_id, value, bid_no):
    cluster_id = os.getenv("NILLION_CLUSTER_ID")

    client = create_nillion_client(
        nillion.UserKey.from_file(os.getenv("NILLION_USERKEY_PATH_PARTY_1"))
    )

    print(cluster_id)

    party_id = client.party_id
    print(party_id)
    party_name = "Party1"

    secret = nillion.Secrets({
        "bid"+str(bid_no): nillion.SecretInteger(value)
    })

    secret_bindings = nillion.ProgramBindings(program_id)
    secret_bindings.add_input_party(party_name, party_id)

    print(program_id)

    # permissions = nillion.Permissions.default_for_user(client.user_id)
    # compute_permissions = {
    #         user_id_1: {program_id},
    #     }


    store_id = await client.store_secrets(
        cluster_id, secret_bindings, secret, None
    )
    print(store_id)

    return store_id