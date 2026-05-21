import os
import subprocess
import threading
from collections import deque
import yaml
from app.core.database import supabase

class MediaMTXManager:
    """Manages the lifecycle of the MediaMTX media server subprocess."""
    
    def __init__(self):
        self.process = None
        self.log_buffer = deque(maxlen=500)
        self.config_path = "/home/whiteshark/Projects/aegis/mediamtx/mediamtx.yml"
        self._thread = None
        self.log_buffer.append("[SYSTEM] MediaMTX Manager Initialized.\n")

    def is_running(self) -> bool:
        """Check if the MediaMTX process is currently active."""
        return self.process is not None and self.process.poll() is None

    def start(self) -> dict:
        """Sync camera configurations and start the MediaMTX subprocess."""
        if self.is_running():
            return {"status": "already_running"}

        # Perform a camera sync before launching mediamtx
        self.sync_cameras()

        try:
            mediamtx_dir = "/home/whiteshark/Projects/aegis/mediamtx"
            self.process = subprocess.Popen(
                ["mediamtx", "mediamtx.yml"],
                cwd=mediamtx_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )

            # Start background thread to capture logs asynchronously
            self._thread = threading.Thread(target=self._read_logs, daemon=True)
            self._thread.start()

            self.log_buffer.append("[SYSTEM] MediaMTX Subprocess Launched.\n")
            return {"status": "started"}
            
        except FileNotFoundError:
            err = "MediaMTX executable not found in system PATH."
            self.log_buffer.append(f"[SYSTEM ERROR] {err}\n")
            return {"status": "error", "message": err}
        except Exception as e:
            err = f"Failed to start MediaMTX: {str(e)}"
            self.log_buffer.append(f"[SYSTEM ERROR] {err}\n")
            return {"status": "error", "message": err}

    def stop(self) -> dict:
        """Safely terminate the MediaMTX subprocess."""
        if not self.is_running():
            return {"status": "already_stopped"}

        try:
            self.log_buffer.append("[SYSTEM] Terminating MediaMTX Subprocess...\n")
            self.process.terminate()
            try:
                self.process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.log_buffer.append("[SYSTEM WARNING] Subprocess did not terminate; killing...\n")
                self.process.kill()
                self.process.wait()
        except Exception as e:
            self.log_buffer.append(f"[SYSTEM ERROR] Exception during stop: {str(e)}\n")

        self.process = None
        self.log_buffer.append("[SYSTEM] MediaMTX Subprocess Stopped.\n")
        return {"status": "stopped"}

    def restart(self) -> dict:
        """Restart the MediaMTX subprocess."""
        self.stop()
        return self.start()

    def get_logs(self) -> list[str]:
        """Get the accumulated logs from the MediaMTX subprocess buffer."""
        return list(self.log_buffer)

    def _read_logs(self):
        """Asynchronously read lines from the subprocess's stdout and append them to log_buffer."""
        while self.is_running():
            try:
                line = self.process.stdout.readline()
                if not line:
                    break
                self.log_buffer.append(line)
            except Exception:
                break

    def sync_cameras(self):
        """Fetch active camera feeds from Supabase and synchronize them with mediamtx.yml."""
        try:
            res = supabase.table("cameras").select("*").execute()
            cameras = res.data if res.data else []

            # Read the current mediamtx configuration file
            if os.path.exists(self.config_path):
                with open(self.config_path, "r") as f:
                    config_data = yaml.safe_load(f) or {}
            else:
                config_data = {}

            # Construct the paths block for MediaMTX configuration
            new_paths = {}
            for cam in cameras:
                name = cam.get("name", "")
                url = cam.get("rtsp_url", "")
                if name and url:
                    # Generate a clean, lowercase, alphanumeric identifier
                    cleaned_name = "".join(c for c in name.lower() if c.isalnum() or c in (" ", "_", "-")).replace(" ", "_")
                    new_paths[cleaned_name] = {"source": url}

            config_data["paths"] = new_paths
            
            # Enforce HTTP authentication configurations
            config_data["authMethod"] = "http"
            config_data["authHTTPAddress"] = "http://localhost:8000/auth_check"

            # Write the updated configuration back to the yml file
            with open(self.config_path, "w") as f:
                yaml.safe_dump(config_data, f, default_flow_style=False)

            self.log_buffer.append("[SYSTEM] Camera streams synced to mediamtx.yml successfully.\n")
        except Exception as e:
            self.log_buffer.append(f"[SYSTEM ERROR] Failed to sync camera streams: {str(e)}\n")

mediamtx_manager = MediaMTXManager()
