from enum import Enum

class AccountStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    DELETED = "deleted"

class SubscriptionPlan(Enum):
    FREE = "free"
    BASIC = "basic"
    PREMIUM = "premium"

class EmploymentType(Enum):
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    CONTRACTOR = "contractor"
    INTERN = "intern"

class RemotePreference(Enum):
    REMOTE = "remote"
    ON_SITE = "on_site"
    HYBRID = "hybrid"

class ApplicationStatus(Enum):
    PENDING = "pending"
    APPLIED = "applied"
    APPROVED = "approved"
    REJECTED = "rejected"
    INTERVIEW_SCHEDULED = "interview_scheduled"

class InterviewStatus(Enum):
    SCHEDULED = "scheduled"
    COMPLETED = "completed"
    CANCELED = "canceled"
    RESCHEDULED = "rescheduled"

class InterviewMode(Enum):
    IN_PERSON = "in_person"
    VIDEO_CALL = "video_call"
    PHONE_CALL = "phone_call"

class NotififcationType(Enum):
    EMAIL = "email"
    SMS = "sms"
    PUSH_NOTIFICATION = "push_notification"

class CompanySize(Enum):
    SMALL = "small"                     #5-50 employees
    MEDIUM = "medium"                   #51-200 employees
    LARGE = "large"                     #201-1000 employees
    ENTERPRISE = "enterprise"           #1001+ employees    

class JobStatus(Enum):
    OPEN = "open"
    CLOSED = "closed"
    ON_HOLD = "on_hold"
    FILLED = "filled"
    
class AIProvider(Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    COHERE = "cohere"
    AI21 = "ai21"