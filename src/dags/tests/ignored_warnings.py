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
sqlalchemy_warning: str = '::'.join(
    (
        'ignore', '.'.join(
            (
                'sqlalchemy', 'exc',
                'SAWarning',
            ),
        ),
    ),
)
deprecation_warning: str = '::'.join(
    (
        'ignore',
        'DeprecationWarning',
    ),
)
