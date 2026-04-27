from fastapi import APIRouter, Depends, HTTPException

from LB7.src.shared.responses import ApiResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])


