from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class WeatherData(Base):
    """
    SQLAlchemy model for storing weather data.
    """
    __tablename__ = "weather_data"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    city = Column(String, nullable=False, index=True)
    temperature = Column(Float, nullable=False)
    weather_condition = Column(String, nullable=False)
    recorded_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<WeatherData(id={self.id}, city={self.city}, temperature={self.temperature}, weather_condition={self.weather_condition})>"