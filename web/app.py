import os, datetime
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from sqlalchemy import create_engine, Column, Integer, String, Float, Text
from sqlalchemy.orm import sessionmaker, declarative_base

DB_PATH = os.environ.get("DB_PATH", "/db/events.db")

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

engine = create_engine(f"sqlite:///{DB_PATH}", echo=False, future=True)
Session = sessionmaker(bind=engine, future=True)
Base = declarative_base()

class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    source = Column(String(32))
    event_type = Column(String(32))
    attack_id = Column(String(64))
    target = Column(String(128))
    timestamp = Column(Float)
    details = Column(Text)

Base.metadata.create_all(engine)

@app.route('/')
def dashboard():
    with Session() as s:
        events = s.query(Event).order_by(Event.timestamp.desc()).limit(200).all()
    return render_template('dashboard.html', events=events)

@app.route('/api/health')
def health():
    return {"status": "ok", "time": datetime.datetime.utcnow().isoformat()}

@app.route('/api/event', methods=['POST'])
def receive_event():
    data = request.get_json(force=True) or {}
    e = Event(
        source=data.get('source', 'unknown'),
        event_type=data.get('event_type', 'event'),
        attack_id=data.get('attack_id', ''),
        target=data.get('target', ''),
        timestamp=float(data.get('timestamp', datetime.datetime.now().timestamp())),
        details=data.get('details', '')
    )
    with Session() as s:
        s.add(e)
        s.commit()
        socketio.emit('new_event', {
            'id': e.id,
            'source': e.source,
            'event_type': e.event_type,
            'attack_id': e.attack_id,
            'target': e.target,
            'timestamp': e.timestamp,
            'details': e.details
        })
    return jsonify({'status': 'ok', 'id': e.id})

@app.route('/api/correlations')
def get_correlations():
    # naive correlation: match attack_id + target, compute latency
    with Session() as s:
        reds = s.query(Event).filter(Event.source=='redbox').all()
        blues = s.query(Event).filter(Event.source=='bluebox').all()
    corrs = []
    for r in reds:
        best = None
        for b in blues:
            if r.attack_id == b.attack_id and r.target == b.target:
                dt = abs(b.timestamp - r.timestamp)
                if best is None or dt < best['latency']:
                    best = {
                        'attack_id': r.attack_id,
                        'target': r.target,
                        'attack_time': r.timestamp,
                        'detection_time': b.timestamp,
                        'latency': dt,
                        'attack_details': r.details,
                        'detection_details': b.details
                    }
        if best: corrs.append(best)
    return jsonify(corrs)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
