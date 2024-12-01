import pytest
from pymongo import MongoClient
from bson.objectid import ObjectId
from fastapi import HTTPException
import sys
import os

# Required row to be able to import the app folder.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.crud import CRUD
from app.config import secrets
from app.db.database import MongoDB

TEST_DB = "test_db"
TEST_COLLECTION_1 = "test_collection_1"
TEST_COLLECTION_2 = "test_collection_2"
TEST_RELATIONSHIP_FIELD = "relationship_field"


def test01_database_connect():
    pytest.mongodb = MongoDB(secrets.DATABASE_URL, TEST_DB)
    pytest.mongodb.connect()
    Coll_1_DB = pytest.mongodb.get_collection(TEST_COLLECTION_1)
    Coll_1_DB.create_index(TEST_RELATIONSHIP_FIELD, unique=True)
    Coll_2_DB = pytest.mongodb.get_collection(TEST_COLLECTION_2)

    pytest.Coll_1_CRUD = CRUD(
        Coll_1_DB, cascaded_collection=Coll_2_DB, cascaded_field=TEST_RELATIONSHIP_FIELD
    )
    pytest.Coll_2_CRUD = CRUD(
        Coll_2_DB, related_collection=Coll_1_DB, reference_field=TEST_RELATIONSHIP_FIELD
    )


def test02_crud():
    # Test create
    data = {"name": "test_item", TEST_RELATIONSHIP_FIELD: "1"}
    data_rel_1 = {"name": "test_rel_item_1", TEST_RELATIONSHIP_FIELD: "1"}
    data_rel_2 = {"name": "test_rel_item_2", TEST_RELATIONSHIP_FIELD: "1"}

    # Should raise an exception since the related object doesn't exist
    with pytest.raises(HTTPException):
        pytest.Coll_2_CRUD.create(data_rel_1)

    pytest.created = pytest.Coll_1_CRUD.create(data)
    assert pytest.created == data

    pytest.created_rel_1 = pytest.Coll_2_CRUD.create(data_rel_1)
    assert pytest.created_rel_1 == data_rel_1
    pytest.created_rel_2 = pytest.Coll_2_CRUD.create(data_rel_2)
    assert pytest.created_rel_2 == data_rel_2
    # assert created["name"] == "test_item"

    # Test read
    with pytest.raises(HTTPException):
        read = pytest.Coll_1_CRUD.read("doesn't exist")
    read = pytest.Coll_1_CRUD.read(str(pytest.created["_id"]))
    assert read is not None
    assert read == pytest.created

    # Test update
    update_data = {"name": "updated_item"}
    with pytest.raises(HTTPException):
        updated_document = pytest.Coll_2_CRUD.update("doesn't exist", update_data)
    updated_document = pytest.Coll_2_CRUD.update(
        str(pytest.created_rel_1["_id"]), update_data
    )
    assert updated_document["name"] == "updated_item"

    # Test successfull find
    found_documents = pytest.Coll_2_CRUD.find({"name": "updated_item"})
    assert len(found_documents) == 1
    assert found_documents[0]["name"] == "updated_item"
    # Test unsuccessfull find
    found_documents = pytest.Coll_2_CRUD.find({"name": "doesn't exist"})
    assert len(found_documents) == 0

    # Test successfull find_one
    found_one = pytest.Coll_2_CRUD.find_one({"name": "updated_item"})
    assert found_one is not None
    assert found_one["name"] == "updated_item"
    # Test unsuccessfull find_one
    found_one = pytest.Coll_2_CRUD.find_one({"name": "doesn't exist"})
    assert found_one is None

    # Test count of existing object
    count = pytest.Coll_2_CRUD.count({"name": "updated_item"})
    assert count == 1
    # Test count of non-existing object
    count = pytest.Coll_2_CRUD.count({"name": "doesn't exist"})
    assert count == 0

    # Test aggregate for existing object
    pipeline = [{"$match": {"name": "updated_item"}}, {"$project": {"name": 1}}]
    aggregated = pytest.Coll_2_CRUD.aggregate(pipeline)
    assert len(aggregated) == 1
    assert aggregated[0]["name"] == "updated_item"
    # Test aggregate for non-existing object
    pipeline = [{"$match": {"name": "doesn't exist"}}, {"$project": {"name": 1}}]
    aggregated = pytest.Coll_2_CRUD.aggregate(pipeline)
    assert len(aggregated) == 0


def test03_delete():
    # Test delete
    deleted, deleted_document = pytest.Coll_2_CRUD.delete(
        str(pytest.created_rel_2["_id"])
    )
    assert deleted
    assert deleted_document["name"] == "test_rel_item_2"

    # Test cascade delete
    deleted, deleted_document = pytest.Coll_1_CRUD.delete(str(pytest.created["_id"]))
    assert deleted
    assert deleted_document["name"] == "test_item"


def test04_drop_close():
    pytest.mongodb.drop()
    pytest.mongodb.close()
