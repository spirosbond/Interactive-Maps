from apscheduler.schedulers.background import BackgroundScheduler
import app.services as app_services
from app.services import pull_position_task
from app.config import app_config


class TaskScheduler:
    """
    A class to manage and schedule tasks using BackgroundScheduler.
    """

    def __init__(self):
        """
        Initializes the TaskScheduler instance with a BackgroundScheduler.
        """
        self.task_scheduler = BackgroundScheduler()

    def start(self):
        """
        Starts the scheduler and configures tasks based on the application's configuration.

        Iterates through the services listed in the app configuration, checks if they are enabled,
        and schedules their associated functions as interval jobs.

        Returns:
            int: The number of tasks that were started.
        """
        tasks_enabled = 0  # Counter for the number of tasks enabled

        # Iterate over each service defined in the application configuration
        for service_key, service_values in app_config.app_services.items():
            if service_values.get("enabled"):  # Check if the service is enabled
                print(
                    f"Enabling service: {service_key} with entrypoint: {service_values.get('entrypoint')}"
                )

                try:
                    # Retrieve the service and function specified in the entrypoint. For example: pull_position_task.main
                    service_str, function_str = service_values.get("entrypoint").split(
                        "."
                    )
                    service = getattr(
                        app_services, service_str
                    )  # Get the service module
                    function = getattr(
                        service, function_str
                    )  # Get the function within the service

                    # Add the function as a scheduled job
                    self.task_scheduler.add_job(
                        function,
                        "interval",  # The job type is interval-based
                        seconds=app_config.app_apis_sat_loc_freq,  # Frequency of execution
                    )
                    tasks_enabled += 1
                except Exception as e:
                    print(
                        f"Error enabling service: {service_key} with entrypoint: {service_values.get('entrypoint')}"
                    )

        # Start the scheduler only if there are tasks to run
        if tasks_enabled > 0:
            self.task_scheduler.start()

        return tasks_enabled  # Return the number of tasks that were started

    def stop(self):
        """
        Stops the scheduler and shuts down all scheduled jobs.
        """
        if self.isrunning():
            self.task_scheduler.shutdown()

    def isrunning(self):
        """
        Checks if the scheduler is running and returns its status.
        Returns:
            bool: True if scheduler is running, False otherwise.
        """
        return self.task_scheduler.running
