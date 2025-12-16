"""
Repositories package for data access layer.
"""
from .technology_repository import TechnologyRepository
from .year_control_repository import YearControlRepository

__all__ = ['TechnologyRepository', 'YearControlRepository']
