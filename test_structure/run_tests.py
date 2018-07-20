#POE
import nose
import xml.etree.ElementTree
import requests
import json
import os, sys
cwd = os.getcwd()

from config import *


report_path = '{0}/output.xml'.format(cwd)

def build_report():
    slack_webhook = SLACK_HOOK

    e = xml.etree.ElementTree.parse(report_path).getroot()
    root = e.findall("testsuite")

    success = []
    failures = []

    data = {}
    data["text"] = "*API Test Execution* Executed Tests: {0} Failures: {1}".format(
        e.attrib["tests"], e.attrib["errors"])
    data["mrkdwn"] = True
    attachments = []

    success = {}
    success["pretext"] = "Succesful Tests"
    success["fields"] = []

    failures = {}
    failures["pretext"] = "Failed Tests"
    failures["fields"] = []

    for node in e.findall("testcase"):
        field = {}
        print node.attrib["name"]
        field["title"] = "TestCase: " + node.attrib["name"]
        errors = node.findall("failure")
        if len(errors) > 0 :
            print errors[0]
            field["value"] = "Error: %s" % errors[0].get("message")
            failures["fields"].append(field)
        else:
            success["fields"].append(field)



    if len(failures['fields']) > 0:
        failures['color'] = 'danger'
    else:
        failures['text'] = 'No Failures'

    if len(success['fields']) > 0:
        success['color'] = 'good'

    attachments.append(failures)
    attachments.append(success)
    data["attachments"] = attachments
    payload = json.dumps(data)
    requests.post(slack_webhook, payload)


def main():
    module = sys.argv[1]
    print module
    testsuite = '{1}.py'.format(cwd,module)
    nose.run(argv=['', testsuite, '--with-xunit','--xunit-file={0}'.format(report_path)])
    build_report()

if __name__ == "__main__":
    main()
