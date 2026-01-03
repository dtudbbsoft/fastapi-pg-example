
import enum


class OnboardingStatusEnum(enum.Enum):
    NEW = "new"
    DETAILS_COMPLETED = "details_completed"
    RULES_ACCEPTED = "rules_accepted"
    FINISHED = "finished"
