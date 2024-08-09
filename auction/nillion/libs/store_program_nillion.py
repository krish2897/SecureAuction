from ..helpers.nillion_client_helper import create_nillion_client
import py_nillion_client as nillion
import os

from django.conf import settings

from dotenv import load_dotenv
load_dotenv()


async def store_program_in_nillion():
    cluster_id = os.getenv("NILLION_CLUSTER_ID")
    client = create_nillion_client(
        nillion.UserKey.from_file(os.getenv("NILLION_USERKEY_PATH_PARTY_1"))
    )

    
    program_name = "main"
    program_mir_path = os.path.join(settings.BASE_DIR, f"auction/nillion/bidding/target/{program_name}.nada.bin")

    await client.store_program(cluster_id, program_name, program_mir_path)

    user_id = client.user_id
    program_id = f"{user_id}/{program_name}"

    print(cluster_id)
    return program_id

