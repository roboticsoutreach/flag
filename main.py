from j5.backends import CommunicationError
from sbot import *
from typing import List, Optional


r = Robot()
flag_motor = r.motor_board.motors[0]

def main():
    student_id = read_rfid()
    if student_id is not None:
        print(student_id)

def read_rfid() -> Optional[str]:
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

if __name__ == "__main__":
    while True:
        main()