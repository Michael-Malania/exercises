# sweeft digital challenges

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

## Project Installation

### Without Doker

URL shortener requires [Python3](https://www.python.org/) v3.6+ to run.

Install the dependencies and start the server.

```sh
cd project
pip install -r requirements.txt
python app.py
```
> Note: Since I use `sqlite3` we don't need to configure a database, project comes with the db file, anyways project comes with the SQL schema, that can be used to build everything, but still it's not needed to run the project

> Note: you can use `test_url_shortener.py` file located in the project folder to test project against various UNITTEST cases

## Docker 

Url Shortener is very easy to install and deploy in a Docker container.

By default, the Docker will expose port 8080, so change this within the
Dockerfile if necessary. When ready, simply use the Dockerfile to
build the image.

```sh
cd project
docker build -t url-shortener .
```

This will create the url shortener image and pull in the necessary dependencies.

Once done, run the Docker image and map the port to whatever you wish on
your host. In this example, we simply map port 5000 of the host to
port 5000 of the Docker (or whatever port was exposed in the Dockerfile):

```sh
docker run -d -p 5000:5000 url-shortener
```

Verify the deployment by navigating to your server address in
your preferred browser.

```sh
127.0.0.1:5000/url_shortener
```

# How to use 

Url shortener is a simple app that can be used to shorten sizes of URL's

It can provide several kind of functionalities, such as shorten the URL, have custom URL option for a premium clients, get statistical data about all of the URL's, such as a counters and ability to delete URL's after certain days


## API call example

URL shortener gives user ability to provide data as a JSON as well as a normal HTTP request, let's start with the cURL example

</br>

### Example 1:

</br>

Let's provide JSON data to API to shorten some urls 😎

```sh
curl --location --request POST 'http://127.0.0.1:5000/shorten_url' \
--header 'Content-Type: application/json' \
--data-raw '{
    "url": "http://google.com"
}'
```
In this case API will return: 

```sh
{
    "original_url": "http://google.com",
    "short_url": "http://127.0.0.1:5000/url/fDo=",
    "success": true
}
```
</br>

### Example 2
</br>

In case if we want to have custom URL we have to use special key value pair, see the example below

```sh
{
    "url": "http://google.com",
    "premium": true,
    "custom_url": "unclegrandpa"
}
```
Which will return: 

```sh
{
    "original_url": "http://google.com",
    "short_url": "http://127.0.0.1:5000/url/unclegrandpa",
    "success": true
}
```

lets move on to the HTTP response example

</br>

### Example 1:

</br>


```sh
<Own IP adress>/shorten_url?url=https://fox.com
```
Here we can see that API accepts input from user directly from the address bar :) 

and here is what it receives 
```sh
{
    "original_url": "http://google.com",
    "short_url": "http://127.0.0.1:5000/url/unclegrandpa",
    "success": true
}
```
as we can see returned data is pretty much same to the first cURL option
</br>

### Example 2

</br>

let's see example in case of a premium user

```sh
http://127.0.0.1:5000/shorten_url?url=https://fox.com&premium=true&custom_url=love_the_news
```
which returns:

```sh
{
    "original_url": "https://fox.com",
    "short_url": "http://127.0.0.1:5000/url/love_the_news",
    "success": true
}
```

In case if we are interested in stats we have special API for it which can be accessed by both cURL and normal HTTP request


Let's start with the cURL variant

</br>

### Example 1

</br>

Here we request for a stats about certain shortened URL

```sh
curl --location --request POST 'http://127.0.0.1:5000/stats/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "stats": "http://127.0.0.1:5000/url/love_the_news"
}'
```
and as a result we get:

```sh
{
    "days_left": 30,
    "visitors": 3
}
```

which consists of visitors counter and also of a total days left till the deletion of shown URL
</br>

### Example 2
</br>
and in the end let's see some stats API examples in case if we use a HTTP request

</br>

```sh
http://127.0.0.1:5000/stats/?url=http://127.0.0.1:5000/url/love_the_news
```
</br>

Which will return same result as it was in case of cURL:

</br>

```sh
{
    "days_left": 30,
    "visitors": 3
}
```

</br>


Have a nice day/night  ;)  

</br>

## License

MIT

**Free Software, Hell Yeah!**