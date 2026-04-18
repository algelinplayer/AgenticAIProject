# Guidelines de Estabilidade e Performance para Agentes de IA

Este documento registra as lições aprendidas sobre a estabilidade do ambiente de execução (Terminal/IDE) e as melhores práticas para evitar travamentos durante o desenvolvimento de workflows agentic.

## 1. Diagnóstico de Travamentos (Causas Raiz)
Identificamos que a thread de execução da Junie/Terminal no PyCharm pode congelar nos seguintes cenários:

- **Loop Infinito no Fatiamento (Chunking):** Algoritmos que dependem de caracteres separadores (`\n`) sem uma garantia de avanço mínimo. Se o separador não for encontrado, o ponteiro de início não se move, causando loop infinito.
- **I/O Bloqueante Síncrono:** Leitura e escrita pesada de arquivos (especialmente CSVs grandes) no mesmo processo da thread de UI/Terminal.
- **Chamadas de API sem Timeout:** Aguardar indefinidamente por respostas de rede da OpenAI ou Vocareum.
- **Excesso de Objetos em Memória:** Criar milhares de objetos de chunk em strings muito longas sem liberar referências.

## 2. Recomendações de Desenvolvimento (Como evitar)

### A. Proteção no Algoritmo de Chunking
Sempre implemente um "Safety Advance" para garantir que o ponteiro de texto avance, mesmo que a condição de quebra não seja satisfeita.
```python
# Exemplo de boa prática
if end <= start:
    end = min(start + 1, text_length) # Avanço mínimo de 1 char
```

### B. Uso de Timeouts Obrigatórios
Nunca instancie um cliente de API sem definir um timeout explícito.
```python
client = OpenAI(api_key=key, timeout=60.0) # Recomendado: 60s
```

### C. Estratégia "Mock-First"
Durante a construção da lógica de orquestração (Fase 2), utilize **Mocks** para embeddings e respostas de chat.
- **Vantagem:** Desenvolvimento 10x mais rápido, sem custos de API e com estabilidade total.
- **Quando usar:** 90% do tempo de desenvolvimento.
- **API Real:** Apenas para testes de integração final.

### D. Execução Segura de Scripts Pesados
Evite rodar scripts que processam grandes volumes de dados ou fazem muitas chamadas de API diretamente no terminal interativo da IDE.
- Se necessário rodar, use scripts de validação reduzidos (datasets menores).
- Monitore o progresso com logs explícitos usando `flush=True` para garantir que a saída apareça imediatamente.

---
*Estas diretrizes devem ser seguidas em todas as fases do projeto AI-Powered Agentic Workflow.*
