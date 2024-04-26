pytest_warning: str = '::'.join(
    (
        'ignore', '.'.join(
            (
                'pytest', ''.join(
                    (
                        'PytestUnraisable',
                        'ExceptionWarning',
                    ),
                ),
            ),
        ),
    ),
)
