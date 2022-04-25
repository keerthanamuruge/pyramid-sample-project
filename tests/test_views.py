from pyramidfull.views.default import my_view
from pyramidfull.views.notfound import notfound_view
import transaction


def _initTestingDB():
    from sqlalchemy import create_engine
    from pyramidfull.models.reg import (
        DBSession,
        Page,
        Base
        )
    engine = create_engine('postgresql://postgres:postgres@localhost:5432/pyramiddatabase')
    Base.metadata.create_all(engine)
    DBSession.configure(bind=engine)
    with transaction.manager:
        model = Page(username='Backend', password='frontpage')
        DBSession.add(model)
    return DBSession

_initTestingDB()


def test_my_view(app_request):
    info = my_view(app_request)
    assert app_request.response.status_int == 200
    assert info['project'] == 'pyramidfull'

def test_notfound_view(app_request):
    info = notfound_view(app_request)
    assert app_request.response.status_int == 404
    assert info == {}
