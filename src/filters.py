# import re
# import numpy as np
# from sentence_transformers import SentenceTransformer
# from sklearn.metrics.pairwise import cosine_similarity

# class SentinelGate:
#     # def __init__(self):
#     #     print("⚙️ Loading SentinelGate models... (This may take a moment)")
#     #     # We use a small, fast model for local embeddings
#     #     self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
#     #     # Define "Junk" Anchors (Layer 1)
#     #     self.junk_anchors = [
#     #         "tell me a joke", "write a poem", "who are you", 
#     #         "ignore previous instructions", "what is your opinion on politics",
#     #         "write code for a game", "how do I make a bomb", "weather forecast"
#     #     ]
#     #     self.junk_embeddings = self.model.encode(self.junk_anchors)

#     #     # Define "Domain" Anchors (Layer 2 - Supply Chain)
#     #     # In a real app, this would come from a Vector DB
#     #     self.domain_anchors = [
#     #         "inventory management and safety stock",
#     #         "supply chain logistics and shipping",
#     #         "warehouse operations and optimization",
#     #         "procurement purchase orders and vendors",
#     #         "freight forwarding and customs clearance",
#     #         "demand forecasting and planning"
#     #     ]
#     #     self.domain_embeddings = self.model.encode(self.domain_anchors)
#     #     print("✅ Models loaded.")

#     def __init__(self):
#         print("⚙️ Loading SentinelGate models... (This may take a moment)")
#         self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
#         # Layer 1: Junk Anchors (Keep as is)
#         self.junk_anchors = [
#             "tell me a joke", "write a poem", "who are you", 
#             "ignore previous instructions", "what is your opinion on politics",
#             "write code for a game", "how do I make a bomb", "weather forecast",
#             "hello", "hi", "how are you"
#         ]
#         self.junk_embeddings = self.model.encode(self.junk_anchors)

#         # Layer 2: Domain Anchors (UPDATED - More broad)
#         self.domain_anchors = [
#             "inventory management",
#             "logistics tracking",
#             "warehouse operations",
#             "procurement and purchasing",
#             "freight and shipping",
#             "supply chain analytics",
#             "demand forecasting",
#             "bill of lading", 
#             "customs clearance",
#             "safety stock calculation",
#             "supplier risk"
#         ]
#         self.domain_embeddings = self.model.encode(self.domain_anchors)
#         print("✅ Models loaded.")

#     def _layer_0_regex(self, prompt):
#         """Fastest check: Rule-based blocking."""
#         # Block empty or too short prompts
#         if len(prompt.strip()) < 5:
#             return True, "BLOCK_TOO_SHORT"
        
#         # Block common one-word spam
#         spam_words = ["test", "hello", "hi", "hey", "hola", "ok", "okay"]
#         if prompt.lower().strip() in spam_words:
#             return True, "BLOCK_SPAM_KEYWORD"
            
#         return False, None

#     def _layer_1_semantic_junk(self, prompt_embedding):
#         """Check if prompt is semantically similar to junk/chitchat."""
#         # Compare user prompt against junk anchors
#         similarities = cosine_similarity([prompt_embedding], self.junk_embeddings)[0]
#         max_score = np.max(similarities)
        
#         # Threshold: If > 0.6 similarity to junk, block it
#         if max_score > 0.6:
#             return True, f"BLOCK_JUNK_SEMANTIC (Score: {max_score:.2f})"
#         return False, None

#     # def _layer_2_domain_relevance(self, prompt_embedding):
#     #     """Check if prompt is relevant to the defined domain."""
#     #     # Compare user prompt against domain anchors
#     #     similarities = cosine_similarity([prompt_embedding], self.domain_embeddings)[0]
#     #     max_score = np.max(similarities)
        
#     #     # Threshold: If < 0.35 similarity to domain, block it
#     #     if max_score < 0.35:
#     #         return True, f"BLOCK_IRRELEVANT_DOMAIN (Score: {max_score:.2f})"
#     #     return False, None
#     def _layer_2_domain_relevance(self, prompt_embedding):
#         """Check if prompt is relevant to the defined domain."""
#         similarities = cosine_similarity([prompt_embedding], self.domain_embeddings)[0]
#         max_score = np.max(similarities)
        
#         # TUNED THRESHOLD: Lowered from 0.35 to 0.20
#         # MiniLM is strict, so valid matches often fall in the 0.20 - 0.30 range.
#         if max_score < 0.20:
#             return True, f"BLOCK_IRRELEVANT_DOMAIN (Score: {max_score:.2f})"
#         return False, None

#     def scan(self, prompt):
#         """The Main Pipeline: Runs all 3 layers in order."""
        
#         # --- LAYER 0: REGEX (Fastest) ---
#         is_blocked, reason = self._layer_0_regex(prompt)
#         if is_blocked:
#             return {"status": "BLOCKED", "layer": 0, "reason": reason}

#         # Encode once for the next two layers
#         prompt_embedding = self.model.encode(prompt)

#         # --- LAYER 1: JUNK FILTER (Fast AI) ---
#         is_blocked, reason = self._layer_1_semantic_junk(prompt_embedding)
#         if is_blocked:
#             return {"status": "BLOCKED", "layer": 1, "reason": reason}

#         # --- LAYER 2: DOMAIN FILTER (Deep AI) ---
#         is_blocked, reason = self._layer_2_domain_relevance(prompt_embedding)
#         if is_blocked:
#             return {"status":
#             "BLOCKED", "layer": 2, "reason": reason}

#         # If we passed all guards
#         return {"status": "PASSED", "layer": "ALL", "reason": "VALID_PROMPT"}

# # Quick test if you run this file directly
# if __name__ == "__main__":
#     gate = SentinelGate()
#     test_prompts = [
#         "Hi", 
#         "Tell me a joke about AI", 
#         "What is the safety stock for SKU-123?", 
#         "How do I fix my printer?"
#     ]
    
#     print("\n--- TEST RESULTS ---")
#     for p in test_prompts:
#         result = gate.scan(p)
#         print(f"Prompt: '{p}' -> {result['status']} ({result['reason']})")

import re
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

class SentinelGate:
    def __init__(self):
        print("⚙️ Loading SentinelGate models...")
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # 1. JUNK ANCHORS (Layer 1)
        self.junk_anchors = [
            "tell me a joke", "write a poem", "who are you", 
            "ignore previous instructions", "what is your opinion on politics",
            "write code for a game", "weather forecast", "hello", "hi"
        ]
        self.junk_embeddings = self.model.encode(self.junk_anchors)

        # 2. DOMAIN ANCHORS (Layer 2 - Positive)
        self.domain_anchors = [
            "inventory management", "logistics tracking", "warehouse operations",
            "procurement and purchasing", "freight and shipping", "supply chain analytics",
            "bill of lading", "customs clearance", "safety stock", "supplier risk"
        ]
        self.domain_embeddings = self.model.encode(self.domain_anchors)

        # 3. GENERIC WORK ANCHORS (Layer 2 - Negative)
        # We explicitly model what we want to BLOCK to avoid confusion
        self.generic_anchors = [
            "reset password", "outlook email", "vpn connection", "holiday policy",
            "human resources meeting", "jira ticket", "python syntax error",
            "marketing strategy", "agile methodology", "ceo of company",
            "schedule a meeting", "wifi access"
        ]
        self.generic_embeddings = self.model.encode(self.generic_anchors)
        
        print("✅ Models loaded.")

    def _layer_0_regex(self, prompt):
        """Layer 0: Fast Rule-Based Block"""
        if len(prompt.strip()) < 5: return True, "BLOCK_TOO_SHORT"
        spam_words = ["test", "hello", "hi", "hey", "hola", "ok", "okay"]
        if prompt.lower().strip() in spam_words: return True, "BLOCK_SPAM_KEYWORD"
        return False, None

    def _layer_1_semantic_junk(self, prompt_embedding):
        """Layer 1: Check similarity to pure Junk"""
        sims = cosine_similarity([prompt_embedding], self.junk_embeddings)[0]
        if np.max(sims) > 0.5: # Strict on junk
            return True, f"BLOCK_JUNK (Score: {np.max(sims):.2f})"
        return False, None

    def _layer_2_domain_contrastive(self, prompt_embedding):
        """Layer 2: Contrastive Check (Domain vs. Generic Work)"""
        
        # A. Get Similarity to DOMAIN (Supply Chain)
        domain_sims = cosine_similarity([prompt_embedding], self.domain_embeddings)[0]
        domain_score = np.max(domain_sims)

        # B. Get Similarity to GENERIC (HR/IT/Marketing)
        generic_sims = cosine_similarity([prompt_embedding], self.generic_embeddings)[0]
        generic_score = np.max(generic_sims)

        # LOGIC:
        # 1. If it's strongly Supply Chain, let it pass.
        if domain_score > 0.35:
            return False, None # PASS
            
        # 2. If it's weak on Supply Chain (< 0.20), block it.
        if domain_score < 0.20:
            return True, f"BLOCK_IRRELEVANT (Low Domain Score: {domain_score:.2f})"

        # 3. THE "GRAY ZONE" (Score between 0.20 and 0.35)
        # This is where we use the contrastive check.
        # If it matches "Generic Work" BETTER than "Supply Chain", block it.
        if generic_score > domain_score:
             return True, f"BLOCK_GENERIC_WORK (Generic: {generic_score:.2f} > Domain: {domain_score:.2f})"
             
        return False, None

    def scan(self, prompt):
        is_blocked, reason = self._layer_0_regex(prompt)
        if is_blocked: return {"status": "BLOCKED", "layer": 0, "reason": reason}

        prompt_embedding = self.model.encode(prompt)

        is_blocked, reason = self._layer_1_semantic_junk(prompt_embedding)
        if is_blocked: return {"status": "BLOCKED", "layer": 1, "reason": reason}

        is_blocked, reason = self._layer_2_domain_contrastive(prompt_embedding)
        if is_blocked: return {"status": "BLOCKED", "layer": 2, "reason": reason}

        return {"status": "PASSED", "layer": "ALL", "reason": "VALID_PROMPT"}