from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from board import models
from board.forms import CreatingThread, Reply, Registration, LogIn, AddSection, AddBoard


def save_reply(request, thread_id):
    if request.method == 'POST':
        form = Reply(request.POST)

        if form.is_valid():
            user = request.user
            text = form.cleaned_data['text']
            tr = models.Thread.objects.filter(id=int(thread_id))[0]  # thread
            models.Answer.objects.create(text=text, thread=tr, user=user)


def home(request, errors=None):
    print(request.user)
    sections = models.Section.objects.all()
    parts = []

    for section in sections:

        part = {'title': section.title,
                'boards': []}
        boards = models.Part.objects.filter(section__title=section)
        for board in boards:
            part['boards'].append({'url': board.short_title,
                                   'name': board.title})

        parts.append(part)

    return render_to_response('index.html',
                              {'sections': parts,
                               'user': request.user,
                               'errors': errors})


def board(request, string):
    ts = models.Thread.objects.filter(part__short_title=string)  # threads'./create_thread'

    if ts: # threads
        threads = []
        board_name = models.Part.objects.filter(short_title=string)[0].title

        for thread in ts:
            t = {
                'user': thread.user,
                'text':  thread.text,
                'date':  thread.date.strftime('%d/%m/%y %a %X'),
                'title':  thread.title,
                'id':  thread.id,
                'current_url': string,
                'short_title': thread.part.short_title
             }
            threads.append(t)

        return render_to_response('board.html', {'board_name': board_name,
                                                 'threads': threads,
                                                 'create_thread': './create_thread',
                                                 'user': request.user})
    else:
        return render_to_response('board.html', {'create_thread': './create_thread'})


@csrf_exempt
def thread(request, string, integer, reply_form=Reply):
    if request.method == 'POST':
        save_reply(request, integer)

    path = request.get_full_path()

    if 'reply' not in path:
        path += '/reply'
    else:
        answer = False
        redirect(path.replace('reply', ''))

    if not isinstance(string, str) or not integer.isdigit():
        return HttpResponse('404 error<br/>Page not found')

    else:
        thread = models.Thread.objects.filter(id=int(integer))[0]  # тред энивей 1 будет
        answers = models.Answer.objects.filter(thread__id=int(integer))
        result = []  # TODO: придумать норм название
        for answer in answers:
            result.append(
                {
                    'user': answer.user,
                    'text': answer.text,
                    'date': answer.date.strftime('%d/%m/%y %a %X'),
                    'id': answer.id
                }
            )

        return render_to_response('thread.html', {'answers': result,
                                                  'thread': thread,
                                                  'url': string,
                                                  'answer': lambda answer: answer if answer else '',
                                                  'form': reply_form,
                                                  'short_title':thread.part.short_title,
                                                  'path': path,
                                                  'user': request.user})


@csrf_exempt
def create_thread(request, string, create_form=CreatingThread):
    if request.method == 'POST':
        form = create_form(request.POST)
        if form.is_valid():
            user = request.user
            title = form.cleaned_data['title']
            text = form.cleaned_data['text']
            part = models.Part.objects.filter(short_title=string)[0]
            thread = models.Thread.objects.create(title=title, text=text, part=part, user=user)

            return redirect('/'+string+'/'+str(thread.id))

    return render_to_response('create_thread.html', {'form': create_form,
                                                     'user': request.user})


@csrf_exempt
def reply(request, board, integer):
    if request.method == 'POST':
        form = Reply(request.POST)

        if form.is_valid():
            user = request.user
            text = form.cleaned_data['text']
            tr = models.Thread.objects.filter(id=int(integer))[0]  # thread
            models.Answer.objects.create(text=text, thread=tr, user=user)

            return redirect('/'+board+'/'+str(tr.id))

    return thread(request, board, integer, answer=True, reply_form=Reply)


@csrf_exempt
def registration(request):
    if request.method == 'POST':
        form = Registration(request.POST)
        errors = []

        if form.is_valid():
            nickname = form.cleaned_data['nickname']
            email = '' if not form.cleaned_data['email'] else form.cleaned_data['email']
            password = form.cleaned_data['password']
            # user = User.objects.create_user('myusername', 'myemail@crazymail.com', 'mypassword')
            import django
            try:
                User.objects.create_user(nickname, email, password)
            except 'django.db.utils.IntegrityError':
                errors.append('Пользователь с таким никнеймом уже есть')
                return render_to_response('reg.html', {'form': Registration,
                                                       'errors': errors})
            else:
                return redirect('/')
    return render_to_response('reg.html', {'form': Registration})


@csrf_exempt
def log_in(request):
    if request.method == 'POST':
        form = LogIn(request.POST)
        errors = []

        if form.is_valid():
            username = request.POST.get("login", "")
            password = request.POST.get("password", "")
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                errors.append('Не верный логин или пароль')
                return render_to_response('login.html', {'form': LogIn,
                                                         'errors': errors})
    return render_to_response('login.html', {'form': LogIn})


@login_required
def log_out(request):
    logout(request)
    return home(request)

@login_required
@csrf_exempt
def add_section(request):
    if request.method == 'POST':
        form = AddSection(request.POST)

        if form.is_valid():
            title = form.cleaned_data['title']
            models.Section.objects.create(title=title)
            return redirect('/')

    return render_to_response('add_section.html', {'form': AddSection,
                                                   'user': request.user})
@login_required
@csrf_exempt
def add_board(request, name):
    section = models.Section.objects.filter(title=name)[0]
    if section:
        form = AddBoard(request.POST)

        if form.is_valid():
            title = form.cleaned_data['title']
            short_title = form.cleaned_data['short_title']
            models.Part.objects.create(title=title,
                                       short_title=short_title,
                                       section=section)
            return redirect('/')

    else:
        return redirect('/')

    return render_to_response('add_board.html', {'user': request.user,
                                                 'form': AddBoard})

@login_required
def del_board(request, board):
    errors = []
    try:
        board = models.Part.objects.filter(title=board)[0]
    except models.Part.DoesNotExist:
        errors.append('Такого раздела не существует')
        return home(request, errors=errors)
    else:
        errors.append(board.delete())
        errors[0][1]['Удалено'] = ""

        try:
            errors[0][1]['Тредов'] = errors[0][1].pop('board.Thread')
        except KeyError:
            errors[0][1]['Тредов'] = 0

        try:
            errors[0][1]['Досок'] = errors[0][1].pop('board.Part')
        except KeyError:
            errors[0][1]['Досок'] = 0

        try:
            errors[0][1]['Ответов'] = errors[0][1].pop('board.Answer')
        except KeyError:
            errors[0][1]['Ответов'] = 0

        return home(request, errors=errors[0][1])


@login_required
def del_thread(request, board, thread):
    errors = []
    try:
        thr = models.Thread.objects.get(part=models.Part.objects.get(short_title=board), id=thread)

    except models.Part.DoesNotExist:
        return redirect('/'+'board'+str(thread))
    else:
        errors.append(thr.delete())

        try:
            errors[0][1]['Ответов'] = errors[0][1].pop('board.Answer')
        except KeyError:
            errors[0][1]['Ответов'] = 0

        try:
            errors[0][1]['Тредов'] = errors[0][1].pop('board.Thread')
        except KeyError:
            errors[0][1]['Тредов'] = 0

        errors[0][1]['Удалено'] = ""

        return redirect('/'+board, {'errors': errors})


@login_required
def del_answer(request, board, thread, answer):
    errors = []
    try:
        answer = models.Answer.objects.get(thread__id = int(thread),
                                       id=int(answer))
    except:
        errors.append('Этого ответа не существует')
    else:
        answer.delete()
        errors.append('Ответ успешно удален')
    return redirect('/'+board+'/'+thread)


@login_required
@csrf_exempt
def edit_answer(request, board, topic, answer):
    errors = []

    try:
        answer = models.Answer.objects.get(thread__id=topic,
                                           id = answer)
    except models.Answer.DoesNotExist:
        return redirect('/'+board+'/'+topic)
    else:
        if request.method == 'POST':
            print("POST")
            answer.text = request.POST['text']
            answer.save()
            errors.append('Ответ успешно отредактирован')
            return redirect('/'+board+'/'+topic, {'errors': errors})
        else:
            form = Reply(initial={'text': answer.text})

            return thread(request=request,
                          string=board,
                          integer=topic,
                          reply_form=form)

@login_required
@csrf_exempt
def edit_thread(request, board, thread):
    errors = []
    try:
        topic = models.Thread.objects.get(id=thread)
    except models.Thread.DoesNotExist:
        return redirect('/'+board+'/'+thread)
    else:
        if request.method == 'POST':
            topic.text = request.POST['text']
            topic.title = request.POST['title']
            topic.save()
            errors.append('Тред успешно отредактирован')
            return redirect('/'+board+'/'+thread, {'errors': errors})
        else:
            form = CreatingThread(initial={
                'text': topic.text,
                'title': topic.title
            })
            return create_thread(request=request,
                                 string=board,
                                 create_form=form
                                  )

