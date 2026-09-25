"""
FastAPI router for Public Benchmark Validation Track.

Exposes endpoints for listing benchmark cases, retrieving case details with complete
data lineage and provenance metadata, and generating evidence-linked benchmark reports.
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse, PlainTextResponse, JSONResponse
from typing import List

from schemas.responses import (
    BenchmarkCaseSummarySchema,
    BenchmarkCaseDetailSchema,
)
from services import benchmark_service

router = APIRouter(prefix="/api/benchmarks", tags=["Public Benchmarks"])


@router.get("", response_model=List[BenchmarkCaseSummarySchema])
async def list_benchmarks():
    """Returns summaries of all 5 available public benchmark cases."""
    return benchmark_service.list_benchmark_cases()


@router.get("/{case_id}", response_model=BenchmarkCaseDetailSchema)
async def get_benchmark_detail(case_id: str):
    """Returns complete detail and provenance for a specific benchmark case."""
    detail = benchmark_service.get_benchmark_case_detail(case_id)
    if not detail:
        raise HTTPException(
            status_code=404,
            detail=f"Benchmark case '{case_id}' not found. Available cases: bench-01-olist-reconciliation, bench-02-olist-logistics, bench-03-uci-cancellations, bench-04-criteo-ad-conversions, bench-05-composite-cod-signals"
        )
    return detail


@router.get("/{case_id}/reports/html", response_class=HTMLResponse)
async def get_benchmark_report_html(case_id: str):
    """Generates and returns an evidence-first, conservative HTML benchmark report."""
    detail = benchmark_service.get_benchmark_case_detail(case_id)
    if not detail:
        raise HTTPException(status_code=404, detail="Benchmark case not found")
    return benchmark_service.generate_benchmark_html_report(detail)


@router.get("/{case_id}/reports/markdown", response_class=PlainTextResponse)
async def get_benchmark_report_markdown(case_id: str):
    """Generates and returns an evidence-first, conservative Markdown benchmark report."""
    detail = benchmark_service.get_benchmark_case_detail(case_id)
    if not detail:
        raise HTTPException(status_code=404, detail="Benchmark case not found")
    return benchmark_service.generate_benchmark_markdown_report(detail)


@router.get("/{case_id}/reports/json")
async def get_benchmark_report_json(case_id: str):
    """Returns the benchmark case detail serialized as JSON."""
    detail = benchmark_service.get_benchmark_case_detail(case_id)
    if not detail:
        raise HTTPException(status_code=404, detail="Benchmark case not found")
    return JSONResponse(content=detail.model_dump())
