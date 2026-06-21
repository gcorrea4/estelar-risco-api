# 🩺 Estelar — API de Risco Clínico (AstraCare)

> Módulo de **triagem de risco clínico** da plataforma **Estelar**, telemedicina via satélite para regiões remotas. Esta API recebe sinais vitais, sintomas e o contexto operacional do paciente e devolve um **nível de risco** (`EMERGENCIA`, `URGENTE`, `ATENCAO` ou `BAIXO`) com alertas e conduta recomendada.

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-API_REST-000000?style=for-the-badge&logo=flask)
![Render](https://img.shields.io/badge/Deploy-Render-46E3B7?style=for-the-badge&logo=render)

---

## 🌐 Onde isto se encaixa no Estelar

```
┌─────────────────────────┐         ┌──────────────────────────┐
│   Frontend (Estelar)    │         │   Backend Java (Quarkus) │
│   React + Vite · Vercel │ ◄─────► │   Login, tickets · Azure │
└───────────┬─────────────┘         └──────────────────────────┘
            │
            │  fetch (HTTP/JSON)
            ▼
┌─────────────────────────┐         ┌──────────────────────────┐
│  🩺 AstraCare (Risco)    │         │  🧠 IA de Triagem         │
│  Flask · Render          │         │  Flask + sklearn · Render│
│  ◄── VOCÊ ESTÁ AQUI      │         │  Modelos de ML           │
└─────────────────────────┘         └──────────────────────────┘
```

No site, a página **Calculadora de Risco** envia os dados do paciente para esta API e exibe o nível de risco calculado em tempo real.

---

## ℹ️ Sobre esta versão

Esta é a **minha versão integrada** do AstraCare para a plataforma Estelar. A lógica de pontuação clínica (`risco.py`) foi originalmente desenvolvida por **Eric Maciel** como ferramenta de linha de comando; aqui ela foi **encapsulada em uma API REST** (`api_risco.py`) para conversar com o frontend, mantendo a mesma regra de pontuação, níveis e recomendações do projeto original.

---

## 🌐 Endpoints

| Método | Rota | Descrição |
|---|---|---|
| `GET`  | `/health` | Health check |
| `POST` | `/calcular-risco` | Calcula o nível de risco clínico |

### Exemplo — `POST /calcular-risco`

```json
{
  "sinais": {
    "temperatura": 39.5,
    "saturacao": 88,
    "frequencia_cardiaca": 135,
    "pressao_sistolica": 185,
    "pressao_diastolica": 125
  },
  "sintomas": { "dor_peito": true, "falta_ar": true },
  "contexto": {
    "distancia_hospital_km": 150,
    "internet_disponivel": false,
    "medicamentos_basicos": false
  }
}
```

Resposta:

```json
{
  "pontuacao": 26,
  "nivel": "EMERGENCIA",
  "alertas": ["temperatura critica", "saturacao muito baixa", "..."],
  "recomendacao": "Acionar evacuacao/resgate, manter monitoramento continuo e contato medico remoto prioritario."
}
```

---

## 🧮 Como o risco é calculado

A pontuação soma três blocos e classifica o resultado:

| Bloco | Avalia |
|---|---|
| **Sinais vitais** | Temperatura, saturação, frequência cardíaca, pressão arterial |
| **Sintomas** | Dor no peito, falta de ar, confusão, desmaio, sangramento, etc. |
| **Contexto** | Distância do hospital, internet disponível, estoque de medicamentos |

| Pontuação | Nível |
|---|---|
| ≥ 10 | 🔴 EMERGÊNCIA |
| 6–9 | 🟠 URGENTE |
| 3–5 | 🟡 ATENÇÃO |
| 0–2 | 🟢 BAIXO |

---

## 🚀 Rodar localmente

```bash
pip install -r requirements.txt
python api_risco.py     # http://localhost:5001
```

Teste: `curl http://localhost:5001/health`

> O projeto original também tem um menu interativo de terminal: `python main.py`.

---

## ☁️ Deploy no Render

O repositório já vem com `render.yaml`. No [Render](https://render.com):

1. **New → Blueprint** e conecte este repositório.
2. O Render configura automaticamente:
   - Build: `pip install -r requirements.txt`
   - Start: `gunicorn api_risco:app`
3. Após o deploy, a URL fica como `https://estelar-risco-api.onrender.com`.
4. No frontend Estelar, defina a variável `VITE_RISCO_API_URL` com essa URL.

> 💡 O plano grátis do Render hiberna após ~15 min sem uso (primeira chamada ~40s para acordar).

---

## 📂 Estrutura

```
estelar-risco-api/
├── api_risco.py        # API REST Flask (CORS) — camada de integração
├── risco.py            # Regras de pontuação e recomendações (lógica original)
├── main.py             # Menu interativo de terminal (CLI original)
├── pacientes.py        # Cadastro, listagem e busca
├── atendimentos.py     # Sinais vitais, sintomas, contexto e histórico
├── relatorios.py       # Resumos, casos críticos e exportação TXT
├── database_oracle.py  # Conexão demonstrativa com Oracle
├── armazenamento.py    # Leitura/gravação de dados em JSON
├── util.py             # Funções auxiliares
├── requirements.txt    # flask, flask-cors, gunicorn
└── render.yaml         # Blueprint de deploy do Render
```

---

## 👥 Equipe — 1TDSPB FIAP

| Nome | RM | Papel |
|---|---|---|
| Gabriel Correa Souza | RM567903 | Integração à plataforma Estelar + API REST |
| Eric Maciel | RM567398 | Lógica original do AstraCare (`risco.py`) |
| Kayque Duarte | RM567980 | — |

Global Solution 2026/1 · FIAP
