from app.schemes.points import PointPublicWithRegion, PointPublic
from app.schemes.regions import RegionPublic
from app.schemes.travels import TravelPublic
from app.schemes.users import UserPublic, UserPublicWithRegion

PointPublicWithRegion.model_rebuild()
UserPublicWithRegion.model_rebuild()
TravelPublic.model_rebuild()
