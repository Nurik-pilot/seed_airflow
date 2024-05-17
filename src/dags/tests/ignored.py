pytest_warning: str = '::'.join(
    (
        'ignore', '.'.join(
            (
                'pytest', ''.join(
                    (
                        'Pytest',
                        'Unraisable',
                        'Exception',
                        'Warning',
                    ),
                ),
            ),
        ),
    ),
)
