from groq import Groq
import httpx

def test_groq():
    api_key = "SUA API KEY AQUI"
    
    try:
        # Teste 1: Cliente padrão
        print("Testando cliente padrão...")
        client = Groq(api_key=api_key)
        print("✅ Cliente padrão criado com sucesso!")
        
        # Teste 2: Fazer uma requisição simples
        print("Testando requisição...")
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": "Diga 'Olá, teste!'"}],
            max_tokens=10
        )
        print(f"✅ Resposta recebida: {response.choices[0].message.content}")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        
        try:
            # Teste alternativo com http_client
            print("\nTentando com http_client...")
            http_client = httpx.Client(timeout=60.0)
            client = Groq(api_key=api_key, http_client=http_client)
            print("✅ Cliente com http_client criado com sucesso!")
        except Exception as e2:
            print(f"❌ Erro alternativo: {e2}")

if __name__ == "__main__":
    test_groq()