from flask import render_template, request, redirect, url_for
from blog import app
from blog.models import Entry, db
from blog.forms import EntryForm

def create_or_edit_entry(entry_id, entry, form):
    errors = None
    if request.method == 'POST':
        if form.validate_on_submit() and entry_id:
            form.populate_obj(entry)
            db.session.commit()
            return redirect(url_for('homepage'))
        elif form.validate_on_submit():
            db.session.add(entry)
            db.session.commit()
        else:
            errors = form.errors
    return render_template(
        "entry_form.html", form=form, errors=errors, entry_id=entry_id)


@app.route("/")
def index():
   all_posts = Entry.query.filter_by(is_published=True).order_by(Entry.pub_date.desc())
   return render_template("homepage.html", all_posts=all_posts)


@app.route("/create", methods=['GET', 'POST'])
def create_entry():
    form = EntryForm()
    entry_id = None
    entry = Entry(
        title=form.title.data,
        body=form.body.data,
        is_published=form.is_published.data
        )
    return create_or_edit_entry(entry_id, entry, form)


@app.route("/edit-post/<int:entry_id>", methods=['GET', 'POST'])
def edit_entry(entry_id):
    entry = Entry.query.filter_by(id=entry_id).first_or_404()
    form = EntryForm(obj=entry)
    return create_or_edit_entry(entry_id, entry, form)
