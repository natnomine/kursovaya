from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Max
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.edit import ModelFormMixin

from messenger.forms import ChatForm, ImageUploadForm
from messenger.models import UserProfile, Chat, Message


def upload_avatar(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            user = UserProfile.objects.get(user__username=request.user.username)
            user.avatar = form.cleaned_data['image']
            user.save()
            return redirect('profile', request.user.username)
    return HttpResponseForbidden('allowed only via POST')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            UserProfile.objects.create(
                user=user
            )
            login(request, user)
            return redirect('friends')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


class ProfileView(LoginRequiredMixin, DetailView):
    model = UserProfile
    template_name = "profile.html"
    slug_url_kwarg = "username"
    slug_field = "user__username"

    def post(self, request, *args, **kwargs):
        action = request.POST['action']
        user_profile = self.get_object()
        current_user = self.request.user.profile
        if action == "Добавить в друзья":
            user_profile.friends.add(current_user)
            current_user.friends.add(user_profile)
            return HttpResponseRedirect(self.request.path_info)
        elif action == "Написать сообщение":
            chat = Chat.objects.filter(members=user_profile.id, is_private=True).filter(members=current_user.id).first()
            if not chat:
                chat = Chat.objects.create(is_private=True, name="Личная переписка")
                chat.members.add(user_profile, current_user)
            return redirect('chats-detailed', chat.id)


class FriendsView(LoginRequiredMixin, ListView):
    template_name = 'friends.html'

    def get_queryset(self):
        return self.request.user.profile.friends.all()


class AddFriendsView(LoginRequiredMixin, ListView):
    template_name = 'add_friends.html'

    def get_queryset(self):
        user = self.request.user.profile
        friends_ids = user.friends.values_list('id')
        return UserProfile.objects.exclude(id__in=friends_ids).exclude(id=user.id)


class ChatsView(LoginRequiredMixin, ListView):
    model = Chat
    template_name = "chats.html"

    def get_queryset(self):
        chats = super().get_queryset()
        chats = chats.filter(members=self.request.user.profile.id)
        return chats.annotate(send_at=Max('messages__send_at')).order_by("-send_at")


class AddChatsView(LoginRequiredMixin, CreateView):
    template_name = "chat_add.html"
    model = Chat
    form_class = ChatForm

    def get_form_kwargs(self):
        kw = super().get_form_kwargs()
        kw['friends'] = self.request.user.profile.friends.values_list("id", flat=True)
        return kw

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        members = list(form.cleaned_data["members"].values_list("id", flat=True))
        members.append(self.request.user.profile.id)
        Chat.objects.get(id=self.object.id).members.add(*members)
        return super(ModelFormMixin, self).form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse_lazy('chats-detailed', kwargs={"pk": self.object.id})


class ChatDetailView(LoginRequiredMixin, DetailView):
    model = Chat
    slug_field = "pk"
    template_name = "chat_detail.html"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if self.request.user.profile.id not in obj.members.values_list('id', flat=True):
            raise PermissionDenied
        return obj

    def post(self, request, *args, **kwargs):
        message = request.POST["message"]
        Message.objects.create(
            text=message,
            sender=request.user.profile,
            chat=Chat.objects.get(id=kwargs["pk"])
        )
        return HttpResponseRedirect(self.request.path_info)
