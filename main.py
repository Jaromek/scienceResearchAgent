from RAG.Generation.generation import Generation
from dataPrepraration.databasePreparation import DatabasePreparation

def rag_answer(query: str, collection_name: str = "scientific_papers") -> str:
    """
    Simple RAG function for main.py
    
    Args:
        query (str): User question
        collection_name (str): Qdrant collection name
        
    Returns:
        str: Generated answer
    """
    try:
        # Initialize RAG system
        rag_system = Generation(collection_name=collection_name, k=10)
        
        # Generate answer
        result = rag_system.generate_answer(query)
        
        if result['error']:
            return f"Error: {result['error']}"
        
        answer = result['answer']
        
        # LLM already includes Sources section in the answer, no need to add it again
        return answer
            
    except Exception as e:
        return f"An error occurred during response generation: {str(e)}"

def prepare_database_if_needed(query: str):
    """
    Prepare database with relevant articles based on user query
    """
    print("Preparing database based on your question...")
    
    try:
        db_preparation = DatabasePreparation(
            user_query=query, 
            max_results=100,  # Smaller number for faster tests
            download_directory='archive'
        )
        db_preparation.prepare_database()
        print("Database prepared successfully!")
        return True
        
    except Exception as e:
        print(f"Error during database preparation: {e}")
        return False

if __name__ == "__main__":
    print("RAG Research Agent - Scientific Assistant")
    print("Ask a question, and I'll retrieve relevant articles and answer based on the latest research.")
    print("Type 'exit' to quit, 'prepare' to prepare a new database.\n")
    
    database_prepared = False
    
    while True:
        user_query = input("Ask a question: ").strip()
        
        if user_query.lower() == "exit":
            print("Goodbye!")
            break
            
        if user_query.lower() == "prepare":
            query_for_prep = input("Provide topic for database preparation for database name: ").strip()
            if query_for_prep:
                database_prepared = prepare_database_if_needed(query_for_prep)
            continue
            
        if not user_query:
            print("Please provide a question.")
            continue
        
        # Prepare database if not already prepared
        if not database_prepared:
            print("First use - preparing database...")
            database_prepared = prepare_database_if_needed(user_query)
            if not database_prepared:
                print("Cannot continue without prepared database.")
                continue
        
        print("Analyzing question and searching for answer...")
        
        try:
            print("Question:\n", user_query)
            answer = rag_answer(user_query)
            print(f"\nAnswer:\n{answer}\n")
            print("-" * 80)
            
        except Exception as e:
            print(f"Error during response generation: {e}")
            print("Try again or type 'prepare' to prepare the database anew.\n")
