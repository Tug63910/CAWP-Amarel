import os
import subprocess
import csv
from flask import (
	Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from CAWPr.auth import login_required
from CAWPr.db import get_db
from CAWPr.models.predict import classifier

bp=Blueprint('application',__name__)

@bp.route('/')
def index():
	db=get_db()
	posts=db.execute(
		'SELECT p.id, url, state, level, office, profession, created'
		' FROM post p'
		' ORDER BY created ASC'
	).fetchall()
	return render_template('application/index.html',posts=posts)


@bp.route('/create', methods=('GET','POST'))
@login_required
def create():
	if request.method=='POST':
		url=request.form['url']
		error=None

		if not url:
			error='Url required'

		if error is not None:
			flash(error)
		else:
			db=get_db()
			#use scrapy for text, stored in temp.cvs
			CAWPwd=os.path.join(os.getcwd(),"CAWPr/CAWPspider")
			subprocess.run(["scrapy","crawl","-a","url="+url,"candidate"],cwd=CAWPwd)
			#concatenate text in temp.cvs to get site text.
			with open(os.path.join(os.getcwd(),"CAWPr/CAWPspider/temp.csv"),'rt') as fin:
				cin=csv.DictReader(fin)
				site_data=[row['text'] for row in cin]
			text='::'.join(site_data)
			entry=classifier(text)
			db.execute(
				'INSERT INTO post (url, state, level, office, profession,text)'
				' VALUES (?,?,?,?,?,?)',
				(url,entry['state'],entry['level'],entry['office'],entry['profession'], entry['text'])
			)
			db.commit()
			return redirect(url_for('application.index'))

	return render_template('application/create.html')

def get_post(id):
	post=get_db().execute(
		'SELECT p.id, url, state, level, office, profession, text'
		' FROM post p'
		' WHERE p.id=?',
		(id,)
	).fetchone()

	if post is None:
		abort(404,"Post id {0} doesn't exist.".format(id))

	return post

@bp.route('/<int:id>/update', methods=('GET','POST'))
@login_required
def update(id):
	post=get_post(id)

	if request.method=='POST':
		url=post['url']
		state=request.form['state']
		level=request.form['level']
		office=request.form['office']
		profession=request.form['profession']
		text=request.form["text"]
		error=None

		if not url:
			error='Url required'
	
		if error is not None:
			flash(error)
		else:
			db=get_db()
			db.execute(
				'UPDATE post SET url=?, state=?, level=?, office=?, profession=?, text=?'
				' WHERE id=?',
				(url,state,level,office,profession,text,id)
			)
			db.commit()
			return redirect(url_for('application.index'))

	return render_template('application/update.html',post=post)
	
@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
	get_post(id)
	db=get_db()
	db.execute('DELETE FROM post WHERE id=?', (id,))
	db.commit()
	return redirect(url_for('application.index'))

