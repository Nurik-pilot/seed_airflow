from typing import TypeAlias

from doit import task_params

default_coverage_report_type = 'term-missing'
default_c = default_coverage_report_type

default_number_of_processes = 1
default_n = default_number_of_processes

default_flake_runs = 1
default_f = default_flake_runs

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
        'pytest', '-vs',
        '--disable-pytest-warnings',
        '{target}',
    ),
)

mypy = 'mypy .'
bandit = 'bandit -r . --exclude tests'
blocklint = 'blocklint .'
flake8 = 'flake8 .'

safety = ' -i '.join(
    (
        'safety check',
        '51668', '42194', '51457', '62582',
        '62583', '40459', '62019',
    ),
)

outdated = 'poetry show --outdated'

up = 'poetry update'

default_verbosity = 2

Actions: TypeAlias = tuple[str, ...]
MetaData: TypeAlias = dict[str, Actions | int]


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


def task_lint() -> MetaData:
    return generate(
        actions=(
            flake8, mypy,
            bandit, blocklint,
        ),
    )


def task_outdated() -> MetaData:
    return generate(actions=(outdated,))


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
            full_run, flake8,
            mypy, bandit,
            blocklint, outdated,
        ),
    )
