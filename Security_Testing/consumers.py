import json
from .zap import *
import time
from channels.generic.websocket import WebsocketConsumer
from channels.exceptions import  StopConsumer
from DW import settings


class SecurityConsumer(WebsocketConsumer):
    def websocket_connect(self, message):
        """
        It accepts the connection and creates a new socket object from the other end of the connection
        """
        self.spider_status = None
        self.scan_status = None
        settings.active_connection = True
        self.accept()

    def websocket_disconnect(self, message):
        settings.active_connection = False
        self.close()


    def receive(self, text_data):
        """
        It takes a url and an attack type as input, starts a spider scan, waits for the spider scan to complete, starts an
        active scan, waits for the active scan to complete, and then checks the results for the attack type specified

        :param text_data: The message sent by the client
        """
        settings.active_connection = True
        text_data_json = json.loads(text_data)
        url = text_data_json["url"]
        attack_type = text_data_json["finde"]
        # Starting a spider scan on the target url.
        scanid = start_spider_scan(target=url)
        # Checking the status of the spider scan. If the spider scan is not completed,
        # it will keep checking the status of
        # the spider scan.
        self.start_spider(scanid=scanid)
        self.start_ascan(url=url)
        self.get_results(url=url, attack_type=attack_type)
        settings.active_connection = False

    def start_spider(self, scanid):
        """
        It checks the status of the spider every second and sends the current status to the client

        :param scanid: The scan id of the scan that is being run
        """
        while self.spider_status != "COMPLETED" and settings.active_connection:
            current_spider = get_spider_scan(scanid)
            self.spider_status = current_spider["status"]
            print(self.spider_status)
            time.sleep(1)
            self.send(json.dumps({'message': "Found by spider"}))
            self.send(json.dumps(current_spider))
            if self.spider_status == "BAD URL!":
                break
        if not settings.active_connection:
            raise StopConsumer()


    def start_ascan(self, url):
        # Starting an active scan on the target url.
        scanid = ascan(url)

        # Checking the status of the active scan.
        # If the active scan is not completed,
        # it will keep checking the status of
        # the active scan.

        while self.scan_status != "COMPLETED" and settings.active_connection:
            print('here!')
            current_scan = get_ascan(scanID=scanid)
            self.scan_status = current_scan["status"]
            print(self.scan_status)
            time.sleep(1)
            self.send(json.dumps(current_scan))
            if self.scan_status == "BAD URL!":
                break
        if not settings.active_connection:
            raise StopConsumer()

    def get_results(self, url, attack_type):
        counter = 0
        # Iterating through the results of the active scan and checking if the attack type specified by the user is
        # present in the results.
        for i in get_result(url):
            if attack_type == "sql_injection":
                if "SQL Injection" in i["alert"]:
                    self.send(
                        json.dumps(
                            {
                                "message": "SQL Injection Found",
                                "status": "COMPLETED",
                                "detail": [i["description"] + " at " + i["url"]],
                            }
                        )
                    )
                    counter += 1
            else:
                if "Cross Site Scripting" in i["alert"]:
                    self.send(
                        json.dumps(
                            {
                                "message": "Cross Site Scripting",
                                "status": "COMPLETED",
                                "detail": [i["description"] + " at " + i["url"]],
                            }
                        )
                    )
                    counter += 1
        # Checking if the counter is 0.
        # If it is 0, it means that the attack type specified by the user is not present in the results.
        if counter == 0:
            self.send(
                json.dumps(
                    {
                        "message": "SQL Injection not found"
                        if attack_type == "sql_injection"
                        else "XSS not found",
                        "status": "COMPLETED",
                    }
                )
            )
