import os
import subprocess
import threading
import yaml
from collections import deque
from app.core.database import supabase

class MediaMTXManager:
    def __init__(self):
        self.process = None
        self.log_buffer = deque(maxlen=500)
        self.config_path = "/home/whiteshark/Projects/aegis/mediamtx/mediamtx.yml"
        self._thread = None
        self.log_buffer.append("[SYSTEM] MediaMTX Manager Initialized.\n")

    def start(self):
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

            # Start background thread to capture stdout/stderr logs
            self._thread = threading.Thread(target=self._read_logs, daemon=True)
            self._thread.start()

            self.log_buffer.append("[SYSTEM] MediaMTX Subprocess Launched.\n")
            return {"status": "started"}
        except FileNotFoundError:
            error_msg = "MediaMTX executable not found in system PATH."
            self.log_buffer.append(f"[SYSTEM ERROR] {error_msg}\n")
            return {"status": "error", "message": error_msg}
        except Exception as e:
            error_msg = f"Failed to start MediaMTX: {str(e)}"
            self.log_buffer.append(f"[SYSTEM ERROR] {error_msg}\n")
            return {"status": "error", "message": error_msg}

    def stop(self):
        if not self.is_running():
            return {"status": "already_stopped"}

        try:
            self.log_buffer.append("[SYSTEM] Terminating MediaMTX Subprocess...\n")
            self.process.terminate()
            try:
                self.process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.log_buffer.append("[SYSTEM WARNING] Subprocess failed to terminate, killing...\n")
                self.process.kill()
                self.process.wait()
        except Exception as e:
            self.log_buffer.append(f"[SYSTEM ERROR] Exception during stop: {str(e)}\n")

        self.process = None
        self.log_buffer.append("[SYSTEM] MediaMTX Subprocess Stopped.\n")
        return {"status": "stopped"}

    def restart(self):
        self.stop()
        return self.start()

    def is_running(self) -> bool:
        return self.process is not None and self.process.poll() is None

    def get_logs(self) -> list[str]:
        return list(self.log_buffer)

    def _read_logs(self):
        while self.is_running():
            try:
                line = self.process.stdout.readline()
                if not line:
                    break
                self.log_buffer.append(line)
            except Exception:
                break

    def sync_cameras(self):
        try:
            # Fetch active cameras from Supabase
            res = supabase.table("cameras").select("*").execute()
            cameras_list = res.data if res.data else []

            # Read current config using PyYAML
            if os.path.exists(self.config_path):
                with open(self.config_path, "r") as f:
                    data = yaml.safe_load(f) or {}
            else:
                data = {}

            # Construct new paths dictionary
            new_paths = {}
            for cam in cameras_list:
                name = cam.get("name", "")
                url = cam.get("rtsp_url", "")
                if name and url:
                    # Form a valid lowercase underscore identifier
                    cleaned_name = "".join(c for c in name.lower() if c.isalnum() or c in (" ", "_", "-")).replace(" ", "_")
                    new_paths[cleaned_name] = {"source": url}

            data["paths"] = new_paths

            # Write back config using PyYAML
            with open(self.config_path, "w") as f:
                yaml.safe_dump(data, f, default_flow_style=False)

            self.log_buffer.append("[SYSTEM] Camera streams synced to config paths successfully via PyYAML.\n")
        except Exception as e:
            self.log_buffer.append(f"[SYSTEM ERROR] Failed to sync camera streams: {str(e)}\n")

mediamtx_manager = MediaMTXManager()
