from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Player
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def right_answer(request, player_turn):
    if request == "POST":
        if player_turn == 1:
            total = Player.player1_answer_right()+1
            Player.objects.create(count=total) 
            return JsonResponse({"total": total}) 
        else:
            total = Player.player2_answer_right()+1
            Player.objects.create(count=total) 
            return JsonResponse({"total": total}) 
 

@csrf_exempt
def wrong_answer(request, player_turn):
    if request == "POST":
        if player_turn == 1:
            total = Player.player1_answer_wrong()+1
            Player.objects.create(count=total) 
            return JsonResponse({"total": total}) 
        else:
            total = Player.player2_answer_wrong()+1
            Player.objects.create(count=total) 
            return JsonResponse({"total": total}) 

def home(request):
    return HttpResponse("Maze!")

def menu(request):
    return render(request, "menu.html")

def play(request):
    return render(request, "play.html")

def options(request):
    return render(request, "options.html")

def maze(request): 
    if request.method == "POST":
        data = json.loads(request.body)
        player_turn = data.get('turn') 
        answer = data.get('answer')
        player1 = Player.player1_name
        player2 = Player.player2_name
        if player_turn == 1 and answer == "right":
            player1.player1_answer_right += 1
        elif player_turn == 1 and answer == "wrong":
            player1.player1_answer_wrong += 1
        elif player_turn == 2 and answer == "right":
            player2.player2_answer_right += 1
        else:
            player2.player2_answer_wrong += 1
        player1.save()
        player2.save()

    return render(request, 'maze.html')

def ai_view(request):
    return render(request, 'ai.html')

def select(request):
    return render(request, 'select.html')

def tutorial(request):
    return render(request, 'tutorial.html')

def name(request):
    if request.method == "POST":
        data = json.loads(request.body)
        p1 = data.get('player1_name') 
        p2 = data.get('player2_name')


        global playerNm 
        playerNm = Player.objects.create(player1_name=p1, player2_name=p2)
        return JsonResponse({"player1_name":playerNm.player1_name, "player2_name":playerNm.player2_name})
        
    return render(request, 'name.html')