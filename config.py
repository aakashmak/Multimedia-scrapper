import configparser

config = configparser.ConfigParser()


url={
    "search":"https://www.google.com/search?hl={}&q={}&q={}&num=10&ie=UTF-8",
    "headers":"'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/605.1.15 (KHTML, like Gecko)Version/12.1.1 Safari/605.1.15'",
    "working_directory":"/datadrive/solr"
}
solr={
    "url":"http://52.53.165.238:8983/solr"
}
