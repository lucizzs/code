from typing import Any, Dict
from fastapi import HTTPException

class APIResponseFactory:
    @staticmethod
    def create_success_response(data: Any) -> Dict:
        return {
            "status": "success",
            "data": data
        }

    @staticmethod
    def create_error_response(error: str, status_code: int = 400) -> Dict:
        raise HTTPException(
            status_code=status_code,
            detail={
                "status": "error",
                "message": error
            }
        )

    @staticmethod
    def create_breed_response(breed_data: Dict) -> Dict:
        return {
            "breed_id": breed_data["id"],
            "name": breed_data["name"],
            "description": breed_data["description"],
            "temperament": breed_data["temperament"],
            "origin": breed_data["origin"],
            "life_span": breed_data["life_span"],
            "weight_imperial": breed_data["weight"]["imperial"],
            "wikipedia_url": breed_data.get("wikipedia_url")
        }
