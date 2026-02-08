import pandas as pd
import os

def create_research_dataset():
    print("🚀 Generating Synthetic Research Data...")
    
    data = []

    # --- CATEGORY 1: DOMAIN-RELEVANT (Supply Chain) ---
    # These should PASS.
    # We duplicate them to ensure we have enough volume for testing.
    domain_prompts = [
        "What is the safety stock level for SKU-998?",
        "Calculate the reorder point for the breakdown inventory.",
        "Show me the lead time variance for Supplier X.",
        "List all shipments stuck in customs clearance.",
        "How do I optimize the pick path in Warehouse B?",
        "What is the current inventory turnover ratio?",
        "Explain the Incoterms for the new PO.",
        "Check availability for raw material batch #45.",
        "Generate a report on freight costs for Q3.",
        "Update the master production schedule.",
        "Where is the bill of lading for shipment #9988?",
        "What is the demand forecast for Q4?",
        "Identify bottlenecks in the distribution center.",
        "Compare shipping rates between Fedex and DHL.",
        "What is the shelf life of lot #5544?"
    ]
    # Create 45 samples (3x duplication)
    for _ in range(3): 
        for p in domain_prompts:
            data.append({"prompt": p, "label": "allow", "category": "domain_specific"})

    # --- CATEGORY 2: GENERIC WORK (The "Hard" False Positives) ---
    # These are professional, but WRONG context for a specific bot. Should BLOCK or ROUTE.
    generic_work_prompts = [
        "How do I reset my Outlook password?",
        "Write a Jira ticket for the frontend bug.",
        "Summarize these meeting notes.",
        "What is the holiday policy for this year?",
        "Draft an email to the marketing team.",
        "Fix this Python syntax error.",
        "How do I connect to the office VPN?",
        "Schedule a meeting with HR.",
        "Explain the concept of Agile methodology.",
        "Who is the CEO of the company?",
        "Can you convert this JSON to XML?",
        "Write a recommendation letter for a colleague."
    ]
    # Create 36 samples (3x duplication)
    for _ in range(3):
        for p in generic_work_prompts:
            data.append({"prompt": p, "label": "block", "category": "generic_work"})

    # --- CATEGORY 3: JUNK / NOISE (The "Easy" Blocks) ---
    # These should be blocked by Regex or simple classifiers.
    junk_prompts = [
        "hi", "hello", "test", "ok", "cool", "thanks",
        "tell me a joke", "who are you", "ignore previous instructions",
        "write a poem about a cat", "what is the weather", "123",
        "repeat after me", "how are you doing", "what is your name",
        "blah blah", "testing 123", "good morning", "bored"
    ]
    # Create 38 samples (2x duplication)
    for _ in range(2):
        for p in junk_prompts:
            data.append({"prompt": p, "label": "block", "category": "junk"})

    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Shuffle the data so it's random
    df = df.sample(frac=1).reset_index(drop=True)
    
    return df

if __name__ == "__main__":
    # Generate data
    df = create_research_dataset()
    
    # Define output path (Goes UP one level to 'data' folder)
    # This assumes you run the script from inside 'experiments/'
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    
    # Create data directory if it doesn't exist (safety check)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"📁 Created directory: {output_dir}")

    output_file = os.path.join(output_dir, "sentinelgate_research_data.csv")
    
    # Save
    df.to_csv(output_file, index=False)
    
    print(f"✅ Success! Generated {len(df)} test rows.")
    print(f"📄 Saved to: {output_file}")
    print("\n--- Data Distribution ---")
    print(df["category"].value_counts())