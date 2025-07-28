#!/usr/bin/env python3
"""
Setup script for PPTMaker with Gemini API
"""

import os
import subprocess
import sys

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def create_env_file():
    """Create .env file if it doesn't exist"""
    env_file = ".env"
    
    if os.path.exists(env_file):
        print("✅ .env file already exists")
        return True
    
    print("📝 Creating .env file...")
    
    env_content = """# MongoDB Configuration
MONGODB_URI=mongodb://localhost:27017/pptmaker

# Unsplash API Configuration
UNSPLASH_ACCESS_TOKEN=your_unsplash_access_token_here

# Gemini API Configuration
GEMINI_API_KEY=your_gemini_api_key_here

# Flask Configuration
FLASK_SECRET_KEY=your_secret_key_here
"""
    
    try:
        with open(env_file, 'w') as f:
            f.write(env_content)
        print("✅ .env file created successfully")
        print("⚠️  Please update the .env file with your actual API keys")
        return True
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False

def install_dependencies():
    """Install Python dependencies"""
    print("📦 Installing dependencies...")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    directories = [
        "static/images/ppt_img",
        "static/css",
        "static/js",
        "templates"
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"📁 Created directory: {directory}")

def main():
    """Main setup function"""
    print("🚀 PPTMaker Setup with Gemini API")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        return
    
    # Create necessary directories
    create_directories()
    
    # Create .env file
    create_env_file()
    
    # Install dependencies
    if not install_dependencies():
        return
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Update the .env file with your API keys:")
    print("   - Get Gemini API key from: https://makersuite.google.com/app/apikey")
    print("   - Get Unsplash API key from: https://unsplash.com/developers")
    print("2. Test the setup: python test_gemini.py")
    print("3. Run the application: python app.py")

if __name__ == "__main__":
    main() 