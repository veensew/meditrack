from dataclasses import dataclass
from datetime import datetime
import uuid

@dataclass
class Notification:
    recipient_email: str
    subject: str
    content: str
    status: str
    id: str = str(uuid.uuid4())
    created_at: datetime = datetime.now()
    sent_at: datetime = None

    def to_dict(self):
        return {
            "id": self.id,
            "recipient_email": self.recipient_email,
            "subject": self.subject,
            "content": self.content,
            "status": self.status,
            "created_at": self.created_at,
            "sent_at": self.sent_at
        }

    @classmethod
    def from_dict(cls, data):
        return cls(**data)
