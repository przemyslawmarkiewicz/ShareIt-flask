from py2neo import Graph, Node, Relationship
from py2neo.matching import NodeMatcher
from passlib.hash import bcrypt
from datetime import datetime
import os
from config import database_uri

url = os.environ.get('GRAPHENEDB_URL')
graph = Graph(url + '/db/data/', username=os.environ.get("NEO4J_USERNAME"), password=os.environ.get("NEO4J_PASSWORD"))
matcher = NodeMatcher(graph)


class User:
    def __init__(self, username):
        self.username = username

    def find(self):
        user = matcher.match('ShareItUser', username= self.username).first()
        return user

    def register(self, password):
        if not self.find():
            user = Node('ShareItUser', username=self.username, password=bcrypt.encrypt(password), num_of_posts=0)
            print(user)
            graph.create(user)
            return True
        else:
            return False

    def verify_password(self, password):
        user = self.find()
        if user:
            return bcrypt.verify(password, user['password'])
        else:
            return False

    def add_post(self, title, tags, text):
        user = matcher.match('ShareItUser', username=self.username).first()
        post = Node(
            'ShareItPost',
            id=str(uuid.uuid4()),
            title=title,
            text=text,
            timestamp=timestamp(),
            likes=0,
            date=date()
        )
        rel = Relationship(user, 'PUBLISHED', post)
        graph.create(rel)


        tags = [x.strip() for x in tags.lower().split(',')]
        for name in set(tags):
            tag = Node('Tag', name=name)
            tag.__primarylabel__ = "Tag"
            tag.__primarykey__ = "name"
            graph.merge(tag)

            rel = Relationship(tag, 'TAGGED', post)
            graph.create(rel)

    def like_post(self, post_id):
        user = self.find()
        post = matcher.match('ShareItPost', id=post_id).first()
        query = """
        MATCH (post:ShareItPost {id:$id})
        SET post.likes = post.likes + 1
        """
        graph.run(query, id=post_id)
        graph.merge(Relationship(user, 'LIKED', post))

    def get_num_of_posts(self):
        query = """
        MATCH (u:ShareItUser {username:$username})-[r:PUBLISHED]->(p:ShareItPost)
        RETURN count(p) as num_of_posts;
        """

        result =  graph.run(query, username=self.username).to_table()
        return result[0][0]

    def get_recent_posts(self):
        query = '''
        MATCH (user:ShareItUser)-[:PUBLISHED]->(post:ShareItPost)<-[:TAGGED]-(tag:Tag)
        WHERE user.username = $username
        RETURN post, COLLECT(tag.name) AS tags
        ORDER BY post.timestamp DESC LIMIT 10
        '''

        return graph.run(query, username=self.username)

    def get_similar_users(self):
        query = '''
        MATCH (you:ShareItUser)-[:PUBLISHED]->(:ShareItPost)<-[:TAGGED]-(tag:Tag),
              (they:ShareItUser)-[:PUBLISHED]->(:ShareItPost)<-[:TAGGED]-(tag)
        WHERE you.username = $username AND you <> they
        WITH they, COLLECT(DISTINCT tag.name) AS tags
        ORDER BY SIZE(tags) DESC LIMIT 3
        RETURN they.username AS similar_user, tags
        '''

        return graph.run(query, username=self.username)


def get_todays_recent_posts():
    query = '''
    MATCH (user:ShareItUser)-[:PUBLISHED]->(post:ShareItPost)<-[:TAGGED]-(tag:Tag)
    WHERE post.date = $today
    RETURN user.username AS username, post, COLLECT(tag.name) AS tags
    ORDER BY post.timestamp DESC LIMIT 5
    '''

    return graph.run(query, today=date())

def timestamp():
    epoch = datetime.utcfromtimestamp(0)
    now = datetime.now()
    delta = now - epoch
    return delta.total_seconds()

def date():
    return datetime.now().strftime('%Y-%m-%d')