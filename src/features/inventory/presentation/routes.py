# src/features/inventory/presentation/routes.py
from datetime import date
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Response

from src.features.inventory.application.services import Actor, InventoryService
from src.features.inventory.dependencies import get_actor, get_inventory_service
from src.features.inventory.domain import schemas
from src.features.inventory.presentation.plant_routes import router as plant_router

router = APIRouter()
router.include_router(plant_router)


def _http_error(e: Exception) -> HTTPException:
    # LookupError → recurso inexistente (o ajeno); ValueError → regla de negocio
    status = 404 if isinstance(e, LookupError) else 400
    return HTTPException(status_code=status, detail=str(e.args[0]) if e.args else str(e))


# ---------- lotes ----------
@router.get("/plots", response_model=list[schemas.PlotResponse])
def list_plots(
    include_inactive: bool = False,
    owner: Optional[UUID] = Query(None, description="Solo admin"),
    actor: Actor = Depends(get_actor),
    service: InventoryService = Depends(get_inventory_service),
):
    return service.list_plots(actor, owner, include_inactive)


@router.post("/plots", response_model=schemas.PlotResponse, status_code=201)
def create_plot(
    data: schemas.PlotCreate,
    actor: Actor = Depends(get_actor),
    service: InventoryService = Depends(get_inventory_service),
):
    try:
        return service.create_plot(actor, data)
    except (ValueError, LookupError) as e:
        raise _http_error(e)


@router.get("/plots/{plot_id}", response_model=schemas.PlotResponse)
def get_plot(
    plot_id: UUID,
    actor: Actor = Depends(get_actor),
    service: InventoryService = Depends(get_inventory_service),
):
    try:
        return service.get_plot(actor, plot_id)
    except (ValueError, LookupError) as e:
        raise _http_error(e)


@router.patch("/plots/{plot_id}", response_model=schemas.PlotResponse)
def update_plot(
    plot_id: UUID,
    data: schemas.PlotUpdate,
    actor: Actor = Depends(get_actor),
    service: InventoryService = Depends(get_inventory_service),
):
    try:
        return service.update_plot(actor, plot_id, data)
    except (ValueError, LookupError) as e:
        raise _http_error(e)


@router.delete("/plots/{plot_id}", status_code=204)
def delete_plot(
    plot_id: UUID,
    actor: Actor = Depends(get_actor),
    service: InventoryService = Depends(get_inventory_service),
):
    try:
        service.delete_plot(actor, plot_id)
    except (ValueError, LookupError) as e:
        raise _http_error(e)
    return Response(status_code=204)


# ---------- cosechas ----------
@router.get("/plots/{plot_id}/harvests", response_model=list[schemas.HarvestResponse])
def list_harvests(
    plot_id: UUID,
    actor: Actor = Depends(get_actor),
    service: InventoryService = Depends(get_inventory_service),
):
    try:
        return service.list_harvests(actor, plot_id)
    except (ValueError, LookupError) as e:
        raise _http_error(e)


@router.post("/plots/{plot_id}/harvests", response_model=schemas.HarvestResponse, status_code=201)
def add_harvest(
    plot_id: UUID,
    data: schemas.HarvestCreate,
    actor: Actor = Depends(get_actor),
    service: InventoryService = Depends(get_inventory_service),
):
    try:
        return service.add_harvest(actor, plot_id, data)
    except (ValueError, LookupError) as e:
        raise _http_error(e)


@router.patch("/harvests/{harvest_id}", response_model=schemas.HarvestResponse)
def update_harvest(
    harvest_id: UUID,
    data: schemas.HarvestUpdate,
    actor: Actor = Depends(get_actor),
    service: InventoryService = Depends(get_inventory_service),
):
    try:
        return service.update_harvest(actor, harvest_id, data)
    except (ValueError, LookupError) as e:
        raise _http_error(e)


@router.delete("/harvests/{harvest_id}", status_code=204)
def delete_harvest(
    harvest_id: UUID,
    actor: Actor = Depends(get_actor),
    service: InventoryService = Depends(get_inventory_service),
):
    try:
        service.delete_harvest(actor, harvest_id)
    except (ValueError, LookupError) as e:
        raise _http_error(e)
    return Response(status_code=204)


# ---------- resumen ----------
@router.get("/summary", response_model=schemas.SummaryResponse)
def summary(
    date_from: Optional[date] = Query(None, alias="from"),
    date_to: Optional[date] = Query(None, alias="to"),
    owner: Optional[UUID] = Query(None, description="Solo admin"),
    actor: Actor = Depends(get_actor),
    service: InventoryService = Depends(get_inventory_service),
):
    try:
        return service.summary(actor, date_from, date_to, owner)
    except (ValueError, LookupError) as e:
        raise _http_error(e)
