from django.test import TestCase
from .algorithms import fcfs, sjf_non_preemptive, sjf_preemptive, round_robin, priority_non_preemptive, priority_preemptive

class FCFSTests(TestCase):
    def test_textbook_order_and_metrics(self):
        result = fcfs([{"pid": "P1", "arrival_time": 0, "burst_time": 5}, {"pid": "P2", "arrival_time": 1, "burst_time": 3}, {"pid": "P3", "arrival_time": 2, "burst_time": 1}])
        self.assertEqual(result["segments"], [{"pid": "P1", "start": 0, "end": 5}, {"pid": "P2", "start": 5, "end": 8}, {"pid": "P3", "start": 8, "end": 9}])
        self.assertEqual(result["aggregate"]["average_waiting_time"], 3.33)

    def test_idle_cpu(self):
        result = fcfs([{"pid": "P1", "arrival_time": 2, "burst_time": 2}, {"pid": "P2", "arrival_time": 5, "burst_time": 1}])
        self.assertEqual(result["segments"], [{"pid": "IDLE", "start": 0, "end": 2}, {"pid": "P1", "start": 2, "end": 4}, {"pid": "IDLE", "start": 4, "end": 5}, {"pid": "P2", "start": 5, "end": 6}])
        self.assertEqual(result["aggregate"]["cpu_utilization"], 50.0)

class SJFTests(TestCase):
    def test_non_preemptive_classic(self):
        result = sjf_non_preemptive([{"pid":"P1","arrival_time":0,"burst_time":7}, {"pid":"P2","arrival_time":2,"burst_time":4}, {"pid":"P3","arrival_time":4,"burst_time":1}])
        self.assertEqual([s["pid"] for s in result["segments"]], ["P1", "P3", "P2"])
    def test_preemptive_shortest_remaining(self):
        result = sjf_preemptive([{"pid":"P1","arrival_time":0,"burst_time":8}, {"pid":"P2","arrival_time":1,"burst_time":4}, {"pid":"P3","arrival_time":2,"burst_time":2}])
        self.assertEqual(result["segments"], [{"pid":"P1","start":0,"end":1},{"pid":"P2","start":1,"end":2},{"pid":"P3","start":2,"end":4},{"pid":"P2","start":4,"end":7},{"pid":"P1","start":7,"end":14}])

class RoundRobinTests(TestCase):
    def test_quantum_two(self):
        result = round_robin([{"pid":"P1","arrival_time":0,"burst_time":5},{"pid":"P2","arrival_time":0,"burst_time":3}], 2)
        self.assertEqual(result["segments"], [{"pid":"P1","start":0,"end":2},{"pid":"P2","start":2,"end":4},{"pid":"P1","start":4,"end":6},{"pid":"P2","start":6,"end":7},{"pid":"P1","start":7,"end":8}])
    def test_arrivals_join_before_requeue(self):
        result = round_robin([{"pid":"P1","arrival_time":0,"burst_time":4},{"pid":"P2","arrival_time":2,"burst_time":1}], 2)
        self.assertEqual([s["pid"] for s in result["segments"]], ["P1", "P2", "P1"])

class PriorityTests(TestCase):
    def test_non_preemptive_lower_number_wins(self):
        result = priority_non_preemptive([{"pid":"P1","arrival_time":0,"burst_time":3,"priority":2},{"pid":"P2","arrival_time":0,"burst_time":2,"priority":1}])
        self.assertEqual([s["pid"] for s in result["segments"]], ["P2", "P1"])
    def test_preemptive_priority(self):
        result = priority_preemptive([{"pid":"P1","arrival_time":0,"burst_time":5,"priority":2},{"pid":"P2","arrival_time":1,"burst_time":2,"priority":1}])
        self.assertEqual(result["segments"], [{"pid":"P1","start":0,"end":1},{"pid":"P2","start":1,"end":3},{"pid":"P1","start":3,"end":7}])
