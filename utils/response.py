def custom_response(message: str = "", status: int = 0, data: dict = {}) -> dict:
    return {"message": message, "status": status, "data": data}