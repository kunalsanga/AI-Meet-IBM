#!/usr/bin/env python3
"""
Setup script for AI Meeting Assistant

This script helps users set up the environment and dependencies
for the AI Meeting Assistant application.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required.")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True


def install_dependencies():
    """Install required dependencies."""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False


def setup_environment():
    """Set up environment file."""
    env_file = Path(".env")
    env_example = Path("env_example.txt")
    
    if env_file.exists():
        print("✅ .env file already exists")
        return True
    
    if env_example.exists():
        print("📝 Creating .env file from template...")
        shutil.copy(env_example, env_file)
        print("✅ .env file created!")
        print("⚠️  Please edit .env file with your IBM API credentials")
        return True
    else:
        print("❌ env_example.txt not found")
        return False


def create_directories():
    """Create necessary directories."""
    directories = ["utils", "samples"]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Created directory: {directory}")


def check_streamlit():
    """Check if Streamlit is properly installed."""
    try:
        import streamlit
        print(f"✅ Streamlit version: {streamlit.__version__}")
        return True
    except ImportError:
        print("❌ Streamlit not found. Please install dependencies first.")
        return False


def run_tests():
    """Run basic tests to ensure everything works."""
    print("🧪 Running basic tests...")
    
    try:
        # Test imports
        from utils.granite_api import granite_api
        from utils.summarizer import summarizer
        print("✅ All modules imported successfully")
        
        # Test mock functionality
        mock_transcript = granite_api._get_mock_transcript()
        mock_summary = granite_api._get_mock_summary()
        
        if mock_transcript and mock_summary:
            print("✅ Mock data generation working")
        else:
            print("❌ Mock data generation failed")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False


def main():
    """Main setup function."""
    print("🚀 AI Meeting Assistant Setup")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Setup environment
    setup_environment()
    
    # Check Streamlit
    if not check_streamlit():
        sys.exit(1)
    
    # Run tests
    if not run_tests():
        print("⚠️  Some tests failed, but setup may still work")
    
    print("\n🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Edit .env file with your IBM API credentials")
    print("2. Run: streamlit run app.py")
    print("3. Open http://localhost:8501 in your browser")
    print("\nFor help, see README.md")


if __name__ == "__main__":
    main() 