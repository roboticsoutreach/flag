from j5.backends import CommunicationError
from j5.components.piezo import Note
from sbot import *
from typing import List, Optional
from random import choice

import time

class FlagBot:
    """A robot that moves a flag when it sees a student id."""

    MAX_FLAG_HEIGHT = 5

    def __init__(self) -> None:
        self._r = Robot(wait_start=False)

        self.target_power = -0.2
        self.flag_height = 0

        self._last_seen_card = time.time()
        self.direction = 1

        self._startup()

    @property
    def r(self) -> Robot:
        """Read only property for robot object."""
        return self._r

    def _startup(self):
        for n in Note:
            self.r.power_board.piezo.buzz(0.03, n)
            time.sleep(0.03)
        self.r.power_board.piezo.buzz(0.2, Note.C6)

        self.power = 0  # HACK AROUND BUG

    @property
    def power(self) -> float:
        return self.r.motor_board.motors[0].power

    @power.setter
    def power(self, val: float) -> None:
        self.r.motor_board.motors[0].power = val


    def loop(self) -> None:
        # If it's too low and going down, or too high and going up
        if (self.flag_height <= 0 and self.power < 0 or
                self.flag_height >= self.MAX_FLAG_HEIGHT and self.power > 0):
            self.power = 0  # Cap flag displacement

        if self.read_rfid() is not None:
            # pass
            self.direction = -1 * self.direction

        print(self._last_seen_card + 2 - time.time())
        if self._last_seen_card + 2 - time.time() > 0:
            self.power = self.direction * 0.2
        else:
            self.power = 0

    def read_rfid(self) -> Optional[str]:
        """Returns the student ID of the card scanned, if present."""
        try:
            response: List[str] = self.r.arduino._backend._command("N")
            if len(response) != 1:
                print("Arduino sent too many responses")
                return None
            elif len(response[0]) < 8:
                return None
            else:
                
                #TODO: Write to file here.
                self._last_seen_card = time.time()
                self.r.power_board.piezo.buzz(0.1, choice([n for n in Note]))
                return response[0]

        except CommunicationError as e:
            print(e)
            return None

def main() -> None:

    flag = FlagBot()

    while True:
        flag.loop()

if __name__ == "__main__":
    main()
