from dataclasses import dataclass

@dataclass
class AlertData:
    headline: str
    description: str
    instruction: str

    def to_dict(self):
        return {
            'ALERT_HEADLINE': self.headline,
            'ALERT_DESCRIPTION': self.description,
            'ALERT_INSTRUCTION': self.instruction,
        }

    @classmethod
    def empty(cls):
        return AlertData("Some Alert Headline", "Some Alert Description", "Some Alert Instruction")