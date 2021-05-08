from multiprocessing import Pool
from decimal import Decimal

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Numeric
from sqlalchemy import String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.exc import StaleDataError
from sqlalchemy.orm import Session
from sqlalchemy.orm import relationship

Base = declarative_base()

TWOPLACES = Decimal(10) ** -2


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    accounts = relationship("Account", back_populates="owner")

    def __repr__(self):
        return f"{self.name} has an account"


class Account(Base):
    __tablename__ = "account"
    id = Column(Integer, primary_key=True)
    amount = Column(Numeric)
    user_id = Column(Integer, ForeignKey("user.id"))
    owner = relationship("User", back_populates="accounts", lazy="select")
    version = Column(Integer, nullable=False)  # or modified_at timestamp

    __mapper_args__ = {"version_id_col": version}

    def __repr__(self):
        return f"{self.owner.name} have ${self.amount.quantize(TWOPLACES)}"


engine = create_engine("postgresql://postgres:mysecretpassword@localhost:5432/postgres")
Base.metadata.create_all(engine)

session = Session(engine)


def create_account():
    bank_account = Account(amount=100)
    albert = User(name="Albert", accounts=[bank_account])
    session.add(albert)
    session.commit()


def update_without_read(change):
    account = session.query(Account).get(1)  # for visual purposes
    session.query(Account).filter_by(id=1).update({"amount": Account.amount + change})
    session.commit()
    print_account(account=account, change=change)


def for_update_lock(change):
    account = session.query(Account).filter_by(id=1).with_for_update().one()
    account.amount = account.amount + change
    print_account(account, change)
    session.commit()


def version_tracking(change):
    try:
        account = session.query(Account).get(1)
        account.amount = account.amount + change
        print_account(account, change)
        session.commit()
    except StaleDataError:
        # if the version changes, it would raise an error auotmatically
        print("someone has changed the account, plz retry.")


def print_account(account=None, change=0):
    account = account or session.query(Account).get(1)
    print(f"{account} changes {change}" if change else account)


def multi_process(my_callable):
    with Pool(5) as pool:
        pool.map(my_callable, [1, -1, 1, -1])


if __name__ == "__main__":
    if not session.query(Account).count():
        create_account()
    print_account()
    print("update based on column value")
    multi_process(update_without_read)
    print("update lock")
    multi_process(for_update_lock)
    print("version tracking, optimistic locking")
    multi_process(version_tracking)
