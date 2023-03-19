from flask import Flask, render_template ,redirect, url_for,request
import requests
import pickle


movies_df = pickle.load(open('movies.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

app = Flask(__name__)



def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=b8d0f958de8242ac18a57db0c313c5c1&language=en-US'
                 .format(movie_id))
    data = response.json()
    print(data)
    return "https://image.tmdb.org/t/p/w500/" + data["poster_path"]



@app.route('/recom/<movie>')
def recom(movie):
    movie_index = movies_df[movies_df['title'] == movie].index[0]
    distance = similarity[movie_index]
    movies_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:20]

    recommended_movies = []
    recommended_movie_posters = []

    for i in movies_list:
            movie_id=movies_df.iloc[i[0]].movie_id
            recommended_movies.append(movies_df.iloc[i[0]].title)
            recommended_movie_posters.append(fetch_poster(movie_id))
    exp={'movies_name':recommended_movies,'movies_poster':recommended_movie_posters}
    return render_template('user_recom_movies.html', output=exp)

movies_lst=movies_df['title']

@app.route('/')
def index():
    # print(movies_lst)
    return render_template('movie.html',new=movies_lst)

@app.route('/movies',methods=['POST'])
def movie():
    if request.method == 'POST':
        # user = (request.form['search movie'])
        user = (request.form['mymovie'])
        return redirect(url_for('recom', movie=user))


if __name__== '__main__':
    app.run(debug=True)
