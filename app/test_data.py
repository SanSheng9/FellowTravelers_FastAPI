from datetime import datetime

from fastapi import APIRouter

from app.database import SessionDep
from app.models.points import Point
from app.models.regions import Region
from app.models.travels import Travel, TravelUserLink
from app.models.users import User

router = APIRouter()

@router.get("/create_test_data/", tags=['Test'])
def create_test_data(session: SessionDep):
    region_1 = Region(name="Приморский", type="край")
    region_2 = Region(name="Хабаровский", type="край")
    region_3 = Region(name="Камчатский", type="край")
    session.add(region_1)
    session.add(region_2)
    session.add(region_3)

    point_1 = Point(name="Владивосток", type="город", ocatd="123", code="123", region=region_1)
    point_2 = Point(name="Уссурийск", type="город", ocatd="123", code="123", region=region_1)

    point_3 = Point(name="Хабаровск", type="город", ocatd="123", code="123", region=region_2)
    point_4 = Point(name="Советская гавань", type="город", ocatd="123", code="123", region=region_2)

    point_5 = Point(name="Вилючинск", type="город", ocatd="123", code="123", region=region_3)
    point_6 = Point(name="Елизово", type="город", ocatd="123", code="123", region=region_3)

    session.add(point_1)
    session.add(point_2)
    session.add(point_3)
    session.add(point_4)
    session.add(point_5)
    session.add(point_6)

    user_1 = User(username="Vasilii228", chat_id="1", region=region_1)
    user_2 = User(username="Petya1337", chat_id="2", region=region_1)
    user_2_1 = User(username="ProstoKissa", chat_id="21", region=region_1)

    user_3 = User(username="Masha_", chat_id="3", region=region_2)
    user_4 = User(username="Natasha_", chat_id="4", region=region_2)

    user_5 = User(username="Iluha_loh", chat_id="5", region=region_3)
    user_6 = User(username="Pizduk1488", chat_id="6", region=region_3)

    session.add(user_1)
    session.add(user_2)
    session.add(user_2_1)
    session.add(user_3)
    session.add(user_4)
    session.add(user_5)
    session.add(user_6)

    travel_1 = Travel(date=datetime(2025, 6, 1, 8, 0),
                      starting_point=point_1,
                      end_point=point_2,
                      driver=user_1,
                      number_of_available_seats=2,
                      current_number_of_available_seats=2
                      )

    travel_2 = Travel(date=datetime(2025, 6, 11, 8, 30),
                      starting_point=point_3,
                      end_point=point_4,
                      driver=user_3,
                      number_of_available_seats=3,
                      current_number_of_available_seats=3
                      )

    travel_3 = Travel(date=datetime(2025, 6, 15, 14, 0),
                      starting_point=point_5,
                      end_point=point_6,
                      driver=user_5,
                      number_of_available_seats=1,
                      current_number_of_available_seats=1
                      )

    session.add(travel_1)
    session.add(travel_2)
    session.add(travel_3)

    passenger_1 = TravelUserLink(
        travel_id = 1,
        user_id = 2,
    )

    passenger_2 = TravelUserLink(
        travel_id = 1,
        user_id = 3,
    )

    session.add(passenger_1)
    session.add(passenger_2)

    session.commit()

