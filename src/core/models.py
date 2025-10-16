from dataclasses import dataclass, asdict, field
from typing import Dict, List, Optional, Any

TRANSFORM_CHOICES: List[str] = [
    "trim",
    "upper",
    "lower",
    "title",
    "to_string",
    "to_int",
    "to_float",
    "date_to_iso",
    "digits_only",
]

TYPE_CHOICES: List[str] = ["general", "text", "integer", "float", "date", "boolean"]

@dataclass
class ColumnMapping:
    target: str
    source: Optional[str] = None
    default: Optional[str] = ""
    transforms: List[str] = field(default_factory=list)
    find_replace: Dict[str, str] = field(default_factory=dict)
    advanced_rules: List[Dict[str, Any]] = field(default_factory=list)
    advanced_else: Optional[str] = None
    data_type: Optional[str] = None
    number_format: Optional[str] = ""
    advanced_format: Optional[str] = ""

@dataclass
class SheetMapping:
    target_sheet: str
    target_headers: List[str]
    source_sheet: Optional[str] = None
    columns: List[ColumnMapping] = field(default_factory=list)
    drop_if_all_blank: bool = True

@dataclass
class MappingSpec:
    template_path: str
    source_path: Optional[str] = None
    sheets: List[SheetMapping] = field(default_factory=list)
    global_find_replace: Dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        # Export mapping-only data; exclude file paths so mappings can be reused with any session files
        return {
            "sheets": [
                {
                    "target_sheet": s.target_sheet,
                    "target_headers": s.target_headers,
                    "source_sheet": s.source_sheet,
                    "columns": [asdict(c) for c in s.columns],
                    "drop_if_all_blank": s.drop_if_all_blank,
                }
                for s in self.sheets
            ],
            "global_find_replace": self.global_find_replace,
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "MappingSpec":
        sheets: List[SheetMapping] = []
        for s in d.get("sheets", []):
            columns = [ColumnMapping(**c) for c in s.get("columns", [])]
            sheets.append(
                SheetMapping(
                    target_sheet=s["target_sheet"],
                    target_headers=s.get("target_headers", []),
                    source_sheet=s.get("source_sheet"),
                    columns=columns,
                    drop_if_all_blank=s.get("drop_if_all_blank", True),
                )
            )
        return MappingSpec(
            template_path=d.get("template_path", ""),
            source_path=d.get("source_path"),
            sheets=sheets,
            global_find_replace=d.get("global_find_replace", {}),
        )