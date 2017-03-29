import os
import sys
import math
import numpy as np
import array
import statistics
import matplotlib.pyplot as plt
 

class WikiGraph:
    def load_from_file(self, filename):
        print('Загружаю граф из файла: ' + filename)

        with open(filename) as f:
            (self.n, self._nlinks) = (map(int, f.readline().split()))
            
            self._titles = []
            self._sizes = array.array('L', [0]*self.n)
            self._links = array.array('L', [0]*self._nlinks)
            self._redirect = array.array('B', [0]*self.n)
            self._offset = array.array('L', [0]*(self.n+1))
            current_link = 0
            for i in range(self.n):
                __title = f.readline()
                self._titles.append(__title.rstrip())
                (size, redirect, amout_links) = (map(int, f.readline().split()))
                self._sizes[i] = size
                self._redirect[i] = redirect
                for j in range(current_link, current_link + amout_links):
                    self._links[j] = int(f.readline())
                current_link += amout_links
                if self.n > 0:
                    self._offset[i+1] = self._offset[i] + amout_links

        print('Граф загружен')
        
    def get_id(self, title):
        _id = 0
        for name in self._titles:
            if name == title:
                return int(_id)
                 
            else:
                 _id += 1
    def get_number_of_links_from(self, _id):
        return int(self._offset[_id+1] - self._offset[_id]) 
                    
    def get_links_from(self, _id):
        return self._links[self._offset[_id]:self._offset[_id+1]]
        
    def get_number_of_pages(self):
        return len(self._titles)

    def is_redirect(self, _id):
        if self._redirect[_id]:
            return True
        else:
            return False
            
    def get_title(self, _id):
        return self._titles[_id]

    def get_page_size(self, _id):
        return self._sizes[_id]

def bfs(G, start, finish):
    start, finish = G.get_id(start), G.get_id(finish)
    parent = {start: None}
    i = 1
    queue = [start]
    while queue:
          new_queue = []
          for current in queue:
               for v in G.get_links_from(current):
                    if v not in parent:
                       parent[v] = current
                       new_queue.append(v)
                    if v == finish:
                       break
          queue = new_queue
    _way = [finish]
    current = parent[finish]
    while  current:
        _way.append(current)
        current = parent[current]
    _way = _way[::-1]
    return _way

def ex3(self):

      rt = 0
      nl = []
      min_kc = 0
      max_kc = 0
      max_links = ''
      
      for i in range(self.get_number_of_pages()):
           if self.is_redirect(i):
               rt += 1
           nl.append(self.get_number_of_links_from(i))
      max_nl = max(nl)
      min_nl = min(nl)

      for i in  range(self.get_number_of_pages()):
           if self.get_number_of_links_from(i) == min_nl:
                min_kc  += 1
           if self.get_number_of_links_from(i) == max_nl:
                max_kc +=1
                max_links += str(self._titles[i])
             
      nlp = [0 for i in range(G.get_number_of_pages())]
      for i in range(G.get_number_of_pages()):
          for elem in G.get_links_from(i):
                      
             nlp[int(elem)] += 1
             if G.is_redirect(i):
                  nlp[int(elem)] -= 1

      redirects_to_page = [0 for i in range(G.get_number_of_pages())]
      for i in range(G.get_number_of_pages()):
          for elem in G.get_links_from(i):
               if G.is_redirect(i) == 1:
                   redirects_to_page[elem] += 1
      pages_max_nr  = [G.get_title(i) for i in range(G.get_number_of_pages()) if redirects_to_page[i] == max(redirects_to_page) ]

      global dict_nlp
      dict_nlp = {}
      for i in range(len(nlp)):
         if  nlp[i] not in  dict_nlp:
            dict_nlp[nlp[i]] = 1
         else:
            dict_nlp[nlp[i]] += 1

      way = bfs(G, 'Python','Список_файловых_систем')
      way = [G.get_title(way[i]) for i in range(len(way)) ]

      print(  'путь, по которому можно добраться от статьи Python до статьи Список_файловых_систем: ' + str(way) + '\n' +
              'количество статей с перенаправлением: ' + str(rt) + '\n' +
              'минимальное количество ссылок из статьи: ' + str(min_nl) + '\n' +
              'количество статей с минимальным количеством ссылок: ' + str(min_kc) + '\n' +
              'максимальное количество ссылок из статьи: ' + str(max_nl) + '\n' +
              'количество статей с максимальным количеством ссылок: ' + str(max_kc) + '\n' +
              'cтатьи с наибольшим количеством ссылок: '+ max_links + '\n' +
              'среднее количество ссылок в статье: ' + str(round(self._nlinks / self.n)) + '\n'  +
              'Минимальное количество ссылок на статью: ' + str(min(nlp)) + '\n'  +
              'Количество статей с минимальным количеством внешних ссылок: ' + str(sum(elem == min(nlp) for elem in nlp )) + '\n' +
              'Максимальное количество ссылок на статью: ' + str(max(nlp)) + '\n'  +
              'Количество статей с максимальным количеством внешних ссылок: ' + str(sum(elem == max(nlp) for elem in nlp )) + '\n' +
              'Статья с наибольшим количеством внешних ссылок' + str([G.get_title(i) for i in range(G.get_number_of_pages()) if nlp[i] == max(nlp)]) + '\n' +
              "Среднее количество внешних ссылок на статью: %0.2f  (ср. откл. : %0.2f)" %(statistics.mean(nlp), statistics.stdev(nlp)) + '\n' +
              'Минимальное количество перенаправлений на статью: ' + str(min(redirects_to_page)) + '\n' +
              'Количество статей с минимальным количеством внешних перенаправлений: ' + str(sum(elem == min(redirects_to_page) for elem in redirects_to_page)) + '\n' + 
              'Максимальное количество перенаправлений на статью: ' + str(max(redirects_to_page)) + '\n'  +
              'Количество статей с максимальным количеством внешних перенаправлений: ' + str(sum(elem == max(redirects_to_page) for elem in redirects_to_page)) + '\n' +
              'Статья с наибольшим количеством внешних перенаправлений:' + str(pages_max_nr)  + '\n' +
              "Среднее количество внешних перенаправлений на статью: %0.2f  (ср. откл. : %0.2f)" %(statistics.mean(redirects_to_page), statistics.stdev(redirects_to_page)) )

def ex4(self):
     x, y = [], []
     liamda = len(dict_nlp)/10
     for elem in dict_nlp:
        x.append(elem)
        y.append(dict_nlp[elem])
     plt.figure(2)
     x_pos = np.arange(len(x))
     x_pos_im = np.arange( 0, max(x), liamda)
     plt.bar(x_pos, y, align='center', alpha=1)
     plt.xticks(x_pos_im)
     plt.plot()
     plt.show()
        
G = WikiGraph()
G.load_from_file('wiki_small.txt')
ex3(G)
ex4(G)

if __name__ == '__main__':

    if len(sys.argv) != 2:
        print('Использование: wiki_stats.py <файл с графом статей>')
        sys.exit(-1)

    if os.path.isfile(sys.argv[1]):
        wg = WikiGraph()
        wg.load_from_file(sys.argv[1])
    else:
        print('Файл с графом не найден')
        sys.exit(-1)
