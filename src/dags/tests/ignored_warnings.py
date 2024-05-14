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

sqlalchemy_warning: str = '::'.join(
    (
        'ignore', '.'.join(
            (
                'sqlalchemy.exc',
                'SAWarning',
            ),
        ),
    ),
)
deprecation_warning: str = '::'.join(
    (
        'ignore', 'DeprecationWarning',
    ),
)
