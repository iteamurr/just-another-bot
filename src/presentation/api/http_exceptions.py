from functools import partial

from fastapi import HTTPException, status

from src.domain.exceptions import DomainException


def _domain_error(status_code: int, exc: DomainException) -> HTTPException:
    return HTTPException(
        status_code=status_code,
        detail={
            "alias": exc.alias,
            "description": exc.description,
            "params": exc.params,
        },
    )


DOMAIN_API_HTTP_400 = partial(_domain_error, status.HTTP_400_BAD_REQUEST)
DOMAIN_API_HTTP_404 = partial(_domain_error, status.HTTP_404_NOT_FOUND)
DOMAIN_API_HTTP_409 = partial(_domain_error, status.HTTP_409_CONFLICT)
DOMAIN_API_HTTP_422 = partial(_domain_error, status.HTTP_422_UNPROCESSABLE_ENTITY)
DOMAIN_API_HTTP_500 = partial(_domain_error, status.HTTP_500_INTERNAL_SERVER_ERROR)
DOMAIN_API_HTTP_502 = partial(_domain_error, status.HTTP_502_BAD_GATEWAY)
