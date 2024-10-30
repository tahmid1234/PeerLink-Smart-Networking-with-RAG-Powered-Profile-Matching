from database import database
import openai
import os
from dotenv import load_dotenv
load_dotenv()
from llama_index.core import VectorStoreIndex,Document

import faiss
import numpy as np


openai.api_key = os.getenv("OPENAI_API_KEY")
def processUsers():
    profiles = database.fetchAllUsers()
    # generate embessings
    
    
    for profile in profiles:
        profile_in_text = f"{profile['profession']} {profile['likings']} {profile['current_project']}"
        profile["embedding"] = generateEmbeddings(profile_in_text)
        
        
    
    index = indexEmbeddedProfile(profiles)
    target_user = profiles[20]
    top_matches = find_top_matches(target_user["embedding"],index,profiles)

    print('macthed profiles/n', top_matches)
   
    response = get_gpt_recommendation(target_user,top_matches)
    print("From GPT",response)

    store_top_matches_in_file(target_user,top_matches,response)
        
        
    
    





def generateEmbeddings(profile_in_text):
    response = openai.embeddings.create(
        model="text-embedding-ada-002",
        input=profile_in_text
    )
    print(type(response.data[0].embedding)," data type")
    return response.data[0].embedding

def indexEmbeddedProfile(embedded_profiles):
    embeddings = np.array([user["embedding"] for user in embedded_profiles]).astype("float32")
    
    embedding_dimension = embeddings.shape[1]
   
    index = faiss.IndexFlatL2(embedding_dimension)
    index.add(embeddings)
    return index

def find_top_matches(user_embedding, index, user_profiles, top_n=6):
    # Convert the user's embedding to float32 format
    metadata = user_profiles
    user_embedding = np.array(user_embedding).astype("float32").reshape(1, -1)
    
    # Search in the index
    distances, indices = index.search(user_embedding, top_n)
    
    # Retrieve user IDs of the top matches
    top_matches = [
    ({k: v for k, v in metadata[idx].items() if k != "embedding"}, distances[0][i]) 
    for i, idx in enumerate(indices[0])
]
    return top_matches
    

def get_gpt_recommendation(target_user, top_matches):
    # Build a clear, minimal prompt for GPT
    prompt = f"""
    Here is a user profile looking to connect with similar people:
    - UserID: {target_user['user_id']}
    - Profession: {target_user['profession']}
    - Current Project: {target_user['current_project']}
    - Interests: {target_user['likings']}
    
    Below are the top 5 potential matches for this user. Which one would make the most meaningful connection based on their profiles?
    
    Matches:
    """
    
    for i, match in enumerate(top_matches[1:], start=1): 

        prompt += f"\n{i}. UserID:{match[0]['user_id']} Profession: {match[0]['profession']}, Project: {match[0]['current_project']}, Interests: {match[0]['likings']}"
    
    prompt += "\n\nPlease recommend the best match and provide a brief reason for your choice. Include the ids of both users. Additionally mention why other choices you didn't select very breifly."
    
    
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    print(response)
    recommendation = response.choices[0].message.content
    return recommendation

# def chunk_data(data, chunk_size):
#     """Split data into smaller chunks of specified size."""
#     for i in range(0, len(data), chunk_size):
#         yield data[i:i + chunk_size]

# import openai

# def get_gpt_recommendation(target_user, top_matches, chunk_size=3):
#     # Split top_matches into chunks
#     recommendations = []
#     for chunk in chunk_data(top_matches[1:], chunk_size):  # Skip the first match if it’s the user themselves
#         # Build the prompt for this chunk
#         print(chunk," chunk")
#         prompt = f"""
#         Here is a user profile looking to connect with similar people:
#         - Profession: {target_user['profession']}
#         - Current Project: {target_user['current_project']}
#         - Interests: {target_user['likings']}
        
#         Below are a few potential matches. Which one would make the most meaningful connection based on their profiles?
        
#         Matches:
#         """
        
#         for i, (match) in enumerate(chunk, start=1):
#             print(match," match")
#             prompt += f"\n{i}. Profession: {match[0]['profession']}, Project: {match[0]['current_project']}, Interests: {match[0]['likings']}"
        
#         prompt += "\n\nPlease recommend the best match in this list and provide a brief reason for your choice."
        
#         # Send the prompt to GPT
#         response = openai.chat.completions.create(
#             model="gpt-4",
#             messages=[{"role": "user", "content": prompt}]
#         )
        
#         # Extract and store GPT's recommendation
#         recommendation = response.choices[0].message.content
#         recommendations.append(recommendation)
    
#     return recommendations


def store_top_matches_in_file(target_user, top_matches, gpt_recommendation, filename="top_matches(2).txt"):
    with open(filename, "w") as file:
        # Write the target user's profile
        file.write("User Profile:\n")
        file.write(f"User ID: {target_user['user_id']}\n")
        file.write(f"Profession: {target_user['profession']}\n")
        file.write(f"Likes: {target_user['likings']}\n")
        file.write(f"Current Project: {target_user['current_project']}\n\n")
        
        # Write the top matches (excluding the first match if it’s the user themselves)
        file.write("Top Matches:\n")
        for i, (match, distance) in enumerate(top_matches[1:], start=1):  # Skip the first match as it’s the user itself
            file.write(f"{i}. User ID {match['user_id']} is a {match['profession']} who likes {match['likings']} and is currently working on {match['current_project']}\n")
        
        # Write the GPT recommendation
        file.write("\nGPT Recommendation:\n")
        file.write(f"{gpt_recommendation}\n")
