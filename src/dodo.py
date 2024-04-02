from pathlib import Path
from typing import TypeAlias, Callable, Generator

from doit import task_params

default_coverage_report_type = 'term-missing'
default_c = default_coverage_report_type

default_number_of_processes = 2
default_n = default_number_of_processes

default_flake_runs = 1
default_f = default_flake_runs

warning = '.'.join(
    (
        'pytest',
        ''.join(
            (
                'PytestUnraisable',
                'ExceptionWarning',
            ),
        ),
    ),
)
warning = f'-W ignore::{warning}'

full_test = ' '.join(
    (
        'pytest', '-v',
        '--cov', '.',
        '--cov-report',
        '{coverage_report_type}',
        '--cov-fail-under=100',
        '--numprocesses',
        '{number_of_processes}',
        '--flake-finder',
        '--flake-runs',
        '{flake_runs}',
        '--durations=4',
        '--exitfirst',
        '--randomly-seed=last',
        '-W error',
        warning,
    ),
)

single_test = ' '.join(
    (
        'pytest', '-vs',
        '--disable-pytest-warnings',
        '{target}',
    ),
)

mypy = 'mypy .'
bandit = 'bandit -r . --exclude tests'
blocklint = 'blocklint . --skip-files=airflow.cfg'
flake8 = 'flake8 .'
ruff: str = 'ruff check .'

safety = ' -i '.join(
    (
        'safety check',
        '51457', '65647', '65278',
        '65212', '62019', '42194',
        '51668',
    ),
)

outdated = 'poetry show --outdated'

up = 'poetry update'

export = ' '.join(
    (
        'poetry export',
        '--format requirements.txt',
        '--output requirements.txt',
        '--with dev',
        '--without-hashes',
        '--without-urls',
    ),
)

default_verbosity = 2

Actions: TypeAlias = tuple[
    str | Callable[[], None], ...,
]
MetaData: TypeAlias = dict[
    str, Actions | int,
]


def generate(
    actions: Actions,
) -> MetaData:
    return {
        'actions': actions,
        'verbosity': default_verbosity,
    }


@task_params(
    param_def=[
        {
            'name': 'target',
            'long': 'target',
            'short': 't', 'type': str,
            'default': '',
        },
        {
            'name': 'number_of_processes',
            'long': 'number_of_processes',
            'short': 'n', 'type': int,
            'default': default_n,
        },
        {
            'name': 'coverage_report_path',
            'long': 'coverage_report_path',
            'short': 'c', 'type': str,
            'default': '',
        },
        {
            'name': 'flake_runs',
            'long': 'flake_runs',
            'short': 'f', 'type': int,
            'default': default_f,
        },
    ],
)
def task_test(
    target: str = '',
    flake_runs: int = default_f,
    coverage_report_path: str = '',
    number_of_processes: int = default_n,
) -> MetaData:
    report_types: dict[str, str] = {
        '': default_c,
    }
    report_type: str = report_types.get(
        coverage_report_path,
        f'xml:{coverage_report_path}',
    )
    first = 'coverage_report_type'
    second = 'number_of_processes'
    third = 'flake_runs'
    kwargs = {
        first: report_type,
        second: number_of_processes,
        third: flake_runs,
    }
    full_run = full_test.format(**kwargs)
    actions: dict[str, str] = {
        '': full_run,
    }
    single_run = single_test.format(
        target=target,
    )
    action: str = actions.get(
        target, single_run,
    )
    return generate(actions=(action,))


def task_ruff() -> MetaData:
    return generate(actions=(ruff,))


def task_flake8() -> MetaData:
    return generate(actions=(flake8,))


def task_mypy() -> MetaData:
    return generate(actions=(mypy,))


def task_bandit() -> MetaData:
    return generate(actions=(bandit,))


def task_safety() -> MetaData:
    return generate(actions=(safety,))


def task_blocklint() -> MetaData:
    return generate(actions=(blocklint,))


def task_up() -> MetaData:
    return generate(actions=(up,))


def task_outdated() -> MetaData:
    return generate(actions=(outdated,))


def task_lint() -> MetaData:
    return generate(
        actions=(
            ruff, flake8, mypy,
            bandit, blocklint,
        ),
    )


def fix_requirements() -> None:
    path = Path('requirements.txt')
    lines: list[str]
    truncated: Generator[
        str, None, None,
    ]
    divided: Generator[
        list[str], None, None,
    ]
    fixed: str
    with path.open(mode='r+') as file:
        lines = file.readlines()
        file.seek(0)
        file.truncate()
        divided = (
            line.split(
                ' ', 1,
            ) for line in lines
        )
        truncated = (
            next(iter(line))
            for line in divided
        )
        fixed = '\n'.join(truncated)
        file.write(fixed + '\n')


def task_export() -> MetaData:
    actions = (export, fix_requirements,)
    return generate(actions=actions)


def task_all() -> MetaData:
    first = 'coverage_report_type'
    second = 'number_of_processes'
    third = 'flake_runs'
    kwargs = {
        first: default_c,
        second: default_n,
        third: default_f,
    }
    full_run = full_test.format(**kwargs)
    return generate(
        actions=(
            full_run, ruff, flake8, mypy,
            bandit, blocklint, outdated,
        ),
    )
