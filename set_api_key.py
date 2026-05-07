"""
Set OpenAI API Key Permanently
This script will save your API key directly in the config file
"""

import re
import sys

def set_api_key():
    print("=" * 60)
    print("🔑 Set OpenAI API Key Permanently")
    print("=" * 60)
    print()
    
    print("Your API key will be stored in config.py")
    print("(Make sure not to share this file publicly)")
    print()
    
    api_key = input("Enter your OpenAI API key (starts with 'sk-'): ").strip()
    
    if not api_key:
        print("❌ No API key entered. Exiting...")
        return False
    
    if not api_key.startswith('sk-'):
        print("⚠️  Warning: API keys usually start with 'sk-'")
        confirm = input("Continue anyway? (y/n): ").lower()
        if confirm != 'y':
            return False
    
    # Read config file
    config_path = 'config.py'
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"❌ Error: {config_path} not found!")
        return False
    
    # Replace the placeholder with actual API key
    # Pattern to match the OPENAI_API_KEY line
    pattern = r"(OPENAI_API_KEY = os\.environ\.get\('OPENAI_API_KEY'\) or )'your-openai-api-key-here'"
    replacement = f"\1'{api_key}'"
    
    new_content = re.sub(pattern, replacement, content)
    
    # Check if replacement was made
    if new_content == content:
        # Try alternative pattern (if already set before)
        pattern2 = r"(OPENAI_API_KEY = os\.environ\.get\('OPENAI_API_KEY'\) or )'sk-[^']*'"
        new_content = re.sub(pattern2, replacement, content)
    
    # Write back to config file
    try:
        with open(config_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print()
        print("✅ API key saved successfully!")
        print(f"📁 Updated: {config_path}")
        print()
        print("🚀 You can now run your chatbot with:")
        print("   python app.py")
        print()
        print("The GPT-4 Healthcare Assistant will be active immediately!")
        print()
        return True
        
    except Exception as e:
        print(f"❌ Error saving API key: {e}")
        return False

def view_current_key():
    """View current API key status (masked)"""
    try:
        with open('config.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract current key
        match = re.search(r"OPENAI_API_KEY = os\.environ\.get\('OPENAI_API_KEY'\) or '(sk-[^']*)'", content)
        if match:
            key = match.group(1)
            if key == 'your-openai-api-key-here':
                print("⚠️  No API key set yet (using placeholder)")
            else:
                masked = key[:10] + "..." + key[-4:]
                print(f"✅ API key is set: {masked}")
        else:
            print("❌ Could not find API key configuration")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    print()
    
    # Show current status
    print("Current Status:")
    view_current_key()
    print()
    
    # Ask what to do
    print("Options:")
    print("1. Set/Update API key")
    print("2. Exit")
    print()
    
    choice = input("Enter your choice (1/2): ").strip()
    
    if choice == '1':
        if set_api_key():
            print("\n🎉 Setup complete! Restart your server to use GPT-4.")
    else:
        print("Exiting...")
        sys.exit(0)
