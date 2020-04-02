from sqlalchemy import desc
from sqlalchemy.orm import aliased

from post_service.models import db
from post_service.models.category import Category
from post_service.models.post import Post
from post_service.models.postvote import Postvote


def get_posts_by_user_uuid(user_uuid):
    post_query = aliased(Post, db.session.query(Post)
                         .filter_by(author_uuid=user_uuid)
                         .order_by(desc(Post.pub_date)).subquery())

    post_vote_query = aliased(Postvote, db.session.query(Postvote).
                              filter_by(user_uuid=user_uuid).subquery())

    results = db.session.query(post_query, post_vote_query)\
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
    results = db.session.query(post_query, post_vote_query)\
        .outerjoin(post_vote_query, post_query.post_uuid == post_vote_query.post_uuid).all()

    # Move vote_type attribute from postVote object into post object
    for r in results:
        if r[1] is not None:
            r[0].vote_type = r[1].vote_type
        else:
            r[0].vote_type = None

    result_posts = [r[0] for r in results]
    return result_posts
