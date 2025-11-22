"""
State Persistence - Storage and retrieval of consciousness states.

Handles saving and loading consciousness states to/from persistent storage.
Supports both file-based and database backends.
"""

import json
import os
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

from .state_machine import ConsciousnessState, ConsciousnessLevel


class StatePersistenceBackend(ABC):
    """Abstract base class for state persistence backends."""

    @abstractmethod
    def save_state(self, state: ConsciousnessState) -> bool:
        """Save a consciousness state."""
        pass

    @abstractmethod
    def load_state(self, part_id: str) -> Optional[ConsciousnessState]:
        """Load a consciousness state by part ID."""
        pass

    @abstractmethod
    def load_all_states(self) -> Dict[str, ConsciousnessState]:
        """Load all consciousness states."""
        pass

    @abstractmethod
    def delete_state(self, part_id: str) -> bool:
        """Delete a consciousness state."""
        pass

    @abstractmethod
    def state_exists(self, part_id: str) -> bool:
        """Check if a state exists."""
        pass


class FileBasedPersistence(StatePersistenceBackend):
    """
    File-based persistence backend.

    Stores consciousness states as JSON files in a directory structure.
    """

    def __init__(self, base_path: str = "data/consciousness_states"):
        """Initialize file-based persistence."""
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)

    def _get_state_path(self, part_id: str) -> Path:
        """Get the file path for a part's state."""
        # Sanitize part_id for filesystem
        safe_id = part_id.replace("/", "_").replace("\\", "_")
        return self.base_path / f"{safe_id}.json"

    def save_state(self, state: ConsciousnessState) -> bool:
        """Save a consciousness state to a JSON file."""
        try:
            path = self._get_state_path(state.part_id)
            with open(path, 'w') as f:
                json.dump(state.to_dict(), f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving state for {state.part_id}: {e}")
            return False

    def load_state(self, part_id: str) -> Optional[ConsciousnessState]:
        """Load a consciousness state from a JSON file."""
        path = self._get_state_path(part_id)
        if not path.exists():
            return None
        try:
            with open(path, 'r') as f:
                data = json.load(f)
            return ConsciousnessState.from_dict(data)
        except Exception as e:
            print(f"Error loading state for {part_id}: {e}")
            return None

    def load_all_states(self) -> Dict[str, ConsciousnessState]:
        """Load all consciousness states from the directory."""
        states = {}
        for path in self.base_path.glob("*.json"):
            try:
                with open(path, 'r') as f:
                    data = json.load(f)
                state = ConsciousnessState.from_dict(data)
                states[state.part_id] = state
            except Exception as e:
                print(f"Error loading state from {path}: {e}")
        return states

    def delete_state(self, part_id: str) -> bool:
        """Delete a consciousness state file."""
        path = self._get_state_path(part_id)
        if path.exists():
            try:
                path.unlink()
                return True
            except Exception as e:
                print(f"Error deleting state for {part_id}: {e}")
                return False
        return False

    def state_exists(self, part_id: str) -> bool:
        """Check if a state file exists."""
        return self._get_state_path(part_id).exists()


class InMemoryPersistence(StatePersistenceBackend):
    """
    In-memory persistence backend for testing and development.
    """

    def __init__(self):
        """Initialize in-memory storage."""
        self._states: Dict[str, ConsciousnessState] = {}

    def save_state(self, state: ConsciousnessState) -> bool:
        """Save state to memory."""
        self._states[state.part_id] = state
        return True

    def load_state(self, part_id: str) -> Optional[ConsciousnessState]:
        """Load state from memory."""
        return self._states.get(part_id)

    def load_all_states(self) -> Dict[str, ConsciousnessState]:
        """Get all states from memory."""
        return self._states.copy()

    def delete_state(self, part_id: str) -> bool:
        """Delete state from memory."""
        if part_id in self._states:
            del self._states[part_id]
            return True
        return False

    def state_exists(self, part_id: str) -> bool:
        """Check if state exists in memory."""
        return part_id in self._states


@dataclass
class PersistenceStats:
    """Statistics about persistence operations."""
    total_states: int = 0
    states_by_level: Dict[ConsciousnessLevel, int] = None
    last_save_time: Optional[datetime] = None
    last_load_time: Optional[datetime] = None
    failed_saves: int = 0
    failed_loads: int = 0

    def __post_init__(self):
        if self.states_by_level is None:
            self.states_by_level = {level: 0 for level in ConsciousnessLevel}


class StatePersistence:
    """
    Main persistence manager for consciousness states.

    Provides a unified interface for saving and loading consciousness states
    with support for multiple backends.
    """

    def __init__(self, backend: Optional[StatePersistenceBackend] = None):
        """
        Initialize the persistence manager.

        Args:
            backend: The persistence backend to use. Defaults to file-based.
        """
        self.backend = backend or FileBasedPersistence()
        self._stats = PersistenceStats()
        self._batch_mode = False
        self._batch_queue: List[ConsciousnessState] = []

    def save(self, state: ConsciousnessState) -> bool:
        """
        Save a consciousness state.

        In batch mode, states are queued for later batch saving.
        """
        if self._batch_mode:
            self._batch_queue.append(state)
            return True

        success = self.backend.save_state(state)
        if success:
            self._stats.last_save_time = datetime.now()
        else:
            self._stats.failed_saves += 1
        return success

    def load(self, part_id: str) -> Optional[ConsciousnessState]:
        """Load a consciousness state by part ID."""
        state = self.backend.load_state(part_id)
        self._stats.last_load_time = datetime.now()
        if state is None:
            self._stats.failed_loads += 1
        return state

    def load_all(self) -> Dict[str, ConsciousnessState]:
        """Load all consciousness states."""
        states = self.backend.load_all_states()
        self._stats.last_load_time = datetime.now()
        self._stats.total_states = len(states)

        # Update level distribution
        self._stats.states_by_level = {level: 0 for level in ConsciousnessLevel}
        for state in states.values():
            self._stats.states_by_level[state.level] += 1

        return states

    def delete(self, part_id: str) -> bool:
        """Delete a consciousness state."""
        return self.backend.delete_state(part_id)

    def exists(self, part_id: str) -> bool:
        """Check if a consciousness state exists."""
        return self.backend.state_exists(part_id)

    def start_batch(self) -> None:
        """Start batch mode for efficient bulk saves."""
        self._batch_mode = True
        self._batch_queue = []

    def commit_batch(self) -> int:
        """
        Commit all queued states in batch mode.

        Returns:
            Number of successfully saved states.
        """
        if not self._batch_mode:
            return 0

        success_count = 0
        for state in self._batch_queue:
            if self.backend.save_state(state):
                success_count += 1
            else:
                self._stats.failed_saves += 1

        self._batch_mode = False
        self._batch_queue = []
        self._stats.last_save_time = datetime.now()

        return success_count

    def rollback_batch(self) -> None:
        """Cancel batch mode and discard queued states."""
        self._batch_mode = False
        self._batch_queue = []

    def get_stats(self) -> PersistenceStats:
        """Get persistence statistics."""
        return self._stats

    def export_all(self, filepath: str) -> bool:
        """
        Export all states to a single JSON file.

        Useful for backups and data transfer.
        """
        try:
            states = self.load_all()
            export_data = {
                "export_time": datetime.now().isoformat(),
                "total_states": len(states),
                "states": {pid: state.to_dict() for pid, state in states.items()}
            }
            with open(filepath, 'w') as f:
                json.dump(export_data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error exporting states: {e}")
            return False

    def import_all(self, filepath: str, overwrite: bool = False) -> int:
        """
        Import states from a JSON export file.

        Args:
            filepath: Path to the export file
            overwrite: Whether to overwrite existing states

        Returns:
            Number of imported states
        """
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)

            imported = 0
            for part_id, state_data in data.get("states", {}).items():
                if not overwrite and self.exists(part_id):
                    continue
                state = ConsciousnessState.from_dict(state_data)
                if self.backend.save_state(state):
                    imported += 1

            return imported
        except Exception as e:
            print(f"Error importing states: {e}")
            return 0
