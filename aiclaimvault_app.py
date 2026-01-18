# aiclaimvault_app.py – AIClaimVault: Proof-of-Intelligence Blockchain

from flask import Flask, jsonify, request, render_template_string
import hashlib
import json
import time
import os
from uuid import uuid4

CHAIN_FILE = 'aiclaimvault_chain.json'
app = Flask(__name__)

class Block:
    def __init__(self, index, timestamp, claim_id, model_id, prompt, response, response_hash, reasoning_trace, score, previous_hash, nonce=0):
        self.index = index
        self.timestamp = timestamp
        self.claim_id = claim_id
        self.model_id = model_id
        self.prompt = prompt
        self.response = response
        self.response_hash = response_hash
        self.reasoning_trace = reasoning_trace
        self.score = score
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.compute_hash()

    def compute_hash(self):
        return hashlib.sha256(json.dumps(self.__dict__, sort_keys=True).encode()).hexdigest()

class AIClaimVault:
    difficulty = 4

    def __init__(self):
        self.submissions = []
        self.chain = self.load_chain()

    def create_genesis_block(self):
        return [Block(0, time.time(), "GENESIS", "System", "N/A", "Genesis Block", "0", "root", 10, "0")]

    def last_block(self):
        return self.chain[-1]

    def submit_claim(self, model_id, prompt, response, reasoning_trace, score):
        claim_id = str(uuid4())
        response_hash = hashlib.sha256(response.encode()).hexdigest()
        self.submissions.append({
            'claim_id': claim_id,
            'model_id': model_id,
            'prompt': prompt,
            'response': response,
            'response_hash': response_hash,
            'reasoning_trace': reasoning_trace,
            'score': score
        })
        return claim_id

    def proof_of_work(self, block):
        block.nonce = 0
        hashed = block.compute_hash()
        while not hashed.startswith('0' * AIClaimVault.difficulty):
            block.nonce += 1
            hashed = block.compute_hash()
        return hashed

    def add_block(self, block, proof):
        if self.last_block().hash != block.previous_hash:
            return False
        if not proof.startswith('0' * AIClaimVault.difficulty):
            return False
        if proof != block.compute_hash():
            return False
        self.chain.append(block)
        self.save_chain()
        return True

    def mine_submission(self):
        if not self.submissions:
            return False
        data = self.submissions.pop(0)
        block = Block(
            index=len(self.chain),
            timestamp=time.time(),
            claim_id=data['claim_id'],
            model_id=data['model_id'],
            prompt=data['prompt'],
            response=data['response'],
            response_hash=data['response_hash'],
            reasoning_trace=data['reasoning_trace'],
            score=data['score'],
            previous_hash=self.last_block().hash
        )
        proof = self.proof_of_work(block)
        if self.add_block(block, proof):
            return block.index
        return False

    def save_chain(self):
        with open(CHAIN_FILE, 'w') as f:
            json.dump([b.__dict__ for b in self.chain], f, indent=4)

    def load_chain(self):
        if not os.path.exists(CHAIN_FILE):
            return self.create_genesis_block()
        with open(CHAIN_FILE, 'r') as f:
            return [Block(**b) for b in json.load(f)]

vault = AIClaimVault()

@app.route('/')
def index():
    html = """
    <html><head><title>AIClaimVault</title><style>
    body { font-family: sans-serif; background: #f5f5f5; padding: 20px; }
    .block { background: white; padding: 15px; margin: 10px 0; border-radius: 6px; box-shadow: 0 0 4px rgba(0,0,0,0.1); }
    </style></head><body>
    <h1>🧠 AIClaimVault Explorer</h1>
    {% for block in chain %}
    <div class="block">
        <h3>Block #{{ block.index }} – {{ block.model_id }}</h3>
        <p><b>Prompt:</b> {{ block.prompt }}</p>
        <p><b>Response:</b> {{ block.response }}</p>
        <p><b>Reasoning:</b> {{ block.reasoning_trace }}</p>
        <p><b>Score:</b> {{ block.score }}</p>
        <p><b>Response Hash:</b> {{ block.response_hash }}</p>
        <p><b>Hash:</b> {{ block.hash }}</p>
        <p><b>Previous Hash:</b> {{ block.previous_hash }}</p>
    </div>
    {% endfor %}
    </body></html>
    """
    return render_template_string(html, chain=vault.chain)

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    required = ('model_id', 'prompt', 'response', 'reasoning_trace', 'score')
    if not all(k in data for k in required):
        return jsonify({'error': 'Missing fields'}), 400
    claim_id = vault.submit_claim(
        data['model_id'], data['prompt'], data['response'],
        data['reasoning_trace'], data['score']
    )
    return jsonify({'message': 'AI claim submitted', 'claim_id': claim_id})

@app.route('/mine')
def mine():
    index = vault.mine_submission()
    return jsonify({'message': f'Block #{index} mined' if index is not False else 'No submissions to mine'})

@app.route('/chain')
def chain_view():
    return jsonify([b.__dict__ for b in vault.chain])

app = app  # Vercel compatibility
