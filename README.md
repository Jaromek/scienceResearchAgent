# researchAgent

Opis: System, który na podstawie zapytania użytkownika:

przeszukuje bazę artykułów (np. ArXiv, lokalne PDF-y, np. LangChain + unstructured + FAISS/Chroma)

buduje RAG-prompt (Retrieval-Augmented Generation)

generuje zrozumiałe podsumowanie, cytując źródła

opcjonalnie używa LangGraph do iteracyjnej analizy (np. osobny agent streszcza, inny sprawdza kontrargumenty)

Stack: LangChain, Chroma/FAISS, Arxiv API, OpenRouter, LangGraph, Streamlit, n8n (opcjonalnie jako front/send)
Zastosowanie: codzienna praca badawcza / przegląd literatury naukowej
