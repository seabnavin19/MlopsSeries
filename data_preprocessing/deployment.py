from main import greeting
from prefect.deployments import Deployment
from prefect.server.schemas.schedules import CronSchedule


greeting_deployment = Deployment.build_from_flow(
        flow = greeting,
        name = 'basic_greeting',
        work_queue_name = 'GreetingWorkQueue',
        parameters = dict(name='Navin'),
        schedule=(CronSchedule(cron="0 8 * * *", timezone="Asia/Phnom_Penh"))
        )

if __name__ == '__main__':
        greeting_deployment.apply()
