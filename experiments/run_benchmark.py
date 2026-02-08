# import pandas as pd
# import sys
# import os
# import time

# # Add the 'src' folder to the python path so we can import filters.py
# sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
# from filters import SentinelGate

# def run_benchmark():
#     # 1. Load Data
#     data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'sentinelgate_research_data.csv')
#     if not os.path.exists(data_path):
#         print("❌ Error: Data file not found. Did you run generate_data.py?")
#         return

#     df = pd.read_csv(data_path)
#     print(f"📊 Loaded {len(df)} test cases.")

#     # 2. Initialize the Guardrail
#     # gate = SentinelGate()
#     from sentinelgate import load_config, SentinelGate
#     gate = SentinelGate(load_config())
#     decision = gate.check(prompt)

#     # 3. Run the Experiment
#     results = []
    
#     print("\n🚀 Running Benchmark... (This measures latency too)")
#     start_time = time.perf_counter()
    
#     total_tokens_saved = 0
#     # approximate cost per 1k tokens (GPT-4 input price)
#     COST_PER_1K_TOKENS = 0.03 

#     for index, row in df.iterrows():
#         prompt = row['prompt']
#         expected = row['label'] # 'allow' or 'block'
#         category = row['category']
        
#         # Measure latency per request
#         req_start = time.perf_counter()
#         decision = gate.scan(prompt)
#         req_end = time.perf_counter()
#         latency_ms = (req_end - req_start) * 1000
        
#         # Determine if we were correct
#         system_status = "allow" if decision["status"] == "PASSED" else "block"
#         is_correct = (system_status == expected)
        
#         # Simulate Token Savings
#         # approx 1 word = 1.3 tokens. 
#         # If BLOCKED, we saved the tokens of the prompt + hypothetical 500 token answer
#         tokens_saved = 0
#         if system_status == "block":
#             tokens_saved = len(prompt.split()) * 1.3 + 500 # Saved input + output cost
#             total_tokens_saved += tokens_saved

#         results.append({
#             "prompt": prompt,
#             "category": category,
#             "expected": expected,
#             "predicted": system_status,
#             "correct": is_correct,
#             "latency_ms": latency_ms,
#             "blocked_reason": decision.get("reason", "N/A"),
#             "layer_caught": decision.get("layer", "N/A")
#         })

#     total_time = time.perf_counter() - start_time

    
#     # 4. Save Results
#     results_df = pd.DataFrame(results)
#     output_path = os.path.join(os.path.dirname(__file__), 'benchmark_results.csv')
#     results_df.to_csv(output_path, index=False)
    
#     # 5. Print Summary Metrics for the Paper
#     accuracy = results_df["correct"].mean() * 100
#     avg_latency = results_df["latency_ms"].mean()
#     estimated_money_saved = (total_tokens_saved / 1000) * COST_PER_1K_TOKENS

#     print("\n" + "="*40)
#     print(f"📝 FINAL RESULTS (For your Research Paper)")
#     print("="*40)
#     print(f"✅ Overall Accuracy:      {accuracy:.2f}%")
#     print(f"⚡ Avg Latency per Call:  {avg_latency:.2f} ms")
#     print(f"💰 Est. Token Savings:    {int(total_tokens_saved)} tokens")
#     print(f"💵 Est. Money Saved:      ${estimated_money_saved:.4f} (per 100 calls)")
    
#     print("\n--- Breakdown by Category ---")
#     print(results_df.groupby("category")["correct"].mean() * 100)
    
#     print("\n--- Breakdown by Blocking Layer ---")
#     print(results_df["layer_caught"].value_counts())
    
#     print(f"\n📂 Detailed results saved to: {output_path}")

# if __name__ == "__main__":
#     run_benchmark()


import time
import pandas as pd



import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


# New engine (config-driven)
from src.sentinelgate import load_config, SentinelGate


def run_benchmark():
    # 1) Load Data
    data_path = os.path.join(
        os.path.dirname(__file__),
        "..",
        "data",
        "sentinelgate_research_data.csv"
    )

    if not os.path.exists(data_path):
        print("❌ Error: Data file not found:", data_path)
        print("Did you run generate_data.py or create sentinelgate_research_data.csv?")
        return

    df = pd.read_csv(data_path)
    print(f"📊 Loaded {len(df)} test cases.")

    # 2) Initialize the Guardrail (new engine)
    cfg = load_config()
    gate = SentinelGate(cfg)

    # 3) Run the Experiment
    results = []
    print("\n🚀 Running Benchmark... (measures latency too)")
    start_time = time.perf_counter()

    total_tokens_saved = 0.0
    COST_PER_1K_TOKENS = 0.03  # approx input price; adjust in paper if needed

    for _, row in df.iterrows():
        prompt = str(row["prompt"])
        expected = str(row["label"]).strip().lower()   # "allow" or "block"
        category = str(row.get("category", "unknown"))

        # Measure latency per request
        req_start = time.perf_counter()
        d = gate.check(prompt)
        req_end = time.perf_counter()
        latency_ms = (req_end - req_start) * 1000.0

        # Map Decision -> allow/block for this benchmark
        # (FinOps strict mode: ROUTE treated as block to avoid LLM call)
        system_status = "allow" if d.decision == "ALLOW" else "block"
        is_correct = (system_status == expected)

        # Simulate token savings (rough)
        tokens_saved = 0.0
        if system_status == "block":
            tokens_saved = (len(prompt.split()) * 1.3) + 500  # saved input + hypothetical output
            total_tokens_saved += tokens_saved

        # Infer layer caught from reason
        if d.reason.startswith("junk_"):
            layer = "L0"
        elif d.reason == "semantic_noise":
            layer = "L1"
        else:
            layer = "L2"

        results.append({
            "prompt": prompt,
            "category": category,
            "expected": expected,
            "predicted": system_status,
            "correct": is_correct,
            "latency_ms": latency_ms,
            "reason": d.reason,
            "layer_caught": layer,
            "similarity": d.similarity,
            "margin": d.margin,
            "tokens_saved": tokens_saved,
        })

    total_time = time.perf_counter() - start_time

    # 4) Save Results
    results_df = pd.DataFrame(results)
    output_path = os.path.join(os.path.dirname(__file__), "benchmark_results.csv")
    results_df.to_csv(output_path, index=False)

    # 5) Print Summary Metrics
    accuracy = results_df["correct"].mean() * 100.0
    avg_latency = results_df["latency_ms"].mean()
    estimated_money_saved = (total_tokens_saved / 1000.0) * COST_PER_1K_TOKENS

    print("\n" + "=" * 44)
    print("📝 FINAL RESULTS (For your Research Paper)")
    print("=" * 44)
    print(f"✅ Overall Accuracy:        {accuracy:.2f}%")
    print(f"⚡ Avg Latency per Call:    {avg_latency:.2f} ms")
    print(f"⏱️ Total Benchmark Time:    {total_time:.2f} s")
    print(f"💰 Est. Token Savings:      {int(total_tokens_saved)} tokens")
    print(f"💵 Est. Money Saved:        ${estimated_money_saved:.4f} (per 100 calls)")

    if "category" in results_df.columns:
        print("\n--- Breakdown by Category ---")
        print((results_df.groupby("category")["correct"].mean() * 100.0).round(2))

    print("\n--- Breakdown by Blocking Layer ---")
    print(results_df["layer_caught"].value_counts())

    print(f"\n📂 Detailed results saved to: {output_path}")


if __name__ == "__main__":
    run_benchmark()
