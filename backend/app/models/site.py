from __future__ import annotations

from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Site(Base):
    """Candidate EV charging site.

    For v1, we model sites as point locations with engineered features + scores.
    """

    __tablename__ = "sites"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    city_slug: Mapped[str] = mapped_column(String(64), index=True)

    lat: Mapped[float] = mapped_column(Float)
    lng: Mapped[float] = mapped_column(Float)

    location_label: Mapped[str | None] = mapped_column(String(256), nullable=True)
    parcel_id: Mapped[str | None] = mapped_column(String(128), nullable=True)

    # engineered features (0-1)
    traffic_index: Mapped[float] = mapped_column(Float)
    pop_density_index: Mapped[float] = mapped_column(Float)
    renters_share: Mapped[float] = mapped_column(Float)
    income_index: Mapped[float] = mapped_column(Float)
    poi_index: Mapped[float] = mapped_column(Float)

    # scores (0-100)
    score_overall: Mapped[float] = mapped_column(Float)
    score_demand: Mapped[float] = mapped_column(Float)
    score_equity: Mapped[float] = mapped_column(Float)
    score_traffic: Mapped[float] = mapped_column(Float)
    score_grid: Mapped[float] = mapped_column(Float)

    daily_kwh_estimate: Mapped[float] = mapped_column(Float)
