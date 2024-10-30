# PeerLink – Smart Networking with RAG-Powered Profile Matching

**Author**: Md. Tahmid Islam

## Overview
This project leverages Retrieval-Augmented Generation (RAG) to connect users within a community by matching them based on their interests, profession, and ongoing projects. The goal is to facilitate networking by identifying potential collaborators with shared focus areas.

## Data Retrieval
User profiles are fetched from the database. Each profile includes three key attributes:
- **Profession**
- **Interests**
- **Ongoing Project**

All attributes are prioritized equally in the matching process.

## Embedding
The features are transformed into embeddings using OpenAI's `text-embedding-ada-002` model, which converts textual input into fixed-size, 1536-dimensional vectors. This model captures semantic meaning in the profiles, aiding in effective comparison.

## Indexing
The `FAISS` library is employed to index the embedded profiles, allowing for efficient nearest-neighbor searches. The `IndexFlatL2` strategy is used, which computes the squared Euclidean distance between vectors for fast similarity measurement.

## Search
The top 5 nearest profiles are retrieved using the FAISS search. It compares the user's embedded profile to all vectors stored in the index. The goal is to find the closest matches, which represent profiles with similar embeddings.

## GPT Recommendation
The top 5 retrieved profiles, along with a predefined prompt, are sent to the GPT-4 model to generate a recommendation and explanation, highlighting the profile that most closely aligns with the user.

## Example Response

### User Profile
- **User ID**: 14
- **Profession**: Fitness Coach
- **Likes**: Exercise, Child Fitness
- **Current Project**: Developing a fitness program for young children

### Top Matches from FAISS Search
| User ID | Profession     | Likes                       | Current Project                                       |
|---------|----------------|-----------------------------|-------------------------------------------------------|
| 5       | Nutritionist   | Cooking, Wellness           | Creating a plant-based diet plan for children         |
| 29      | Nutritionist   | Diet Planning, Wellness     | Developing a school-based nutrition program           |
| 20      | Chef           | Culinary Arts, Nutrition    | Creating recipes for a healthy kids’ cookbook         |
| 11      | Teacher        | Education, Child Development| Creating a curriculum focused on nutrition awareness  |
| 8       | Chef           | Baking, Experimenting       | Developing healthy snack recipes for kids             |

### GPT Recommendation
The most meaningful connection would be between **User ID: 14** (Fitness Coach) and **User ID: 5** (Nutritionist).

**Reason for Selection**:  
Both users focus on children's health and wellness. **User ID: 14** is developing a fitness program for young children, while **User ID: 5** is working on a plant-based diet plan for children. Their expertise in fitness and nutrition is complementary, leading to a holistic approach to child health.

#### Other Matches
- **User ID: 29** - Their project aligns with child nutrition but focuses more on school-based programs, which may not directly support User ID 14's fitness program.
- **User ID: 20** - Although their project involves healthy recipes for kids, the primary focus on culinary arts may not be as relevant to fitness.
- **User ID: 11** - Their expertise in education and curriculum development is valuable but may not directly support the fitness aspect.
- **User ID: 8** - Similar to User ID 20, their focus on culinary arts and snack recipes may not closely align with fitness and exercise for children.

