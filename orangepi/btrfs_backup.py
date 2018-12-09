#!/usr/bin/env python3
from subprocess import check_output
import logging
from datetime import datetime
from typing import List, Callable
import re



logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

SUBVOL_RULE = re.compile(r'.*path +(?P<name>[0-9]+)')
TIME_FORMAT = '%Y%m%d%H%M'


class Response:
    __slots__ = ('code', 'output', 'exception')


def run_command(command: List[str], shell: bool=False)->Response:
    resp = Response()
    try:
        output = check_output(command, shell=shell)
    except Exception as e:
        resp.output = str(e)
        resp.code = e.errno
    else:
        resp.output = output
        resp.code = 0
    return resp


def create_new_snapshot(source: str, dst: str)->None:
    command = ['btrfs', 'subvolume', 'create', '-r', source, dst]
    resp = run_command(command)
    if resp.code != 0:
        logger.error(
            f'create new snapshot for {source} at {dst} failed')
    else:
        logger.info(
            f'create new snapshot for {source} at {dst} successfully')


def send_snapshot(source: str, dst: str)->None:
    command = ['btrfs', 'send', source, '|', 'btrfs', 'receive', dst]
    resp = run_command(command, shell=True)
    if resp.code != 0:
        logger.error(
            f'send snapshot from {source} to {dst} failed')
    else:
        logger.error(
            f'send snapshot from {source} to {dst} successfully')



def delete_old_snapshots(snapshots: List[str], policy: Callable[[str], bool])->None:
    old_subvol_dates = policy(snapshots)

    old_snapshots = [directory+subvol for subvol in old_subvol_dates]

    for old_snapshot in old_snapshots:
        _delete_snapshot(old_snapshot)


def get_all_rsorted_snapshots(directory: str) -> List[str]:
    directory = directory if directory.endswith('/') else directory + '/'

    list_snapshots_command = ['btrfs', 'subvolume', 'list', '-o', directory]
    resp = run_command(list_snapshots_command)
    if resp.code != 0:
        logger.error(f'error while listing subvols in dir {directory}')
        return
    return sorted(_find_all_subvols(resp.output), reverse=True)


def need_new_snapshot(snapshots: List[str]):
    newest_snapshot_datetime = datetime.strptime(snapshots[0], TIME_FORMAT)
    datetime_now = datetime.now()

    delta = datetime_now - newest_snapshot_datetime
    return delta.days >= 1



def _find_all_subvols(output: str)->List[str]:
    return SUBVOL_RULE.findall(output)


def _delete_snapshot(path: str) -> None:
    command = ['btrfs', 'subvol', 'del', path]
    resp = rum_command(command)
    if resp.code != 0:
        logger.error(
            f'failed to delete subvol {path}')
    else:
        logger.info(
            f'delete subvol at {path} successfully')



class Policy:
    def __init__(self,
                 small_remain_day_num: int,
                 bigger_remain_day_num: int,
                 bigger_remain_day_interval: int):
        self._small_remain_day_num = small_remain_day_num
        self._bigger_remain_day_num = bigger_remain_day_num
        self._bigger_remain_day_interval = bigger_remain_day_interval

    def __call__(self, snapshots: List[str]) -> bool:
        date_time_now = datetime.now()

        subvols = snapshots
        subvols_to_be_deleted = list()
        date_time_dict = {datetime.strptime(subvol, TIME_FORMAT): subvol
                          for subvol in subvols}
        date_times= sorted(date_time_dict, reverse=True)

        # date_times 0->biggest newest-> oldest
        oldest_snapshot_datetime = date_times[-1]
        big_day_count = 0
        small_day_count = 0
        for date_time in date_times:
            if self._is_big_day(oldest_snapshot_datetime, date_time):
                big_day_count += 1
                # if a big day is found, set small_day_count to small_remain_day_num
                # which means all small days before this big day should be deleted
                small_day_count = self._small_remain_day_num
                if big_day_count > self._bigger_remain_day_num:
                    subvols_to_be_deleted.append(date_time_dict[date_time])
            else:
                # small day
                small_day_count += 1
                if small_day_count > self._small_remain_day_num:
                    subvols_to_be_deleted.append(date_time_dict[date_time])
        return subvols_to_be_deleted

    def _is_big_day(self,
                    first_big_day: datetime,
                    date_time: datetime) -> bool:
        delta = date_time - first_big_day
        return (delta.days % self._bigger_remain_day_interval) == 0

    def _should_delete_small_day(
            self,
            farest_small_day: datetime,
            date_time: datetime) -> bool:
        delta = date_time - farest_small_day
        return delta.days > self._small_remain_day_num



def main(storage_dir, source_dir, snapshots_dir):
    policy = Policy(small_remain_day_num=5, bigger_remain_day_num=7, bigger_remain_day_interval=10)

    snapshots = get_all_rsorted_snapshots(storage_dir)

    if need_new_snapshot(snapshots):
        snapshot_name = datetime.now().strftime(TIME_FORMAT)
        snapshot_path = snapshots_dir + '/' + snapshot_name
        create_new_snapshot(source_dir, snapshot_path)
        send_snapshot(snapshot_path, storage_dir)
        delete_old_snapshots(snapshots.insert(0, snapshot_name), policy)


if __name__ == '__main__':
    main('/media/raid1', '/media/u-sda1', '/media/u-sda1/.snapshots')
