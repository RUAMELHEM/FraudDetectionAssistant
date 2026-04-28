"""
Visionerr Fraud Guard API Startup Script
This script properly sets up the environment and starts the API server
"""

import os
import sys
import subprocess

def main():
    # Get the script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    # Change to backend directory
    os.chdir(script_dir)
    
    print("="*70)
    print("🚀 VISIONERR FRAUD GUARD API SERVER")
    print("="*70)
    print(f"\n📍 Backend Directory: {script_dir}")
    print(f"📍 Project Root: {project_root}")
    print(f"📍 Current Working Directory: {os.getcwd()}")
    print(f"\n🔗 API URL: http://127.0.0.1:8000")
    print(f"📚 Docs URL: http://127.0.0.1:8000/docs")
    print(f"📚 ReDoc URL: http://127.0.0.1:8000/redoc")
    print("\n" + "="*70)
    print("Press Ctrl+C to stop the server")
    print("="*70 + "\n")
    
    # Start uvicorn server
    try:
        import uvicorn
        uvicorn.run(
            "api:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except ImportError:
        print("❌ Error: uvicorn not installed")
        print("\nTo install dependencies, run:")
        print(f"  pip install -r {os.path.join(project_root, 'requirements.txt')}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
