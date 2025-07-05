from tradx.backend.AT import _rss

def get_all_at():
    ## news
    # first we do rss.
    _rss.rss_comp.main()
    _rss.rss_notify.main()
    
    ## prices
    # first we do the stocks



def main():    
    get_all_at()


if __name__ == "__main__":
    main()