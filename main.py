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
            return f"Błąd: {result['error']}"
        
        answer = result['answer']
        
        if result['context_used'] and result['sources']:
            sources_info = f"\n\nŹródła: {', '.join(result['sources'])}"
            return answer + sources_info
        else:
            return answer
            
    except Exception as e:
        return f"Wystąpił błąd podczas generowania odpowiedzi: {str(e)}"

def prepare_database_if_needed(query: str):
    """
    Prepare database with relevant articles based on user query
    """
    print("Przygotowuję bazę danych na podstawie Twojego pytania...")
    
    try:
        db_preparation = DatabasePreparation(
            user_query=query, 
            max_results=5,  # Mniejsza liczba dla szybszych testów
            download_directory='archive'
        )
        db_preparation.prepare_database()
        print("Baza danych przygotowana pomyślnie!")
        return True
        
    except Exception as e:
        print(f"Błąd podczas przygotowania bazy: {e}")
        return False

if __name__ == "__main__":
    print("RAG Research Agent - Asystent Naukowy")
    print("Zadaj pytanie, a pobiorę odpowiednie artykuły i odpowiem na podstawie najnowszych badań.")
    print("Wpisz 'exit' aby zakończyć, 'prepare' aby przygotować bazę na nowo.\n")
    
    database_prepared = False
    
    while True:
        user_query = input("Zadaj pytanie: ").strip()
        
        if user_query.lower() == "exit":
            print("Do widzenia!")
            break
            
        if user_query.lower() == "prepare":
            query_for_prep = input("Podaj temat do przygotowania bazy danych: ").strip()
            if query_for_prep:
                database_prepared = prepare_database_if_needed(query_for_prep)
            continue
            
        if not user_query:
            print("Proszę podaj pytanie.")
            continue
        
        # Przygotuj bazę danych jeśli jeszcze nie została przygotowana
        if not database_prepared:
            print("Pierwszego użycie - przygotowuję bazę danych...")
            database_prepared = prepare_database_if_needed(user_query)
            if not database_prepared:
                print("Nie mogę kontynuować bez przygotowanej bazy danych.")
                continue
        
        print("Analizuję pytanie i wyszukuję odpowiedź...")
        
        try:
            answer = rag_answer(user_query)
            print(f"\nOdpowiedź:\n{answer}\n")
            print("-" * 80)
            
        except Exception as e:
            print(f"Błąd podczas generowania odpowiedzi: {e}")
            print("Spróbuj ponownie lub wpisz 'prepare' aby przygotować bazę na nowo.\n")
