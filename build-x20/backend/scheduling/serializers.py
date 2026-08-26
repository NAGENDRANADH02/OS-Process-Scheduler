from rest_framework import serializers

class ProcessSerializer(serializers.Serializer):
    pid = serializers.CharField()
    arrival_time = serializers.IntegerField(min_value=0)
    burst_time = serializers.IntegerField(min_value=1)
    priority = serializers.IntegerField(required=False, allow_null=True)

class ScheduleRequestSerializer(serializers.Serializer):
    algorithm = serializers.ChoiceField(choices=["fcfs", "sjf_non_preemptive", "sjf_preemptive", "round_robin", "priority_non_preemptive", "priority_preemptive"])
    time_quantum = serializers.IntegerField(min_value=1, required=False)
    processes = ProcessSerializer(many=True, min_length=1)

    def validate(self, attrs):
        algorithm, processes = attrs["algorithm"], attrs["processes"]
        if algorithm == "round_robin" and not attrs.get("time_quantum"):
            raise serializers.ValidationError({"time_quantum": "Required for Round Robin."})
        if algorithm.startswith("priority") and any(p.get("priority") is None for p in processes):
            raise serializers.ValidationError({"processes": "Priority is required for priority scheduling."})
        if len({p["pid"] for p in processes}) != len(processes):
            raise serializers.ValidationError({"processes": "Process IDs must be unique."})
        return attrs
