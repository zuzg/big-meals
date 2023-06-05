from cassandra.cluster import Cluster, Session
from cassandra.policies import RoundRobinPolicy
from cassandra import ConsistencyLevel

from .Tables import Tables
from .query import QueryMeal
from .MockData import MockData


IP_ADDRESS = "127.0.0.1"
PORT = "9042"
KEYSPACE = "bigmeals"
CONSISTENCY = ConsistencyLevel.QUORUM
REPLICATION_FACTOR = 3


def create_keyspace(session: Session) -> None:
    statement = (
        f"CREATE KEYSPACE IF NOT EXISTS {KEYSPACE} "
        + "WITH REPLICATION = {'class': 'SimpleStrategy', 'replication_factor': "
        + f"'{REPLICATION_FACTOR}'" + "}"
    )
    session.execute(statement)
    session.set_keyspace(KEYSPACE)


def create_tables(session: Session) -> None:
    for table in Tables.all:
        session.execute(table)


def fill_meals(query: QueryMeal, n: int = 5) -> None:
    for _ in range(n):
        mock = MockData()
        query.insert(mock.food_type, mock.provider, mock.pickup_time)


def prepare_cassandra() -> Session:
    cluster = Cluster(
        [IP_ADDRESS],
        port=PORT,
        protocol_version=5,
        load_balancing_policy=RoundRobinPolicy(),
    )
    session = cluster.connect()
    create_keyspace(session)
    create_tables(session)
    query = QueryMeal(session)
    fill_meals(query)
    return session
