# MurMur - Système de détection intelligente des bugs
# Architecture modulaire pour détecter et corriger automatiquement les problèmes

import time
import psutil
import threading
from dataclasses import dataclass
from typing import Dict, List, Callable, Any
from collections import deque, defaultdict

@dataclass
class SystemEvent:
    """Représente un événement système détecté"""
    timestamp: float
    event_type: str
    source: str
    data: Dict[str, Any]
    severity: int  # 1-5

@dataclass
class Pattern:
    """Définit un pattern de bug à détecter"""
    name: str
    conditions: List[Callable]
    time_window: int  # secondes
    threshold: int    # nombre d'occurrences
    action: Callable
    cooldown: int = 300  # 5 min avant re-déclenchement

class EventCollector:
    """Collecte et analyse les événements système en temps réel"""
    
    def __init__(self):
        self.events = deque(maxlen=1000)  # Buffer circulaire
        self.patterns = []
        self.last_triggers = defaultdict(float)
        self.user_behavior = {
            'click_patterns': deque(maxlen=50),
            'app_usage': defaultdict(list),
            'error_frequency': defaultdict(int)
        }
    
    def add_event(self, event: SystemEvent):
        """Ajoute un événement et déclenche l'analyse"""
        self.events.append(event)
        self._analyze_patterns()
    
    def _analyze_patterns(self):
        """Analyse les patterns en temps réel"""
        current_time = time.time()
        
        for pattern in self.patterns:
            # Éviter le spam avec cooldown
            if current_time - self.last_triggers[pattern.name] < pattern.cooldown:
                continue
                
            # Analyser les événements dans la fenêtre temporelle
            recent_events = [e for e in self.events 
                           if current_time - e.timestamp <= pattern.time_window]
            
            # Vérifier si le pattern match
            if self._pattern_matches(pattern, recent_events):
                print(f"🔧 Pattern détecté: {pattern.name}")
                self._execute_fix(pattern)
                self.last_triggers[pattern.name] = current_time

    def _pattern_matches(self, pattern: Pattern, events: List[SystemEvent]) -> bool:
        """Vérifie si un pattern correspond aux événements récents"""
        matching_events = []
        
        for event in events:
            if all(condition(event) for condition in pattern.conditions):
                matching_events.append(event)
        
        return len(matching_events) >= pattern.threshold

    def _execute_fix(self, pattern: Pattern):
        """Exécute la correction associée au pattern"""
        try:
            pattern.action()
            print(f"✅ Correction appliquée: {pattern.name}")
        except Exception as e:
            print(f"❌ Erreur lors de la correction: {e}")

class NetworkMonitor:
    """Moniteur spécialisé pour les problèmes réseau"""
    
    def __init__(self, event_collector: EventCollector):
        self.collector = event_collector
        self.last_connection_state = True
        self.disconnection_count = 0
        
    def monitor_wifi(self):
        """Surveille l'état du Wi-Fi"""
        while True:
            try:
                # Vérification de la connectivité
                current_state = self._check_internet_connection()
                
                if not current_state and self.last_connection_state:
                    # Déconnexion détectée
                    self.disconnection_count += 1
                    event = SystemEvent(
                        timestamp=time.time(),
                        event_type="network_disconnect",
                        source="wifi_monitor",
                        data={"disconnect_count": self.disconnection_count},
                        severity=3
                    )
                    self.collector.add_event(event)
                
                self.last_connection_state = current_state
                time.sleep(5)  # Check toutes les 5 secondes
                
            except Exception as e:
                print(f"Erreur monitoring Wi-Fi: {e}")
                time.sleep(10)
    
    def _check_internet_connection(self) -> bool:
        """Vérifie la connectivité internet"""
        try:
            import socket
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            return True
        except OSError:
            return False

class ProcessMonitor:
    """Moniteur pour les processus qui plantent ou se bloquent"""
    
    def __init__(self, event_collector: EventCollector):
        self.collector = event_collector
        self.process_states = {}
        
    def monitor_critical_processes(self):
        """Surveille les processus critiques"""
        critical_processes = [
            "explorer.exe",  # Windows Explorer
            "dwm.exe",       # Desktop Window Manager
            "winlogon.exe",  # Windows Logon
        ]
        
        while True:
            try:
                for proc_name in critical_processes:
                    self._check_process_health(proc_name)
                time.sleep(10)
            except Exception as e:
                print(f"Erreur monitoring processus: {e}")
                time.sleep(15)
    
    def _check_process_health(self, process_name: str):
        """Vérifie la santé d'un processus spécifique"""
        try:
            processes = [p for p in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']) 
                        if p.info['name'].lower() == process_name.lower()]
            
            if not processes:
                # Processus critique manquant
                event = SystemEvent(
                    timestamp=time.time(),
                    event_type="process_missing",
                    source="process_monitor",
                    data={"process_name": process_name},
                    severity=5
                )
                self.collector.add_event(event)
                return
            
            for proc in processes:
                # Détection de processus figé (CPU=0% pendant longtemps)
                cpu_usage = proc.info['cpu_percent']
                if cpu_usage == 0.0 and process_name in self.process_states:
                    # Processus potentiellement figé
                    event = SystemEvent(
                        timestamp=time.time(),
                        event_type="process_frozen",
                        source="process_monitor",
                        data={"process_name": process_name, "pid": proc.info['pid']},
                        severity=4
                    )
                    self.collector.add_event(event)
                
                self.process_states[process_name] = {
                    'last_cpu': cpu_usage,
                    'last_check': time.time()
                }
                
        except Exception as e:
            print(f"Erreur check process {process_name}: {e}")

class FixEngine:
    """Moteur de corrections automatiques"""
    
    @staticmethod
    def restart_wifi():
        """Redémarre la connexion Wi-Fi (Windows uniquement)"""
        import subprocess
        import platform
        import re

        if platform.system() != "Windows":
            print("Cette fonction n'est disponible que sous Windows")
            return

        try:
            # Récupération des profils Wi-Fi enregistrés
            profiles_output = subprocess.check_output(
                ["netsh", "wlan", "show", "profiles"], encoding="utf-8", errors="ignore"
            )

            matches = re.findall(
                r"(?:Profil Tous les utilisateurs|All User Profile)\s*:\s*(.*)",
                profiles_output,
            )

            if not matches:
                print("❌ Aucun profil Wi-Fi trouvé")
                return

            profile_name = matches[0].strip()

            subprocess.run(["netsh", "wlan", "disconnect"], check=True)
            time.sleep(2)
            print(f"🔄 Tentative de reconnexion à : {profile_name}")
            subprocess.run([
                "netsh",
                "wlan",
                "connect",
                f"name={profile_name}",
            ], check=True)
            print("✅ Wi-Fi reconnecté avec succès")

        except subprocess.CalledProcessError as e:
            print(f"❌ Erreur de reconnexion : {e}")
    
    @staticmethod
    def restart_explorer():
        """Redémarre l'explorateur Windows"""
        try:
            # Tuer explorer.exe
            for proc in psutil.process_iter(['pid', 'name']):
                if proc.info['name'].lower() == 'explorer.exe':
                    proc.kill()
            
            time.sleep(2)
            
            # Relancer explorer.exe
            import subprocess
            subprocess.Popen(["explorer.exe"])
        except Exception as e:
            print(f"Erreur redémarrage Explorer: {e}")
    
    @staticmethod
    def clear_temp_files():
        """Nettoie les fichiers temporaires corrompus"""
        import tempfile
        import shutil
        import os
        
        try:
            temp_dir = tempfile.gettempdir()
            for filename in os.listdir(temp_dir):
                filepath = os.path.join(temp_dir, filename)
                try:
                    if os.path.isfile(filepath):
                        # Tenter de supprimer les fichiers de plus de 1 jour
                        if time.time() - os.path.getctime(filepath) > 86400:
                            os.remove(filepath)
                except (PermissionError, FileNotFoundError):
                    continue  # Ignorer les fichiers en cours d'utilisation
        except Exception as e:
            print(f"Erreur nettoyage temp: {e}")

def setup_murmur_patterns(collector: EventCollector):
    """Configure les patterns de détection pour MurMur"""
    
    # Pattern 1: Wi-Fi qui décroche répétitivement
    wifi_pattern = Pattern(
        name="wifi_instability",
        conditions=[
            lambda e: e.event_type == "network_disconnect",
            lambda e: e.severity >= 3
        ],
        time_window=300,  # 5 minutes
        threshold=2,      # 2 déconnexions en 5 min
        action=FixEngine.restart_wifi,
        cooldown=600      # 10 min avant re-déclenchement
    )
    
    # Pattern 2: Explorer Windows qui plante
    explorer_pattern = Pattern(
        name="explorer_freeze",
        conditions=[
            lambda e: e.event_type == "process_frozen",
            lambda e: e.data.get("process_name", "").lower() == "explorer.exe"
        ],
        time_window=60,   # 1 minute
        threshold=1,      # 1 seule détection suffit
        action=FixEngine.restart_explorer,
        cooldown=300
    )
    
    # Pattern 3: Accumulation de fichiers temp
    temp_cleanup_pattern = Pattern(
        name="temp_files_cleanup",
        conditions=[
            lambda e: e.event_type == "disk_space_low" or e.event_type == "temp_files_corrupted"
        ],
        time_window=3600, # 1 heure
        threshold=1,
        action=FixEngine.clear_temp_files,
        cooldown=7200     # 2 heures
    )
    
    collector.patterns.extend([wifi_pattern, explorer_pattern, temp_cleanup_pattern])

# Point d'entrée principal
if __name__ == "__main__":
    print("🤫 MurMur - Agent silencieux démarré")
    
    # Initialisation
    collector = EventCollector()
    setup_murmur_patterns(collector)
    
    # Lancement des moniteurs
    network_monitor = NetworkMonitor(collector)
    process_monitor = ProcessMonitor(collector)
    
    # Threads de monitoring
    network_thread = threading.Thread(target=network_monitor.monitor_wifi, daemon=True)
    process_thread = threading.Thread(target=process_monitor.monitor_critical_processes, daemon=True)
    
    network_thread.start()
    process_thread.start()
    
    print("✅ Monitoring actif - MurMur surveille votre système...")
    
    # Boucle principale
    try:
        while True:
            time.sleep(30)  # Heartbeat toutes les 30 secondes
    except KeyboardInterrupt:
        print("🛑 MurMur arrêté par l'utilisateur")