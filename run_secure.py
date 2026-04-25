# Secure Configuration - Improved run.py
# ============================================

from app import create_app
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

if __name__ == '__main__':
    app = create_app()
    
    # Read configuration from environment with secure defaults
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    host = os.getenv('FLASK_HOST', '127.0.0.1')  # Default: localhost only (SECURE)
    port = int(os.getenv('FLASK_PORT', 5000))
    
    # Security logging
    print("\n" + "="*60)
    print("🚀 RUMAH MAKAN DIADOEK - STARTING APPLICATION")
    print("="*60)
    print(f"📌 Environment: {os.getenv('FLASK_ENV', 'development')}")
    print(f"🔍 Debug Mode: {debug_mode} {'⚠️  INSECURE' if debug_mode else '✅ Secure'}")
    print(f"🌐 Host: {host} {'✅ Localhost only' if host == '127.0.0.1' else '⚠️  Network accessible'}")
    print(f"🔌 Port: {port}")
    
    if debug_mode:
        print("\n⚠️  WARNING: Debug mode is enabled!")
        print("   This allows remote code execution!")
        print("   Do NOT use in production or on untrusted networks!")
    
    if host != '127.0.0.1' and not debug_mode:
        print("\n✅ Application will be accessible from network")
    elif host == '127.0.0.1':
        print("\n✅ Application is localhost-only (secure)")
    
    print("="*60 + "\n")
    
    app.run(debug=debug_mode, host=host, port=port)
