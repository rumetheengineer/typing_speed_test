from dataclasses import dataclass


@dataclass
class TypingStats:
    """
    A dataclass containing the final stats for the typing speed test.
    The class calculates the words per minute (wpm) and the characters per second(cps) as properties.
    Also creates the summary displayed at the end of the test
    """
    #Variables
    characters_typed : int = 0
    words_typed : int = 0
    time_spent : float = 0
    accuracy : float = 0

    @property
    def wpm(self) -> float:
        """Words per minute calculated from the updated statistic variables"""
        return (self.words_typed/self.time_spent) *60 if self.time_spent >0 else 0.00

    @property
    def cps(self) -> float:
        """Average characters typed per second. Calculated from updated variable"""
        return (self.characters_typed/self.time_spent) if self.time_spent >0 else 0.00

    @property
    def summary(self) -> str:
        """Returns the string containing the stat summary for information label and final display"""
        return (f"Typing Stats:\n"
                f"Characters Per Second (CPS): {self.cps:.2f}\n"
                f"Words Per Minute (WPM): {self.wpm:.2f}\n"
                f"Time Spent (seconds): {self.time_spent:.2f}\n"
                f"Accuracy: {self.accuracy:.2f}%")
    

