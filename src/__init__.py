# Source package for Excel Template Mapper

# Only expose the most commonly used classes for convenience
from .core.models import MappingSpec
from .widgets.main_window import MainWindow

# Import version info dynamically
from ._version import __version__, __author__, __email__, __description__