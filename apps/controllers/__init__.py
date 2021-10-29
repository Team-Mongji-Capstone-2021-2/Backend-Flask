# -*- coding: utf-8 -*-
from flask import Flask, render_template

def page_not_found(e):
    return render_template('error/404.html'), 404