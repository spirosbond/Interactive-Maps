import pytest

# from fastapi.testclient import TestClient
import sys
import os
from apscheduler.schedulers.background import BackgroundScheduler

# Required row to be able to import the app folder.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app
from app.services.task_scheduler import TaskScheduler
from app.services import pull_position_task
from app.config import app_config

# client = TestClient(app)

taskScheduler = TaskScheduler()

# Dummy misconfigured task - missing freq key
dummy_task_1 = {"enabled": True, "entrypoint": "pull_position_task.main"}
# Dummy misconfigured task - none existing entrypoint
dummy_task_2 = {"enabled": True, "entrypoint": "dummy.main", "freq": 5}


def test01_init():
    taskScheduler.task_scheduler
    assert isinstance(taskScheduler.task_scheduler, BackgroundScheduler)


def test02_start():
    n_of_enabled_services = 0

    app_config.app_services["dummy_task_1"] = dummy_task_1
    # Should fail because dummy task is missing the key "freq"
    with pytest.raises(TypeError):
        n_of_started_services = taskScheduler.start()
    # Remove the dummy task and try again
    del app_config.app_services["dummy_task_1"]

    app_config.app_services["dummy_task_2"] = dummy_task_2
    # Should fail because dummy task has a none existing entrypoint
    with pytest.raises(AttributeError):
        n_of_started_services = taskScheduler.start()
    # Remove the dummy task and try again
    del app_config.app_services["dummy_task_2"]

    for service_key, service_values in app_config.app_services.items():
        if service_values.get("enabled"):  # Check if the service is enabled
            n_of_enabled_services += 1
    n_of_started_services = taskScheduler.start()

    assert n_of_started_services == n_of_enabled_services
    assert taskScheduler.task_scheduler.running == True


def test03_stop():
    # Test stopping the task scheduler
    taskScheduler.stop()
    assert taskScheduler.task_scheduler.running == False


def test04_pull_position_task():
    # Test the pull_position task
    location, status = pull_position_task.main()
    assert location != {}
    assert status == 200
    assert location["sat_id"] == app_config.app_iss_id

    app_config.app_iss_id = 0
    location, status = pull_position_task.main()
    assert location == {}
    assert status != 200
