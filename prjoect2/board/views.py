from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import render
from pip._vendor.requests import Response

from board.models import Board,Users,Comment
from django.shortcuts import redirect
from board.forms import LoginForm

from django.db import connection

import pymysql

def home(request):
    rsBoard = Board.objects.all()
    return render(request, "home.html", {
        'rsBoard': rsBoard
    })

def board_write(request):
    return render(request, "board_write.html", )

def board_insert(request):
    btitle = request.GET['title']
    bnote = request.GET['b_context']
    user_name = request.session.get('loginuser')
    member = Users.objects.get(name=user_name)
    if btitle != "":
        rows = Board.objects.create(title=btitle, b_context=bnote, id=member)
        return redirect('/home')
    else:
        return redirect('/board_write')

def board_view(request):
    bno = request.GET['b_number']
    rsDetail = Board.objects.filter(b_number=bno)
    request.session['cur_board'] = bno
    print (  bno, "***", rsDetail   )
    return render(request, "board_view.html", {
        'rsDetail': rsDetail
    })

def comment_insert(request):
    ccontext = request.GET['c_context']
    user_name = request.session.get('loginuser')
    member = Users.objects.get(name=user_name)
    num = int(request.session.get('cur_board'))
    # bno = {'b_number': num}
    bno = request.GET['board']
    bno = Board.objects.get(b_number=bno)
    rsDetail = Board.objects.filter(b_number=num)
    if ccontext != "":
        comment = Comment()
        comment.c_context = ccontext
        comment.b_number = bno
        comment.id = member
        comment.save()
        rsComment = Comment.objects.filter(b_number=num)

        return render(request, "board_view.html", {
            'rsDetail': rsDetail, 'rsComment': rsComment
        })
    else:
        return redirect('home')

def board_edit(request):
    bno = request.GET['b_number']
    rsDetail = Board.objects.filter(b_number=bno)

    return render(request, "board_edit.html", {
        'rsDetail': rsDetail
    })


def board_update(request):
    bno = request.GET['b_number']
    btitle = request.GET['title']
    bnote = request.GET['b_context']


    try:
        board = Board.objects.get(b_number=bno)
        if btitle != "":
            board.title = btitle
        if bnote != "":
            board.b_context = bnote


        try:
            board.save()
            return redirect('/home')
        except ValueError:
            return Response({"success": False, "msg": "에러입니다."})

    except ObjectDoesNotExist:
        return Response({"success": False, "msg": "게시글 없음"})


def board_delete(request):
    bno = request.GET['b_number']
    rows = Board.objects.get(b_number=bno).delete()
    return redirect('/home')


def ds_querytolist(request):

    rsBoard = Board.objects.all()

    print("Type of model query result : ")
    print(type(rsBoard))

    rsList = []

    for record in rsBoard:
        lst = list(record.b_title)
        rsList.append(lst)

    print("Type of list : ")
    print(type(rsList))
    print(rsList)

    return render(request, "datastudy.html", {})

def ds_orm(request):
    # CASE1 :
    rsBoard = Board.objects.all()
    print(type(rsBoard))

    # CASE2 :
    rsBoard2 = Board.objects.raw('SELECT * FROM board')
    print(type(rsBoard2))

    # CASE3 :
    with connection.cursor() as cursor0:
        cursor0.execute('SELECT * FROM board')
        rsBoard3 = cursor0.fetchall()
        cursor0.close

    print(type(rsBoard3))


    # CASE4 :
    dbCon = pymysql.connect('localhost', 'root', 'intra165', 'edudb')
    cursor1 = dbCon.cursor()
    cursor1.execute('SELECT * FROM board')
    rsBoard4 = cursor1.fetchall()
    cursor1.close

    print(type(rsBoard4))


    return render(request, "ds_orm.html", {
        'rsBoard': rsBoard,
        'rsBoard2': rsBoard2,
        'rsBoard3': rsBoard3,
        'rsBoard4': rsBoard4,
    })


def markdown2(request):
    return render(request, "markdown2.html")


def login(request):
    form = LoginForm()
    return render(request, "login.html", {'form': form})

def loginProcess(request):
    form = LoginForm(request.POST)
    errormessage = ""

    if form.is_valid():
        login_id = form.cleaned_data["login_id"]
        login_pw = form.cleaned_data["login_pw"]
        print(login_id, login_pw)

        try:
            user = Users.objects.get(pk=login_id, pw=login_pw)
            print(user)
            if user:
                request.session["loginuser"] = user.name
                return HttpResponseRedirect("/home")
            else:
                errormessage = "1 로그인 실패. 다시 로그인하세요"
                context = {"errormessage": errormessage}
                return render(request, "login.html", context)

        except(Users.DoesNotExist):
            errormessage = "2 로그인 실패, 다시 로그인하세요"
            context = {"errormessage": errormessage}
            return render(request, "login.html", context)