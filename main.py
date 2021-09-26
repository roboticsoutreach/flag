from j5.backends import CommunicationError
from sbot import *
from typing import List, Optional


r = Robot()

def read_rfid() -> Optional[str]:
    result: Optional[str] = None

    try:
        response: List[str] = r.arduino._command("N")
        if len(response) != 1:
            print("Arduino sent too many responses")
            return None
        else:
            return response[0]

    except CommunicationError as e:
        print(e)
        return None
