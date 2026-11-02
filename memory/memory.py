import json
import os


import dotenv
import numpy as np
from openai import OpenAI
from dotenv import load_dotenv

from memory.db import create_memory, create_semantic_memory, get_semantic_memories





load_dotenv()

embedding_client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)


def create_embedding(text):
    response = embedding_client.embeddings.create(
        model=os.getenv("EMBEDDING_MODEL"),
        input=text
    )
    
    return response.data[0].embedding


def cosine_similarity(vector1, vector2):
    v1 = np.array(vector1)
    v2 = np.array(vector2)

    return np.dot(v1, v2) / (
        np.linalg.norm(v1) *
        np.linalg.norm(v2)
    )


def save_memory(user_message, assistant_message):
    text = user_message + "\n" + assistant_message

    embedding = create_embedding(text)

    create_memory(
        user_message,
        assistant_message,
        json.dumps(embedding)
    )
    
 

def search_semantic_memories(
    query,
    top_k=3,
    threshold=0.20
):
    query_embedding = create_embedding(query)
    rows = get_semantic_memories()

    results = []

    for (
        user_message,
        assistant_message,
        embedding_json,
        created_at
    ) in rows:

        memory_embedding = json.loads(
            embedding_json
        )

        score = cosine_similarity(
            query_embedding,
            memory_embedding
        )
        
        if score >= threshold:
            results.append({
                "user_message": user_message,
                "assistant_message": assistant_message,
                "created_at": created_at,
                "score": score
            })

    results.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    #print(results)

    return results[:top_k]

def save_semantic_memory(fact):
    embedding = create_embedding(fact)

    create_semantic_memory(
        fact,
        json.dumps(embedding)
    )
 

