from faker import Faker
import random
from models.User_model import User
from models.Transaction_model import Transaction

fake = Faker()


# generate fake data for users and users transaction
def generate_fake_data(db, num_users=100, num_transactions=1000):
    users_resp = {"success": 0, "failed": 0}
    transactions_resp = {"success": 0, "failed": 0}
    for _ in range(num_users):
        try:
            user = {
                "name": fake.name(),
                "email": fake.email(),
                "created_at": fake.date_time_this_decade(),
            }

            user = User(
                name=fake.name(),
                email=fake.email(),
                created_at=fake.date_time_this_decade(),
            )
            db.add(user)
            db.commit()
            users_resp["success"] += 1
        except Exception as e:
            print(e)
            users_resp["failed"] += 1

    for _ in range(num_transactions):
        try:

            transc = Transaction(
                user_id=random.randint(4, num_users),
                amount=round(random.uniform(1, 1000), 2),
                timestamp=fake.date_time_this_year(),
                type=random.choice(["credit", "debit"]),
            )

            db.add(transc)
            db.commit()
            transactions_resp["success"] += 1
        except Exception as e:
            print(e)
            transactions_resp["failed"] += 1

    return {"user": users_resp, "transaction": transactions_resp}
