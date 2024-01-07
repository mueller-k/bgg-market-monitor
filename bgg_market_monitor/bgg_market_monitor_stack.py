from aws_cdk import Stack, aws_events, aws_lambda, aws_sns
from constructs import Construct


class BggMarketMonitorStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # TODO: Correct initialization of these

        topic = aws_sns.Topic(self, "topic")

        function = aws_lambda.Function(self, "function")

        schedule = aws_events.Rule(self, "event")
