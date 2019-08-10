from . import api
from ..models import User,Post,Permission
from flask import jsonify,request,url_for,current_app


@api.route('/users/<int:id>')
def get_user(id):
    user=User.query.get_or_404(id)
    return jsonify(user.to_json())

@api.route('/users/<int:id>/posts/')
def get_user_posts(id):
    user=User.query.get_or_404(id)
    page=request.args.get('page',1,type=int)
    pagination=Post.query.filter_by(author_id=user.id).order_by(Post.timestamp.desc()).paginate(
        page,per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],error_out=False)
    posts=pagination.items
    prev=None
    if pagination.has_prev:
        prev=url_for('get_user_posts',page=page-1,id=id)
    next=None
    if pagination.has_next:
        next=url_for('get_user_posts',page=page+1,id=id)
    return jsonify({
        'posts':[post.to_json() for post in posts],
        'prev':prev,
        'next':next,
        'count':pagination.total
    })

@api.route('/users/<int:id>/timeline')
def get_user_followed_posts(id):
    user=User.query.get_or_404(id)
    page=request.args.get('page',1,type=int)
    pagination=user.followed_posts.order_by(Post.timestamp.desc()).paginate(page,
        per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],error_out=False)
    posts=pagination.items
    prev=None
    prev=None
    if pagination.has_prev:
        prev=url_for('get_user_followed_posts',page=page-1,id=id)
    next=None
    if pagination.has_next:
        next=url_for('get_user_followed_posts',page=page+1,id=id)
    return jsonify({
        'posts':[post.to_json() for post in posts],
        'prev':prev,
        'next':next,
        'count':pagination.total
    })
