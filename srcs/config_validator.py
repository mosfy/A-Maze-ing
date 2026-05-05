from pydantic import BaseModel, Field, model_validator
from typing import Tuple, Optional, Any
import sys


class ConfigValidator(BaseModel):
    """
    Valide et stocke la configuration du labyrinthe.
    Parse et valide les données depuis un fichier config.
    """
    width: int = Field(..., gt=0, description="Largeur")
    height: int = Field(..., gt=0, description="Hauteur")
    entry: Tuple[int, int] = Field(..., description="Entrée (x, y)")
    exit: Tuple[int, int] = Field(..., description="Sortie (x, y)")
    output_file: str = Field(..., min_length=1, description="Fichier sortie")
    perfect: bool = Field(default=True, description="Labyrinthe parfait")
    seed: Optional[int] = Field(default=None, description="Seed optionnelle")

    @model_validator(mode="before")
    @classmethod
    def validate_before(cls, data: Any) -> Any:
        """Convertit les données avant la validation Pydantic."""
        if not isinstance(data, dict):
            return data

        # Convertir entry de string à tuple
        if "entry" in data and isinstance(data["entry"], str):
            try:
                x, y = data["entry"].split(",")
                data["entry"] = (int(x.strip()), int(y.strip()))
            except ValueError:
                raise ValueError("Format coords 'x,y' attendu pour entry")

        # Convertir exit de string à tuple
        if "exit" in data and isinstance(data["exit"], str):
            try:
                x, y = data["exit"].split(",")
                data["exit"] = (int(x.strip()), int(y.strip()))
            except ValueError:
                raise ValueError("Format coords 'x,y' attendu pour exit")

        # Convertir perfect de string à bool
        if "perfect" in data and isinstance(data["perfect"], str):
            if data["perfect"].lower() in ("true", "1", "yes"):
                data["perfect"] = True
            elif data["perfect"].lower() in ("false", "0", "no"):
                data["perfect"] = False
            else:
                raise ValueError("PERFECT doit être 'true' ou 'false'")

        return data

    @model_validator(mode="after")
    def validate_after(self) -> "ConfigValidator":
        """Valide les contraintes après la création du modèle."""
        x_entry, y_entry = self.entry
        x_exit, y_exit = self.exit

        if self.width * self.height < 2:
            raise ValueError(
                "La taille minimale est de 2 cellules "
                "(ex: 1x2, 2x1, 2x2...)"
            )

        if self.entry == self.exit:
            raise ValueError("ENTRY et EXIT doivent être différents")

        if not (0 <= x_entry < self.width and 0 <= y_entry < self.height):
            raise ValueError(
                f"ENTRY hors limites ({x_entry}, {y_entry}) vs "
                f"({self.width}x{self.height})"
            )
        if not (0 <= x_exit < self.width and 0 <= y_exit < self.height):
            raise ValueError(
                f"EXIT hors limites ({x_exit}, {y_exit}) vs "
                f"({self.width}x{self.height})"
            )
        return self

    @classmethod
    def from_config_file(cls, filepath: str) -> "ConfigValidator":
        """
        Parse un fichier config au format KEY=value\n

        Args:
            filepath: Chemin du fichier config

        Returns:
            ConfigValidator instance

        Raises:
            FileNotFoundError: Si le fichier n'existe pas
            ValueError: Si des paramètres manquent ou sont invalides
        """
        parameters = {}
        try:
            with open(filepath, "r") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    if line and "=" in line:
                        key, value = line.split("=", 1)
                        parameters[key.strip()] = value.strip()
        except FileNotFoundError:
            raise FileNotFoundError(f"Fichier config non trouvé: {filepath}")

        # Mapper les keys du fichier config aux champs Pydantic
        config_mapping = {
            "WIDTH": "width",
            "HEIGHT": "height",
            "ENTRY": "entry",
            "EXIT": "exit",
            "OUTPUT_FILE": "output_file",
            "PERFECT": "perfect",
            "SEED": "seed",
        }

        validated_data: dict[str, Any] = {}
        for file_key, model_key in config_mapping.items():
            if file_key in parameters:
                validated_data[model_key] = parameters[file_key]

        return cls(**validated_data)

    @classmethod
    def from_argv(cls, argv_index: int = 1) -> "ConfigValidator":
        """
        Parse le chemin config depuis sys.argv et le charge.

        Args:
            argv_index: Index dans sys.argv du chemin config

        Returns:
            ConfigValidator instance
        """
        if len(sys.argv) <= argv_index:
            raise ValueError(
                f"Veuillez fournir le chemin du fichier config "
                f"en argument {argv_index}"
            )
        return cls.from_config_file(sys.argv[argv_index])
