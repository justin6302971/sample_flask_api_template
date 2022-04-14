from flask import Blueprint, request, jsonify
import validators
from src.constants.http_status_codes import *
from src.db.database import db, Bookmark
import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity

bookmarks = Blueprint("bookmarks", __name__, url_prefix="/api/v1/bookmarks")


@bookmarks.route('/', methods=['GET', 'POST'], strict_slashes=False)
@jwt_required()
def handle_bookmarks():
    current_user_id = get_jwt_identity()

    if request.method == 'POST':
        body = request.get_json().get('body', '')
        url = request.get_json().get('url', '')

        if not validators.url(url):
            return jsonify({"error": "Enter a valid url"}), HTTP_400_BAD_REQUEST

        bookmark = Bookmark.query.filter_by(url=url).first()
        if bookmark:
            return jsonify({"error": "Url already exists"}), HTTP_409_CONFLICT

        new_bookmark = Bookmark(url=url, body=body, user_id=current_user_id)
        db.session.add(new_bookmark)
        db.session.commit()

        return jsonify({"isSuccess": True,
                        "data": [
                            {
                                'id': new_bookmark.id,
                                'url': url,
                                'body': body,
                                'short_url': new_bookmark.short_url,
                                'visits': new_bookmark.visits,
                                'created_at': new_bookmark.created_at,
                                'modified_at': new_bookmark.modified_at,
                            }
                        ]
                        }), HTTP_201_CREATED
    else:

        page = request.args.get('page', 1, type=int)
        size = request.args.get('size', 5, type=int)

        bookmarks = Bookmark.query.filter_by(user_id=current_user_id).order_by(
            Bookmark.modified_at.desc()).paginate(page=page, per_page=size)

        data = []
        for bookmark in bookmarks.items:
            data.append({
                'id': bookmark.id,
                'url': bookmark.url,
                'body': bookmark.body,
                'short_url': bookmark.short_url,
                'visits': bookmark.visits,
                'created_at': bookmark.created_at,
                'modified_at': bookmark.modified_at,
            })

        meta = {
            "page": bookmarks.page,
            "pages": bookmarks.pages,
            "total_count": bookmarks.total,
            "prev_page": bookmarks.prev_num,
            "next_page": bookmarks.next_num,
            "has_next": bookmarks.has_next,
            "has_prev": bookmarks.has_prev,
        }

        return jsonify({"isSuccess": True,
                        "data": data,
                        "meta": meta
                        }), HTTP_200_OK


@bookmarks.get("/<int:id>")
@jwt_required()
def get_bookmark(id):
    current_user_id = get_jwt_identity()

    bookmark = Bookmark.query.filter_by(user_id=current_user_id, id=id).first()
    if not bookmark:
        return jsonify({"error": "Item not found"}), HTTP_404_NOT_FOUND

    return jsonify({"isSuccess": True,
                    "data": {
                        'id': bookmark.id,
                        'url': bookmark.url,
                        'body': bookmark.body,
                        'short_url': bookmark.short_url,
                        'visits': bookmark.visits,
                        'created_at': bookmark.created_at,
                        'modified_at': bookmark.modified_at,
                    }}), HTTP_200_OK


@bookmarks.put("/<int:id>")
@bookmarks.patch("/<int:id>")
@jwt_required()
def edit_bookmark(id):
    current_user_id = get_jwt_identity()

    bookmark = Bookmark.query.filter_by(user_id=current_user_id, id=id).first()
    if not bookmark:
        return jsonify({"error": "Item not found"}), HTTP_404_NOT_FOUND

    body = request.get_json().get('body', '')
    url = request.get_json().get('url', '')

    if not validators.url(url):
        return jsonify({"error": "Enter a valid url"}), HTTP_400_BAD_REQUEST

    bookmark.url = url

    if body:
        bookmark.body = body

    bookmark.modified_at = datetime.datetime.now()

    db.session.commit()

    return jsonify({"isSuccess": True,
                    "data": {
                        'id': bookmark.id,
                        'url': bookmark.url,
                        'body': bookmark.body,
                        'short_url': bookmark.short_url,
                        'visits': bookmark.visits,
                        'created_at': bookmark.created_at,
                        'modified_at': bookmark.modified_at,
                    }}), HTTP_200_OK


@bookmarks.delete("/<int:id>")
@jwt_required()
def delete_bookmark(id):
    current_user_id = get_jwt_identity()

    bookmark = Bookmark.query.filter_by(user_id=current_user_id, id=id).first()
    if not bookmark:
        return jsonify({"error": "Item not found"}), HTTP_404_NOT_FOUND
   
    db.session.delete(bookmark)
    db.session.commit()
    return jsonify({}),HTTP_204_NO_CONTENT