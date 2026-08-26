from rest_framework.response import Response
from rest_framework.views import APIView

from .algorithms import ALGORITHMS
from .serializers import ScheduleRequestSerializer
from .models import SchedulingRun


class ScheduleView(APIView):
    def post(self, request):
        serializer = ScheduleRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        fn = ALGORITHMS[data["algorithm"]]
        result = fn(data["processes"], data["time_quantum"]) if data["algorithm"] == "round_robin" else fn(data["processes"])
        return Response({"algorithm": data["algorithm"], "time_quantum": data.get("time_quantum"), **result})


class SaveScheduleView(APIView):
    def post(self, request):
        serializer = ScheduleRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        fn = ALGORITHMS[data["algorithm"]]
        result = fn(data["processes"], data["time_quantum"]) if data["algorithm"] == "round_robin" else fn(data["processes"])
        run = SchedulingRun.objects.create(algorithm=data["algorithm"], time_quantum=data.get("time_quantum"),
            inputs={"processes": data["processes"]}, results=result)
        return Response({"id": run.id, "created_at": run.created_at, "algorithm": run.algorithm, **result}, status=201)


class ScheduleHistoryView(APIView):
    def get(self, request):
        runs = SchedulingRun.objects.all()[:100]
        return Response([{"id": r.id, "algorithm": r.algorithm, "time_quantum": r.time_quantum,
            "inputs": r.inputs, "results": r.results, "created_at": r.created_at} for r in runs])
