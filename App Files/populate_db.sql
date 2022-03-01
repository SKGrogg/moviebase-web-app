
-- Data for Name: movies; Type: TABLE DATA; Schema:  Owner: Sean Grogg
--
--movies(movie_name, year_released, budget, gross, genre, studio_id, country_id, director_id)

INSERT INTO movies (movie_name, year_released, budget, gross, genre) VALUES ('Tommy Boy', 1995, 20000000, 30700000, "Comedy");
INSERT INTO movies (movie_name, year_released, budget, gross, genre) VALUES ('Gladiator', 2000, 103000000, 465380802, "Action");
INSERT INTO movies (movie_name, year_released, budget, gross, genre) VALUES ('Jumanji', 1995, 65000000, 262841920, "Adventure");
INSERT INTO movies (movie_name, year_released, budget, gross, genre) VALUES ('Catch Me If You Can', 2002, 52000000, 352114312, "Crime");
INSERT INTO movies (movie_name, year_released, budget, gross, genre) VALUES ('Django Unchained', 2012, 100000000, 426074373, "Western");
INSERT INTO movies (movie_name, year_released, budget, gross, genre) VALUES ('Pineapple Express', 2008, 27000000, 101624843, "Comedy");
INSERT INTO movies (movie_name, year_released, budget, gross, genre) VALUES ('Les Intouchable', 2011, 10000000, 426588510, "Comedy");
INSERT INTO movies (movie_name, year_released, budget, gross, genre) VALUES ('Roma', 2018, 15000000, 5100000, "Drama");
INSERT INTO movies (movie_name, year_released, budget, gross, genre) VALUES ("Pan's Labyrinth", 2018, 19000000, 83850267, "Fantasy");
INSERT INTO movies (movie_name, year_released, budget, gross, genre) VALUES ('Zodiac', 2007, 65000000, 84785914, "Crime");
INSERT INTO movies (movie_name, year_released, budget, gross, genre) VALUES ('Marriage Story', 2019, 13000000, 330000, "Romance");
INSERT INTO movies (movie_name, year_released, budget, gross, genre) VALUES ('Titanic', 1997, 200000000, 2200000000, "Romance");
INSERT INTO movies (movie_name, year_released, budget, gross, genre) VALUES ('Inception', 2010, 168000000, 836836967, "Sci-Fi");
INSERT INTO movies (movie_name, year_released, budget, gross, genre) VALUES ('Cloudy With A Chance of Meatballs', 2009, 100000000, 243006126, "Comedy");
INSERT INTO movies (movie_name, year_released, budget, gross, genre) VALUES ('Step Brothers', 2008, 65000000, 128108211, "Comedy");
INSERT INTO movies (movie_name, year_released, budget, gross, genre) VALUES ('Ghost', 1990, 22000000, 505703557, "Romance");
INSERT INTO movies (movie_name, year_released, budget, gross, genre) VALUES ('Mars Attacks!', 1996, 70000000, 101371017, "Sci-Fi");
INSERT INTO movies (movie_name, year_released, budget, gross, genre) VALUES ('The Ballad of Buster Scruggs', 2018, NULL, NULL, "Western");
INSERT INTO movies (movie_name, year_released, budget, gross, genre) VALUES ('Hubie Halloween', 2020, NULL, NULL, "Comedy");
INSERT INTO movies (movie_name, year_released, budget, gross, genre) VALUES ("A Knight's Tale", 2001, 65000000, 117487473, "Adventure");
INSERT INTO movies (movie_name, year_released, budget, gross, genre) VALUES ("The Artist", 2011, 15000000, 133432856, "Comedy");
INSERT INTO movies (movie_name, year_released, budget, gross, genre) VALUES ("Million Dollar Baby", 2004, 30000000, 216763646, "Sports");
INSERT INTO movies (movie_name, year_released, budget, gross, genre) VALUES ("Dune", 2021, 175000000, 400000000, "Sci-Fi");
INSERT INTO movies (movie_name, year_released, budget, gross, genre) VALUES ("The Green Knight", 2021, 15000000, 18900000, "Adventure");




--
-- Data for Name: reviews; Type: TABLE DATA; Schema:  Owner: Sean Grogg
--
--reviews(review_id, review_text, movie_id, critic_id)

INSERT INTO reviews (review_text, movie_id, critic_id) VALUES ("Stupid is apparently in.", 1, 1);
INSERT INTO reviews (review_text, movie_id, critic_id) VALUES ("Tommy Boy is a good belly laugh of a movie.", 1, 2);
INSERT INTO reviews (review_text, movie_id, critic_id) VALUES ("The most peculiar aspect of the movie is that some of it is played straight.", 1, 3);
INSERT INTO reviews (review_text, movie_id, critic_id) VALUES ("Russell Crowe solidly anchors this epic-scale gladiator movie - the first in nearly four decades - by using his burly frame and expressive face to give dimension to what might otherwise have been comic book heroics.", 2, 4);
INSERT INTO reviews (review_text, movie_id, critic_id) VALUES ("The most peculiar aspect of the movie is that some of it is played straight.", 2, 5);
INSERT INTO reviews (review_text, movie_id, critic_id) VALUES ("Rather than getting lost in the world Scott has created on screen, Scott asks filmgoers to marvel at how he created that world, and how smoothly he succeeds in manipulating us.", 2, 6);
INSERT INTO reviews (review_text, movie_id, critic_id) VALUES ("A gloomy special-effects extravaganza filled with grotesque images, generating fear and despair.", 3, 7);
INSERT INTO reviews (review_text, movie_id, critic_id) VALUES ("Take away the CGI mayhem and what emerges is a rather touching tale of second chances and innocence prematurely lost.", 3, 8);
INSERT INTO reviews (review_text, movie_id, critic_id) VALUES ("The humans are wooden, the computer-animals have that floating, jerky gait of animated fauna.", 3, 9);
INSERT INTO reviews (review_text, movie_id, critic_id) VALUES ("Hanratty isn't a strictly factual character - he's called O'Reilly in the book, not his real name either - but the performance Hanks gives makes you wish he were. Abagnale isn't strictly factual either, but DiCaprio makes him an attractive counterfeit.", 4, 9);
INSERT INTO reviews (review_text, movie_id, critic_id) VALUES ("Excellent account of FBI's youngest Most Wanted.", 4, 10);
INSERT INTO reviews (review_text, movie_id, critic_id) VALUES ("This is a delectable film indeed.", 4, 11);
INSERT INTO reviews (review_text, movie_id, critic_id) VALUES ("Vibrating with the geekery of a filmmaker off the chain, the movie plays like no other this year.", 5, 12);
INSERT INTO reviews (review_text, movie_id, critic_id) VALUES ("An immensely satisfying taste of antebellum empowerment packaged as spaghetti-Western homage.", 5, 13);
INSERT INTO reviews (review_text, movie_id, critic_id) VALUES ("Whatever Django's issues, failing to deliver on its promises isn't one of them.", 5, 14);
INSERT INTO reviews (review_text, movie_id, critic_id) VALUES ("But there's still time for a gloriously unexpected coda, a moment of quiet reflection and narrative ingenuity that confirms 'Pineapple Express' as the finest comedy of the year.", 6, 15);
INSERT INTO reviews (review_text, movie_id, critic_id) VALUES ("Watching Pineapple Express is like sitting dead sober in a room with a bunch of stoned people who are laughing uproariously. They're having a great time. You're not.", 6, 16);
INSERT INTO reviews (review_text, movie_id, critic_id) VALUES ("It's not subtle. It's not innovative. But it guarantees good humour, pranks, japes and welling-up for two hours.", 7, 17);
INSERT INTO reviews (review_text, movie_id, critic_id) VALUES ("It is the clarity of Cuarón's eye, and the sea-like sway of his remembrance, that compel you to trust the tale he tells.", 8, 17);
INSERT INTO reviews (review_text, movie_id, critic_id) VALUES ("It's as if Lewis Carroll's Alice had wandered into a Francisco Goya painting, particularly the famously gruesome Saturn Devouring His Son, in which an ancient demon has ripped the head off his progeny.", 9, 9);
INSERT INTO reviews (review_text, movie_id, critic_id) VALUES ("This is a delectable film indeed.", 9, 18);
INSERT INTO reviews (review_text, movie_id, critic_id) VALUES ("More than any American movie of the past decade, Zodiac accepts and embraces irresolvability, which may be why it's so hypnotically rewatchable.", 10, 19);
INSERT INTO reviews (review_text, movie_id, critic_id) VALUES ("Marriage Story is so raw and emotionally burning that the experience is best savoured alone.", 11, 20);
INSERT INTO reviews (review_text, movie_id, critic_id) VALUES ("Maybe there's nothing terribly new in 'Marriage Story.' But it manages to make you forget that very fact, in surprising, affecting, singular and revelatory ways.", 11, 6);
INSERT INTO reviews (review_text, movie_id, critic_id) VALUES ("James Cameron's 194-minute, $200 million film of the tragic voyage is in the tradition of the great Hollywood epics. It is flawlessly crafted, intelligently constructed, strongly acted and spellbinding.", 12, 7);
INSERT INTO reviews (review_text, movie_id, critic_id) VALUES ("This endlessly fascinating swirl of a film could have come only from Nolan, who blends the cerebral twistiness of Memento (his thriller that moves backward in time) with the spectacular action of his Batman megahit, The Dark Knight.", 13, 3);
INSERT INTO reviews (review_text, movie_id, critic_id) VALUES ("Invention runs lower once we're on those snowy slopes, and the hard narrative punch keeps disintegrating into a floating cloud of pixels. But what a display they make.", 13, 21);
INSERT INTO reviews (review_text, movie_id, critic_id) VALUES ("This 3D cartoon based on the popular children's book is sweet and fun -- not to mention a little trippy.", 14, 9);
INSERT INTO reviews (review_text, movie_id, critic_id) VALUES ("The shouty variety of manchild comedy that Ferrell has cribbed from Jerry Lewis divides movie fans intensely. Here's the one we should put in the time capsule.", 15, 12);
INSERT INTO reviews (review_text, movie_id, critic_id) VALUES ("The potentially gooey conclusion is leavened with cynical irreverence.", 15, 18);
INSERT INTO reviews (review_text, movie_id, critic_id) VALUES ("Rubin's script is a lethally effective tragicomic fantasy.", 16, 21);
INSERT INTO reviews (review_text, movie_id, critic_id) VALUES ("Oh, those Martians! They are funny, mean little buggers, and they're worthing checking out.", 17, 22);
INSERT INTO reviews (review_text, movie_id, critic_id) VALUES ("Though the stories are individually captivating and very much worth the price of admission-see the film on a big screen if you can-they fit together awkwardly.", 18, 23);
INSERT INTO reviews (review_text, movie_id, critic_id) VALUES ("Sandler surely knew this mildly offensive, juvenile celebration of cheap scares, slapstick gags and bodily function 'jokes' was sure to land near the bottom of the large pile of terrible movies starring [himself].", 19, 16);
INSERT INTO reviews (review_text, movie_id, critic_id) VALUES ("The movie has an innocence and charm that grow on you.", 20, 7);
INSERT INTO reviews (review_text, movie_id, critic_id) VALUES ("The food on the boat was incredible!", 12, 24);
INSERT INTO reviews (review_text, movie_id, critic_id) VALUES ("I've been waiting for this movie my entire life. It has changed me to my core.", 23, 25);
INSERT INTO reviews (review_text, movie_id, critic_id) VALUES ("This movie is waaaaaayyy out there... in space!", 17, 26);
INSERT INTO reviews (review_text, movie_id, critic_id) VALUES ("Great source of pottery inspiration!", 16, 27);
INSERT INTO reviews (review_text, movie_id, critic_id) VALUES ("This movie is quiet. Too quiet. Good for a Sunday nap.", 21, 28);
INSERT INTO reviews (review_text, movie_id, critic_id) VALUES ("A Masterpiece.", 8, 28);
INSERT INTO reviews (review_text, movie_id, critic_id) VALUES ("Spoiler Alert: Still no clue who the killer is", 10, 25);
INSERT INTO reviews (review_text, movie_id, critic_id) VALUES ("Not much of a song, but quite a good movie", 18, 29);
INSERT INTO reviews (review_text, movie_id, critic_id) VALUES ("These people sure can box! And I like that!", 22, 25);
INSERT INTO reviews (review_text, movie_id, critic_id) VALUES ("Could have used a happier ending.", 22, 28);
INSERT INTO reviews (review_text, movie_id, critic_id) VALUES ("More like 'The Great Knight!", 24, 25);

--
-- Data for Name: critics; Type: TABLE DATA; Schema:  Owner: Sean Grogg
--

INSERT INTO critics (critic_name) VALUES ("Brian Lowry");
INSERT INTO critics (critic_name) VALUES ("Kevin Thomas");
INSERT INTO critics (critic_name) VALUES ("Caryn James");
INSERT INTO critics (critic_name) VALUES ("Kirk Honeycutt");
INSERT INTO critics (critic_name) VALUES ("Marc Lee");
INSERT INTO critics (critic_name) VALUES ("Ann Hornaday");
INSERT INTO critics (critic_name) VALUES ("Roger Ebert");
INSERT INTO critics (critic_name) VALUES ("Neil Smith");
INSERT INTO critics (critic_name) VALUES ("Paul Byrnes");
INSERT INTO critics (critic_name) VALUES ("Nell Minow");
INSERT INTO critics (critic_name) VALUES ("Glenn Kenny");
INSERT INTO critics (critic_name) VALUES ("Joshua Rothkopf");
INSERT INTO critics (critic_name) VALUES ("Peter Debruge");
INSERT INTO critics (critic_name) VALUES ("Matt Singer");
INSERT INTO critics (critic_name) VALUES ("Tom Huddleston");
INSERT INTO critics (critic_name) VALUES ("Richard Roeper");
INSERT INTO critics (critic_name) VALUES ("Anthony Lane");
INSERT INTO critics (critic_name) VALUES ("Nigel Andrews");
INSERT INTO critics (critic_name) VALUES ("Adam Nayman");
INSERT INTO critics (critic_name) VALUES ("Wenlel Ma");
INSERT INTO critics (critic_name) VALUES ("Peter Bradshaw");
INSERT INTO critics (critic_name) VALUES ("Gene Siskel");
INSERT INTO critics (critic_name) VALUES ("Christopher Orr");
INSERT INTO critics (critic_name) VALUES ("Sammy 'Foody' Figgs");
INSERT INTO critics (critic_name) VALUES ("Sean Grogg");
INSERT INTO critics (critic_name) VALUES ("Ian Leeds");
INSERT INTO critics (critic_name) VALUES ("Seth Rogen");
INSERT INTO critics (critic_name) VALUES ("Taylor Wilde");
INSERT INTO critics (critic_name) VALUES ("Haley Lilling");


