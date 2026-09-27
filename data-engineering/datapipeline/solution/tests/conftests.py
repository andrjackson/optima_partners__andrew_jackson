import pytest
from pipeline import create_spark_session

@pytest.fixture(scope="session")
def spark():
    session = create_spark_session("f1-race-stats-tests")
    # small session, small data so just one partition
    session.conf.set("spark.sql.shuffle.partitions", "1")
    yield session
    session.stop()