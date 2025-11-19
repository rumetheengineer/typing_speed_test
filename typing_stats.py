from dataclasses import dataclass


@dataclass
class TypingStats:
    characters_typed : int = 0
    words_typed : int = 0
    time_spent : float = 0
    accuracy : float = 0

    @property
    def wpm(self) -> float:
        return (self.words_typed/self.time_spent) *60 if self.time_spent >0 else 0.00

    @property
    def cps(self) -> float:
        return (self.characters_typed/self.time_spent) if self.time_spent >0 else 0.00

    @property
    def summary(self) -> str:
        return (f"Typing Stats:\n"
                f"Characters Per Second (CPS): {self.cps:.2f}\n"
                f"Words Per Minute (WPM): {self.wpm:.2f}\n"
                f"Time Spent (seconds): {self.time_spent:.2f}\n"
                f"Accuracy: {self.accuracy:.2f}%")
    

