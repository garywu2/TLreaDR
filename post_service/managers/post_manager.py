from datetime import datetime

import requests
from flask_restplus import marshal
from sqlalchemy import desc
from sqlalchemy.orm import aliased

from post_service.api.models import post_dto
from post_service.models import db
from post_service.models.category import Category
from post_service.models.post import Post
from post_service.models.postvote import Postvote


def get_posts_by_category(category, user_uuid):
    post_query = db.session.query(Post)

    # Filter by category unless all is specified
    if category != 'all':
        queried_category = Category.query.filter_by(name=category).first()
        post_query = post_query.filter_by(category_uuid=queried_category.category_uuid)

    # Order posts by new, then by votes, then by publish date
    post_query = aliased(Post, post_query.
                         order_by(desc(Post.new_flag), desc(Post.votes), desc(Post.pub_date)).subquery())

    # Filter post votes to only those made by the user
    post_vote_query = aliased(Postvote, db.session.query(Postvote).filter_by(user_uuid=user_uuid).subquery())

    # Outer join posts and post votes
    results = db.session.query(post_query, post_vote_query) \
        .outerjoin(post_vote_query, post_query.post_uuid == post_vote_query.post_uuid).all()

    # Move vote_type attribute from postVote object into post object
    for r in results:
        if r[1] is not None:
            r[0].vote_type = r[1].vote_type
        else:
            r[0].vote_type = None

    result_posts = [r[0] for r in results]
    return result_posts


def get_posts_by_user_uuid(user_uuid):
    post_query = aliased(Post, db.session.query(Post)
                         .filter_by(author_uuid=user_uuid)
                         .order_by(desc(Post.pub_date)).subquery())

    post_vote_query = aliased(Postvote, db.session.query(Postvote).
                              filter_by(user_uuid=user_uuid).subquery())

    results = db.session.query(post_query, post_vote_query) \
        .outerjoin(post_vote_query, post_query.post_uuid == post_vote_query.post_uuid).all()

    for r in results:
        if r[1] is not None:
            r[0].vote_type = r[1].vote_type
        else:
            r[0].vote_type = None

    result_posts = [r[0] for r in results]
    return result_posts


def get_post_by_post_uuid(post_uuid, user_uuid):
    post_query = aliased(Post, db.session.query(Post).filter_by(post_uuid=post_uuid).subquery())
    post_vote_query = aliased(Postvote, db.session.query(Postvote).filter_by(user_uuid=user_uuid).subquery())
    result = db.session.query(post_query, post_vote_query) \
        .outerjoin(post_vote_query, post_query.post_uuid == post_vote_query.post_uuid).first()

    if result[1] is not None:
        result[0].vote_type = result[1].vote_type
    else:
        result[0].vote_type = None

    return result[0]


def add_post(category, args):
    queried_category = Category.query.filter_by(name=category).first()
    if queried_category is None:
        return {"message": "category not found."}, 201

    new_post = Post(args['title'], args['body'], queried_category.category_uuid, args['author_uuid'],
                    args['image_link'], args['article_link'])
    db.session.add(new_post)
    db.session.commit()

    return marshal(new_post, post_dto), 200


def edit_post(post_uuid, args):
    post_to_be_edited = Post.query.filter_by(post_uuid=post_uuid).first()

    if post_to_be_edited:
        if args['new_title']:
            post_to_be_edited.title = args['new_title']
        if args['new_body']:
            post_to_be_edited.body = args['new_body']
        if args['new_image_link']:
            post_to_be_edited.image_link = args['new_image_link']
        if args['new_article_link']:
            post_to_be_edited.article_link = args['new_article_link']

        post_to_be_edited.edited_date = datetime.utcnow()
        post_to_be_edited.edited_flag = True
    else:
        return {'message': 'post specified not found in database'}, 404

    db.session.commit()


def delete_post(post_uuid):
    post_to_be_deleted = Post.query.filter_by(post_uuid=post_uuid).first()
    if post_to_be_deleted:
        # Delete all comments related to post
        response = requests.delete('http://comment_service:7082/api/comments/post/' + str(post_uuid))
        if response.status_code != 200:
            return {'message': 'error deleting posts comments'}, response.status_code

        # Delete all votes related to post
        votes_to_be_deleted = Postvote.query.filter_by(post_uuid=post_uuid).all()
        for vote in votes_to_be_deleted:
            db.session.delete(vote)
        db.session.delete(post_to_be_deleted)
        db.session.commit()
        return {'message': 'post has been deleted successfully.'}, 200
    return {'message': 'post not found.'}, 404


def add_post_vote(post_uuid, args):
    """
    Adds a vote on a post by a user to the post vote table.

    If a post has -20 or less votes the post will be removed.

    :param post_uuid: the post uuid of the post being voted on
    :param args: the arguments provided in the HTTP request
    """
    new_post_vote = Postvote(post_uuid, args['user_uuid'], args['vote_type'])
    post_voted_on = Post.query.filter_by(post_uuid=post_uuid).first()
    post_voted_on.assign_vote(args['vote_type'])

    if post_voted_on.votes <= -20:
        db.session.delete(post_voted_on)
        db.session.commit()
    else:
        db.session.add(new_post_vote)

    db.session.commit()


def edit_post_vote(post_uuid, args):
    """
    Edits a user's vote on a post.

    If a post has -20 or less votes the post will be removed.

    :param post_uuid: the post uuid of the post being voted on
    :param args: the arguments provided in the HTTP request
    """
    user_uuid = args['user_uuid']
    new_vote_type = args['new_vote_type']
    post_to_be_edited = Post.query.filter_by(post_uuid=post_uuid).first()
    vote_to_be_edited = Postvote.query.filter_by(post_uuid=post_uuid) \
        .filter_by(user_uuid=user_uuid).first()

    if vote_to_be_edited and post_to_be_edited:
        if vote_to_be_edited.vote_type == new_vote_type:
            return {'message': 'cannot vote twice on the same post'}, 404
        vote_to_be_edited.vote_type = new_vote_type
        post_to_be_edited.assign_vote(2 * new_vote_type)
        if post_to_be_edited.votes <= -20:
            db.session.delete(post_to_be_edited)
        else:
            db.session.add(post_to_be_edited)
        db.session.commit()
        return {'message': 'vote has been edited successfully.'}, 201
    return {'message': 'vote or post not found.'}, 404


def delete_post_vote(post_uuid, args):
    user_uuid = args['user_uuid']
    post_to_be_edited = Post.query.filter_by(post_uuid=post_uuid).first()
    vote_to_be_deleted = Postvote.query.filter_by(post_uuid=post_uuid) \
        .filter_by(user_uuid=user_uuid).first()
    post_to_be_edited.delete_vote(vote_to_be_deleted.vote_type)
    db.session.delete(vote_to_be_deleted)
    db.session.commit()

def delete_posts_with_same_article_link():
    pass