from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_width
from flask_sqlalchemy import SQLAlchemy

# db migrations
# flask_restful, SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config('SQLALCHEMY_DATABASE_URI') = 'sqlite:///database.db'
db = SQLAlchemy(app)

class VideoModel(db.Model)
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), nullable=False)
  views = db.Column(db.Integer)
  likes = db.Column(db.Integer)

  def __repr__(self):
    return f"Video(name = {name}, views = {views}), likes = {likes})"

# db.create_all(db.Model):

videos_put_args = reqparse.RequestParser()
videos_put_args.add_argument("name", type=str, help="Name of the video is required", required=True)
videos_put_args.add_argument("views", type=int, help="Views of the video is required", required=True)
videos_put_args.add_argument("likes", type=int, help="Likes on the video is required", required=True)

video_update_args = reqparse.RequestParser()
videos_update_args.add_argument("name", type=str)
videos_update_args.add_argument("views", type=int)
videos_update_args.add_argument("likes", type=int)

resource_fields = {
  'id': fields.Integer,
  'name': fields.String,
  'views': fields.Integer,
  'likes': fields.Integer,
}

class Video(Resource):
  @marshal_width(resource_fields)
  def get(self, video_id):
    result = VideoModel.query.filter_by(id=video_id).first
    if not result:
      abort(404, 'Could not find video.')
    return result

  @marshal_width(resource_fields)
  def put(self, video_id):
    args = videos_put_args.parse_args()
    result = VideoModel.query.filter_by(id=video_id).first
    if result:
      abort(409, message="Video id taken.")
    video = VideoModel(id=video_id, name=args['name'], views=args['views'], likes=args['likes'])
    db.session.add(video)
    db.session.commit()
    return video, 201

  @marshal_width(resource_fields)
  def patch(self, video_id):
    args = videos_update_args.parse_args()
    result = VideoModel.query.filter_by(id=video_id).first
    if not result:
      abort(404, "Video doesn't exist.")

    if args['name']:
      result.name = args['name']
    if args['views']:
      result.views = args['views']
    if args['likes']:
      result.likes = args['likes']

    db.session.add(result)
    db.session.commit()

    return result  

  def delete(self, video_id):
    abort_if_video_id_doesnt_exist(video_id)
    del videos[video_id]
    return '', 204


api.add_resource(Video, "/videos/<int:video_id>")

if __name__ == "__main__":
  app.run(debug=True)