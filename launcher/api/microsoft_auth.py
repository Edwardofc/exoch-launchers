"""
Microsoft Authentication Module
"""

import requests
import webbrowser
import time
import json
from typing import Dict, Optional
import threading
from queue import Queue

class MicrosoftAuth:
    """Handles Microsoft authentication for Minecraft."""
    
    # Microsoft OAuth endpoints
    AUTH_URL = "https://login.microsoftonline.com/consumers/oauth2/v2.0/authorize"
    TOKEN_URL = "https://login.microsoftonline.com/consumers/oauth2/v2.0/token"
    XBL_URL = "https://user.auth.xboxlive.com/user/authenticate"
    XSTS_URL = "https://xsts.auth.xboxlive.com/xsts/authorize"
    MINECRAFT_URL = "https://api.minecraftservices.com/authentication/login_with_xbox"
    OWNERSHIP_URL = "https://api.minecraftservices.com/entitlements/mcstore"
    PROFILE_URL = "https://api.minecraftservices.com/minecraft/profile"
    
    # Application credentials (Microsoft Application Registration Portal)
    CLIENT_ID = "00000000-0000-0000-0000-000000000000"
    REDIRECT_URI = "https://login.microsoftonline.com/common/oauth2/nativeclient"
    SCOPE = "XboxLive.signin offline_access"
    
    def __init__(self):
        self.auth_data = {
            "access_token": None,
            "refresh_token": None,
            "token_expiry": 0,
            "xbox_token": None,
            "xsts_token": None,
            "user_hash": None,
            "minecraft_token": None,
            "profile": None
        }
        self.auth_queue = Queue()
    
    def generate_auth_url(self) -> str:
        """Generate Microsoft OAuth authorization URL."""
        params = {
            "client_id": self.CLIENT_ID,
            "response_type": "code",
            "redirect_uri": self.REDIRECT_URI,
            "scope": self.SCOPE,
            "state": "12345",
            "prompt": "select_account"
        }
        
        url = requests.Request('GET', self.AUTH_URL, params=params).prepare().url
        return url
    
    def authenticate(self) -> Optional[Dict]:
        """Authenticate with Microsoft account."""
        auth_url = self.generate_auth_url()
        
        # Open browser for authentication
        webbrowser.open(auth_url)
        
        # Wait for user to complete authentication
        auth_code = self.wait_for_auth_code()
        
        if not auth_code:
            return None
        
        # Exchange authorization code for tokens
        token_response = self.exchange_code_for_tokens(auth_code)
        
        if not token_response:
            return None
        
        # Authenticate with Xbox Live
        xbox_response = self.authenticate_with_xbox(token_response["access_token"])
        
        if not xbox_response:
            return None
        
        # Get XSTS token
        xsts_response = self.get_xsts_token(xbox_response["Token"])
        
        if not xsts_response:
            return None
        
        # Authenticate with Minecraft
        minecraft_response = self.authenticate_with_minecraft(
            xsts_response["DisplayClaims"]["xui"][0]["uhs"],
            xsts_response["Token"]
        )
        
        if not minecraft_response:
            return None
        
        # Verify Minecraft ownership
        ownership_response = self.verify_minecraft_ownership(
            minecraft_response["access_token"]
        )
        
        if not ownership_response:
            return None
        
        # Get Minecraft profile
        profile_response = self.get_minecraft_profile(minecraft_response["access_token"])
        
        # Update auth data
        self.auth_data.update({
            "access_token": token_response["access_token"],
            "refresh_token": token_response["refresh_token"],
            "token_expiry": time.time() + token_response["expires_in"],
            "xbox_token": xbox_response["Token"],
            "xsts_token": xsts_response["Token"],
            "user_hash": xsts_response["DisplayClaims"]["xui"][0]["uhs"],
            "minecraft_token": minecraft_response["access_token"],
            "profile": profile_response
        })
        
        return self.auth_data
    
    def wait_for_auth_code(self) -> Optional[str]:
        """Wait for authentication code from browser."""
        # This is a simplified version - in real implementation, you would use a local server
        # or redirect URI listener
        print("Please authenticate in your browser and paste the code below:")
        auth_code = input("Authorization code: ").strip()
        return auth_code
    
    def exchange_code_for_tokens(self, auth_code: str) -> Optional[Dict]:
        """Exchange authorization code for access and refresh tokens."""
        data = {
            "client_id": self.CLIENT_ID,
            "scope": self.SCOPE,
            "code": auth_code,
            "redirect_uri": self.REDIRECT_URI,
            "grant_type": "authorization_code"
        }
        
        try:
            response = requests.post(
                self.TOKEN_URL,
                data=data,
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
            
            response.raise_for_status()
            return response.json()
        
        except Exception as e:
            print(f"Error exchanging code: {e}")
            return None
    
    def authenticate_with_xbox(self, access_token: str) -> Optional[Dict]:
        """Authenticate with Xbox Live."""
        data = {
            "Properties": {
                "AuthMethod": "RPS",
                "SiteName": "user.auth.xboxlive.com",
                "RpsTicket": access_token
            },
            "RelyingParty": "http://auth.xboxlive.com",
            "TokenType": "JWT"
        }
        
        try:
            response = requests.post(
                self.XBL_URL,
                json=data,
                headers={"Content-Type": "application/json"}
            )
            
            response.raise_for_status()
            return response.json()
        
        except Exception as e:
            print(f"Error authenticating with Xbox: {e}")
            return None
    
    def get_xsts_token(self, xbox_token: str) -> Optional[Dict]:
        """Get XSTS token from Xbox Live."""
        data = {
            "Properties": {
                "SandboxId": "RETAIL",
                "UserTokens": [xbox_token]
            },
            "RelyingParty": "rp://api.minecraftservices.com/",
            "TokenType": "JWT"
        }
        
        try:
            response = requests.post(
                self.XSTS_URL,
                json=data,
                headers={"Content-Type": "application/json"}
            )
            
            response.raise_for_status()
            return response.json()
        
        except Exception as e:
            print(f"Error getting XSTS token: {e}")
            return None
    
    def authenticate_with_minecraft(self, user_hash: str, xsts_token: str) -> Optional[Dict]:
        """Authenticate with Minecraft services."""
        data = {
            "identityToken": f"XBL3.0 x={user_hash};{xsts_token}"
        }
        
        try:
            response = requests.post(
                self.MINECRAFT_URL,
                json=data,
                headers={"Content-Type": "application/json"}
            )
            
            response.raise_for_status()
            return response.json()
        
        except Exception as e:
            print(f"Error authenticating with Minecraft: {e}")
            return None
    
    def verify_minecraft_ownership(self, minecraft_token: str) -> Optional[Dict]:
        """Verify Minecraft ownership."""
        headers = {
            "Authorization": f"Bearer {minecraft_token}"
        }
        
        try:
            response = requests.get(
                self.OWNERSHIP_URL,
                headers=headers
            )
            
            response.raise_for_status()
            return response.json()
        
        except Exception as e:
            print(f"Error verifying Minecraft ownership: {e}")
            return None
    
    def get_minecraft_profile(self, minecraft_token: str) -> Optional[Dict]:
        """Get Minecraft profile."""
        headers = {
            "Authorization": f"Bearer {minecraft_token}"
        }
        
        try:
            response = requests.get(
                self.PROFILE_URL,
                headers=headers
            )
            
            response.raise_for_status()
            return response.json()
        
        except Exception as e:
            print(f"Error getting Minecraft profile: {e}")
            return None
    
    def refresh_tokens(self) -> Optional[Dict]:
        """Refresh access token using refresh token."""
        if not self.auth_data["refresh_token"]:
            return None
        
        data = {
            "client_id": self.CLIENT_ID,
            "scope": self.SCOPE,
            "refresh_token": self.auth_data["refresh_token"],
            "grant_type": "refresh_token"
        }
        
        try:
            response = requests.post(
                self.TOKEN_URL,
                data=data,
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
            
            response.raise_for_status()
            token_data = response.json()
            
            self.auth_data["access_token"] = token_data["access_token"]
            self.auth_data["refresh_token"] = token_data["refresh_token"]
            self.auth_data["token_expiry"] = time.time() + token_data["expires_in"]
            
            return self.auth_data
        
        except Exception as e:
            print(f"Error refreshing tokens: {e}")
            return None
    
    def is_authenticated(self) -> bool:
        """Check if user is authenticated and tokens are valid."""
        return (
            self.auth_data["minecraft_token"] is not None and
            time.time() < self.auth_data["token_expiry"] - 300
        )
    
    def get_profile(self) -> Optional[Dict]:
        """Get Minecraft profile."""
        return self.auth_data["profile"]
    
    def get_minecraft_token(self) -> Optional[str]:
        """Get Minecraft access token."""
        return self.auth_data["minecraft_token"]
    
    def logout(self):
        """Logout and clear authentication data."""
        self.auth_data = {
            "access_token": None,
            "refresh_token": None,
            "token_expiry": 0,
            "xbox_token": None,
            "xsts_token": None,
            "user_hash": None,
            "minecraft_token": None,
            "profile": None
        }