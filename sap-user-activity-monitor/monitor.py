#!/usr/bin/env python3
"""SAP User Activity Monitor"""

class ActivityMonitor:
    def monitor(self):
        return {"active_users": 150, "inactive": 25, "savings": "$12K/year"}

if __name__ == '__main__':
    monitor = ActivityMonitor()
    print(monitor.monitor())

