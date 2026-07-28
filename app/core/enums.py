from enum import Enum

#User
class AccountStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    SUSPENDED = "SUSPENDED"
    DELETED = "DELETED"

class SubscriptionPlan(str, Enum):
    FREE = "FREE"
    BASIC = "BASIC"
    PREMIUM = "PREMIUM"


#Jobs
class EmploymentType(str, Enum):
    FULL_TIME = "FULL_TIME"
    PART_TIME = "PART_TIME"
    CONTRACTOR = "CONTRACTOR"
    INTERN = "INTERN"

class RemoteType(str, Enum):
    REMOTE = "REMOTE"
    ON_SITE = "ON_SITE"
    HYBRID = "HYBRID"

class JobStatus(str, Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"
    ON_HOLD = "ON_HOLD"
    FILLED = "FILLED"


#Applications
class ApplicationStatus(str, Enum):
    PENDING = "PENDING"
    FAILED = "FAILED"
    APPLIED = "APPLIED"
    INTERVIEW_SCHEDULED = "INTERVIEW_SCHEDULED"
    OFFER_RECEIVED = "OFFER_RECEIVED"
    REJECTED = "REJECTED"
    WITHDRAWN = "WITHDRAWN"

class InterviewStatus(str, Enum):
    SCHEDULED = "SCHEDULED"
    COMPLETED = "COMPLETED"
    CANCELED = "CANCELED"
    RESCHEDULED = "RESCHEDULED"

class InterviewMode(str, Enum):
    IN_PERSON = "IN_PERSON"
    VIDEO_CALL = "VIDEO_CALL"
    PHONE_CALL = "PHONE_CALL"


#Notifications
class NotificationType(str, Enum):
    EMAIL = "EMAIL"
    SMS = "SMS"
    PUSH_NOTIFICATION = "PUSH_NOTIFICATION"


#Company
class CompanySize(str, Enum):
    SMALL = "SMALL"                     #5-50 employees
    MEDIUM = "MEDIUM"                   #51-200 employees
    LARGE = "LARGE"                     #201-1000 employees
    ENTERPRISE = "ENTERPRISE"           #1001+ employees    


#AI Providers
class AIProvider(str, Enum):
    OPENAI = "OPENAI"
    ANTHROPIC = "ANTHROPIC"
    COHERE = "COHERE"
    AI21 = "AI21"


#Storage Providers
class StorageProvider(str, Enum):
    AWS_S3 = "AWS_S3"
    GOOGLE_CLOUD_STORAGE = "GOOGLE_CLOUD_STORAGE"
    CLOUDFLARE_R2 = "CLOUDFLARE_R2"
    LOCAL = "LOCAL"


#Mime Types
class MimeType(str, Enum):
    PDF = "application/pdf"
    DOCX = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    DOC = "application/msword"
    TXT = "text/plain"
    JPEG = "image/jpeg"
    PNG = "image/png"
    GIF = "image/gif"
    MP4 = "video/mp4"
    MP3 = "audio/mpeg"

#Skills
class SkillCategory(str, Enum):
    TECHNICAL = "TECHNICAL"
    SOFTWARE = "SOFTWARE"
    LANGUAGE = "LANGUAGE"
    CERTIFICATION = "CERTIFICATION"
    SOFT_SKILL = "SOFT_SKILL"
    MANAGEMENT = "MANAGEMENT"
    BUSINESS = "BUSINESS"
    DESIGN = "DESIGN"
    SALES = "SALES"
    MARKETING = "MARKETING"
    FINANCE = "FINANCE"
    HEALTHCARE = "HEALTHCARE"
    LEGAL = "LEGAL"
    EDUCATION = "EDUCATION"
    TRADES = "TRADES"
    OTHER = "OTHER"

#JobSources
class SourceType(str, Enum):
    SCRAPABLE = "SCRAPABLE"
    FREEAPI = "FREEAPI"
    PAIDAPI = "PAIDAPI"

class ModelProviders(str, Enum):
    OPENAI = "OPENAI"
    ANTHROPIC = "ANTHROPIC"
    GOOGLE = "GOOGLE"
    GROQ = "GROQ"
    MISTRAL = "MISTRAL"
    DEEPSEEK = "DEEPSEEK"
    OLLAMA = "OLLAMA"
    OTHER = "OTHER"

class Currency(str, Enum):
    INR = "INR"
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"
    CAD = "CAD"
    AUD = "AUD"
    SGD = "SGD"
    AED = "AED"
    JPY = "JPY"

class SkillImportance(str, Enum):
    REQUIRED = "REQUIRED"
    PREFERRED = "PREFERRED"
    OPTIONAL = "OPTIONAL"

class SkillProficiency(str, Enum):
    BEGINNER = "BEGINNER"
    INTERMEDIATE = "INTERMEDIATE"    
    EXPERT = "EXPERT"


class AnalysisType(str, Enum):
    LIGHT = "LIGHT"
    INTERMEDIATE = "INTERMEDIATE"
    DEEP = "DEEP"

class ActivityAction(str, Enum):
    LOGIN = "LOGIN"
    LOGOUT = "LOGOUT"

    CREATE = "CREATE"
    UPDATE = "UPDATE"
    DELETE = "DELETE"

    APPLY_JOB = "APPLY_JOB"
    SAVE_JOB = "SAVE_JOB"
    UNSAVE_JOB = "UNSAVE_JOB"

    GENERATE_RESUME = "GENERATE_RESUME"
    GENERATE_COVER_LETTER = "GENERATE_COVER_LETTER"

    UPLOAD_DOCUMENT = "UPLOAD_DOCUMENT"

    ANALYZE_RESUME = "ANALYZE_RESUME"


class EntityType(str, Enum):
    USER = "USER"
    DOCUMENT = "DOCUMENT"
    RESUME = "RESUME"
    JOB = "JOB"
    APPLICATION = "APPLICATION"
    COVER_LETTER = "COVER_LETTER"
