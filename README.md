# 🧠 AIClaimVault

**AIClaimVault** is a decentralized blockchain system built to record and verify the outputs of AI models in a transparent, immutable, and cryptographically secure way. It anchors prompts, responses, reasoning paths, and scoring metadata to a tamper-proof ledger — enabling accountability, reproducibility, and verifiability in machine intelligence.

This platform is ideal for AI researchers, auditors, educators, and decentralized agents requiring public proof of thought, capability, or compliance.

---

## 🚀 Features

- ✅ Immutable storage of AI prompts, responses, and reasoning
- 🔐 Cryptographic response hashing for tamper detection
- 📊 Evaluation score logging for performance benchmarking
- ⛓️ Proof-of-Work secured block validation
- 🧾 REST API for submissions, mining, and chain retrieval
- 🌍 Web-based blockchain explorer interface
- ⚙️ Deployed serverlessly on **Vercel**

---

## 📁 Project Structure

```
/
├── aiclaimvault_app.py       # Flask blockchain application
├── aiclaimvault_chain.json   # Local chain data store
├── requirements.txt          # Python dependency list
└── vercel.json               # Vercel deployment config
```

---

## 📡 API Endpoints

| Method | Endpoint     | Description                             |
|--------|--------------|-----------------------------------------|
| `GET`  | `/`          | HTML Explorer of the blockchain         |
| `GET`  | `/chain`     | Full chain JSON view                    |
| `GET`  | `/mine`      | Mines the next pending AI submission    |
| `POST` | `/submit`    | Submit new AI prompt/response block     |

### Example Payload for `/submit`:

```json
{
  "model_id": "gpt-4o",
  "prompt": "Explain quantum tunneling in 50 words.",
  "response": "Quantum tunneling allows particles to pass through potential barriers...",
  "reasoning_trace": "Generated via transformer attention layers with uncertainty reduction.",
  "score": 8.7
}
```

---

## 🔍 Use Cases

- AI performance benchmarking over time
- Model audit trails and reproducibility
- Proof of knowledge and reasoning for autonomous agents
- AI-generated intellectual property tracking
- Decentralized transparency and AI ethics systems

---

> **AIClaimVault** creates a cryptographic mirror for machine intelligence. Anchor your AI's mind — on-chain, immutable, and verifiable.
