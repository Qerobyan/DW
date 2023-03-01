zap_url = "http://localhost:8080"
from  DW.settings import zap_api_key

from zapv2 import ZAPv2

apiKey = zap_api_key

zap = ZAPv2(
    apikey=apiKey,
    proxies={"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"},
)


def start_spider_scan(target):
    """
    It removes all previous scans, then starts a new scan on the target.

    :param target: The URL of the site you want to scan
    :return: The scanID is being returned.
    """
    zap.spider.remove_all_scans(apikey=apiKey)
    scanID = zap.spider.scan(target)
    return scanID


def get_spider_scan(scanID):
    """
    It checks the status of the spider scan and returns a message and status

    :param scanID: The ID of the scan
    :return: A dictionary with the message and status of the spider scan.
    """
    try:
        if not int(zap.spider.status(scanID)) < 100:
            message = (
                "Spider has completed! Found "
                + str(len(zap.spider.results(scanID)))
                + " URLs:"
            )
            status = "COMPLETED"
            return {
                "message": message,
                "status": status,
                "detail": zap.spider.results(scanID),
            }
    except ValueError:
        message = "URL does not exist"
        status = "BAD URL!"
        return {"message": message, "status": status}
    message = "Spider progress %: {}".format(zap.spider.status(scanID))
    status = "IN_PROGRESS!"
    return {"message": message, "status": status}


def ascan(target):
    """
    It removes all existing scans, then scans the target and returns the scan ID.

    :param target: The URL of the target to be scanned
    :return: The scanID is being returned.
    """
    zap.ascan.remove_all_scans(apikey=apiKey)
    scanID = zap.ascan.scan(target)
    return scanID


def get_ascan(scanID):
    """
    The function takes a scanID as an argument and returns a dictionary with a message and status

    :param scanID: The ID of the scan
    :return: A dictionary with two keys: message and status.
    """
    try:
        if not int(zap.ascan.status(scanID)) < 100:
            message = "Active scan COMPLETED!"
            status = "COMPLETED"
            return {"message": message, "status": status}
    except ValueError:
        message = "URL does not exist"
        status = "BAD URL!"
        return {"message": message, "status": status}

    message = "Scan progress %: {}".format(zap.ascan.status(scanID))
    status = "IN_PROGRESS!"
    return {"message": message, "status": status}


def get_result(target):
    """
    > This function will return a list of all the alerts that ZAP has found on the target

    :param target: The target URL to scan
    """
    return zap.core.alerts(baseurl=target)
