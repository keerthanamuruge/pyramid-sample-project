import json
import colander
import deform.widget
from pyramid.httpexceptions import HTTPUnauthorized, exception_response, HTTPFound
from pyramid.response import Response
from pyramid.view import view_config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..models.reg import DBSession, Page, Base


class WikiPage(colander.MappingSchema):
    username = colander.SchemaNode(colander.String())
    password = colander.SchemaNode(
        colander.String(),
        widget=deform.widget.RichTextWidget()
    )


@view_config(route_name='home', renderer='string')
def my_view(request):
    return {'project': 'pyramidfull'}


@view_config(route_name='login', renderer='pyramidfull:templates/login.jinja2')
def my_login(request):
    name = request.POST.get('username')
    password = request.POST.get('password')

    if name and password:
        user = DBSession.query(Page).filter(Page.username == name).first()

        if not user:
            return Response("sorry not found")
        else:
            if password == user.password:
                return HTTPFound(location='http://127.0.0.1:6543/')

    return {'login':"Login successfully"}


@view_config(route_name='register', renderer='pyramidfull:templates/register.jinja2')
def my_register(request):
    print("register")
    name = request.POST.get('username')
    password = request.POST.get('password')
    print(name, password)
    model = Page(username=name, password=password)
    DBSession.add(model)
    return {
        'name':None,
        'password':None
    }

@view_config(route_name="unauthorise")
def aview(request):
    # raise HTTPUnauthorized()
    # return HTTPUnauthorized()
    raise exception_response(401)

@view_config(route_name='httpfound')
def myview(request):
    raise HTTPFound(location='https://www.google.com/')

@view_config(route_name='notfound', renderer='pyramidfull:templates/mytemplate.jinja2')
def nview(request):
    request.response.status = '404 Not Found'
    return {'URL': request.URL}