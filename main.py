# main.py

import os
from dotenv import load_dotenv
from utils.linkedin_lookup import search_linkedin_profiles
from utils.email_finder import extract_email_and_phone
from utils.reddit_scraper import get_reddit_posts
from utils.pdf_exporter import export_to_pdf
from utils.gemini_profession_classifier import classify_profession_and_industry

load_dotenv()

print("[🧠] AI Lead Finder - LinkedIn + Reddit + PDF Export\n")

# 📥 Step 1: Get input from user
name = input("🔎 Enter a name or role (e.g., 'Sarah AI CEO'): ").strip()

# 🔗 Step 2: Try finding LinkedIn profile via Gemini & Google
print(f"\n[🔍] Searching LinkedIn for: {name}\n")
linkedin_url, profile_text = get_linkedin_profile(name)

# ✅ Step 3: If LinkedIn not found, ask user to manually paste
if not linkedin_url:
    print("❌ No LinkedIn profile found for given name.")
    manual = input("🔗 Do you want to paste a LinkedIn profile URL manually? (y/n): ").strip().lower()
    if manual == 'y':
        linkedin_url = input("📎 Paste LinkedIn profile URL: ").strip()
        linkedin_url, profile_text = get_linkedin_profile(linkedin_url, manual=True)
    else:
        linkedin_url = "Not Found"
        profile_text = ""

# 🤖 Step 4: Classify role and industry using Gemini
role, company = classify_profession_and_industry(profile_text)

# 📧 Step 5: Extract contact info from LinkedIn profile content
email, phone = extract_email_and_phone(profile_text)

# 🔎 Step 6: Search Reddit for relevant posts
reddit_posts = get_reddit_posts(name)

# 📦 Step 7: Format result
result = {
    "name": name,
    "role": role,
    "company": company,
    "email": email,
    "phone": phone,
    "linkedin": linkedin_url,
    "reddit_posts": reddit_posts,
    "source_input": name,
}

# 📝 Step 8: Export to PDF
export_to_pdf([result], filename="data/output.pdf")

print("\n[✅] SUCCESS!")
print("📁 Saved to data/output.pdf")
