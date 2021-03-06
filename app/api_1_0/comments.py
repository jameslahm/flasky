from flask import current_app,url_for,request,g,jsonify
from ..models import User,Post,Comment
from . import api
from .. import db


@api.route('/comments/')
def get_comments():
    page=request.args.get('page',1,type=int)
    pagination=Comment.query.order_by(Comment.timestamp.desc()).paginate(
        page,per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],error_out=False)
    comments=pagination.items
    prev=None
    if pagination.has_prev:
        prev=url_for('get_comments',page=page-1)
    next=None
    if pagination.has_next:
        next=url_for('get_comments',page=page+1)
    return jsonify({
        'comments':[comment.to_json() for comment in comments],
        'prev':prev,
        'next':next,
        'count':pagination.total
    })

@api.route('/comments/<int:id>')
def get_comment(id):
    comment=Comment.query.get_or_404(id)
    return jsonify(comment.to_json())

@api.route('/posts/<int:id>/comments')
def get_post_comments(id):
    post=Post.query.get_or_404(id)
    page=request.args.get('page',1,type=int)
    pagination=Comment.query.filter_by(post_id=post.id).order_by(Comment.timestamp.desc()).paginate(
        page,per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],error_out=False)
    comments=pagination.items
    prev=None
    if pagination.has_prev:
        prev=url_for('get_post_comments',page=page-1,id=id)
    next=None
    if pagination.has_next:
        next=url_for('get_post_comments',page=page+1,id=id)
    return jsonify({
        'comments':[comment.to_json() for comment in comments],
        'prev':prev,
        'next':next,
        'count':pagination.total
    })

@api.route('/posts/<int:id>/comments/',methods=['POST'])
def new_post_comment(id):
    post=Post.query.get_or_404(id)
    comment=Comment.from_json(request.json)
    comment.author=g.current_user
    comment.post=post
    db.session.add(comment)
    db.session.commit()
    return jsonify(comment.to_json()),201,\
        {'Location':url_for('api.get_comment',id=comment.id)}
