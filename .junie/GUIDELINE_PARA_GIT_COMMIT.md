## 🧱 Estrutura de um Commit Convencional

```bash
<tipo>(escopo opcional): <mensagem curta em inglês>

<descrição opcional mais detalhada>

<rodapé opcional para breaking changes ou issues relacionadas>
```

---

## 📋 Diretrizes Gerais (OBRIGATÓRIAS)
- **Idioma:** Todos os commits devem ser escritos obrigatoriamente em **inglês**.
- **Rastreabilidade:** Sempre que o commit estiver relacionado a um ticket (ex.: Jira), inclua o identificador do ticket no rodapé do commit utilizando o formato `Refs: #ID-TICKET`.

---

## 🔤 Tipos mais comuns

| Tipo       | Descrição                                                                 |
|------------|---------------------------------------------------------------------------|
| `feat`     | Adição de nova funcionalidade                                             |
| `fix`      | Correção de bug                                                           |
| `docs`     | Alterações na documentação                                                |
| `style`    | Ajustes de formatação, espaços, ponto e vírgula, etc.                     |
| `refactor` | Refatoração de código (sem mudança de funcionalidade ou correção de bug)  |
| `test`     | Criação ou modificação de testes                                          |
| `chore`    | Tarefas de manutenção (build, dependências, scripts, etc.)                |
| `perf`     | Melhorias de performance                                                  |
| `ci`       | Mudanças em arquivos/configs de integração contínua                       |
| `build`    | Mudanças que afetam o sistema de build ou dependências externas           |

---

## 🧪 Exemplos práticos (baseados no código real)

```bash
feat(distribution-fiscais): load RAFs dynamically based on user profile
Refs: #PLF-123

fix(distribution-fiscais): prevent double loading of data when paginating
Refs: #PLF-124

refactor(distribution-fiscais): move RAF search by orgao into separate method
Refs: #PLF-125

test(fiscalization-program): ensure component initializes correctly
Refs: #PLF-126

style(distribution-table): adjust column widths for better alignment
Refs: #PLF-127

chore(distribution-fiscais): inject UserService and DistributionRafService in component
Refs: #PLF-128

perf(distribution-fiscais): cache inspetoria data to reduce API calls
Refs: #PLF-129

docs(distribution-fiscais): document steps to configure ETAPA_DISTR_FISC
Refs: #PLF-130

ci(pipeline): trigger deploy only on feat or fix commits
Refs: #PLF-131
```
