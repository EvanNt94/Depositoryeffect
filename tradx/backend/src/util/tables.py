import requests 
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO


def request_text_with_dfs(url:str):
    """
    Returns:
        text, dfs
    """
    resp = requests.get(url)
    if resp.status_code != 200:
        raise RuntimeError("Status not 200 -> error!")
    text = resp.text
    sio = StringIO(text)
    dfs = pd.read_html(sio)
    return text, dfs


def request_soup_with_dfs(url:str):
    """
    Returns:
        soup, dfs
    """
    resp = requests.get(url)
    if resp.status_code != 200:
        raise RuntimeError("Status not 200 -> error!")
    text = resp.text
    soup = BeautifulSoup(text, "lxml")
    sio = StringIO(text)
    dfs = pd.read_html(sio)
    return soup, dfs