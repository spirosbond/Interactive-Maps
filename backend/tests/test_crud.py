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
    # Test database connection and initialization of CRUD objects.
    pytest.mongodb = MongoDB(secrets.DATABASE_URL, TEST_DB)
    pytest.mongodb.connect()
    Coll_1_DB = pytest.mongodb.get_collection(TEST_COLLECTION_1)
    Coll_1_DB.create_index(
        TEST_RELATIONSHIP_FIELD, unique=True
    )  # Ensure unique index on a field.
    Coll_2_DB = pytest.mongodb.get_collection(TEST_COLLECTION_2)

    # Initialize CRUD objects with cascading and reference relationships.
    # When Coll_1_DB object is deleted or updated, this cascades to Coll_2_DB
    pytest.Coll_1_CRUD = CRUD(
        Coll_1_DB, cascaded_collection=Coll_2_DB, cascaded_field=TEST_RELATIONSHIP_FIELD
    )
    # When Coll_2_DB object is created or updated, we validate that the reference exists in Coll_1_DB
    pytest.Coll_2_CRUD = CRUD(
        Coll_2_DB, related_collection=Coll_1_DB, reference_field=TEST_RELATIONSHIP_FIELD
    )


def test02_crud():
    # Test CRUD operations with related and cascaded collections.

    # Prepare data for tests.
    data = {"name": "test_item", TEST_RELATIONSHIP_FIELD: "1"}
    data_rel_1 = {"name": "test_rel_item_1", TEST_RELATIONSHIP_FIELD: "1"}
    data_rel_2 = {"name": "test_rel_item_2", TEST_RELATIONSHIP_FIELD: "1"}

    # Test create: Should raise an exception since the related object doesn't exist.
    with pytest.raises(HTTPException):
        pytest.Coll_2_CRUD.create(data_rel_1)

    # Test successful creation of the main document.
    pytest.created = pytest.Coll_1_CRUD.create(data)
    assert pytest.created == data

    # Test creation of related documents after the main document exists.
    pytest.created_rel_1 = pytest.Coll_2_CRUD.create(data_rel_1)
    assert pytest.created_rel_1 == data_rel_1
    pytest.created_rel_2 = pytest.Coll_2_CRUD.create(data_rel_2)
    assert pytest.created_rel_2 == data_rel_2

    # Test read: Should raise an exception if the document does not exist.
    with pytest.raises(HTTPException):
        pytest.Coll_1_CRUD.read("doesn't exist")

    # Test successful retrieval of an existing document.
    read = pytest.Coll_1_CRUD.read(str(pytest.created["_id"]))
    assert read is not None
    assert read == pytest.created

    # Test update: Should raise an exception if the document does not exist.
    update_data = {"name": "updated_item"}
    with pytest.raises(HTTPException):
        pytest.Coll_2_CRUD.update("doesn't exist", update_data)

    # Test successful update of an existing document.
    updated_document = pytest.Coll_2_CRUD.update(
        str(pytest.created_rel_1["_id"]), update_data
    )
    assert updated_document["name"] == "updated_item"

    # Test successful update of an existing document with cascade.
    update_data = {TEST_RELATIONSHIP_FIELD: "2"}
    updated_document = pytest.Coll_1_CRUD.update(
        str(pytest.created["_id"]), update_data
    )
    assert updated_document[TEST_RELATIONSHIP_FIELD] == "2"
    updated_rel_document_1 = pytest.Coll_2_CRUD.read(str(pytest.created_rel_1["_id"]))
    updated_rel_document_2 = pytest.Coll_2_CRUD.read(str(pytest.created_rel_2["_id"]))
    assert (
        updated_rel_document_1[TEST_RELATIONSHIP_FIELD]
        == updated_rel_document_2[TEST_RELATIONSHIP_FIELD]
        == "2"
    )

    # Test successful find operation for existing documents.
    found_documents = pytest.Coll_2_CRUD.find({"name": "updated_item"})
    assert len(found_documents) == 1
    assert found_documents[0]["name"] == "updated_item"

    # Test unsuccessful find operation for non-existing documents.
    found_documents = pytest.Coll_2_CRUD.find({"name": "doesn't exist"})
    assert len(found_documents) == 0

    # Test successful find_one operation for existing documents.
    found_one = pytest.Coll_2_CRUD.find_one({"name": "updated_item"})
    assert found_one is not None
    assert found_one["name"] == "updated_item"

    # Test unsuccessful find_one operation for non-existing documents.
    found_one = pytest.Coll_2_CRUD.find_one({"name": "doesn't exist"})
    assert found_one is None

    # Test count of existing documents.
    count = pytest.Coll_2_CRUD.count({"name": "updated_item"})
    assert count == 1

    # Test count of non-existing documents.
    count = pytest.Coll_2_CRUD.count({"name": "doesn't exist"})
    assert count == 0

    # Test aggregation pipeline for existing documents.
    pipeline = [{"$match": {"name": "updated_item"}}, {"$project": {"name": 1}}]
    aggregated = pytest.Coll_2_CRUD.aggregate(pipeline)
    assert len(aggregated) == 1
    assert aggregated[0]["name"] == "updated_item"

    # Test aggregation pipeline for non-existing documents.
    pipeline = [{"$match": {"name": "doesn't exist"}}, {"$project": {"name": 1}}]
    aggregated = pytest.Coll_2_CRUD.aggregate(pipeline)
    assert len(aggregated) == 0


def test03_delete():
    # Test deletion of documents and cascading behavior.

    # Test deletion of a single document.
    deleted, deleted_document = pytest.Coll_2_CRUD.delete(
        str(pytest.created_rel_2["_id"])
    )
    assert deleted
    assert deleted_document["name"] == "test_rel_item_2"

    # Test cascading deletion of related documents.
    deleted, deleted_document = pytest.Coll_1_CRUD.delete(str(pytest.created["_id"]))
    assert deleted
    assert deleted_document["name"] == "test_item"


def test04_drop_close():
    # Cleanup: Drop the test database and close the connection.
    pytest.mongodb.drop()
    pytest.mongodb.close()
