"""Memory Service for NEXUS-Ω.

Encapsulates all Hindsight organizational memory operations (retain, recall, reflect, bank management).
The rest of the application must use this service rather than calling the Hindsight client directly.
"""

from typing import Optional, List, Dict, Any
import httpx
from hindsight_client import Hindsight

from app.core.config import get_settings
from app.core.logging import logger

settings = get_settings()


class MemoryService:
    def __init__(self, base_url: Optional[str] = None, api_key: Optional[str] = None):
        self.base_url = (base_url or settings.HINDSIGHT_URL).rstrip("/")
        self.api_key = api_key or settings.HINDSIGHT_API_KEY
        self.client = Hindsight(
            base_url=self.base_url,
            api_key=self.api_key if self.api_key else None,
            timeout=5.0,
        )
        self._last_check_time: float = 0.0
        self._last_health_status: bool = False

    def health_check(self, force_refresh: bool = False) -> bool:
        """Verifies if Hindsight is reachable and responsive via direct fast probe."""
        import time
        now = time.time()
        if not force_refresh and (now - self._last_check_time < 2.0):
            return self._last_health_status

        self._last_check_time = now
        # Fast socket probe before issuing HTTP requests to eliminate Windows dual-stack timeout hangs
        try:
            from urllib.parse import urlparse
            import socket
            parsed = urlparse(self.base_url)
            host = parsed.hostname or "127.0.0.1"
            if host == "localhost":
                host = "127.0.0.1"
            port = parsed.port or 8888

            with socket.create_connection((host, port), timeout=0.15):
                pass
        except Exception:
            self._last_health_status = False
            return False

        try:
            probe_url = self.base_url.replace("localhost", "127.0.0.1")
            with httpx.Client(timeout=0.5) as http_client:
                r = http_client.get(f"{probe_url}/health")
                if r.status_code in [200, 401, 403]:
                    self._last_health_status = True
                    return True
        except Exception as err:
            logger.debug(f"Hindsight health check probe notice: {err}")

        self._last_health_status = False
        return False

    def create_memory_bank(
        self,
        bank_id: Optional[str] = None,
        name: Optional[str] = None,
        mission: Optional[str] = None,
    ) -> bool:
        """Creates an organizational memory bank if it does not already exist."""
        target_bank = bank_id or settings.HINDSIGHT_BANK_ID
        bank_name = name or settings.HINDSIGHT_BANK_NAME or "NEXUS Organizational Memory"
        default_mission = (
            mission
            or "Store, synthesize, and reason over enterprise events, operational experiences, "
               "incident resolutions, and strategic organizational decisions."
        )

        try:
            self.client.create_bank(
                bank_id=target_bank,
                name=bank_name,
                mission=default_mission,
            )
            logger.info(f"Created Hindsight memory bank: {target_bank} ('{bank_name}')")
            return True
        except Exception as e:
            # If bank already exists or offline, log notice and return
            logger.info(f"Hindsight bank '{target_bank}' verification/creation notice: {e}")
            return True

    def retain_experience(
        self,
        content: str,
        bank_id: Optional[str] = None,
        context: Optional[str] = None,
        metadata: Optional[Dict[str, str]] = None,
        tags: Optional[List[str]] = None,
        document_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Retains an experience or narrative in the Hindsight bank."""
        target_bank = bank_id or settings.HINDSIGHT_BANK_ID
        try:
            clean_metadata = {str(k): str(v) for k, v in (metadata or {}).items()}
            response = self.client.retain(
                bank_id=target_bank,
                content=content,
                context=context,
                metadata=clean_metadata if clean_metadata else None,
                tags=tags,
                document_id=document_id,
            )
            return {
                "success": True,
                "bank_id": target_bank,
                "operation_id": getattr(response, "operation_id", None),
                "details": str(response),
            }
        except Exception as e:
            logger.warning(f"Notice retaining experience in Hindsight bank '{target_bank}': {e}")
            return {"success": False, "bank_id": target_bank, "notice": str(e)}

    def recall_memories(
        self,
        query: str,
        bank_id: Optional[str] = None,
        max_tokens: int = 4096,
        tags: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        """Recalls relevant memories from Hindsight given a query."""
        target_bank = bank_id or settings.HINDSIGHT_BANK_ID
        try:
            response = self.client.recall(
                bank_id=target_bank,
                query=query,
                max_tokens=max_tokens,
                tags=tags,
            )

            results: List[Dict[str, Any]] = []
            if hasattr(response, "results") and response.results:
                for item in response.results:
                    results.append({
                        "id": getattr(item, "id", None),
                        "text": getattr(item, "text", ""),
                        "type": getattr(item, "type", None),
                        "entities": getattr(item, "entities", None),
                        "context": getattr(item, "context", None),
                        "metadata": getattr(item, "metadata", None),
                        "tags": getattr(item, "tags", None),
                        "scores": getattr(item, "scores", None),
                    })
            return results
        except Exception as e:
            logger.warning(f"Notice recalling memories from Hindsight bank '{target_bank}': {e}")
            return []

    def reflect_on_memories(
        self,
        query: str,
        bank_id: Optional[str] = None,
        context: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Generates organizational reflections and synthesis over retained experiences."""
        target_bank = bank_id or settings.HINDSIGHT_BANK_ID
        try:
            response = self.client.reflect(
                bank_id=target_bank,
                query=query,
                context=context,
            )
            return {
                "bank_id": target_bank,
                "text": getattr(response, "text", ""),
                "based_on": getattr(response, "based_on", []),
                "structured_output": getattr(response, "structured_output", None),
            }
        except Exception as e:
            logger.error(f"Error reflecting over Hindsight bank '{target_bank}': {e}")
            raise


# Global singleton instance
memory_service = MemoryService()
