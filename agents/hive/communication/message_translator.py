"""
Message Translator - Translates messages between swarm contexts.

When a message is sent from one swarm to another, it needs to be
translated to make sense in the target swarm's context.
"""

from dataclasses import dataclass
from typing import Any, Optional
from uuid import UUID

from ..models import SwarmMessage, Swarm


@dataclass
class TranslationResult:
    """Result of message translation."""
    original_message: SwarmMessage
    translated_message: SwarmMessage
    source_context: str
    target_context: str
    transformations_applied: list[str]


class MessageTranslator:
    """
    Translates messages between swarm contexts.

    Example: "M8 bolts work well with these torque specs"
    Becomes: "M8 nuts should expect these torque applications"
    """

    # Context mappings for translation
    CONTEXT_MAPPINGS = {
        ("bolts", "nuts"): {
            "torque_applied": "torque_received",
            "tensile_load": "clamping_force",
            "thread_engagement": "thread_provided",
            "preload": "compressive_load",
        },
        ("bearings", "shafts"): {
            "load_capacity": "shaft_load",
            "rotation_speed": "shaft_speed",
            "friction": "shaft_friction",
            "temperature_rise": "shaft_heat_generation",
        },
        ("seals", "housings"): {
            "sealing_pressure": "housing_pressure",
            "compression": "housing_groove_depth",
            "temperature_limit": "housing_temperature",
        },
        ("gears", "bearings"): {
            "tooth_load": "radial_load",
            "axial_thrust": "thrust_load",
            "mesh_frequency": "rotation_frequency",
        },
    }

    # Perspective shifts for different part types
    PERSPECTIVE_SHIFTS = {
        "bolts": "applying force",
        "nuts": "receiving force",
        "bearings": "supporting",
        "shafts": "transmitting",
        "seals": "containing",
        "housings": "enclosing",
        "gears": "driving",
        "pistons": "reciprocating",
        "springs": "storing energy",
    }

    def translate(
        self,
        message: SwarmMessage,
        source_swarm: Swarm,
        target_swarm: Swarm,
    ) -> TranslationResult:
        """
        Translate a message from source swarm's context to target's.

        Args:
            message: The message to translate
            source_swarm: The sending swarm
            target_swarm: The receiving swarm

        Returns:
            Translation result with transformed message
        """
        transformations = []

        # Determine swarm types
        source_type = self._get_swarm_type(source_swarm)
        target_type = self._get_swarm_type(target_swarm)

        # Create translated message copy
        translated_content = dict(message.content)

        # Apply context-specific translations
        mapping_key = (source_type, target_type)
        reverse_key = (target_type, source_type)

        if mapping_key in self.CONTEXT_MAPPINGS:
            mappings = self.CONTEXT_MAPPINGS[mapping_key]
            translated_content = self._apply_mappings(
                translated_content, mappings, transformations
            )
        elif reverse_key in self.CONTEXT_MAPPINGS:
            # Reverse the mappings
            mappings = {v: k for k, v in self.CONTEXT_MAPPINGS[reverse_key].items()}
            translated_content = self._apply_mappings(
                translated_content, mappings, transformations
            )

        # Apply perspective shift
        if source_type in self.PERSPECTIVE_SHIFTS and target_type in self.PERSPECTIVE_SHIFTS:
            translated_content = self._apply_perspective_shift(
                translated_content,
                source_type,
                target_type,
                transformations,
            )

        # Create translated message
        translated_message = SwarmMessage(
            id=message.id,
            source_swarm_id=message.source_swarm_id,
            target_swarm_ids=[target_swarm.id],
            message_type=message.message_type,
            content=translated_content,
            priority=message.priority,
            created_at=message.created_at,
        )

        return TranslationResult(
            original_message=message,
            translated_message=translated_message,
            source_context=source_type,
            target_context=target_type,
            transformations_applied=transformations,
        )

    def _get_swarm_type(self, swarm: Swarm) -> str:
        """Extract the type/category from a swarm."""
        # Use category or extract from identifier
        if swarm.category:
            return swarm.category.lower()
        if swarm.identifier:
            return swarm.identifier.split(":")[0].lower()
        return "unknown"

    def _apply_mappings(
        self,
        content: dict[str, Any],
        mappings: dict[str, str],
        transformations: list[str],
    ) -> dict[str, Any]:
        """Apply term mappings to content."""
        result = {}

        for key, value in content.items():
            if key in mappings:
                new_key = mappings[key]
                result[new_key] = value
                transformations.append(f"Renamed '{key}' to '{new_key}'")
            else:
                result[key] = value

            # Recursively handle nested dicts
            if isinstance(value, dict):
                result[key if key not in mappings else mappings[key]] = self._apply_mappings(
                    value, mappings, transformations
                )

        return result

    def _apply_perspective_shift(
        self,
        content: dict[str, Any],
        source_type: str,
        target_type: str,
        transformations: list[str],
    ) -> dict[str, Any]:
        """Apply perspective shift to content."""
        result = dict(content)

        source_perspective = self.PERSPECTIVE_SHIFTS.get(source_type, "active")
        target_perspective = self.PERSPECTIVE_SHIFTS.get(target_type, "passive")

        # Add perspective context
        result["_translated_from"] = {
            "source_type": source_type,
            "source_perspective": source_perspective,
            "target_type": target_type,
            "target_perspective": target_perspective,
        }

        transformations.append(
            f"Shifted perspective from '{source_perspective}' to '{target_perspective}'"
        )

        return result

    def translate_compatibility_update(
        self,
        message: SwarmMessage,
        source_swarm: Swarm,
        target_swarm: Swarm,
    ) -> SwarmMessage:
        """
        Specialized translation for compatibility updates.

        When one swarm learns about compatibility, the mating swarm
        needs to receive the reciprocal information.
        """
        content = dict(message.content)

        # Swap roles in compatibility data
        if "compatible_with" in content:
            content["provides_compatibility_for"] = content.pop("compatible_with")

        if "thread_compatibility" in content:
            thread_data = content["thread_compatibility"]
            # Swap internal/external perspectives
            if "external_thread" in thread_data:
                thread_data["internal_thread"] = thread_data.pop("external_thread")
            if "internal_thread" in thread_data:
                thread_data["external_thread"] = thread_data.pop("internal_thread")

        if "torque_range" in content:
            # Target swarm expects to receive this torque
            content["expected_torque"] = content.pop("torque_range")

        return SwarmMessage(
            id=message.id,
            source_swarm_id=message.source_swarm_id,
            target_swarm_ids=[target_swarm.id],
            message_type=message.message_type,
            content=content,
            priority=message.priority,
            created_at=message.created_at,
        )


class CompatibilityTranslator:
    """
    Specialized translator for compatibility information.
    """

    def translate_mating_compatibility(
        self,
        source_category: str,
        target_category: str,
        compatibility_data: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Translate compatibility data between mating part categories.

        Example: Bolt's thread data → Nut's expected thread data
        """
        result = dict(compatibility_data)

        if source_category == "bolt" and target_category == "nut":
            # Bolt provides external thread, nut expects it
            if "thread_specification" in result:
                result["expected_thread"] = result.pop("thread_specification")
            if "proof_load" in result:
                result["expected_clamping_force"] = result.pop("proof_load")

        elif source_category == "bearing" and target_category == "shaft":
            # Bearing provides bore, shaft fits into it
            if "bore_diameter" in result:
                result["required_diameter"] = result.pop("bore_diameter")
            if "load_rating" in result:
                result["maximum_transmittable_load"] = result.pop("load_rating")

        return result
