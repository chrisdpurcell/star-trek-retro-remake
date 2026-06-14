"""QGraphicsItem subclasses (DESIGN.md §9.1 item table): GridCellItem,
GridLineItem, StarshipItem, AnomalyItem, ProjectileItem.

The `Item` suffix is canonical — it keeps the view's `StarshipItem` distinct
from the model-layer entity `Starship`, which would otherwise share a root name.
"""
