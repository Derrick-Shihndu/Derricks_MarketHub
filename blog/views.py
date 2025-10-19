from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from .forms import CommentForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.db.models import Q 

@login_required
def edit_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if comment.author != request.user:
        return HttpResponseForbidden("You are not allowed to edit this comment.")

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=comment.post.pk)
    else:
        form = CommentForm(instance=comment)

    return render(request, 'blog/edit_comment.html', {'form': form, 'comment': comment})

from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from django.contrib.auth.decorators import login_required
@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, id=pk)
    comments = post.comments.filter(parent__isnull=True)

    if request.method == 'POST':
        content = request.POST.get('content')
        parent_id = request.POST.get('parent_id')
        parent_comment = Comment.objects.get(id=parent_id) if parent_id else None

        Comment.objects.create(
            post=post,
            author=request.user,
            content=content,
            parent=parent_comment
        )
        return redirect('blog:post_detail', pk=post.id)

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments
    })
@login_required
def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'blog/post_list.html', {'posts': posts})
@login_required
def post_list(request):
    query = request.GET.get('q')  # Get search query
    if query:
        posts = Post.objects.filter(Q(title__icontains=query)).order_by('-created_at')
    else:
        posts = Post.objects.all().order_by('-created_at')
    
    return render(request, 'blog/post_list.html', {'posts': posts, 'query': query})

@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if comment.author != request.user:
        return HttpResponseForbidden("You are not allowed to delete this comment.")

    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', pk=post_pk)
