import aws_cdk as core
import aws_cdk.assertions as assertions

from bgg_market_monitor.bgg_market_monitor_stack import BggMarketMonitorStack


# example tests. To run these tests, uncomment this file along with the example
# resource in bgg_market_monitor/bgg_market_monitor_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = BggMarketMonitorStack(app, "bgg-market-monitor")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
