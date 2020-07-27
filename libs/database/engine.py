from datetime import datetime
from flask import g
from sqlalchemy import create_engine, types, Integer, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('mysql+pymysql://root:22380476@localhost/twolip', pool_recycle=300)
SessionMaker = sessionmaker(bind=engine)


def set_session_destroyer(app):
    '''
    app 설정 단계에서 반드시 한 번 호출해 주어야 합니다.
    이 함수를 호출하지 않았다면 Session() 함수로 인해 생성된 session 연결이
    끊어지지 않고 계속 남아, QueuePool 을 가득 채우게 됩니다. (꽉 차면 더 이상 sql alchemy 못 씀)
    '''
    @app.teardown_appcontext
    def close_session(exc):
        if 'session' in g:
            if g.session_changed is True:
                g.session.commit()
            g.session.close()


def Session(changed=False, committed=False):
    '''
    g 에 등록된 세션을 리턴하는 헬퍼함수
    '''
    if 'session' not in g:
        g.session = SessionMaker()
        g.session_changed = False # session 을 처음 만들때 False 로
    if changed is True:
        g.session_changed = True
    if committed is True:
        g.session_changed = False

    return g.session


def afr(*args):
    '''
    auto add flush return
    '''
    Session(changed=True).add_all(args)
    Session().flush()

    if len(args) == 1:
        return args[0]

    return args

