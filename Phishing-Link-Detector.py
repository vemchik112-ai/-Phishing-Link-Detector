import sys
import subprocess
import urllib.parse
from urllib.parse import urlparse

def install_dependencies():
    try:
        import tldextract
        return True
    except ImportError:
        print("Installing required library tldextract...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "tldextract"])
            print("Library tldextract successfully installed!")
            return True
        except subprocess.CalledProcessError:
            print("Error: Failed to install tldextract")
            print("Try to install manually: pip install tldextract")
            return False

if not install_dependencies():
    sys.exit(1)

import tldextract
from difflib import SequenceMatcher

class PhishingLinkChecker:
    def __init__(self):
        self.original_domains = {
            'roblox.com': 'Roblox',
            'robloxlabs.com': 'Roblox Labs',
            'minecraft.net': 'Minecraft',
            'mojang.com': 'Mojang',
            'minecraftshop.com': 'Minecraft Shop',
            'steampowered.com': 'Steam',
            'steamcommunity.com': 'Steam Community',
            'valvesoftware.com': 'Valve Software',
            'store.steampowered.com': 'Steam Store',
            'help.steampowered.com': 'Steam Support',
            'login.steampowered.com': 'Steam Login',
            'epicgames.com': 'Epic Games',
            'unrealengine.com': 'Unreal Engine',
            'fortnite.com': 'Fortnite',
            'store.epicgames.com': 'Epic Games Store',
            'ea.com': 'Electronic Arts',
            'origin.com': 'Origin',
            'battlefield.com': 'Battlefield',
            'fifa.com': 'FIFA',
            'ubisoft.com': 'Ubisoft',
            'ubisoftconnect.com': 'Ubisoft Connect',
            'rainbowsix.com': 'Rainbow Six',
            'assassinscreed.com': 'Assassins Creed',
            'xbox.com': 'Xbox',
            'microsoft.com': 'Microsoft',
            'microsoftstore.com': 'Microsoft Store',
            'windows.com': 'Windows',
            'live.com': 'Microsoft Live',
            'playstation.com': 'PlayStation',
            'sony.com': 'Sony',
            'store.playstation.com': 'PlayStation Store',
            'nintendo.com': 'Nintendo',
            'nintendoswitch.com': 'Nintendo Switch',
            'battle.net': 'Battle.net',
            'blizzard.com': 'Blizzard',
            'worldofwarcraft.com': 'World of Warcraft',
            'diablo.com': 'Diablo',
            'overwatch.com': 'Overwatch',
            'discord.com': 'Discord',
            'discordapp.com': 'Discord App',
            'discord.gg': 'Discord Invite',
            'twitch.tv': 'Twitch',
            'twitch.com': 'Twitch',
            'riotgames.com': 'Riot Games',
            'leagueoflegends.com': 'League of Legends',
            'valorant.com': 'Valorant',
            'playvalorant.com': 'Play Valorant',
            'genshin.hoyoverse.com': 'Genshin Impact',
            'hoyoverse.com': 'HoYoverse',
            'hoyolab.com': 'HoYoLab',
            'facebook.com': 'Facebook',
            'instagram.com': 'Instagram',
            'twitter.com': 'Twitter',
            'x.com': 'X',
            'tiktok.com': 'TikTok',
            'linkedin.com': 'LinkedIn',
            'vk.com': 'VK',
            'telegram.org': 'Telegram',
            'whatsapp.com': 'WhatsApp',
            'reddit.com': 'Reddit',
            'pinterest.com': 'Pinterest',
            'snapchat.com': 'Snapchat',
            'google.com': 'Google',
            'youtube.com': 'YouTube',
            'github.com': 'GitHub',
            'apple.com': 'Apple',
            'icloud.com': 'iCloud',
            'amazon.com': 'Amazon',
            'netflix.com': 'Netflix',
            'cloudflare.com': 'Cloudflare',
            'paypal.com': 'PayPal',
            'wise.com': 'Wise',
            'revolut.com': 'Revolut',
            'binance.com': 'Binance',
            'coinbase.com': 'Coinbase',
            'privat24.ua': 'Privat24',
            'monobank.ua': 'MonoBank',
            'gmail.com': 'Gmail',
            'outlook.com': 'Outlook',
            'yahoo.com': 'Yahoo',
            'protonmail.com': 'ProtonMail',
            'dropbox.com': 'Dropbox',
            'mega.nz': 'MEGA',
            'drive.google.com': 'Google Drive'
        }

    def extract_base_domain(self, url):
        try:
            extracted = tldextract.extract(url)
            base_domain = f"{extracted.domain}.{extracted.suffix}"
            return base_domain.lower()
        except Exception as e:
            print(f"Error extracting domain: {e}")
            return None

    def extract_full_domain(self, url):
        try:
            parsed = urlparse(url)
            if not parsed.netloc:
                parsed = urlparse('https://' + url)
            return parsed.netloc.lower()
        except Exception as e:
            print(f"Error extracting domain: {e}")
            return None

    def calculate_similarity(self, str1, str2):
        if not str1 or not str2:
            return 0
        return int(SequenceMatcher(None, str1, str2).ratio() * 100)

    def find_most_similar_original(self, test_domain):
        best_match = None
        best_similarity = 0
        
        for original_domain, service_name in self.original_domains.items():
            similarity = self.calculate_similarity(test_domain, original_domain)
            if similarity > best_similarity:
                best_similarity = similarity
                best_match = (original_domain, service_name)
        
        return best_match, best_similarity

    def is_phishing(self, url):
        full_domain = self.extract_full_domain(url)
        base_domain = self.extract_base_domain(url)
        
        if not full_domain or not base_domain:
            return True, "Failed to extract domain", None
        
        if base_domain in self.original_domains:
            return False, f"Original domain {self.original_domains[base_domain]}", None
        
        best_match, similarity = self.find_most_similar_original(base_domain)
        
        if best_match and similarity > 70:
            original_domain, service_name = best_match
            return True, f"PHISHING! Fake domain of {service_name}", service_name
        
        return True, "Unknown domain - possible phishing", None

    def analyze_url(self, url):
        print(f"Analyzing URL: {url}")
        print("=" * 50)
        
        full_domain = self.extract_full_domain(url)
        base_domain = self.extract_base_domain(url)
        print(f"Full domain: {full_domain}")
        print(f"Base domain: {base_domain}")
        
        is_phishing, message, service_name = self.is_phishing(url)
        
        if is_phishing:
            print(f"RESULT: {message}")
            print("HIGH PHISHING RISK!")
            print("Do not enter personal data on this site!")
        else:
            print(f"RESULT: {message}")
            print("Domain is safe")
        
        print("=" * 50)
        return not is_phishing

def main():
    checker = PhishingLinkChecker()
    
    print("Phishing Link Analyzer")
    print("=" * 30)
    
    while True:
        print("\nEnter URL to check (or 'quit' to exit):")
        url = input().strip()
        
        if url.lower() in ['quit', 'exit', 'q']:
            break
            
        if not url:
            continue
            
        try:
            checker.analyze_url(url)
                
        except Exception as e:
            print(f"Error analyzing URL: {e}")

if __name__ == "__main__":
    main()