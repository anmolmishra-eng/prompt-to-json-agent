"""
Per-Object ID Schema (Day 1 Requirement)
Spec schema with per-object IDs and editable material properties
"""

from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime

class MaterialProperties(BaseModel):
    """Editable material properties for each object (Day 1 Requirement)"""
    type: str = Field(..., description="Material type (e.g., wood, metal, fabric, concrete, glass)")
    color: Optional[str] = Field(None, description="Material color (hex code or name)")
    texture: Optional[str] = Field(None, description="Texture type (smooth, rough, glossy, matte)")
    finish: Optional[str] = Field(None, description="Surface finish (matte, glossy, satin, brushed)")
    reflectivity: Optional[float] = Field(None, ge=0.0, le=1.0, description="Reflectivity (0.0-1.0)")
    roughness: Optional[float] = Field(None, ge=0.0, le=1.0, description="Surface roughness (0.0-1.0)")
    metallic: Optional[float] = Field(None, ge=0.0, le=1.0, description="Metallic property (0.0-1.0)")
    properties: Dict[str, Any] = Field(default_factory=dict, description="Additional material properties")
    editable: bool = Field(True, description="Whether material can be edited via switch API")

class Position(BaseModel):
    """3D position coordinates"""
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0

class Dimensions(BaseModel):
    """Object dimensions"""
    length: float
    width: float
    height: float
    units: str = "meters"

class DesignObject(BaseModel):
    """Individual design object with unique ID (Day 1 Requirement)"""
    object_id: str = Field(..., description="Unique object ID following pattern: {type}_{number} (e.g., floor_1, sofa_1, chair_2)")
    object_type: str = Field(..., description="Type of object (floor, wall, ceiling, door, window, furniture, etc.)")
    material: MaterialProperties = Field(..., description="Editable material properties")
    position: Position = Field(default_factory=Position, description="3D position in scene")
    dimensions: Dimensions = Field(..., description="Object dimensions")
    rotation: Optional[Dict[str, float]] = Field(None, description="Rotation angles in degrees (x, y, z)")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional object metadata")
    editable: bool = Field(True, description="Whether object properties can be modified")
    
    @staticmethod
    def generate_id(object_type: str, index: int) -> str:
        """Generate object ID following naming convention: {type}_{number}"""
        return f"{object_type.lower()}_{index}"

class SpecSchema(BaseModel):
    """Complete specification with per-object IDs"""
    spec_id: str = Field(..., description="Unique specification ID")
    objects: List[DesignObject] = Field(..., description="List of design objects with unique IDs")
    scene_metadata: Dict[str, Any] = Field(default_factory=dict, description="Scene-level metadata")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_schema_extra = {
            "example": {
                "spec_id": "spec_12345",
                "objects": [
                    {
                        "object_id": "floor_1",
                        "object_type": "floor",
                        "material": {
                            "type": "wood",
                            "color": "#8B4513",
                            "texture": "smooth",
                            "finish": "glossy",
                            "properties": {"hardness": "medium"},
                            "editable": True
                        },
                        "position": {"x": 0, "y": 0, "z": 0},
                        "dimensions": {"length": 10, "width": 10, "height": 0.1, "units": "meters"},
                        "editable": True
                    },
                    {
                        "object_id": "sofa_1",
                        "object_type": "furniture",
                        "material": {
                            "type": "fabric",
                            "color": "#4A4A4A",
                            "texture": "soft",
                            "finish": "matte",
                            "properties": {"comfort": "high"},
                            "editable": True
                        },
                        "position": {"x": 2, "y": 0, "z": 3},
                        "dimensions": {"length": 2, "width": 0.9, "height": 0.8, "units": "meters"},
                        "editable": True
                    }
                ],
                "scene_metadata": {
                    "environment": "living_room",
                    "lighting": "natural",
                    "style": "modern"
                }
            }
        }
