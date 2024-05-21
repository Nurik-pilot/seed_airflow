from datetime import datetime
from logging import getLogger
from typing import Any

logger = getLogger(name=__name__)


def print_hello_world(
    logical_date: datetime,
    **kwargs: dict[str, Any],
) -> None:
    logger.info(
        'logical_date: %s',
        logical_date.isoformat(),
    )
    message = ' '.join(
        (
            'hello world by',
            'PythonOperator',
        ),
    )
    logger.info(msg=message)
