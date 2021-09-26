from j5.backends import CommunicationError
from sbot import *
from typing import List, Optional

import time

r = Robot()

def main() -> None:
    flag_motor = r.motor_board.motors[0]
    target_power: float = -0.2
    flag_height: float = 0
    MAX_HEIGHT: float = target_power * 10  # Find this value experimentally
    
    start_time: float = time.time()
    while True:
        # If it's too low and going down, or too high and going up
        if (flag_height <= target_power and flag_motor.power < 0 or
                flag_height >= MAX_HEIGHT and flag_motor.power > 0):
            flag_motor.power = 0  # Cap flag displacement

        student_id = read_rfid()

        # Update elapsed time for this loop. Do it here
        # so it's not affected by motor power updates.
        loop_time: float = time.time() - start_time
        flag_height += flag_motor.power * loop_time

        start_time = time.time()
        if student_id is not None:
            print(student_id)
            target_power, flag_motor.power = -target_power  # Swap direction


def read_rfid() -> Optional[str]:
    """Returns the student ID of the card scanned, if present."""
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
    main()