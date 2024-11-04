from django.db import models
import os
from dotenv import load_dotenv
from supabase import create_client, Client
from datetime import datetime

# Create a Supabase client

load_dotenv()

supabase_url = os.getenv('DB_URL')
supabase_key = os.getenv('DB_KEY')

supabase = create_client(supabase_url, supabase_key)

def fetch_resumes(userID):
    # Fetch resumes from the database
    resumes = supabase.table('Resume').select().eq("userID", userID).execute()
    return resumes

def fetch_resum_by_id(userID, id):
    # Fetch a specific resume from the database
    resume = supabase.table('Resume').select().eq("userID", userID).eq("id", id).execute()
    return resume

def create_resume(userID, title, content = '{}'):
    # Create a new resume in the database
    dateTime = datetime.now().isoformat()
    resume = supabase.table('Resume').insert({'userID': userID, 'title': title, 'content': content, 'createdAt': dateTime, 'lastModified': dateTime}).execute()
    return resume

def update_resume(userID, id, title = None, content = None):
    # Update a resume in the database
    dateTime = datetime.now().isoformat()
    if title is None and content is None:
        return {'message': 'No changes made'}
    if title is None:
        resume = supabase.table('Resume').update({'content': content, 'lastModified': dateTime}).eq("userID", userID).eq("id", id).execute()
    elif content is None:
        resume = supabase.table('Resume').update({'title': title, 'lastModified': dateTime}).eq("userID", userID).eq("id", id).execute()
    resume = supabase.table('Resume').update({'title': title, 'content': content, 'lastModified': dateTime}).eq("userID", userID).eq("id", id).execute()
    return resume

def delete_resume(userID, id):
    # Delete a resume from the database
    resume = supabase.table('Resume').delete().eq("userID", userID).eq("id", id).execute()
    return resume
