# Core module for Excel Template Mapper

# Main exports for the core package
from .models import MappingSpec, SheetMapping, ColumnMapping, TRANSFORM_CHOICES, TYPE_CHOICES
from .engine import build_initial_spec, generate_preview_data, apply_template
from .utils import read_workbook_headers, safe_str, is_blank, suggest_header_mapping