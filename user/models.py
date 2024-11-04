from django.db import models

# Create your models here.

import os
from supabase import create_client


SUPABASE_KEY = os.getenv('SUPABASE_KEY')
SUPABASE_URL = os.getenv('SUPABASE_URL')

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

from typing import Union

def update_user_data(user_uuid: str, new_username: str, new_password: str) -> Union[dict, str]:
    try:
        user = supabase.table("users").select("*").eq("id", user_uuid).single().execute()
        
        if not user or user['data'] is None:
            return {"status": "error", "message": "User not found."}
        
        updated_user = supabase.table("users").update({
            "username": new_username,
            "password": new_password
        }).eq("id", user_uuid).execute()
        
        return {
            "status": "success",
            "message": "User data updated successfully.",
            "data": updated_user['data']
        }
    except Exception as e:
        return {"status": "error", "message": f"An error occurred: {str(e)}"}
