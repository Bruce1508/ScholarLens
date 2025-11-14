"""
Winner Essay Cluster model
"""
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, func
from sqlalchemy.dialects.postgresql import JSONB, ARRAY
from config.database import Base


class WinnerEssayCluster(Base):
    """
    Winner essay cluster archetypes
    Learned patterns from successful scholarship essays
    """
    __tablename__ = "winner_essay_clusters"

    id = Column(Integer, primary_key=True, index=True)
    cluster_id = Column(Integer, nullable=False, unique=True)
    archetype_name = Column(String(100))
    style_summary = Column(Text)
    dominant_tone = Column(String(100))
    weights = Column(JSONB)  # Trait weights for this cluster
    keywords = Column(JSONB)  # Array of keywords
    sample_essays = Column(ARRAY(Text))  # Array of essay texts
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())

    def __repr__(self):
        return f"<WinnerEssayCluster(id={self.id}, archetype='{self.archetype_name}')>"
