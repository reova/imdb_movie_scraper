from parse import parse_html
import os


def main():
    os.mkdir('images')
    os.mkdir('poster')
    
    for i in parse_html('https://www.imdb.com/title/tt0493464/?ref_=nv_sr_srsg_0'):
        print(i)
    
if __name__ == '__main__':
    main()
