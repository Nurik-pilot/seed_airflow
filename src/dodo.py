from pathlib import Path
from typing import (
    Callable, Generator,
)

from doit import task_params

default_c = 'term-missing'

default_n = 2

default_f = 1

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
    ),
)

single_test = ' '.join(
    (
        'pytest', '-vs', '{target}',
        '--disable-pytest-warnings',
    ),
)

mypy = 'mypy .'
bandit = 'bandit -r . --exclude tests'

blocklint = ' '.join(
    (
        'blocklint .',
        '--skip-files',
        'airflow.cfg',
    ),
)
flake8 = 'flake8 .'
ruff: str = 'ruff check .'

safety = ' -i '.join(
    (
        'safety check',
        '51457', '62019',
        '42194', '51668',
    ),
)

outdated = 'poetry show --outdated'

up = ' && '.join(
    (
        ' '.join(
            (
                'poetry self add',
                'poetry-plugin-up',
            ),
        ),
        'poetry update',
        'poetry up --latest',
    ),
)

export = ' && '.join(
    (
        ' '.join(
            (
                'poetry', 'self', 'add',
                'poetry-plugin-export',
            ),
        ),
        'rm --force requirements.txt',
        ' '.join(
            (
                'poetry export',
                '--format requirements.txt',
                '--output requirements.txt',
                '--with dev',
                '--without-hashes',
                '--without-urls',
            ),
        ),
    ),
)

default_verbosity = 2

type Command = str | Callable[[], None]

type Actions = tuple[Command, ...]

type MetaData = dict[
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
            ruff, flake8,
            mypy, bandit,
            blocklint, safety,
        ),
    )


def fix_requirements() -> None:
    path = Path('requirements.txt')
    text: str = path.read_text()
    lines: list[str]
    lines = text.splitlines()
    divided: Generator[
        list[str], None, None,
    ]
    divided = (
        line.split(
            ' ', 1,
        ) for line in lines
    )
    truncated: Generator[
        str, None, None,
    ]
    truncated = (
        next(iter(line))
        for line in divided
    )
    fixed: str = '\n'.join(truncated)
    data: str = fixed + '\n'
    path.write_text(data=data)


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
            full_run, ruff, flake8,
            mypy, bandit, blocklint,
            safety, outdated,
        ),
    )
