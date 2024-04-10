from flask import Flask, request,jsonify, send_from_directory
from flask_restful import Resource, Api
from sqlalchemy import Column, Integer, Text, Float, DateTime, create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.expression import func, or_
from flask_restful import Resource, Api
from dataclasses import dataclass
import json

Base = declarative_base()  # Basisklasse aller in SQLAlchemy verwendeten Klassen
metadata = Base.metadata

engine = create_engine('sqlite:///flask_fotoserver/data/binary.sqlite3') #Welche Datenbank wird verwendet
db_session = scoped_session(sessionmaker(autoflush=True, bind=engine))
Base.query = db_session.query_property() #Dadurch hat jedes Base - Objekt (also auch ein GeoInfo) ein Attribut query für Abfragen
app = Flask(__name__) #Die Flask-Anwendung
api = Api(app) #Die Flask API

@dataclass #Diese ermoeglicht das Schreiben als JSON mit jsonify
class BinaryWithMetadata(Base):
    __tablename__ = 'binary_with_metadata'  # Abbildung auf diese Tabelle
    id: int
    name: str
    ext: str
    data: str
    desc : str
    when: str

    id = Column(Integer, primary_key=True)
    name = Column(Text)
    ext = Column(Text)
    data = Column(Text)
    desc = Column(Text)
    when = Column(DateTime, default=func.now())

class BinaryWithMetadataREST(Resource):
    def get(self, id):
        infos = BinaryWithMetadata.query.get(id)
        return jsonify(infos)

    def put(self,id):
        d = request.get_json(force=True)
        info = BinaryWithMetadata(id=id, name=d['name'], ext=d['ext'], data=d['data'], desc=d['desc'])
        db_session.add(info)
        db_session.commit()
        return 'saved'
    def delete (self, id):
        db_session.delete(BinaryWithMetadata.query.get(id))
        db_session.commit()
        return 'deleted'
    
api.add_resource(BinaryWithMetadataREST, '/img_meta/<int:id>')


class MetdataSearchREST(Resource):
    def get(self, str):
        infos = BinaryWithMetadata.query.filter(or_(BinaryWithMetadata.desc.contains(str), BinaryWithMetadata.name.contains(str))).all()
        print(infos)
        return jsonify(infos)

api.add_resource(MetdataSearchREST, '/img_meta/search/<string:str>')




@app.teardown_appcontext
def shutdown_session(exception=None):
    print("Shutdown Session")
    db_session.remove()

def init_db():
    # Erzeugen der Tabellen für die Klassen, die oben deklariert sind (muss nicht sein, wenn diese schon existiert)
    Base.metadata.create_all(bind=engine)

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port="5000")