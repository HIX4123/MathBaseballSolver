from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from math_baseball_solver import create_candidates, filter

from random import choice


class Attempt:
    def __init__(self, guess, strike, ball, candidates, completeness):
        self.guess = guess
        self.strike = strike
        self.ball = ball
        self.candidates = candidates
        self.completeness = completeness

    def __str__(self):
        return f"Guess: {self.guess}, Strike: {self.strike}, Ball: {self.ball}, Completeness: {self.completeness}"


def create_attempts():
    attempts = [Attempt("0000", 0, 0, [], 0) for _ in range(9)]
    attempts[0].candidates = create_candidates()
    attempts[0].guess = choice(attempts[0].candidates)
    return attempts


@csrf_exempt
def index(request):
    request.session["times"] = request.session.get("times", 0)
    request.session["attempts"] = request.session.get("attempts", create_attempts())

    if request.method == "POST":
        if "less_strike" in request.POST:
            attempt_index = int(request.POST["less_strike"])
            if request.session["attempts"][attempt_index].strike > 0:
                request.session["attempts"][attempt_index].strike -= 1
        if "more_strike" in request.POST:
            attempt_index = int(request.POST["more_strike"])
            if request.session["attempts"][attempt_index].strike < 3:
                request.session["attempts"][attempt_index].strike += 1
        if "less_ball" in request.POST:
            attempt_index = int(request.POST["less_ball"])
            if request.session["attempts"][attempt_index].ball > 0:
                request.session["attempts"][attempt_index].ball -= 1
        if "more_ball" in request.POST:
            attempt_index = int(request.POST["more_ball"])
            if request.session["attempts"][attempt_index].ball < 4:
                request.session["attempts"][attempt_index].ball += 1
        if "OK" in request.POST:
            request.session["times"] = int(request.POST["OK"])
            request.session["attempts"][request.session["times"]].candidates = filter(
                request.session["attempts"][request.session["times"] - 1].candidates,
                request.session["attempts"][request.session["times"] - 1].guess,
                request.session["attempts"][request.session["times"] - 1].strike,
                request.session["attempts"][request.session["times"] - 1].ball,
            )
            request.session["attempts"][request.session["times"]].guess = choice(
                request.session["attempts"][request.session["times"]].candidates
            )
            print()
            print(request.session["attempts"][request.session["times"]].candidates)
            request.session["attempts"][request.session["times"]].completeness = round(
                (
                    1
                    - (
                        len(
                            request.session["attempts"][
                                request.session["times"]
                            ].candidates
                        )
                        - 1
                    )
                    / 5175
                )
                * 100,
                2,
            )
        if "reset" in request.POST:
            request.session["times"] = 0
            request.session["attempts"] = create_attempts()

    return render(
        request,
        "index.html",
        {"Attempts": request.session["attempts"][: request.session["times"] + 1]},
    )
