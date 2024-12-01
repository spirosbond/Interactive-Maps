from typing import Tuple, Any, Dict, List, Optional
from pymongo.collection import Collection
from bson import ObjectId
from fastapi import HTTPException, status
from pymongo.errors import PyMongoError


class CRUD:
    def __init__(
        self,
        collection: Collection,
        related_collection: Optional[Collection] = None,
        reference_field: Optional[str] = None,
        cascaded_collection: Optional[Collection] = None,
        cascaded_field: Optional[str] = None,
    ):
        """
        Initialize the CRUD object with a specific MongoDB collection.
        :param collection: The pymongo collection instance.
        """
        if collection is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Collection must not be None.",
            )
        self.collection = collection
        self.related_collection = related_collection
        self.reference_field = reference_field
        self.cascaded_collection = cascaded_collection
        self.cascaded_field = cascaded_field

    def _validate_reference(self, data: Dict) -> None:
        """
        Validate that the reference field exists in the related collection.
        :param data: The document data being validated.
        """
        if self.related_collection is not None and self.reference_field is not None:
            ref_value = data.get(self.reference_field)
            if ref_value is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"{self.reference_field} is required for this operation.",
                )
            if not self.related_collection.find_one({self.reference_field: ref_value}):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Reference {self.reference_field} with value {ref_value} does not exist.",
                )

    def _validate_object_id(self, document_id: str) -> ObjectId:
        """
        Validate and convert a string to an ObjectId.
        :param document_id: The document's ID as a string.
        :return: The ObjectId instance.
        """
        if not isinstance(document_id, str):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Document ID must be a string.",
            )
        try:
            return ObjectId(document_id)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid ObjectId: {document_id}",
            )

    def create(self, data: Dict) -> Dict:
        """
        Insert a new document into the collection.
        :param data: The data to be inserted.
        :return: The inserted document with its `_id`.
        """
        if not isinstance(data, dict) or not data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Data must be a non-empty dictionary.",
            )

        if self.reference_field in data.keys():
            self._validate_reference(data)

        try:
            result = self.collection.insert_one(data)
            data["_id"] = result.inserted_id
            return data
        except PyMongoError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error: {str(e)}",
            )

    def read(self, document_id: str) -> Optional[Dict]:
        """
        Retrieve a document by its ID.
        :param document_id: The document's ID as a string.
        :return: The document if found, otherwise None.
        """
        object_id = self._validate_object_id(document_id)
        try:
            document = self.collection.find_one({"_id": object_id})
            if not document:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Document not found."
                )
            return document
        except PyMongoError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error: {str(e)}",
            )

    def update(self, document_id: str, update_data: Dict) -> Optional[Dict]:
        """
        Update a document by its ID.
        :param document_id: The document's ID as a string.
        :param update_data: The data to update the document with.
        :return: The updated document if successful, otherwise None.
        """
        object_id = self._validate_object_id(document_id)
        if not isinstance(update_data, dict) or not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Update data must be a non-empty dictionary.",
            )
        if self.reference_field in update_data.keys():
            self._validate_reference(update_data)
        try:
            result = self.collection.find_one_and_update(
                {"_id": object_id}, {"$set": update_data}, return_document=True
            )
            if not result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Document not found for update.",
                )
            return result
        except PyMongoError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error: {str(e)}",
            )

    def delete(self, document_id: str) -> Tuple[bool, Dict[str, Any]]:
        """
        Delete a document by its ID.
        :param document_id: The document's ID as a string.
        :return: A tuple where the first element is True if the document was deleted,
                 and the second element is the deleted document.
        """
        object_id = self._validate_object_id(document_id)
        try:
            result = self.collection.find_one_and_delete({"_id": object_id})
            if result is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Document not found for deletion.",
                )
            # Cascade deletion if a related collection exists
            if self.cascaded_collection is not None and self.cascaded_field is not None:
                ref_value = result.get(self.cascaded_field)
                if ref_value is not None:
                    deleted_related = self.cascaded_collection.delete_many(
                        {self.cascaded_field: ref_value}
                    )
                    print(
                        f"Cascaded deletion: {deleted_related.deleted_count} related documents removed."
                    )

            return True, result
        except PyMongoError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error: {str(e)}",
            )

    def find(
        self, filters: Dict = {}, projection: Optional[Dict] = None, limit: int = 0
    ) -> List[Dict]:
        """
        Find documents matching the given filters.
        :param filters: Query filters.
        :param projection: Projection to include/exclude specific fields.
        :param limit: The maximum number of documents to return (0 for no limit).
        :return: A list of matching documents.
        """
        if not isinstance(filters, dict):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Filters must be a dictionary.",
            )
        if projection is not None and not isinstance(projection, dict):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Projection must be a dictionary or None.",
            )
        if not isinstance(limit, int) or limit < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Limit must be a non-negative integer.",
            )
        try:
            cursor = self.collection.find(filters, projection).limit(limit)
            return list(cursor)
        except PyMongoError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error: {str(e)}",
            )

    def find_one(self, filters: Dict = {}) -> Optional[Dict]:
        """
        Find a document matching the given filters.
        :param filters: Query filters.
        :return: The document if found, otherwise None.
        """
        try:
            document = self.collection.find_one(filters)
            return document
        except PyMongoError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error: {str(e)}",
            )

    def count(self, filters: Dict = {}) -> int:
        """
        Count documents matching the given filters.
        :param filters: Query filters.
        :return: The count of matching documents.
        """
        if not isinstance(filters, dict):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Filters must be a dictionary.",
            )
        try:
            return self.collection.count_documents(filters)
        except PyMongoError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error: {str(e)}",
            )

    def aggregate(self, pipeline: List[Dict]) -> List[Dict]:
        """
        Perform an aggregation pipeline query.
        :param pipeline: The aggregation pipeline as a list of stages.
        :return: The aggregation results as a list.
        """
        if not isinstance(pipeline, list) or not all(
            isinstance(stage, dict) for stage in pipeline
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Pipeline must be a list of dictionaries.",
            )
        try:
            return list(self.collection.aggregate(pipeline))
        except PyMongoError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error: {str(e)}",
            )
