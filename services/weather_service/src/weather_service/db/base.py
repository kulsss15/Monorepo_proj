from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy import MetaData

# Define naming convention for constraints
NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

# Use custom metadata with naming conventions
metadata = MetaData(naming_convention=NAMING_CONVENTION)

@as_declarative(metadata=metadata)
class Base:
    """
    Base class for all SQLAlchemy models.
    
    Attributes:
        id (int): Primary key, auto-incremented.
        __tablename__ (str): Automatically generated table name (lowercase class name).
    """
    id: int
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        """
        Generate table names automatically based on the class name.
        Converts the class name to lowercase.
        """
        return cls.__name__.lower()

    @declared_attr
    def __table_args__(cls):
        """
        Optional table arguments, such as a schema or additional options.
        Can be overridden in individual models.
        """
        return {"schema": "public"}  # Default schema is 'public'; adjust as needed